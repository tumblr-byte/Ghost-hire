# Implementation Plan

- [x] 1. Create database models for Ghost Trials system




  - Create Opportunity model with type-specific fields (paid_trial, internship, skill_challenge)
  - Create Invitation model with status tracking (pending/accepted/declined)
  - Create Submission model with rating and feedback fields
  - Enhance existing Notification model with new notification types
  - Create and run Django migrations
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 5.2, 5.4_

- [x] 2. Implement Ghost Selector (company browse page)






  - [ ] 2.1 Create ghost_selector view with developer filtering
    - Query all developers (is_company=False) with portfolio data
    - Implement filters: skills (multi-select), ghost level (range), code authenticity (min %)
    - Store shortlist in session


    - _Requirements: 1.1, 1.2_
  
  - [ ] 2.2 Create ghost_selector.html template
    - Display developer cards in grid layout
    - Show avatar, username, top 3 skills, ghost level, key stats
    - Add "Add to Shortlist" button on each card
    - Create floating shortlist panel showing selected developers
    - Style with haunted theme (neon purple/green, dark background)
    - _Requirements: 1.3, 1.4, 1.5_

- [ ] 3. Implement Create Opportunity form
  - [ ] 3.1 Create OpportunityForm with conditional fields
    - Add common fields: title, description, skills_needed, full_job_details
    - Add type-specific fields for paid_trial, internship, skill_challenge
    - Implement form validation for required fields based on type

    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [ ] 3.2 Create create_opportunity view
    - Handle GET request to display form
    - Handle POST request to save opportunity
    - Retrieve shortlist from session
    - Redirect to send invitations page after creation
    - _Requirements: 2.5_
  
  - [ ] 3.3 Create create_opportunity.html template
    - Display radio buttons for opportunity type selection
    - Show/hide fields based on selected type using JavaScript
    - Display shortlist from session with remove option
    - Style form with haunted theme

    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 4. Implement invitation sending system
  - [ ] 4.1 Create send_invitations view
    - Retrieve opportunity and shortlisted developer IDs from session
    - Create Invitation record for each developer with status "pending"
    - Create Notification for each invited developer

    - Clear shortlist from session
    - Redirect to company dashboard
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ] 4.2 Add invitation notification creation logic
    - Generate notification title and message based on opportunity type

    - Include company name and opportunity details
    - Set notification link to invitation detail page
    - _Requirements: 3.3, 4.1_

- [ ] 5. Implement Company Dashboard
  - [ ] 5.1 Create company_dashboard view
    - Query opportunities created by company
    - Query invitations grouped by opportunity with status counts
    - Query submissions awaiting rating
    - _Requirements: 3.5_
  
  - [ ] 5.2 Create company_dashboard.html template
    - Display "My Opportunities" section with opportunity cards
    - Display "Sent Invitations" section grouped by opportunity

    - Display "To Review" section with pending submissions
    - Add links to rate submissions
    - Style with haunted theme
    - _Requirements: 3.5_

- [ ] 6. Implement Developer Invitations page
  - [ ] 6.1 Create my_invitations view
    - Query invitations for current developer
    - Separate into: pending, active (accepted), completed (rated)
    - _Requirements: 4.2, 7.3_
  
  - [ ] 6.2 Create my_invitations.html template
    - Display three sections: Pending Invitations, Active Trials, Completed
    - Show invitation cards with company name, type icon, description, payment, deadline, skills

    - Add "Accept Invitation" and "Decline" buttons for pending
    - Show submission form link for active trials
    - Display ratings for completed challenges
    - Style with haunted theme and type-specific icons (💰/🎓/⭐)
    - _Requirements: 4.2, 4.3, 7.1, 7.2, 7.3, 7.4_


- [ ] 7. Implement invitation response system
  - [ ] 7.1 Create accept_invitation view
    - Update invitation status to "accepted"
    - Set responded_at timestamp
    - Create notification for company
    - Redirect to active trials section
    - _Requirements: 4.4_
  
  - [ ] 7.2 Create decline_invitation view
    - Update invitation status to "declined"
    - Set responded_at timestamp
    - Create notification for company

    - Redirect to invitations page
    - _Requirements: 4.5_

- [ ] 8. Implement submission system
  - [ ] 8.1 Create SubmissionForm
    - Add fields: files (FileField), code_text (TextField), github_link (URLField), notes (TextField)
    - Validate that at least one submission method is provided
    - _Requirements: 5.1_
  
  - [ ] 8.2 Create submit_work view
    - Verify invitation is accepted and belongs to current user
    - Handle file upload and form submission
    - Create Submission record
    - Create notification for company
    - Update invitation status display
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ] 8.3 Create submit_work.html template
    - Display opportunity details at top
    - Show file upload field with drag-and-drop
    - Show code text area with syntax highlighting
    - Show GitHub link field
    - Show notes field
    - Add submit button

    - Style with haunted theme
    - _Requirements: 5.1_

- [ ] 9. Implement rating system
  - [ ] 9.1 Create RatingForm
    - Add star rating field (1-5)
    - Add feedback TextField
    - Add public_feedback checkbox
    - _Requirements: 5.4_
  
  - [ ] 9.2 Create rate_submission view
    - Verify submission belongs to company's opportunity
    - Save rating, feedback, and rated_at timestamp
    - Create notification for developer
    - Redirect to company dashboard
    - _Requirements: 5.4, 5.5_
  
  - [ ] 9.3 Create rate_submission.html template
    - Display submission details and files
    - Show star rating selector (interactive)
    - Show feedback text area
    - Show public feedback checkbox with explanation
    - Add submit button
    - Style with haunted theme
    - _Requirements: 5.4_

- [ ] 10. Add Challenge Experience section to developer profile
  - [ ] 10.1 Update haunted_portfolio.html with Challenge Experience section
    - Display experience summary: average rating, challenges completed, companies endorsed
    - Display challenge cards for each rated submission
    - Show company logo/name, challenge title, star rating, type badge, feedback quote, completion date
    - Handle empty state with encouraging message
    - Style with haunted theme and animations
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ] 10.2 Create helper function to calculate challenge experience stats
    - Calculate average rating from all rated submissions
    - Count total challenges completed
    - Count unique companies that rated the developer
    - Return stats dictionary for template

    - _Requirements: 6.3_


- [ ] 11. Implement notification bell system
  - [ ] 11.1 Update base.html with notification bell icon
    - Add bell icon to navigation bar
    - Display unread notification count badge
    - Add dropdown showing recent notifications
    - Mark notifications as read when clicked


    - Style with haunted theme (pulsing animation for unread)
    - _Requirements: 4.1_
  
  - [ ] 11.2 Create notifications_api view
    - Return JSON with unread count and recent notifications
    - Mark notification as read endpoint
    - Mark all as read endpoint
    - _Requirements: 4.1_

- [ ] 12. Add deadline reminder system
  - Create Celery task to check for approaching deadlines (24 hours)
  - Send "deadline_approaching" notifications to developers
  - Schedule task to run hourly
  - _Requirements: 4.1_



- [x] 13. Implement role-based access control


  - [ ] 13.1 Add is_company field to User model
    - Create migration to add boolean field
    - Update user registration to set is_company flag


    - _Requirements: 7.1, 7.2_
  
  - [ ] 13.2 Create permission decorators
    - Create @company_required decorator for company-only views
    - Create @developer_required decorator for developer-only views
    - Apply decorators to all relevant views
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 14. Add URL routing for Ghost Trials
  - Add URL patterns for all new views
  - Include: ghost_selector, create_opportunity, send_invitations, company_dashboard, my_invitations, accept_invitation, decline_invitation, submit_work, rate_submission
  - Add notification API endpoints
  - _Requirements: All requirements_

- [ ] 15. Style Ghost Trials with haunted theme
  - [ ] 15.1 Create ghost_trials.css stylesheet
    - Define color palette (neon purple, neon green, dark backgrounds)
    - Style opportunity type badges (💰/🎓/⭐)
    - Style invitation cards with hover effects
    - Style rating stars with glow effect
    - Add floating ghost animations
    - Ensure mobile responsiveness
    - _Requirements: All requirements_
  
  - [ ] 15.2 Add JavaScript interactions
    - Shortlist add/remove functionality
    - Opportunity form field show/hide based on type
    - Star rating interactive selector
    - Notification dropdown toggle
    - Smooth scroll animations

    - _Requirements: All requirements_

- [ ] 16. Add navigation links for Ghost Trials
  - Update base.html navigation to include Ghost Trials links
  - Show "Ghost Selector" and "My Opportunities" for companies
  - Show "My Invitations" for developers
  - Add notification bell for all users
  - _Requirements: All requirements_

- [ ] 17. Add email notifications
  - Send email when invitation received
  - Send email when submission rated
  - Send email for deadline reminders
  - Use Django email backend
  - _Requirements: 4.1, 5.5_

- [ ] 18. Add analytics dashboard for companies
  - Show invitation acceptance rate
  - Show average time to submission
  - Show rating distribution
  - Display charts with Chart.js
  - _Requirements: 3.5_
