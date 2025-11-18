# Implementation Plan

- [x] 1. Set up Django project structure and configuration


  - Create Django project named 'ghosthire' with app 'haunted_profiles'
  - Configure settings.py with MySQL database connection using environment variables
  - Set up MEDIA_ROOT and STATIC_ROOT directories
  - Install and configure django-allauth with Google OAuth provider
  - Create .env.example file with required environment variable templates
  - _Requirements: 1.1, 6.1, 6.2, 6.4, 6.5_




- [x] 2. Implement custom User model with authentication

  - [x] 2.1 Create User model with all required fields

    - Define User model extending AbstractBaseUser and PermissionsMixin
    - Add fields: google_id, email, username, verification_photo, ghost_avatar, is_verified, ghost_level, skills, bio, github_link, created_at

    - Implement CustomUserManager for user creation
    - Set USERNAME_FIELD to 'email' and configure REQUIRED_FIELDS
    - _Requirements: 1.2, 1.3, 1.4, 3.1, 3.2, 3.3, 3.4, 3.5, 8.1_

  - [x] 2.2 Create custom social account adapter for username generation

    - Implement CustomSocialAccountAdapter extending DefaultSocialAccountAdapter
    - Override save_user method to auto-generate username as "ghost_" + 5 random digits
    - Save google_id from sociallogin.account.uid
    - Configure adapter in settings.py
    - _Requirements: 1.3, 1.4_




  - [ ] 2.3 Configure allauth settings and URL routing
    - Add allauth apps to INSTALLED_APPS
    - Configure AUTHENTICATION_BACKENDS
    - Set up SOCIALACCOUNT_PROVIDERS for Google with proper scopes
    - Include allauth URLs in project urls.py
    - Create custom redirect logic based on verification status
    - _Requirements: 1.1, 1.5, 8.2, 8.3_

  - [ ]* 2.4 Write unit tests for User model and authentication
    - Test User model creation with all fields




    - Test username auto-generation and uniqueness
    - Test default values for ghost_level, is_verified, ghost_avatar
    - Test JSONField skills storage
    - _Requirements: 1.2, 1.3, 1.4, 3.1, 3.2, 3.3, 3.4, 3.5_


- [ ] 3. Implement photo verification system with fraud detection
  - [ ] 3.1 Create Siamese network model class
    - Implement SiameseNetwork class with ResNet18 backbone
    - Define forward_once and forward methods
    - Create image preprocessing transform pipeline (resize to 224x224, convert to tensor)
    - Implement model loading function with GPU/CPU device selection
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_


  - [ ] 3.2 Implement duplicate face detection utility
    - Create check_duplicate_face function in utils.py
    - Load and preprocess uploaded photo
    - Query all verified users with verification photos
    - Compare uploaded photo against each existing photo using Siamese network
    - Return True and matched username if similarity > 0.9
    - _Requirements: 9.3, 9.4, 10.3, 10.4_


  - [ ] 3.3 Implement reverse image search integration
    - Create check_image_online function in utils.py
    - Read SERPAPI_KEY from environment variables
    - Make API request to SerpAPI for reverse image search
    - Check Google Images and Pinterest results
    - Return True if image found online with source list
    - Handle API errors and rate limits gracefully
    - _Requirements: 9.1, 9.2, 14.1, 14.2, 14.3, 14.4_

  - [ ] 3.4 Create verification view with complete validation flow
    - Implement verification view requiring login
    - Handle file upload for verification_photo
    - Execute reverse image search check first
    - Execute duplicate face detection check second
    - Set is_verified=True and save photo if both checks pass
    - Display appropriate error messages for each rejection case
    - Redirect to haunt_setup on success
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 15.1, 15.2, 15.3_

  - [ ]* 3.5 Write unit tests for verification utilities
    - Test check_image_online with mocked SerpAPI responses




    - Test check_duplicate_face with sample images
    - Test Siamese model loading and inference
    - Test error handling for missing API keys and model files
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 10.1, 10.5_

- [ ] 4. Create homepage and authentication pages
  - [x] 4.1 Implement homepage view and template


    - Create index view rendering homepage
    - Build index.html template with hero section
    - Display "Where Dead Careers Come to Life" header
    - Display tagline "No degree? No problem. Your skills will haunt the gatekeepers."
    - Add "Rise from the Grave" button linking to Google OAuth
    - Include logo.png in navigation bar
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 7.1_


  - [ ] 4.2 Create verification page template
    - Build verification.html template extending base
    - Display header "Prove You Belong to Our Ghost Community"
    - Add subtext about photo verification
    - Create file upload form for verification_photo




    - Add "Verify Me" button with haunted styling
    - Display warning text about photo privacy
    - Show error messages for rejection cases
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 15.1, 15.2, 15.3, 15.4_

  - [x] 4.3 Configure URL routing for authentication flow


    - Add URL pattern for homepage (/)
    - Add URL pattern for verification page (/verification/)
    - Configure allauth URLs for Google OAuth
    - Set up LOGIN_REDIRECT_URL based on verification status
    - _Requirements: 1.1, 1.5, 8.3_

- [ ] 5. Implement profile setup functionality
  - [ ] 5.1 Create ProfileSetupForm with skill choices
    - Define ProfileSetupForm extending ModelForm
    - Add SKILL_CHOICES with 8 predefined skills

    - Configure MultipleChoiceField with CheckboxSelectMultiple widget
    - Add bio field with 500 character max length
    - Add github_link and ghost_avatar fields
    - _Requirements: 11.3, 11.4, 11.5, 11.6_

  - [ ] 5.2 Implement haunt_setup view and template
    - Create haunt_setup view requiring login and verification
    - Redirect to verification if user not verified
    - Handle POST request to save skills, bio, github_link, and optional ghost_avatar



    - Build haunt_setup.html template with form
    - Display header "Summon Your Ghost"
    - Show auto-generated username
    - Render skill checkboxes and bio textarea
    - Add "Summon My Ghost" button with neon green styling
    - Redirect to profile page on successful submission


    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

  - [ ] 5.3 Add URL routing for profile setup
    - Add URL pattern for haunt_setup (/haunt-setup/)
    - _Requirements: 11.1, 11.7_

  - [ ]* 5.4 Write tests for profile setup form and view
    - Test ProfileSetupForm validation
    - Test bio max length enforcement

    - Test skills checkbox selection
    - Test haunt_setup view redirects
    - _Requirements: 11.3, 11.4, 11.5, 11.6, 11.7_

- [ ] 6. Create profile display page
  - [ ] 6.1 Implement profile view for user and public profiles
    - Create profile view accepting optional username parameter
    - Display current user's profile if no username provided
    - Display specified user's profile if username provided
    - Handle 404 for non-existent usernames
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8_

  - [ ] 6.2 Build profile.html template with all user information
    - Display ghost_avatar with floating animation
    - Display username (ghost name)
    - Display ghost_level as star icons
    - Render skills as neon purple pill elements
    - Display bio text
    - Display GitHub link if provided
    - Show verified badge for verified users
    - Ensure verification_photo is never displayed
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8_





  - [ ] 6.3 Add URL routing for profile pages
    - Add URL pattern for own profile (/profile/)
    - Add URL pattern for public profiles (/profile/<username>/)
    - _Requirements: 12.1, 12.2_

- [x] 7. Implement haunted CSS theme and animations

  - [ ] 7.1 Create base CSS file with theme variables and global styles
    - Define CSS variables for colors (bg-black, neon-purple, neon-green, text-gray, neon-red)
    - Define CSS variables for fonts (Creepster, Roboto Mono)




    - Import Google Fonts
    - Set global body styles with pitch black background
    - Apply Roboto Mono to body text and Creepster to headers

    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_



  - [ ] 7.2 Implement animation keyframes
    - Create flickering animation for text with opacity changes and text-shadow
    - Create glitch animation for button hover with transform translations



    - Create floating animation for ghost avatars with translateY
    - Create fog animation for background with translateX and translateY


    - _Requirements: 4.6, 4.7, 4.8, 13.1, 13.2, 13.3_





  - [ ] 7.3 Style interactive elements with neon glow effects
    - Style buttons with neon purple background and glitch hover effect
    - Add neon glow box-shadow on button hover (multiple layers)
    - Style input focus with neon purple glow
    - Style skill pills with neon purple background and rounded borders

    - Apply floating animation to ghost avatar images
    - _Requirements: 4.6, 4.7, 13.4, 13.5_



  - [ ] 7.4 Create base.html template with navigation and footer
    - Build base template with HTML structure
    - Add navigation bar with logo.png

    - Add navigation links with haunted terminology
    - Include messages display area
    - Add footer with copyright
    - Link haunted.css stylesheet
    - _Requirements: 5.3, 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ] 7.5 Apply haunted terminology throughout templates
    - Replace "Sign Up" with "Rise from the Grave"
    - Replace "Login" with "Enter the Crypt"
    - Replace "Dashboard" with "Your Haunted Lair"
    - Replace "Profile" with "Your Ghost"
    - Replace "Logout" with "Return to Shadows"
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 8. Configure media file handling and security
  - [ ] 8.1 Set up media directories and serving
    - Create media/verification_photos/ directory for private photos
    - Create media/ghost_avatars/ directory for public avatars
    - Add default 1.png avatar to ghost_avatars directory
    - Configure MEDIA_URL and MEDIA_ROOT in settings.py
    - Add media URL pattern for development
    - _Requirements: 6.4, 6.5_

  - [ ] 8.2 Implement security for verification photos
    - Document that verification_photos should not be publicly accessible
    - Add comment in settings.py about production nginx/apache configuration
    - Ensure verification_photo field is never rendered in templates
    - _Requirements: 2.3, 2.5, 12.8_

- [ ] 9. Create logout functionality
  - [ ] 9.1 Implement logout view and URL routing
    - Create logout view using Django's logout function
    - Add URL pattern for logout (/return-to-shadows/)
    - Redirect to homepage after logout
    - Update navigation to show "Return to Shadows" link
    - _Requirements: 7.5_

- [ ] 10. Finalize project configuration and dependencies
  - [ ] 10.1 Create requirements.txt with all dependencies
    - Add Django
    - Add mysqlclient
    - Add django-allauth
    - Add Pillow
    - Add torch and torchvision
    - Add requests
    - Add python-dotenv
    - _Requirements: 1.1, 6.1, 9.1, 10.1, 14.1_

  - [ ] 10.2 Create initial migration and migrate database
    - Run makemigrations for haunted_profiles app
    - Run migrate to create all database tables
    - Verify User table created with correct schema
    - _Requirements: 2.1, 6.2, 8.1_

  - [ ] 10.3 Add best_siamese_model.pth to project
    - Document where to place the model file (project root or ml_models/)
    - Add instructions for obtaining the model file
    - Update .gitignore to exclude large model file if needed
    - _Requirements: 10.1_

  - [ ]* 10.4 Create comprehensive README documentation
    - Document project setup instructions
    - List all environment variables needed
    - Explain Google OAuth setup process
    - Document SerpAPI configuration
    - Include instructions for running migrations
    - Add development server startup commands
    - _Requirements: 1.1, 6.1, 14.1_
