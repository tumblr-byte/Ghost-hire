from django.urls import path
from . import views, auth_views

urlpatterns = [
    path('', views.index, name='index'),
    
    # WorkOS Authentication
    path('auth/login/', auth_views.workos_login, name='workos_login'),
    path('auth/callback/', auth_views.workos_callback, name='workos_callback'),
    
    # App Pages
    path('verification/', views.verification, name='verification'),
    path('tell-kiro-about-you/', views.tell_kiro_about_you, name='tell_kiro_about_you'),
    path('haunt-setup/', views.haunt_setup, name='haunt_setup'),
    path('haunted-portfolio/', views.haunted_portfolio, name='haunted_portfolio'),
    path('haunted-portfolio/<str:username>/', views.haunted_portfolio, name='haunted_portfolio_public'),
    path('refresh-portfolio/', views.refresh_portfolio, name='refresh_portfolio'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile_public'),
    path('return-to-shadows/', views.logout_view, name='logout'),
    
    # The Graveyard (Ghost Chants)
    path('graveyard/', views.graveyard, name='graveyard'),
    path('graveyard/create/', views.create_graveyard_post, name='create_graveyard_post'),
    path('graveyard/<int:post_id>/chant/', views.add_ghost_chant, name='add_ghost_chant'),
    
    # The Summoning Circle (Jobs)
    path('summoning-circle/', views.summoning_circle, name='summoning_circle'),
    path('summoning-circle/create/', views.create_summoning_post, name='create_summoning_post'),
    path('summoning-circle/<int:job_id>/haunt/', views.haunt_job, name='haunt_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('job/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    
    # Ghost Crew
    path('ghost-hunt/', views.ghost_hunt, name='ghost_hunt'),
    path('my-crews/', views.my_crews, name='my_crews'),
    path('crew/create/', views.create_crew, name='create_crew'),
    path('crew/<int:crew_id>/', views.crew_detail, name='crew_detail'),
    path('crew/invite/<int:user_id>/', views.send_crew_invitation, name='send_crew_invitation'),
    path('crew/invitations/', views.crew_invitations, name='crew_invitations'),
    path('crew/invitation/<int:invitation_id>/respond/', views.respond_to_invitation, name='respond_to_invitation'),
    path('crew/<int:crew_id>/message/', views.send_crew_message, name='send_crew_message'),
    
    # Ghost Trials - Invitation-Only Opportunities
    path('ghost-selector/', views.ghost_selector, name='ghost_selector'),
    path('create-opportunity/', views.create_opportunity, name='create_opportunity'),
    path('send-invitations/<int:opportunity_id>/', views.send_invitations, name='send_invitations'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('my-invitations/', views.my_invitations, name='my_invitations'),
    path('accept-invitation/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),
    path('decline-invitation/<int:invitation_id>/', views.decline_invitation, name='decline_invitation'),
    path('submit-work/<int:invitation_id>/', views.submit_work, name='submit_work'),
    path('rate-submission/<int:submission_id>/', views.rate_submission, name='rate_submission'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    
    # Toggle company mode (for testing/prototyping)
    path('toggle-company-mode/', views.toggle_company_mode, name='toggle_company_mode'),
]
