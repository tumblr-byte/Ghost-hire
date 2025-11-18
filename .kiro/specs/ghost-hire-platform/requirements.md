# Requirements Document

## Introduction

Ghost Hire is a haunted-themed hiring platform designed for self-taught developers to showcase their skills without traditional degree requirements. The platform uses Google OAuth for authentication, implements a verification system to ensure authentic users, and features a spooky aesthetic with neon colors and horror-themed terminology. The system allows developers to create profiles with custom avatars, upload verification photos, and display their skills in a unique, engaging environment.

## Glossary

- **Ghost Hire System**: The complete Django-based web application for the haunted hiring platform
- **Haunted Profile**: A user profile within the Ghost Hire System
- **Ghost Avatar**: A publicly visible profile image representing the user
- **Verification Photo**: A private photo uploaded by users for identity verification purposes
- **Ghost Level**: A numeric indicator of user status or progression within the platform
- **OAuth Provider**: Google's authentication service used for user login
- **Haunted Lair**: The user dashboard area (terminology replacement for "Dashboard")
- **Crypt**: The login area (terminology replacement for "Login")
- **Reverse Image Search**: A process that checks if an uploaded photo exists on the internet using SerpAPI
- **Siamese Network**: A neural network architecture used to compare two images and determine their similarity
- **Similarity Score**: A numeric value between 0 and 1 indicating how similar two face images are
- **SerpAPI**: A third-party API service for performing reverse image searches on Google Images and Pinterest
- **Profile Setup Page**: The page where verified users complete their profile information including skills and bio
- **Verified Badge**: A visual indicator shown on profiles to denote that the user has completed photo verification

## Requirements

### Requirement 1

**User Story:** As a self-taught developer, I want to authenticate using my Google account, so that I can quickly access the platform without creating separate credentials

#### Acceptance Criteria

1. WHEN a user clicks the "Rise from the Grave" button on the homepage, THE Ghost Hire System SHALL initiate Google OAuth authentication flow
2. WHEN Google OAuth successfully authenticates a user, THE Ghost Hire System SHALL create a new user record with google_id and email if the user does not exist
3. WHEN a new user record is created, THE Ghost Hire System SHALL generate a username in the format "ghost_" followed by 5 random digits
4. WHEN a new user record is created, THE Ghost Hire System SHALL set the ghost_avatar field to "1.png" as the default value
5. WHEN Google OAuth authentication completes successfully, THE Ghost Hire System SHALL redirect the user to the verification page

### Requirement 2

**User Story:** As a platform administrator, I want users to upload verification photos, so that I can ensure authentic users and prevent fraudulent accounts

#### Acceptance Criteria

1. WHEN a newly authenticated user is redirected to the verification page, THE Ghost Hire System SHALL display a file upload interface for verification photos
2. WHEN a user selects a verification photo file, THE Ghost Hire System SHALL accept image file formats including JPEG, PNG, and GIF
3. WHEN a user submits a verification photo, THE Ghost Hire System SHALL store the photo in a private media directory not accessible publicly
4. WHEN a verification photo is uploaded, THE Ghost Hire System SHALL associate the photo with the user's account record
5. THE Ghost Hire System SHALL display warning text stating "This photo is private - only for verification, never shown publicly" on the verification page

### Requirement 3

**User Story:** As a user, I want my profile to store my skills and biographical information, so that I can showcase my abilities to potential employers

#### Acceptance Criteria

1. THE Ghost Hire System SHALL store user skills as a JSON array in the database
2. THE Ghost Hire System SHALL allow the bio field to remain empty without validation errors
3. WHEN a user account is created, THE Ghost Hire System SHALL set is_verified to False by default
4. WHEN a user account is created, THE Ghost Hire System SHALL set ghost_level to 1 by default
5. WHEN a user account is created, THE Ghost Hire System SHALL record the created_at timestamp automatically

### Requirement 4

**User Story:** As a user, I want to see a haunted-themed interface with spooky aesthetics, so that I have an engaging and memorable experience on the platform

#### Acceptance Criteria

1. THE Ghost Hire System SHALL apply a pitch black background color (#0a0a0a) to all pages
2. THE Ghost Hire System SHALL use neon purple (#9d4edd) as the primary accent color for interactive elements
3. THE Ghost Hire System SHALL use neon green (#39ff14) as the secondary accent color
4. THE Ghost Hire System SHALL apply the "Creepster" font from Google Fonts to all header elements
5. THE Ghost Hire System SHALL apply the "Roboto Mono" monospace font to all body text
6. WHEN a user hovers over a button, THE Ghost Hire System SHALL display a glitch effect animation
7. WHEN a user focuses on an input field, THE Ghost Hire System SHALL display a neon glow effect
8. THE Ghost Hire System SHALL display ghost avatars with a floating animation effect

### Requirement 5

**User Story:** As a visitor, I want to see an engaging homepage with clear calls to action, so that I understand the platform's purpose and can easily sign up

#### Acceptance Criteria

1. THE Ghost Hire System SHALL display the hero text "Where Dead Careers Come to Life" on the homepage
2. THE Ghost Hire System SHALL display the tagline "No degree? No problem. Your skills will haunt the gatekeepers." on the homepage
3. THE Ghost Hire System SHALL display the logo.png image in the navigation bar
4. THE Ghost Hire System SHALL display a "Rise from the Grave" button that initiates Google OAuth authentication
5. THE Ghost Hire System SHALL render a fog effect animation in the background of the homepage

### Requirement 6

**User Story:** As a developer, I want the application to use environment variables for database credentials, so that sensitive information is not hardcoded in the codebase

#### Acceptance Criteria

1. THE Ghost Hire System SHALL read MySQL database credentials from environment variables
2. THE Ghost Hire System SHALL connect to a MySQL database named "ghosthire_db"
3. WHEN environment variables for database credentials are missing, THE Ghost Hire System SHALL raise a configuration error with a descriptive message
4. THE Ghost Hire System SHALL store static files in a designated static folder for CSS, JavaScript, and images
5. THE Ghost Hire System SHALL store uploaded media files in a designated media folder

### Requirement 7

**User Story:** As a user, I want to see haunted-themed terminology throughout the interface, so that the experience feels cohesive and immersive

#### Acceptance Criteria

1. THE Ghost Hire System SHALL display "Rise from the Grave" instead of "Sign Up" throughout the interface
2. THE Ghost Hire System SHALL display "Enter the Crypt" instead of "Login" throughout the interface
3. THE Ghost Hire System SHALL display "Your Haunted Lair" instead of "Dashboard" throughout the interface
4. THE Ghost Hire System SHALL display "Your Ghost" instead of "Profile" throughout the interface
5. THE Ghost Hire System SHALL display "Return to Shadows" instead of "Logout" throughout the interface

### Requirement 8

**User Story:** As a user, I want my Google ID to be unique in the system, so that I cannot create duplicate accounts with the same Google account

#### Acceptance Criteria

1. THE Ghost Hire System SHALL enforce uniqueness constraint on the google_id field in the database
2. WHEN a user attempts to authenticate with a Google account that already exists, THE Ghost Hire System SHALL retrieve the existing user record instead of creating a new one
3. WHEN a user with an existing account authenticates, THE Ghost Hire System SHALL redirect the user based on their verification status

### Requirement 9

**User Story:** As a platform administrator, I want to detect stolen or duplicate verification photos, so that I can prevent fraudulent accounts and ensure one account per person

#### Acceptance Criteria

1. WHEN a user uploads a verification photo, THE Ghost Hire System SHALL perform a reverse image search using SerpAPI to check if the photo exists online
2. WHEN a verification photo is found on Google Images or Pinterest, THE Ghost Hire System SHALL reject the upload with the message "This photo exists online. Upload your real face, ghost."
3. WHEN a verification photo passes the reverse image search, THE Ghost Hire System SHALL compare the photo against all existing verified users' verification photos using a Siamese neural network
4. WHEN the Siamese network detects a similarity score greater than 0.9 with an existing user's photo, THE Ghost Hire System SHALL reject the upload with the message "This face already haunts our community. One ghost per person."
5. WHEN a verification photo passes both the reverse image search and duplicate face detection, THE Ghost Hire System SHALL set the user's is_verified field to True

### Requirement 10

**User Story:** As a developer, I want to integrate a Siamese neural network for face comparison, so that I can accurately detect duplicate faces across different photos

#### Acceptance Criteria

1. THE Ghost Hire System SHALL load a pre-trained Siamese network model from the file "best_siamese_model.pth"
2. THE Ghost Hire System SHALL use ResNet18 as the feature extraction backbone in the Siamese network
3. WHEN comparing two face images, THE Ghost Hire System SHALL preprocess both images to 224x224 pixels and convert them to tensors
4. THE Ghost Hire System SHALL compute a similarity score between 0 and 1 for any two face images
5. THE Ghost Hire System SHALL utilize GPU acceleration when available, otherwise fall back to CPU processing

### Requirement 11

**User Story:** As a verified user, I want to complete my profile setup with skills and bio, so that I can showcase my abilities to potential employers

#### Acceptance Criteria

1. WHEN a user successfully completes verification, THE Ghost Hire System SHALL redirect the user to the profile setup page
2. THE Ghost Hire System SHALL display the auto-generated username on the profile setup page
3. THE Ghost Hire System SHALL provide checkboxes for the following skills: Computer Vision, Machine Learning, Django/Python, React/Frontend, Game Development, Mobile Apps, DevOps, and UI/UX Design
4. THE Ghost Hire System SHALL limit the bio text area to 500 characters maximum
5. THE Ghost Hire System SHALL allow users to optionally upload a custom ghost avatar image
6. THE Ghost Hire System SHALL allow users to optionally provide a GitHub profile link
7. WHEN a user submits the profile setup form, THE Ghost Hire System SHALL save all provided information to the User model and redirect to the profile page

### Requirement 12

**User Story:** As a user, I want to view my completed profile, so that I can see how my information is displayed to others

#### Acceptance Criteria

1. THE Ghost Hire System SHALL display the user's ghost avatar on the profile page
2. THE Ghost Hire System SHALL display the user's ghost name on the profile page
3. THE Ghost Hire System SHALL display the user's ghost level as star icons on the profile page
4. THE Ghost Hire System SHALL display the user's selected skills as neon purple pill-shaped elements on the profile page
5. THE Ghost Hire System SHALL display the user's bio text on the profile page
6. THE Ghost Hire System SHALL display the user's GitHub link on the profile page if provided
7. THE Ghost Hire System SHALL display a verified badge on the profile page for verified users
8. THE Ghost Hire System SHALL NOT display the verification photo on the profile page or any public-facing page

### Requirement 13

**User Story:** As a user, I want to see smooth animations and visual effects throughout the interface, so that the haunted theme feels polished and immersive

#### Acceptance Criteria

1. THE Ghost Hire System SHALL apply a flickering animation to header text elements that simulates old horror movie effects
2. THE Ghost Hire System SHALL apply a glitch animation to buttons when users hover over them
3. THE Ghost Hire System SHALL apply a floating animation to ghost avatar images
4. THE Ghost Hire System SHALL apply a neon glow box-shadow effect to interactive elements on focus or hover
5. THE Ghost Hire System SHALL apply neon glow effects using the primary accent color (#9d4edd) with multiple shadow layers

### Requirement 14

**User Story:** As a platform administrator, I want to configure the SerpAPI integration using environment variables, so that API credentials are kept secure

#### Acceptance Criteria

1. THE Ghost Hire System SHALL read the SerpAPI key from an environment variable
2. WHEN performing reverse image search, THE Ghost Hire System SHALL query both Google Images and Pinterest through SerpAPI
3. WHEN the SerpAPI key is missing or invalid, THE Ghost Hire System SHALL log an error and skip the reverse image search check
4. THE Ghost Hire System SHALL handle SerpAPI rate limits gracefully with appropriate error messages

### Requirement 15

**User Story:** As a user, I want to receive clear feedback during the verification process, so that I understand whether my photo was accepted or rejected and why

#### Acceptance Criteria

1. WHEN a verification photo is rejected due to reverse image search, THE Ghost Hire System SHALL display the error message "This photo exists online. Upload your real face, ghost."
2. WHEN a verification photo is rejected due to duplicate face detection, THE Ghost Hire System SHALL display the error message "This face already haunts our community. One ghost per person."
3. WHEN a verification photo is successfully accepted, THE Ghost Hire System SHALL display the success message "✅ Verified Ghost! Welcome to the cemetery."
4. THE Ghost Hire System SHALL display all verification status messages with appropriate styling consistent with the haunted theme
