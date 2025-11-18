from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from .models import User, GhostCrew, CrewInvitation, CrewMessage, GraveyardPost, GhostChant, SummoningPost, JobApplication
from .forms import ProfileSetupForm
from .utils import check_image_online, check_duplicate_face
import os
import logging

logger = logging.getLogger(__name__)


def index(request):
    """Homepage with hero section"""
    return render(request, 'index.html')


@login_required
def verification(request):
    """Photo verification page"""
    # Redirect if already verified
    if request.user.is_verified:
        return redirect('tell_kiro_about_you')
    
    if request.method == 'POST' and request.FILES.get('verification_photo'):
        uploaded_file = request.FILES['verification_photo']
        
        # Save temporarily
        temp_path = f'/tmp/{uploaded_file.name}'
        with open(temp_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        try:
            # Step 1: Reverse image search
            exists_online, sources = check_image_online(temp_path)
            if exists_online:
                os.remove(temp_path)
                messages.error(request, 'This photo exists online. Upload your real face, ghost.')
                return render(request, 'verification.html')
            
            # Step 2: Duplicate face check
            is_duplicate, matched_user = check_duplicate_face(temp_path)
            if is_duplicate:
                os.remove(temp_path)
                messages.error(request, 'This face already haunts our community. One ghost per person.')
                return render(request, 'verification.html')
            
            # Step 3: Success - save and verify
            user = request.user
            user.verification_photo = uploaded_file
            user.is_verified = True
            user.save()
            
            os.remove(temp_path)
            messages.success(request, '✅ Verified Ghost! Welcome to the cemetery.')
            return redirect('tell_kiro_about_you')
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            messages.error(request, f'Verification error: {str(e)}')
            return render(request, 'verification.html')
    
    return render(request, 'verification.html')


@login_required
def tell_kiro_about_you(request):
    """Self-description page - helps AI understand the user better"""
    # Redirect to verification if not verified
    if not request.user.is_verified:
        return redirect('verification')
    
    if request.method == 'POST':
        user = request.user
        user.developer_role = request.POST.get('developer_role', '')
        user.core_skills = request.POST.get('core_skills', '')
        user.strengths = request.POST.get('strengths', '')
        user.weaknesses = request.POST.get('weaknesses', '')
        user.coding_journey = request.POST.get('coding_journey', '')
        
        # Enhanced expertise fields
        user.expertise_area = request.POST.get('expertise_area', '')
        user.expertise_details = request.POST.get('expertise_details', '')
        user.learning_journey = request.POST.get('learning_journey', '')
        user.ai_usage_context = request.POST.get('ai_usage_context', '')
        user.non_expertise_areas = request.POST.get('non_expertise_areas', '')
        
        user.save()
        
        messages.success(request, '✅ Thanks! This will help our AI understand you better!')
        return redirect('haunt_setup')
    
    return render(request, 'tell_kiro_about_you.html')


@login_required
def haunt_setup(request):
    """Profile setup page - Gen Z style!"""
    # Redirect to verification if not verified
    if not request.user.is_verified:
        return redirect('verification')
    
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Save LinkedIn and Devpost URLs
            user.linkedin_url = form.cleaned_data.get('linkedin_url', '')
            user.devpost_url = form.cleaned_data.get('devpost_url', '')
            
            user.save()
            
            # Analyze portfolio in background (async would be better, but keeping it simple)
            from .portfolio_analyzer import analyze_full_portfolio
            try:
                # Prepare user profile for AI analysis
                user_profile = {
                    'developer_role': user.developer_role,
                    'core_skills': user.core_skills,
                    'strengths': user.strengths,
                    'weaknesses': user.weaknesses,
                    'coding_journey': user.coding_journey,
                    'expertise_area': user.expertise_area,
                    'expertise_details': user.expertise_details,
                    'learning_journey': user.learning_journey,
                    'ai_usage_context': user.ai_usage_context,
                    'non_expertise_areas': user.non_expertise_areas,
                }
                
                portfolio_data = analyze_full_portfolio(
                    github_url=user.github_link,
                    linkedin_url=user.linkedin_url,
                    devpost_url=user.devpost_url,
                    user_profile=user_profile,
                )
                user.portfolio_data = portfolio_data
                user.last_portfolio_update = timezone.now()
                user.save()
            except Exception as e:
                logger.error(f"Error analyzing portfolio: {e}")
            
            messages.success(request, '🎃 Your haunted portfolio is ready!')
            return redirect('haunted_portfolio')
    else:
        form = ProfileSetupForm(instance=request.user)
    
    return render(request, 'haunt_setup.html', {'form': form})


@login_required
def profile(request, username=None):
    """User profile page"""
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    # Generate star rating based on ghost_level
    stars = '⭐' * profile_user.ghost_level
    
    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'stars': stars,
        'is_own_profile': profile_user == request.user
    })


def logout_view(request):
    """Logout and redirect to homepage"""
    logout(request)
    messages.success(request, 'You have returned to the shadows...')
    return redirect('index')



@login_required
def refresh_portfolio(request):
    """Manually refresh portfolio analysis"""
    user = request.user
    
    if not user.github_link:
        messages.error(request, '❌ Add your GitHub link first!')
        return redirect('haunt_setup')
    
    from .portfolio_analyzer import analyze_full_portfolio
    
    try:
        # Prepare user profile for AI analysis
        user_profile = {
            'developer_role': user.developer_role,
            'core_skills': user.core_skills,
            'strengths': user.strengths,
            'weaknesses': user.weaknesses,
            'coding_journey': user.coding_journey,
            'expertise_area': user.expertise_area,
            'expertise_details': user.expertise_details,
            'learning_journey': user.learning_journey,
            'ai_usage_context': user.ai_usage_context,
            'non_expertise_areas': user.non_expertise_areas,
        }
        
        messages.info(request, '🔄 Analyzing your GitHub... This may take a moment!')
        
        portfolio_data = analyze_full_portfolio(
            github_url=user.github_link,
            linkedin_url=user.linkedin_url,
            devpost_url=user.devpost_url,
            user_profile=user_profile,
        )
        
        user.portfolio_data = portfolio_data
        user.last_portfolio_update = timezone.now()
        user.save()
        
        messages.success(request, '✅ Portfolio refreshed! Check out your updated analysis!')
    except Exception as e:
        logger.error(f"Error refreshing portfolio: {e}")
        messages.error(request, f'❌ Error analyzing GitHub: {str(e)}')
    
    return redirect('haunted_portfolio')


@login_required
def haunted_portfolio(request, username=None):
    """
    Haunted Portfolio - Shows AI-analyzed skills and achievements
    Gen Z style - visual, fun, and REAL! 🔥
    """
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    
    # Get portfolio data
    portfolio = profile_user.portfolio_data or {}
    github_data = portfolio.get('github', {})
    devpost_data = portfolio.get('devpost', {})
    linkedin_data = portfolio.get('linkedin', {})
    
    # Generate star rating based on ghost_level
    stars = '⭐' * profile_user.ghost_level
    
    # Calculate skill level based on portfolio
    overall_score = portfolio.get('overall_score', 0)
    
    context = {
        'profile_user': profile_user,
        'stars': stars,
        'is_own_profile': profile_user == request.user,
        'portfolio': portfolio,
        'github_data': github_data,
        'devpost_data': devpost_data,
        'linkedin_data': linkedin_data,
        'overall_score': overall_score,
    }
    
    return render(request, 'haunted_portfolio.html', context)



# ============================================
# THE GRAVEYARD (Roast Zone) VIEWS
# ============================================

@login_required
def graveyard(request):
    """The Graveyard - Post projects and get roasted! 🔥"""
    posts = GraveyardPost.objects.all()
    
    context = {
        'posts': posts,
    }
    return render(request, 'graveyard.html', context)


@login_required
def create_graveyard_post(request):
    """Create a new post in The Graveyard"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        code_snippet = request.POST.get('code_snippet', '')
        project_link = request.POST.get('project_link', '')
        image = request.FILES.get('image')
        
        post = GraveyardPost.objects.create(
            author=request.user,
            title=title,
            description=description,
            code_snippet=code_snippet,
            project_link=project_link,
            image=image,
        )
        
        messages.success(request, '🪦 Your project is in The Graveyard! Prepare to get roasted!')
        return redirect('graveyard')
    
    return render(request, 'create_graveyard_post.html')


@login_required
def add_ghost_chant(request, post_id):
    """Add a Ghost Chant (comment) to a Graveyard post"""
    post = get_object_or_404(GraveyardPost, id=post_id)
    
    if request.method == 'POST':
        chant_text = request.POST.get('chant')
        
        GhostChant.objects.create(
            post=post,
            author=request.user,
            chant=chant_text,
        )
        
        messages.success(request, '👻 Ghost Chant added!')
        return redirect('graveyard')
    
    return redirect('graveyard')


# ============================================
# GHOST CREW VIEWS
# ============================================

@login_required
def ghost_hunt(request):
    """Ghost Hunt - Find developers by username or ghost_id"""
    from django.db.models import Q
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Get all verified users except current user
    developers = User.objects.filter(is_verified=True).exclude(id=request.user.id)
    
    # Apply search filter if provided
    if search_query:
        developers = developers.filter(
            Q(username__icontains=search_query) |  # Search by username (ghost_id)
            Q(email__icontains=search_query)       # Or email
        )
    
    context = {
        'developers': developers,
        'search_query': search_query,
    }
    return render(request, 'ghost_hunt.html', context)


@login_required
def my_crews(request):
    """View all crews the user is part of"""
    created_crews = request.user.created_crews.all()
    member_crews = request.user.crews.all()
    
    context = {
        'created_crews': created_crews,
        'member_crews': member_crews,
    }
    return render(request, 'my_crews.html', context)


@login_required
def create_crew(request):
    """Create a new Ghost Crew"""
    if request.method == 'POST':
        name = request.POST.get('name')
        crew_bio = request.POST.get('crew_bio', '')
        
        crew = GhostCrew.objects.create(
            name=name,
            created_by=request.user,
            crew_bio=crew_bio,
        )
        
        # Add creator as first member
        crew.members.add(request.user)
        
        messages.success(request, f'👻 {name} crew created! Start hunting for members!')
        return redirect('crew_detail', crew_id=crew.id)
    
    return render(request, 'create_crew.html')


@login_required
def crew_detail(request, crew_id):
    """View a Ghost Crew and its chat"""
    crew = get_object_or_404(GhostCrew, id=crew_id)
    
    # Check if user is a member
    is_member = request.user in crew.members.all()
    
    if not is_member:
        messages.error(request, "You're not part of this crew!")
        return redirect('my_crews')
    
    # Get crew messages
    messages_list = crew.messages.all()
    
    context = {
        'crew': crew,
        'messages_list': messages_list,
        'is_creator': crew.created_by == request.user,
    }
    return render(request, 'crew_detail.html', context)


@login_required
def send_crew_invitation(request, user_id):
    """Send a crew invitation to another user"""
    to_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        crew_id = request.POST.get('crew_id')
        message = request.POST.get('message', '')
        
        crew = get_object_or_404(GhostCrew, id=crew_id)
        
        # Check if user is crew creator
        if crew.created_by != request.user:
            messages.error(request, "Only the crew creator can send invitations!")
            return redirect('ghost_hunt')
        
        # Check if crew is full
        if crew.is_full():
            messages.error(request, "Your crew is full (max 5 members)!")
            return redirect('ghost_hunt')
        
        # Create invitation
        CrewInvitation.objects.create(
            crew=crew,
            from_user=request.user,
            to_user=to_user,
            message=message,
        )
        
        messages.success(request, f'👻 Invitation sent to {to_user.username}!')
        return redirect('ghost_hunt')
    
    # Show user's crews to choose from (that aren't full)
    user_crews = request.user.created_crews.all()
    available_crews = [crew for crew in user_crews if not crew.is_full()]
    
    context = {
        'to_user': to_user,
        'user_crews': available_crews,
    }
    return render(request, 'send_crew_invitation.html', context)


@login_required
def crew_invitations(request):
    """View pending crew invitations"""
    invitations = request.user.received_invitations.filter(status='pending')
    
    context = {
        'invitations': invitations,
    }
    return render(request, 'crew_invitations.html', context)


@login_required
def respond_to_invitation(request, invitation_id):
    """Accept or decline a crew invitation"""
    invitation = get_object_or_404(CrewInvitation, id=invitation_id, to_user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
            invitation.status = 'accepted'
            invitation.crew.members.add(request.user)
            messages.success(request, f'🎃 You joined {invitation.crew.name}!')
        elif action == 'decline':
            invitation.status = 'declined'
            messages.info(request, 'Invitation declined.')
        
        invitation.save()
        return redirect('crew_invitations')
    
    return redirect('crew_invitations')


@login_required
def send_crew_message(request, crew_id):
    """Send a message in crew chat"""
    crew = get_object_or_404(GhostCrew, id=crew_id)
    
    # Check if user is a member
    if request.user not in crew.members.all():
        messages.error(request, "You're not part of this crew!")
        return redirect('my_crews')
    
    if request.method == 'POST':
        message_text = request.POST.get('message')
        is_code = request.POST.get('is_code') == 'on'
        
        CrewMessage.objects.create(
            crew=crew,
            sender=request.user,
            message=message_text,
            is_code=is_code,
        )
        
        return redirect('crew_detail', crew_id=crew.id)
    
    return redirect('crew_detail', crew_id=crew.id)



# ============================================
# THE SUMMONING CIRCLE (Hiring) VIEWS
# ============================================

def summoning_circle(request):
    """The Summoning Circle - Jobs that don't require degrees!"""
    jobs = SummoningPost.objects.filter(is_active=True)
    
    # Filter by skills if provided
    skill_filter = request.GET.get('skill')
    if skill_filter:
        jobs = jobs.filter(required_skills__contains=skill_filter)
    
    context = {
        'jobs': jobs,
        'skill_filter': skill_filter,
    }
    return render(request, 'summoning_circle.html', context)


@login_required
def create_summoning_post(request):
    """Create a job posting (for companies)"""
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        required_skills = request.POST.getlist('required_skills')
        location = request.POST.get('location')
        salary_range = request.POST.get('salary_range', '')
        is_remote = request.POST.get('is_remote') == 'on'
        
        SummoningPost.objects.create(
            company_name=company_name,
            posted_by=request.user,
            job_title=job_title,
            description=description,
            required_skills=required_skills,
            location=location,
            salary_range=salary_range,
            is_remote=is_remote,
        )
        
        messages.success(request, '🔮 Summoning post created! Ghosts will start haunting!')
        return redirect('summoning_circle')
    
    return render(request, 'create_summoning_post.html')


@login_required
def haunt_job(request, job_id):
    """Apply to a job (haunt it!)"""
    job = get_object_or_404(SummoningPost, id=job_id)
    
    # Check if already applied
    existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()
    if existing_application:
        messages.info(request, "You're already haunting this job!")
        return redirect('summoning_circle')
    
    if request.method == 'POST':
        cover_message = request.POST.get('cover_message')
        
        JobApplication.objects.create(
            job=job,
            applicant=request.user,
            cover_message=cover_message,
        )
        
        messages.success(request, '👻 You\'re now haunting this job! They\'ll review your portfolio!')
        return redirect('summoning_circle')
    
    context = {
        'job': job,
    }
    return render(request, 'haunt_job.html', context)


@login_required
def my_applications(request):
    """View your job applications"""
    applications = request.user.job_applications.all()
    
    context = {
        'applications': applications,
    }
    return render(request, 'my_applications.html', context)


@login_required
def job_applications(request, job_id):
    """View applications for a job (for job posters)"""
    job = get_object_or_404(SummoningPost, id=job_id, posted_by=request.user)
    applications = job.applications.all()
    
    context = {
        'job': job,
        'applications': applications,
    }
    return render(request, 'job_applications.html', context)


# ============================================
# GHOST TRIALS - INVITATION-ONLY OPPORTUNITIES
# ============================================

from .models import Opportunity, Invitation, Submission, Notification
from .decorators import company_required, developer_required
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.core.paginator import Paginator


@login_required
@company_required
def ghost_selector(request):
    """Company browse page to find and shortlist developers"""
    # Get all developers (non-company users)
    developers = User.objects.filter(is_company=False, is_verified=True)
    
    # Apply filters
    skills_filter = request.GET.getlist('skills')
    min_ghost_level = request.GET.get('min_ghost_level')
    min_authenticity = request.GET.get('min_authenticity')
    
    if skills_filter:
        # Filter by skills (portfolio_data contains skills)
        for skill in skills_filter:
            developers = developers.filter(portfolio_data__icontains=skill)
    
    if min_ghost_level:
        developers = developers.filter(ghost_level__gte=int(min_ghost_level))
    
    if min_authenticity:
        # Filter by AI percentage (authenticity = 100 - ai_percentage)
        # This requires checking portfolio_data JSON field
        pass  # Will implement after seeing portfolio_data structure
    
    # Pagination
    paginator = Paginator(developers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get shortlist from session
    shortlist_ids = request.session.get('shortlist', [])
    shortlist = User.objects.filter(id__in=shortlist_ids)
    
    # Handle shortlist actions
    if request.method == 'POST':
        action = request.POST.get('action')
        developer_id = request.POST.get('developer_id')
        
        if action == 'add_to_shortlist' and developer_id:
            if developer_id not in shortlist_ids:
                shortlist_ids.append(developer_id)
                request.session['shortlist'] = shortlist_ids
                messages.success(request, 'Developer added to shortlist!')
        
        elif action == 'remove_from_shortlist' and developer_id:
            if developer_id in shortlist_ids:
                shortlist_ids.remove(developer_id)
                request.session['shortlist'] = shortlist_ids
                messages.success(request, 'Developer removed from shortlist!')
        
        return redirect('ghost_selector')
    
    context = {
        'developers': page_obj,
        'shortlist': shortlist,
        'shortlist_count': len(shortlist_ids),
    }
    return render(request, 'ghost_selector.html', context)


@login_required
@company_required
def create_opportunity(request):
    """Create a new opportunity (Paid Trial, Internship, or Skill Challenge)"""
    if request.method == 'POST':
        # Get common fields
        opportunity_type = request.POST.get('opportunity_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills_needed = request.POST.getlist('skills_needed')
        full_job_details = request.POST.get('full_job_details', '')
        
        # Create opportunity
        opportunity = Opportunity.objects.create(
            company=request.user,
            opportunity_type=opportunity_type,
            title=title,
            description=description,
            skills_needed=skills_needed,
            full_job_details=full_job_details
        )
        
        # Add type-specific fields
        if opportunity_type == 'paid_trial':
            opportunity.payment = request.POST.get('payment')
            opportunity.time_limit_hours = request.POST.get('time_limit_hours')
            opportunity.success_criteria = request.POST.get('success_criteria')
        
        elif opportunity_type == 'internship':
            opportunity.duration_months = request.POST.get('duration_months')
            opportunity.stipend_amount = request.POST.get('stipend_amount')
            opportunity.responsibilities = request.POST.get('responsibilities')
            opportunity.conversion_potential = request.POST.get('conversion_potential') == 'on'
        
        elif opportunity_type == 'skill_challenge':
            opportunity.challenge_description = request.POST.get('challenge_description')
            if request.FILES.get('dataset_file'):
                opportunity.dataset_file = request.FILES['dataset_file']
            opportunity.dataset_link = request.POST.get('dataset_link', '')
            opportunity.submission_deadline = request.POST.get('submission_deadline')
            opportunity.public_rating = request.POST.get('public_rating') == 'on'
        
        opportunity.save()
        
        # Redirect to send invitations
        return redirect('send_invitations', opportunity_id=opportunity.id)
    
    # GET request - show form
    shortlist_ids = request.session.get('shortlist', [])
    shortlist = User.objects.filter(id__in=shortlist_ids)
    
    context = {
        'shortlist': shortlist,
        'shortlist_count': len(shortlist_ids),
    }
    return render(request, 'create_opportunity.html', context)


@login_required
@company_required
def send_invitations(request, opportunity_id):
    """Send invitations to shortlisted developers"""
    opportunity = get_object_or_404(Opportunity, id=opportunity_id, company=request.user)
    
    if request.method == 'POST':
        # Get shortlisted developers
        shortlist_ids = request.session.get('shortlist', [])
        
        if not shortlist_ids:
            messages.error(request, 'Please add at least one developer to your shortlist.')
            return redirect('ghost_selector')
        
        # Create invitations
        created_count = 0
        for dev_id in shortlist_ids:
            developer = User.objects.get(id=dev_id)
            
            # Check if invitation already exists
            if not Invitation.objects.filter(opportunity=opportunity, developer=developer).exists():
                invitation = Invitation.objects.create(
                    opportunity=opportunity,
                    developer=developer,
                    status='pending'
                )
                
                # Create notification
                type_icons = {
                    'paid_trial': '💰',
                    'internship': '🎓',
                    'skill_challenge': '⭐'
                }
                icon = type_icons.get(opportunity.opportunity_type, '👻')
                
                Notification.objects.create(
                    user=developer,
                    notification_type='invitation_received',
                    title=f'{icon} New Invitation from {request.user.username}',
                    message=f'{request.user.username} invited you to: {opportunity.title}',
                    link=f'/my-invitations/',
                    invitation=invitation
                )
                
                created_count += 1
        
        # Clear shortlist
        request.session['shortlist'] = []
        
        messages.success(request, f'Successfully sent {created_count} invitations!')
        return redirect('company_dashboard')
    
    # GET request - show confirmation page
    shortlist_ids = request.session.get('shortlist', [])
    shortlist = User.objects.filter(id__in=shortlist_ids)
    
    context = {
        'opportunity': opportunity,
        'shortlist': shortlist,
    }
    return render(request, 'send_invitations.html', context)


@login_required
@company_required
def company_dashboard(request):
    """Company dashboard showing opportunities, invitations, and submissions"""
    # Get company's opportunities
    opportunities = Opportunity.objects.filter(company=request.user).order_by('-created_at')
    
    # Get invitations grouped by status
    invitations = Invitation.objects.filter(opportunity__company=request.user).select_related('opportunity', 'developer')
    
    # Get submissions awaiting rating
    pending_submissions = Submission.objects.filter(
        invitation__opportunity__company=request.user,
        rating__isnull=True
    ).select_related('invitation__developer', 'invitation__opportunity')
    
    context = {
        'opportunities': opportunities,
        'invitations': invitations,
        'pending_submissions': pending_submissions,
    }
    return render(request, 'company_dashboard.html', context)


@login_required
@developer_required
def my_invitations(request):
    """Developer page showing all invitations (pending, active, completed)"""
    # Get all invitations for this developer
    invitations = Invitation.objects.filter(developer=request.user).select_related('opportunity__company')
    
    # Separate by status
    pending = invitations.filter(status='pending')
    active = invitations.filter(status='accepted', submission__isnull=True)
    completed = invitations.filter(status='accepted', submission__isnull=False)
    
    context = {
        'pending_invitations': pending,
        'active_trials': active,
        'completed_challenges': completed,
    }
    return render(request, 'my_invitations.html', context)


@login_required
@developer_required
def accept_invitation(request, invitation_id):
    """Accept an invitation"""
    invitation = get_object_or_404(Invitation, id=invitation_id, developer=request.user)
    
    if invitation.status != 'pending':
        messages.error(request, 'This invitation has already been responded to.')
        return redirect('my_invitations')
    
    invitation.status = 'accepted'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    # Notify company
    Notification.objects.create(
        user=invitation.opportunity.company,
        notification_type='invitation_accepted',
        title=f'✅ {request.user.username} accepted your invitation',
        message=f'{request.user.username} accepted: {invitation.opportunity.title}',
        link=f'/company-dashboard/',
        invitation=invitation
    )
    
    messages.success(request, f'You accepted the invitation for {invitation.opportunity.title}!')
    return redirect('my_invitations')


@login_required
@developer_required
def decline_invitation(request, invitation_id):
    """Decline an invitation"""
    invitation = get_object_or_404(Invitation, id=invitation_id, developer=request.user)
    
    if invitation.status != 'pending':
        messages.error(request, 'This invitation has already been responded to.')
        return redirect('my_invitations')
    
    invitation.status = 'declined'
    invitation.responded_at = timezone.now()
    invitation.save()
    
    # Notify company
    Notification.objects.create(
        user=invitation.opportunity.company,
        notification_type='invitation_declined',
        title=f'❌ {request.user.username} declined your invitation',
        message=f'{request.user.username} declined: {invitation.opportunity.title}',
        link=f'/company-dashboard/',
        invitation=invitation
    )
    
    messages.info(request, 'You declined the invitation.')
    return redirect('my_invitations')


@login_required
@developer_required
def submit_work(request, invitation_id):
    """Submit work for an accepted invitation"""
    invitation = get_object_or_404(Invitation, id=invitation_id, developer=request.user, status='accepted')
    
    # Check if already submitted
    if hasattr(invitation, 'submission'):
        messages.error(request, 'You have already submitted work for this opportunity.')
        return redirect('my_invitations')
    
    if request.method == 'POST':
        # Create submission
        submission = Submission.objects.create(
            invitation=invitation,
            code_text=request.POST.get('code_text', ''),
            github_link=request.POST.get('github_link', ''),
            notes=request.POST.get('notes', '')
        )
        
        if request.FILES.get('files'):
            submission.files = request.FILES['files']
            submission.save()
        
        # Notify company
        Notification.objects.create(
            user=invitation.opportunity.company,
            notification_type='submission_received',
            title=f'📥 New submission from {request.user.username}',
            message=f'{request.user.username} submitted work for: {invitation.opportunity.title}',
            link=f'/rate-submission/{submission.id}/',
            invitation=invitation
        )
        
        messages.success(request, 'Your work has been submitted! Waiting for company rating...')
        return redirect('my_invitations')
    
    context = {
        'invitation': invitation,
    }
    return render(request, 'submit_work.html', context)


@login_required
@company_required
def rate_submission(request, submission_id):
    """Rate a developer's submission"""
    submission = get_object_or_404(Submission, id=submission_id, invitation__opportunity__company=request.user)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        feedback = request.POST.get('feedback', '')
        public_feedback = request.POST.get('public_feedback') == 'on'
        
        submission.rating = rating
        submission.feedback = feedback
        submission.public_feedback = public_feedback
        submission.rated_at = timezone.now()
        submission.save()
        
        # Notify developer
        Notification.objects.create(
            user=submission.invitation.developer,
            notification_type='submission_rated',
            title=f'⭐ Your submission was rated!',
            message=f'{request.user.username} rated your submission: {rating}/5 stars',
            link=f'/my-invitations/',
            invitation=submission.invitation
        )
        
        messages.success(request, 'Submission rated successfully!')
        return redirect('company_dashboard')
    
    context = {
        'submission': submission,
    }
    return render(request, 'rate_submission.html', context)


@login_required
def notifications_api(request):
    """API endpoint for notifications"""
    if request.method == 'GET':
        # Get unread count and recent notifications
        notifications = request.user.notifications.all()[:10]
        unread_count = request.user.notifications.filter(is_read=False).count()
        
        notifications_data = [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'link': n.link,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M'),
        } for n in notifications]
        
        return JsonResponse({
            'unread_count': unread_count,
            'notifications': notifications_data
        })
    
    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_read':
            notification_id = request.POST.get('notification_id')
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        
        elif action == 'mark_all_read':
            request.user.notifications.filter(is_read=False).update(is_read=True)
            return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# ============================================
# GHOST TRIALS - INVITATION-ONLY OPPORTUNITIES
# ============================================

from .models import Opportunity, Invitation, Submission
from .decorators import company_required, developer_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse


@login_required
@company_required
def ghost_selector(request):
    """Company view to browse and filter developers"""
    # Get all developers (non-company users)
    developers = User.objects.filter(is_company=False, is_verified=True)
    
    # Apply filters
    skills_filter = request.GET.get('skills', '').strip()
    min_ghost_level = request.GET.get('min_ghost_level', '').strip()
    min_authenticity = request.GET.get('min_authenticity', '').strip()
    
    if skills_filter:
        # Filter by skills (search in core_skills or portfolio_data)
        skills_list = [s.strip() for s in skills_filter.split(',')]
        q_objects = Q()
        for skill in skills_list:
            q_objects |= Q(core_skills__icontains=skill) | Q(portfolio_data__top_skills__icontains=skill)
        developers = developers.filter(q_objects)
    
    if min_ghost_level:
        developers = developers.filter(ghost_level__gte=int(min_ghost_level))
    
    if min_authenticity:
        # This would need to filter by portfolio_data authenticity
        pass  # Implement if needed
    
    # Handle shortlist actions
    if request.method == 'POST':
        action = request.POST.get('action')
        developer_id = request.POST.get('developer_id')
        
        if 'shortlist' not in request.session:
            request.session['shortlist'] = []
        
        if action == 'add_to_shortlist' and developer_id:
            if developer_id not in request.session['shortlist']:
                request.session['shortlist'].append(developer_id)
                request.session.modified = True
                messages.success(request, '👻 Added to shortlist!')
        
        elif action == 'remove_from_shortlist' and developer_id:
            if developer_id in request.session['shortlist']:
                request.session['shortlist'].remove(developer_id)
                request.session.modified = True
                messages.success(request, '✅ Removed from shortlist')
        
        return redirect('ghost_selector')
    
    # Paginate developers
    paginator = Paginator(developers, 20)
    page_number = request.GET.get('page')
    developers_page = paginator.get_page(page_number)
    
    # Get shortlisted developers
    shortlist_ids = request.session.get('shortlist', [])
    shortlist = User.objects.filter(id__in=shortlist_ids)
    
    context = {
        'developers': developers_page,
        'shortlist': shortlist,
        'shortlist_count': len(shortlist_ids),
    }
    
    return render(request, 'ghost_selector.html', context)


@login_required
@company_required
def create_opportunity(request):
    """Company view to create an opportunity and invite developers"""
    # Get shortlist from session
    shortlist_ids = request.session.get('shortlist', [])
    shortlist = User.objects.filter(id__in=shortlist_ids)
    
    if request.method == 'POST':
        # Validate shortlist
        if not shortlist_ids:
            messages.error(request, '⚠️ Please add developers to your shortlist first!')
            return redirect('ghost_selector')
        
        # Create opportunity
        opportunity_type = request.POST.get('opportunity_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills_needed = [s.strip() for s in request.POST.get('skills_needed', '').split(',')]
        full_job_details = request.POST.get('full_job_details', '')
        
        opportunity = Opportunity.objects.create(
            company=request.user,
            opportunity_type=opportunity_type,
            title=title,
            description=description,
            skills_needed=skills_needed,
            full_job_details=full_job_details
        )
        
        # Type-specific fields
        if opportunity_type == 'paid_trial':
            opportunity.payment = request.POST.get('payment')
            opportunity.time_limit_hours = request.POST.get('time_limit_hours')
            opportunity.success_criteria = request.POST.get('success_criteria')
        
        elif opportunity_type == 'internship':
            opportunity.duration_months = request.POST.get('duration_months')
            opportunity.stipend_amount = request.POST.get('stipend_amount')
            opportunity.responsibilities = request.POST.get('responsibilities')
            opportunity.conversion_potential = request.POST.get('conversion_potential') == 'on'
        
        elif opportunity_type == 'skill_challenge':
            opportunity.challenge_description = request.POST.get('challenge_description')
            if request.FILES.get('dataset_file'):
                opportunity.dataset_file = request.FILES['dataset_file']
            opportunity.dataset_link = request.POST.get('dataset_link')
            deadline_str = request.POST.get('submission_deadline')
            if deadline_str:
                opportunity.submission_deadline = deadline_str
            opportunity.public_rating = request.POST.get('public_rating') == 'on'
        
        opportunity.save()
        
        # Send invitations to shortlisted developers
        for dev_id in shortlist_ids:
            developer = User.objects.get(id=dev_id)
            invitation = Invitation.objects.create(
                opportunity=opportunity,
                developer=developer,
                status='pending'
            )
            
            # Create notification
            from .models import Notification
            Notification.objects.create(
                user=developer,
                notification_type='invitation_received',
                title=f'New {opportunity.get_opportunity_type_display()} Invitation!',
                message=f'{request.user.username} invited you to: {opportunity.title}',
                link=f'/my-invitations/',
                invitation=invitation
            )
        
        # Clear shortlist
        request.session['shortlist'] = []
        request.session.modified = True
        
        messages.success(request, f'✨ Opportunity created and {len(shortlist_ids)} invitations sent!')
        return redirect('company_dashboard')
    
    context = {
        'shortlist': shortlist,
        'shortlist_count': len(shortlist_ids),
    }
    
    return render(request, 'create_opportunity.html', context)


@login_required
@company_required
def company_dashboard(request):
    """Company dashboard showing opportunities, invitations, and submissions"""
    opportunities = Opportunity.objects.filter(company=request.user).annotate(
        invitation_count=Count('invitations'),
        accepted_count=Count('invitations', filter=Q(invitations__status='accepted')),
        submission_count=Count('invitations__submission')
    )
    
    invitations = Invitation.objects.filter(opportunity__company=request.user).select_related(
        'developer', 'opportunity'
    )
    
    # Get submissions awaiting rating
    pending_submissions = Submission.objects.filter(
        invitation__opportunity__company=request.user,
        rating__isnull=True
    ).select_related('invitation__developer', 'invitation__opportunity')
    
    context = {
        'opportunities': opportunities,
        'invitations': invitations,
        'pending_submissions': pending_submissions,
    }
    
    return render(request, 'company_dashboard.html', context)


@login_required
@developer_required
def my_invitations(request):
    """Developer view to see all invitations"""
    # Pending invitations
    pending_invitations = Invitation.objects.filter(
        developer=request.user,
        status='pending'
    ).select_related('opportunity__company')
    
    # Active trials (accepted but not submitted)
    active_trials = Invitation.objects.filter(
        developer=request.user,
        status='accepted',
        submission__isnull=True
    ).select_related('opportunity__company')
    
    # Completed challenges (submitted)
    completed_challenges = Invitation.objects.filter(
        developer=request.user,
        status='accepted',
        submission__isnull=False
    ).select_related('opportunity__company', 'submission')
    
    context = {
        'pending_invitations': pending_invitations,
        'active_trials': active_trials,
        'completed_challenges': completed_challenges,
    }
    
    return render(request, 'my_invitations.html', context)


@login_required
@developer_required
def accept_invitation(request, invitation_id):
    """Developer accepts an invitation"""
    invitation = get_object_or_404(Invitation, id=invitation_id, developer=request.user)
    
    if invitation.status != 'pending':
        messages.error(request, '⚠️ This invitation has already been responded to.')
        return redirect('my_invitations')
    
    if request.method == 'POST':
        invitation.status = 'accepted'
        invitation.responded_at = timezone.now()
        invitation.save()
        
        # Notify company
        from .models import Notification
        Notification.objects.create(
            user=invitation.opportunity.company,
            notification_type='invitation_accepted',
            title=f'{request.user.username} accepted your invitation!',
            message=f'{request.user.username} accepted: {invitation.opportunity.title}',
            link=f'/company-dashboard/',
            invitation=invitation
        )
        
        messages.success(request, '✅ Invitation accepted! You can now submit your work.')
        return redirect('my_invitations')
    
    return redirect('my_invitations')


@login_required
@developer_required
def decline_invitation(request, invitation_id):
    """Developer declines an invitation"""
    invitation = get_object_or_404(Invitation, id=invitation_id, developer=request.user)
    
    if invitation.status != 'pending':
        messages.error(request, '⚠️ This invitation has already been responded to.')
        return redirect('my_invitations')
    
    if request.method == 'POST':
        invitation.status = 'declined'
        invitation.responded_at = timezone.now()
        invitation.save()
        
        # Notify company
        from .models import Notification
        Notification.objects.create(
            user=invitation.opportunity.company,
            notification_type='invitation_declined',
            title=f'{request.user.username} declined your invitation',
            message=f'{request.user.username} declined: {invitation.opportunity.title}',
            link=f'/company-dashboard/',
            invitation=invitation
        )
        
        messages.success(request, '✅ Invitation declined.')
        return redirect('my_invitations')
    
    return redirect('my_invitations')


@login_required
@developer_required
def submit_work(request, invitation_id):
    """Developer submits work for an accepted invitation"""
    invitation = get_object_or_404(Invitation, id=invitation_id, developer=request.user, status='accepted')
    
    # Check if already submitted
    if hasattr(invitation, 'submission'):
        messages.error(request, '⚠️ You have already submitted work for this opportunity.')
        return redirect('my_invitations')
    
    if request.method == 'POST':
        # Validate at least one submission method
        files = request.FILES.get('files')
        code_text = request.POST.get('code_text', '').strip()
        github_link = request.POST.get('github_link', '').strip()
        
        if not files and not code_text and not github_link:
            messages.error(request, '⚠️ Please provide at least one: files, code, or GitHub link.')
            return render(request, 'submit_work.html', {'invitation': invitation})
        
        # Create submission
        submission = Submission.objects.create(
            invitation=invitation,
            code_text=code_text,
            github_link=github_link,
            notes=request.POST.get('notes', '')
        )
        
        if files:
            submission.files = files
            submission.save()
        
        # Notify company
        from .models import Notification
        Notification.objects.create(
            user=invitation.opportunity.company,
            notification_type='submission_received',
            title=f'New submission from {request.user.username}!',
            message=f'{request.user.username} submitted work for: {invitation.opportunity.title}',
            link=f'/rate-submission/{submission.id}/',
        )
        
        messages.success(request, '🚀 Work submitted successfully! Waiting for company rating...')
        return redirect('my_invitations')
    
    context = {
        'invitation': invitation,
    }
    
    return render(request, 'submit_work.html', context)


@login_required
@company_required
def rate_submission(request, submission_id):
    """Company rates a developer's submission"""
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        invitation__opportunity__company=request.user
    )
    
    if submission.rating:
        messages.error(request, '⚠️ This submission has already been rated.')
        return redirect('company_dashboard')
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        feedback = request.POST.get('feedback', '').strip()
        public_feedback = request.POST.get('public_feedback') == 'on'
        
        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, '⚠️ Rating must be between 1 and 5.')
            return render(request, 'rate_submission.html', {'submission': submission})
        
        # Save rating
        submission.rating = rating
        submission.feedback = feedback
        submission.public_feedback = public_feedback
        submission.rated_at = timezone.now()
        submission.save()
        
        # Notify developer
        from .models import Notification
        Notification.objects.create(
            user=submission.invitation.developer,
            notification_type='submission_rated',
            title=f'Your submission was rated!',
            message=f'{request.user.username} rated your work: {submission.star_display()}',
            link=f'/my-invitations/',
        )
        
        messages.success(request, f'⭐ Submission rated {rating}/5!')
        return redirect('company_dashboard')
    
    context = {
        'submission': submission,
    }
    
    return render(request, 'rate_submission.html', context)



@login_required
def notifications_api(request):
    """API endpoint for notifications"""
    if request.method == 'GET':
        notifications = request.user.notifications.all()[:10]
        unread_count = request.user.notifications.filter(is_read=False).count()
        
        notifications_data = [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'link': n.link,
            'is_read': n.is_read,
            'created_at': n.created_at.strftime('%b %d, %Y %H:%M'),
        } for n in notifications]
        
        return JsonResponse({
            'notifications': notifications_data,
            'unread_count': unread_count,
        })
    
    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'mark_read':
            notification_id = request.POST.get('notification_id')
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        
        elif action == 'mark_all_read':
            request.user.notifications.filter(is_read=False).update(is_read=True)
            return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
def toggle_company_mode(request):
    """Toggle between company and developer mode (for testing/prototyping)"""
    request.user.is_company = not request.user.is_company
    request.user.save()
    
    if request.user.is_company:
        messages.success(request, '🏢 Switched to Company Mode! You can now browse developers and create opportunities.')
        return redirect('ghost_selector')
    else:
        messages.success(request, '👻 Switched to Developer Mode! You can now receive invitations.')
        return redirect('haunted_portfolio')
