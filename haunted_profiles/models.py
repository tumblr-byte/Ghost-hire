from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom manager for User model"""
    
    def create_user(self, email, username, password=None, **extra_fields):
        """Create and save a regular user"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model for Ghost Hire platform"""
    
    google_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    verification_photo = models.ImageField(
        upload_to='verification_photos/', 
        blank=True, 
        null=True,
        help_text='Private photo for verification only - never shown publicly'
    )
    ghost_avatar = models.ImageField(
        upload_to='ghost_avatars/', 
        default='ghost_avatars/1.png',
        help_text='Public profile avatar'
    )
    is_verified = models.BooleanField(default=False)
    ghost_level = models.IntegerField(default=1)
    skills = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    
    # Self-Description for AI Analysis
    developer_role = models.CharField(
        max_length=200, 
        blank=True,
        help_text='What you do (e.g., Computer Vision Developer, Full Stack Engineer)'
    )
    core_skills = models.TextField(
        blank=True,
        help_text='Your main skills (e.g., Object Detection, SGAN, PyTorch, React)'
    )
    strengths = models.TextField(
        blank=True,
        help_text='What you are good at (e.g., ML algorithms, backend optimization)'
    )
    weaknesses = models.TextField(
        blank=True,
        help_text='What you use AI help for (e.g., UI/UX, Streamlit, CSS styling)'
    )
    coding_journey = models.TextField(
        blank=True,
        help_text='Your coding journey and what you are learning'
    )
    
    # Enhanced Expertise Fields for Portfolio Analysis
    expertise_area = models.CharField(
        max_length=200,
        blank=True,
        help_text='Primary expertise (e.g., Computer Vision, Backend Engineering)'
    )
    expertise_details = models.TextField(
        blank=True,
        help_text='What you know in your expertise area'
    )
    learning_journey = models.TextField(
        blank=True,
        help_text='Your learning path and growth story'
    )
    ai_usage_context = models.TextField(
        blank=True,
        help_text='Where and how you use AI in your workflow'
    )
    non_expertise_areas = models.TextField(
        blank=True,
        help_text='Areas where you rely on AI (e.g., UI/UX, DevOps)'
    )
    
    # Social Links
    github_link = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    devpost_url = models.URLField(blank=True)
    
    # AI-Analyzed Portfolio Data (scraped from links)
    portfolio_data = models.JSONField(default=dict, blank=True, help_text='AI-analyzed skills and achievements')
    last_portfolio_update = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Required fields for Django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_company = models.BooleanField(default=False, help_text='Is this user a company account?')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'haunted_profiles_user'
        indexes = [
            models.Index(fields=['google_id']),
            models.Index(fields=['username']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username



# ============================================
# GHOST CREW MODELS
# ============================================

class GhostCrew(models.Model):
    """A crew of max 5 developers for hackathons"""
    name = models.CharField(max_length=100, help_text="Crew name (e.g., 'The Python Haunters')")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_crews')
    members = models.ManyToManyField(User, related_name='crews', blank=True)
    crew_bio = models.TextField(max_length=300, blank=True, help_text="What's your crew about?")
    hackathons_won = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Ghost Crews"
    
    def __str__(self):
        return self.name
    
    def member_count(self):
        return self.members.count()
    
    def is_full(self):
        return self.members.count() >= 5


class CrewInvitation(models.Model):
    """Invitation to join a Ghost Crew"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    crew = models.ForeignKey(GhostCrew, on_delete=models.CASCADE, related_name='invitations')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    message = models.TextField(max_length=200, blank=True, help_text="Why should they join?")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['crew', 'to_user']
    
    def __str__(self):
        return f"{self.from_user.username} invited {self.to_user.username} to {self.crew.name}"


class CrewMessage(models.Model):
    """Messages in Ghost Crew chat"""
    crew = models.ForeignKey(GhostCrew, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    is_code = models.BooleanField(default=False, help_text="Is this a code snippet?")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username} in {self.crew.name}"


# ============================================
# THE GRAVEYARD MODELS (Roast Zone)
# ============================================

class GraveyardPost(models.Model):
    """A project post in The Graveyard to get roasted"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='graveyard_posts')
    title = models.CharField(max_length=200, help_text="What did you build?")
    description = models.TextField(max_length=1000, help_text="Tell us about it")
    code_snippet = models.TextField(blank=True, help_text="Paste your code (optional)")
    project_link = models.URLField(blank=True, help_text="GitHub/Demo link")
    image = models.ImageField(upload_to='graveyard_posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    roast_score = models.IntegerField(default=0, help_text="How helpful are the roasts?")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    def chant_count(self):
        return self.chants.count()


class GhostChant(models.Model):
    """A Ghost Chant (comment) on a Graveyard post - can be praise or constructive feedback!"""
    post = models.ForeignKey(GraveyardPost, on_delete=models.CASCADE, related_name='chants')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chants')
    chant = models.TextField(max_length=500, help_text="Be honest - praise or constructive feedback!")
    is_helpful = models.BooleanField(default=False, help_text="Marked helpful by post author")
    upvotes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upvotes', '-created_at']
    
    def __str__(self):
        return f"Ghost Chant by {self.author.username} on {self.post.title}"



# ============================================
# THE SUMMONING CIRCLE (Hiring/Jobs)
# ============================================

class SummoningPost(models.Model):
    """A job posting in The Summoning Circle - NO DEGREE REQUIRED!"""
    company_name = models.CharField(max_length=200)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    job_title = models.CharField(max_length=200, help_text="What role are you summoning?")
    description = models.TextField(max_length=2000, help_text="What will they do?")
    required_skills = models.JSONField(default=list, help_text="Skills needed (e.g., Python, React)")
    location = models.CharField(max_length=200, help_text="Remote/City")
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., $60k-$80k")
    is_remote = models.BooleanField(default=True)
    no_degree_required = models.BooleanField(default=True, help_text="Self-taught devs welcome!")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    def application_count(self):
        return self.applications.count()


class JobApplication(models.Model):
    """When a ghost haunts a job (applies)"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('summoned', 'Summoned! (Hired)'),
        ('rejected', 'Not This Time'),
    ]
    
    job = models.ForeignKey(SummoningPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    cover_message = models.TextField(max_length=500, help_text="Why should they summon you?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.applicant.username} haunting {self.job.job_title}"



# ============================================
# GHOST HUNT - CONNECTION SYSTEM
# ============================================

class Connection(models.Model):
    """Connection between two ghosts (users)"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['requester', 'receiver']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.requester.username} → {self.receiver.username} ({self.status})"


class Notification(models.Model):
    """In-app notifications for users"""
    NOTIFICATION_TYPES = [
        ('connection_request', 'Connection Request'),
        ('connection_accepted', 'Connection Accepted'),
        ('connection_rejected', 'Connection Rejected'),
        ('invitation_received', 'Invitation Received'),
        ('invitation_accepted', 'Invitation Accepted'),
        ('invitation_declined', 'Invitation Declined'),
        ('submission_received', 'Submission Received'),
        ('submission_rated', 'Submission Rated'),
        ('deadline_approaching', 'Deadline Approaching'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200, blank=True, default='')
    link = models.CharField(max_length=200, null=True, blank=True)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='triggered_notifications', null=True, blank=True)
    related_connection = models.ForeignKey(Connection, on_delete=models.CASCADE, null=True, blank=True)
    invitation = models.ForeignKey('Invitation', on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.notification_type}"
    
    def time_ago(self):
        """Return human-readable time ago"""
        from django.utils import timezone
        diff = timezone.now() - self.created_at
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "just now"



# ============================================
# GHOST TRIALS - INVITATION-ONLY OPPORTUNITIES
# ============================================

class Opportunity(models.Model):
    """Opportunities created by companies (Paid Trials, Internships, Skill Challenges)"""
    OPPORTUNITY_TYPES = [
        ('paid_trial', 'Paid Trial'),
        ('internship', 'Internship'),
        ('skill_challenge', 'Skill Challenge'),
    ]
    
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_needed = models.JSONField(default=list, help_text='List of required skills')
    full_job_details = models.TextField(blank=True, help_text='Full job description if successful')
    
    # Paid Trial fields
    payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Payment amount')
    time_limit_hours = models.IntegerField(null=True, blank=True, help_text='Time limit in hours')
    success_criteria = models.TextField(null=True, blank=True, help_text='What defines success')
    
    # Internship fields
    duration_months = models.IntegerField(null=True, blank=True, help_text='Duration in months (1-6)')
    stipend_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Monthly stipend (₹0 if unpaid)')
    responsibilities = models.TextField(null=True, blank=True, help_text='Day-to-day responsibilities')
    conversion_potential = models.BooleanField(default=False, help_text='Can lead to full-time role')
    
    # Skill Challenge fields
    challenge_description = models.TextField(null=True, blank=True, help_text='Challenge details')
    dataset_file = models.FileField(upload_to='challenge_datasets/', null=True, blank=True, help_text='Dataset or requirements file')
    dataset_link = models.URLField(null=True, blank=True, help_text='Link to dataset/requirements')
    submission_deadline = models.DateTimeField(null=True, blank=True, help_text='Submission deadline')
    public_rating = models.BooleanField(default=False, help_text='Will publicly rate all submissions')
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Opportunities'
    
    def __str__(self):
        return f"{self.title} ({self.get_opportunity_type_display()})"
    
    def invitation_count(self):
        return self.invitations.count()
    
    def accepted_count(self):
        return self.invitations.filter(status='accepted').count()
    
    def submission_count(self):
        return Submission.objects.filter(invitation__opportunity=self).count()


class Invitation(models.Model):
    """Invitation sent by company to developer for an opportunity"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='invitations')
    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trial_invitations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['opportunity', 'developer']
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.opportunity.title} → {self.developer.username} ({self.status})"
    
    def has_submission(self):
        return hasattr(self, 'submission')
    
    def is_expired(self):
        """Check if invitation deadline has passed"""
        if self.opportunity.submission_deadline:
            from django.utils import timezone
            return timezone.now() > self.opportunity.submission_deadline
        return False


class Submission(models.Model):
    """Work submitted by developer for an accepted opportunity"""
    invitation = models.OneToOneField(Invitation, on_delete=models.CASCADE, related_name='submission')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Submission content
    files = models.FileField(upload_to='submissions/', null=True, blank=True, help_text='Uploaded files/code')
    code_text = models.TextField(blank=True, help_text='Code or text submission')
    github_link = models.URLField(null=True, blank=True, help_text='GitHub repository link')
    notes = models.TextField(blank=True, help_text='Additional notes for company')
    
    # Rating from company
    rating = models.IntegerField(null=True, blank=True, help_text='Rating from 1-5 stars')
    feedback = models.TextField(null=True, blank=True, help_text='Feedback from company')
    public_feedback = models.BooleanField(default=False, help_text='Show feedback on profile')
    rated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Submission for {self.invitation.opportunity.title} by {self.invitation.developer.username}"
    
    def is_rated(self):
        return self.rating is not None
    
    def star_display(self):
        """Return star rating as string (e.g., '⭐⭐⭐⭐⭐')"""
        if self.rating:
            return '⭐' * self.rating
        return 'Not rated yet'
