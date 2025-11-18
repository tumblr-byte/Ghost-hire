# Requirements Document - Ghost Trials System

## Introduction

Ghost Trials is an invitation-only opportunity system where companies browse developer portfolios, create opportunities (paid trials, internships, or skill challenges), and invite selected developers. Developers receive invitations passively, complete work, and receive ratings that become their "experience" proof on their profile. This system eliminates traditional job applications and focuses on invitation-based opportunities.

## Glossary

- **System**: The Ghost Trials opportunity and invitation system
- **Company**: A user account representing a company that can create opportunities and invite developers
- **Developer**: A user account representing a developer who receives invitations
- **Opportunity**: A paid trial, internship, or skill challenge created by a company
- **Invitation**: A request sent by a company to a specific developer for an opportunity
- **Submission**: Work submitted by a developer for an accepted opportunity
- **Rating**: A 1-5 star rating given by a company on a developer's submission
- **Challenge Experience**: The section on a developer's profile showing completed challenges with ratings

## Requirements

### Requirement 1: Company Ghost Selector

**User Story:** As a company, I want to browse and filter developers by skills and metrics, so that I can find the right candidates for my opportunity

#### Acceptance Criteria

1. WHEN a company user accesses the Ghost Selector, THE System SHALL display all verified developers with their portfolios
2. WHEN a company applies filters, THE System SHALL filter developers by skills, ghost level, and code authenticity percentage
3. WHEN a company views a developer card, THE System SHALL display the developer's avatar, username, top 3 skills, ghost level, and key stats
4. WHEN a company clicks "Add to Shortlist", THE System SHALL add the developer to the company's shortlist for the current session
5. WHEN a company views their shortlist, THE System SHALL display all selected developers with an option to remove them

### Requirement 2: Create Opportunity with Type Selection

**User Story:** As a company, I want to create different types of opportunities (paid trial, internship, challenge), so that I can offer various engagement models to developers

#### Acceptance Criteria

1. WHEN a company creates an opportunity, THE System SHALL provide radio button options for opportunity type: Paid Trial, Internship, or Skill Challenge
2. WHEN "Paid Trial" is selected, THE System SHALL display fields for trial description, payment amount, time limit in hours, and success criteria
3. WHEN "Internship" is selected, THE System SHALL display fields for duration (1-6 months), stipend amount, responsibilities, and full-time conversion potential
4. WHEN "Skill Challenge" is selected, THE System SHALL display fields for challenge description, dataset/requirements upload, submission deadline, and public rating checkbox
5. WHEN a company submits the opportunity form, THE System SHALL create the opportunity record and allow selection of developers to invite

### Requirement 3: Send Invitations to Selected Developers

**User Story:** As a company, I want to send invitations to my shortlisted developers, so that they can review and accept the opportunity

#### Acceptance Criteria

1. WHEN a company completes the opportunity form, THE System SHALL display the shortlist of selected developers
2. WHEN a company clicks "Send Invitations", THE System SHALL create an invitation record for each selected developer with status "pending"
3. WHEN invitations are sent, THE System SHALL create notifications for each invited developer
4. WHEN invitations are created, THE System SHALL redirect the company to their Invitation Dashboard
5. WHEN a company views their dashboard, THE System SHALL display sent invitations with current status (pending/accepted/declined)

### Requirement 4: Developer Receives and Responds to Invitations

**User Story:** As a developer, I want to receive invitation notifications and review opportunity details, so that I can decide whether to accept or decline

#### Acceptance Criteria

1. WHEN a developer receives an invitation, THE System SHALL create a notification with the company name and opportunity type
2. WHEN a developer clicks the notification, THE System SHALL navigate to the "My Invitations" page
3. WHEN a developer views an invitation, THE System SHALL display company name, opportunity type icon, description, payment/stipend, deadline, and required skills
4. WHEN a developer clicks "Accept Invitation", THE System SHALL update invitation status to "accepted" and notify the company
5. WHEN a developer clicks "Decline", THE System SHALL update invitation status to "declined" and notify the company

### Requirement 5: Submission and Rating System

**User Story:** As a developer, I want to submit my work for accepted opportunities, so that I can complete the challenge and receive a rating

#### Acceptance Criteria

1. WHEN a developer accepts an invitation, THE System SHALL display the opportunity in the "Active Trials" section with a submission form
2. WHEN a developer submits work, THE System SHALL create a submission record with files/code and timestamp
3. WHEN a submission is created, THE System SHALL notify the company and update status to "Waiting for rating"
4. WHEN a company rates a submission, THE System SHALL store the rating (1-5 stars) and optional feedback
5. WHEN a submission is rated, THE System SHALL notify the developer and display the rating on their profile

### Requirement 6: Challenge Experience on Developer Profile

**User Story:** As a developer, I want completed challenges with ratings to appear on my profile, so that I can showcase my experience to other companies

#### Acceptance Criteria

1. WHEN a developer's submission is rated, THE System SHALL add the challenge to the "Challenge Experience" section on their profile
2. WHEN displaying challenge experience, THE System SHALL show company name, challenge title, star rating, feedback quote, completion date, and type badge
3. WHEN calculating profile summary, THE System SHALL display average rating, total challenges completed, and number of companies endorsed by
4. WHEN a company views a developer profile, THE System SHALL prominently display the Challenge Experience section
5. WHEN challenge experience is empty, THE System SHALL display a message encouraging the developer to accept invitations

### Requirement 7: Passive Developer Experience

**User Story:** As a developer, I want to only see opportunities I'm invited to, so that I'm not overwhelmed by browsing job boards

#### Acceptance Criteria

1. WHEN a developer accesses the opportunities section, THE System SHALL only display invitations sent to them
2. WHEN a developer searches for opportunities, THE System SHALL not provide a browse or search feature for all opportunities
3. WHEN a developer views their dashboard, THE System SHALL show three sections: Pending Invitations, Active Trials, and Completed Challenges
4. WHEN a developer has no invitations, THE System SHALL display a message explaining the invitation-only model
5. WHEN a developer completes their profile, THE System SHALL encourage them to make their portfolio visible to companies
