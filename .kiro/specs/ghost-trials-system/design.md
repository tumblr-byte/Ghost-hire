# Ghost Trials System - Design Document

## Overview

Ghost Trials is an invitation-only opportunity platform where companies actively browse and invite developers, while developers passively receive and respond to invitations. The system supports three opportunity types (Paid Trials, Internships, Skill Challenges) and builds developer "experience" through company ratings.

**Key Design Principles:**
- Developers are passive recipients (no browsing/applying)
- Companies are active selectors (browse, filter, invite)
- Rating system creates verifiable experience
- Haunted theme throughout UI

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     COMPANY WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│  Ghost Selector → Shortlist → Create Opportunity → Invite   │
│       ↓              ↓              ↓                ↓       │
│   Filter/Browse   Session Store   Form with Types   Batch   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   DEVELOPER WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│  Notification → View Invitation → Accept → Submit → Rating  │
│       ↓              ↓              ↓         ↓        ↓     │
│   Bell Icon    Invitation Page   Active    Upload   Profile │
└─────────────────────────────────────────────────────────────┘
```

### User Roles

**Company Users:**
- Can browse all developer profiles
- Can create opportunities
- Can send invitations
- Can rate submissions
- Cannot receive invitations

**Developer Users:**
- Can receive invitations
- Can accept/decline invitations
- Can submit work
- Can view their ratings
- Cannot browse opportunities

## Components and Interfaces

### 1. Ghost Selector (Company Browse Page)

**URL:** `/ghost-selector/`

**View:** `ghost_selector(request)`

**Features:**
- Grid of developer cards with key stats
- Filters: skills (multi-select), ghost level (range), code authenticity (min %)
- "Add to Shortlist" button on each card
- Floating shortlist panel showing selected developers
- Shortlist stored in session

**Template:** `templates/ghost_selector.html`

**Data Required:**
- All developers with `is_company=False`
- Portfolio data (ghost_level, ai_percentage, top_skills)
- Session-based shortlist

### 2. Create Opportunity Form

**URL:** `/create-opportunity/`

**View:** `create_opportunity(request)`

**Form Structure:**
```python
# Common fields (all types)
- title (CharField)
- description (TextField)
- skills_needed (MultipleChoiceField)
- full_job_details (TextField, optional)

# Type-specific fields (conditional rendering)
PAID_TRIAL:
  - payment (DecimalField)
  - time_limit_hours (IntegerField)
  - success_criteria (TextField)

INTERNSHIP:
  - duration_months (IntegerField, 1-6)
  - stipend_amount (DecimalField, can be 0)
  - responsibilities (TextField)
  - conversion_potential (BooleanField)

SKILL_CHALLENGE:
  - challenge_description (TextField)
  - dataset_file (FileField, optional)
  - dataset_link (URLField, optional)
  - submission_deadline (DateTimeField)
  - public_rating (BooleanField)
```

**Template:** `templates/create_opportunity.html`

**JavaScript:**
- Show/hide fields based on opportunity type radio selection
- Display shortlist from session
- Allow removing developers from shortlist

### 3. Send Invitations

**URL:** `/send-invitations/<opportunity_id>/`

**View:** `send_invitations(request, opportunity_id)`

**Logic:**
1. Retrieve opportunity
2. Get shortlisted developer IDs from session
3. Create Invitation record for each developer
4. Create Notification for each developer
5. Clear shortlist from session
6. Redirect to company dashboard

### 4. Company Dashboard

**URL:** `/company-dashboard/`

**View:** `company_dashboard(request)`

**Sections:**
- **My Opportunities:** List of created opportunities
- **Sent Invitations:** Grouped by opportunity, showing status
- **Pending Submissions:** Accepted invitations awaiting submission
- **To Review:** Submissions awaiting rating

**Template:** `templates/company_dashboard.html`

### 5. Developer Invitations Page

**URL:** `/my-invitations/`

**View:** `my_invitations(request)`

**Sections:**
- **Pending Invitations:** Awaiting response
- **Active Trials:** Accepted, awaiting submission
- **Completed:** Submitted and rated

**Template:** `templates/my_invitations.html`

**Invitation Card Display:**
```
┌─────────────────────────────────────────┐
│ 💰 PAID TRIAL                           │
│ [Company Logo] Company Name             │
│ ─────────────────────────────────────   │
│ Title: Senior Backend Trial             │
│ Payment: ₹15,000                        │
│ Duration: 40 hours                      │
│ Deadline: Dec 25, 2025                  │
│ Skills: Python, Django, PostgreSQL      │
│ ─────────────────────────────────────   │
│ [Accept Invitation] [Decline]           │
└─────────────────────────────────────────┘
```

### 6. Submission Interface

**URL:** `/submit-work/<invitation_id>/`

**View:** `submit_work(request, invitation_id)`

**Form:**
- File upload (multiple files)
- Code/text submission (TextField)
- GitHub repo link (URLField, optional)
- Notes for company (TextField, optional)

**Template:** `templates/submit_work.html`

### 7. Rate Submission

**URL:** `/rate-submission/<submission_id>/`

**View:** `rate_submission(request, submission_id)`

**Form:**
- Star rating (1-5)
- Feedback (TextField)
- Public feedback checkbox (for profile display)

**Template:** `templates/rate_submission.html`

### 8. Challenge Experience Section (Profile)

**Location:** Added to `templates/haunted_portfolio.html`

**Display:**
```html
<section class="challenge-experience">
  <h2>👻 Challenge Experience</h2>
  
  <div class="experience-summary">
    <div class="stat">⭐ 4.7/5 Average Rating</div>
    <div class="stat">🏆 12 Challenges Completed</div>
    <div class="stat">🏢 8 Companies Endorsed</div>
  </div>
  
  <div class="challenge-cards">
    <!-- For each rated submission -->
    <div class="challenge-card">
      <div class="company-info">
        <img src="company_logo" />
        <span>Company Name</span>
      </div>
      <h3>Challenge Title</h3>
      <div class="rating">⭐⭐⭐⭐⭐</div>
      <div class="type-badge">💰 Paid Trial</div>
      <blockquote>"Excellent problem-solving skills..."</blockquote>
      <div class="date">Completed: Nov 15, 2025</div>
    </div>
  </div>
</section>
```

## Data Models

### Opportunity Model

```python
class Opportunity(models.Model):
    OPPORTUNITY_TYPES = [
        ('paid_trial', 'Paid Trial'),
        ('internship', 'Internship'),
        ('skill_challenge', 'Skill Challenge'),
    ]
    
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    skills_needed = models.JSONField()  # List of skill strings
    full_job_details = models.TextField(blank=True, null=True)
    
    # Paid Trial fields
    payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    time_limit_hours = models.IntegerField(null=True, blank=True)
    success_criteria = models.TextField(null=True, blank=True)
    
    # Internship fields
    duration_months = models.IntegerField(null=True, blank=True)
    stipend_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    responsibilities = models.TextField(null=True, blank=True)
    conversion_potential = models.BooleanField(default=False)
    
    # Skill Challenge fields
    challenge_description = models.TextField(null=True, blank=True)
    dataset_file = models.FileField(upload_to='challenge_datasets/', null=True, blank=True)
    dataset_link = models.URLField(null=True, blank=True)
    submission_deadline = models.DateTimeField(null=True, blank=True)
    public_rating = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_opportunity_type_display()})"
```

### Invitation Model

```python
class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='invitations')
    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['opportunity', 'developer']
    
    def __str__(self):
        return f"{self.opportunity.title} → {self.developer.username}"
```

### Submission Model

```python
class Submission(models.Model):
    invitation = models.OneToOneField(Invitation, on_delete=models.CASCADE, related_name='submission')
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    # Submission content
    files = models.FileField(upload_to='submissions/', null=True, blank=True)
    code_text = models.TextField(blank=True)
    github_link = models.URLField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Rating
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(null=True, blank=True)
    public_feedback = models.BooleanField(default=False)
    rated_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Submission for {self.invitation}"
```

### Notification Model (Enhanced)

```python
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('invitation_received', 'Invitation Received'),
        ('invitation_accepted', 'Invitation Accepted'),
        ('invitation_declined', 'Invitation Declined'),
        ('submission_received', 'Submission Received'),
        ('submission_rated', 'Submission Rated'),
        ('deadline_approaching', 'Deadline Approaching'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Related objects
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
```

## Error Handling

### Company Workflow Errors

1. **Empty Shortlist:** Display error message "Please add at least one developer to your shortlist"
2. **Invalid Opportunity Data:** Form validation with clear error messages
3. **Duplicate Invitation:** Prevent sending invitation to same developer twice for same opportunity
4. **Unauthorized Access:** Redirect non-company users attempting to access company features

### Developer Workflow Errors

1. **Expired Invitation:** Display "This invitation has expired" if past deadline
2. **Already Responded:** Prevent accepting/declining already-responded invitations
3. **Missing Submission:** Validate that files or code are provided before submission
4. **Unauthorized Access:** Prevent viewing other developers' invitations

## Testing Strategy

### Unit Tests

1. **Model Tests:**
   - Opportunity creation with different types
   - Invitation status transitions
   - Submission rating validation
   - Notification creation

2. **View Tests:**
   - Ghost selector filtering
   - Opportunity form validation
   - Invitation sending logic
   - Submission upload

### Integration Tests

1. **Complete Company Flow:**
   - Browse developers → Shortlist → Create opportunity → Send invitations
   
2. **Complete Developer Flow:**
   - Receive notification → View invitation → Accept → Submit → View rating

3. **Profile Display:**
   - Challenge experience section renders correctly
   - Average rating calculation
   - Empty state handling

### UI/UX Tests

1. **Responsive Design:** Test on mobile, tablet, desktop
2. **Haunted Theme:** Verify neon colors, ghost icons, spooky animations
3. **Interactive Elements:** Shortlist panel, notification bell, card hover effects
4. **Form Validation:** Real-time feedback on form errors

## Security Considerations

1. **Role-Based Access:**
   - Companies cannot receive invitations
   - Developers cannot browse opportunities
   - Users can only view their own invitations/submissions

2. **File Upload Security:**
   - Validate file types for submissions and datasets
   - Limit file sizes
   - Scan for malicious content

3. **Data Privacy:**
   - Developers control profile visibility
   - Companies cannot see declined invitation reasons
   - Feedback visibility controlled by public_feedback flag

## Performance Optimization

1. **Ghost Selector:**
   - Paginate developer list (20 per page)
   - Cache portfolio data
   - Index on skills_needed for filtering

2. **Notifications:**
   - Batch create invitations
   - Use Celery for async notification creation
   - Mark notifications as read in bulk

3. **Profile Display:**
   - Cache challenge experience section
   - Lazy load challenge cards
   - Precompute average ratings

## Haunted Theme Design

### Color Palette
- Primary: Neon Purple (#9D4EDD)
- Secondary: Neon Green (#39FF14)
- Background: Dark (#0D0D0D)
- Cards: Dark Gray (#1A1A1A)
- Text: Light Gray (#E0E0E0)

### Icons
- 💰 Paid Trial
- 🎓 Internship
- ⭐ Skill Challenge
- 🔔 Notifications
- 👻 Ghost Level
- 🏆 Achievements

### Animations
- Floating ghost on hover
- Pulsing notification bell
- Card glow on hover
- Smooth transitions
- Lightning effects on ratings
