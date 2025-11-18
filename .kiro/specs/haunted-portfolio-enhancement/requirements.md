# Requirements Document

## Introduction

The Haunted Portfolio Enhancement transforms the existing portfolio into an intelligent career showcase that combines user self-declaration with deep GitHub analysis. The system extracts meaningful insights about a developer's expertise, AI usage patterns, career stage, and job readiness, presenting this information in a visually stunning and honest way that helps employers understand the developer's true capabilities.

## Glossary

- **Portfolio System**: The haunted_portfolio feature that displays developer profiles
- **User Profile**: The authenticated user's account and associated data
- **GitHub Analyzer**: The component that analyzes GitHub repositories for code patterns
- **AI Detection Engine**: The system that identifies AI-generated vs human-written code
- **Career Assessment Module**: The component that evaluates career stage and job readiness
- **Expertise Matcher**: The system that matches user-declared skills with actual code evidence
- **Journey Extractor**: The component that builds a narrative from user input and GitHub history

## Requirements

### Requirement 1

**User Story:** As a developer, I want to declare my expertise area and journey, so that the system can analyze my work in the context of what I claim to know

#### Acceptance Criteria

1. WHEN the User Profile accesses the portfolio setup page, THE Portfolio System SHALL display a form to capture expertise area, skills, learning journey, and AI usage preferences
2. THE Portfolio System SHALL store the user's declared expertise area (e.g., "Computer Vision Developer", "Backend Engineer", "Data Scientist")
3. THE Portfolio System SHALL capture what the user has learned in their expertise area through a structured text input
4. THE Portfolio System SHALL record where and how the user applies AI in their workflow
5. THE Portfolio System SHALL save the user's personal journey narrative for display on their portfolio

### Requirement 2

**User Story:** As a developer, I want the system to analyze my GitHub repositories based on my declared expertise, so that it can show how much of my core work is genuinely mine vs AI-assisted

#### Acceptance Criteria

1. WHEN the GitHub Analyzer processes repositories, THE GitHub Analyzer SHALL identify code files related to the user's declared expertise area
2. THE AI Detection Engine SHALL analyze each code file to determine the percentage of AI-generated code vs human-written code
3. THE Expertise Matcher SHALL calculate separate AI usage percentages for core expertise areas vs non-expertise areas (e.g., UI/UX code for a backend developer)
4. THE GitHub Analyzer SHALL extract unique projects that demonstrate the user's expertise
5. THE Portfolio System SHALL display the AI vs human code ratio with context about where AI was appropriately used

### Requirement 3

**User Story:** As a developer, I want the system to show how smartly I use AI, so that employers can see I use AI as a tool rather than a crutch

#### Acceptance Criteria

1. THE AI Detection Engine SHALL identify patterns where AI is used for non-core tasks (e.g., UI generation, boilerplate code)
2. THE AI Detection Engine SHALL identify patterns where human code dominates in the user's expertise area
3. THE Portfolio System SHALL generate a "Smart AI Usage" score based on appropriate AI delegation
4. THE Portfolio System SHALL display examples of smart AI usage with explanations
5. IF the user heavily relies on AI for their core expertise, THEN THE Portfolio System SHALL provide constructive feedback on improvement areas

### Requirement 4

**User Story:** As a developer, I want the system to assess my career stage in my expertise area, so that employers understand my experience level

#### Acceptance Criteria

1. THE Career Assessment Module SHALL analyze repository complexity, commit patterns, and code quality to determine career stage
2. THE Career Assessment Module SHALL classify the user as Beginner, Intermediate, Advanced, or Expert in their declared expertise area
3. THE Career Assessment Module SHALL provide specific evidence for the career stage classification
4. THE Portfolio System SHALL display the career stage with visual indicators and supporting metrics
5. THE Career Assessment Module SHALL consider factors including: years of activity, project complexity, code patterns, and contribution consistency

### Requirement 5

**User Story:** As a developer, I want a job readiness assessment, so that I can understand how prepared I am for employment opportunities

#### Acceptance Criteria

1. THE Career Assessment Module SHALL calculate a job readiness score from 0-100 based on multiple factors
2. THE Career Assessment Module SHALL evaluate technical skills breadth and depth from GitHub analysis
3. THE Career Assessment Module SHALL assess project portfolio quality and diversity
4. THE Career Assessment Module SHALL consider code quality, documentation, and best practices adherence
5. THE Portfolio System SHALL display the job readiness score with actionable recommendations for improvement

### Requirement 6

**User Story:** As a developer, I want my unique projects highlighted with context, so that employers can see my best work and innovation

#### Acceptance Criteria

1. THE GitHub Analyzer SHALL identify projects with unique characteristics (high stars, innovative tech stack, original concepts)
2. THE Portfolio System SHALL extract and display project descriptions, technologies used, and impact metrics
3. THE Portfolio System SHALL highlight which projects demonstrate core expertise vs exploratory work
4. THE Portfolio System SHALL show the human vs AI code ratio for each unique project
5. THE Portfolio System SHALL rank projects by relevance to the user's declared expertise area

### Requirement 7

**User Story:** As a developer, I want my complete tech stack and skills displayed beautifully, so that employers can quickly assess my capabilities

#### Acceptance Criteria

1. THE GitHub Analyzer SHALL extract all programming languages, frameworks, and tools from repositories
2. THE Portfolio System SHALL categorize skills into expertise areas (core skills, supporting skills, exploratory skills)
3. THE Portfolio System SHALL display skill proficiency levels based on usage frequency and code quality
4. THE Portfolio System SHALL show which skills are human-developed vs AI-assisted
5. THE Portfolio System SHALL present skills in an interactive, visually appealing format with neon-themed styling

### Requirement 8

**User Story:** As a developer, I want my journey and growth narrative displayed, so that employers can understand my learning path and motivation

#### Acceptance Criteria

1. THE Journey Extractor SHALL combine user-provided journey narrative with GitHub timeline analysis
2. THE Portfolio System SHALL display a visual timeline showing skill acquisition and project milestones
3. THE Portfolio System SHALL highlight key learning moments and breakthrough projects
4. THE Portfolio System SHALL show progression in code quality and complexity over time
5. THE Portfolio System SHALL present the journey narrative in an engaging, story-like format

### Requirement 9

**User Story:** As a developer, I want all portfolio information presented in a stunning visual design, so that my profile stands out and is memorable

#### Acceptance Criteria

1. THE Portfolio System SHALL use the existing haunted theme with neon purple and green color scheme
2. THE Portfolio System SHALL display all metrics with animated visual elements (progress bars, charts, badges)
3. THE Portfolio System SHALL organize information in a logical flow: header → expertise → AI analysis → projects → skills → journey → job readiness
4. THE Portfolio System SHALL ensure responsive design that works on mobile, tablet, and desktop devices
5. THE Portfolio System SHALL include hover effects, animations, and interactive elements that enhance user engagement

### Requirement 10

**User Story:** As an employer viewing a portfolio, I want to see an honest assessment of the developer's capabilities, so that I can make informed hiring decisions

#### Acceptance Criteria

1. THE Portfolio System SHALL display both strengths and areas for improvement without bias
2. THE Portfolio System SHALL provide evidence-based claims with links to actual code and projects
3. THE Portfolio System SHALL show AI usage transparency without penalizing appropriate AI use
4. THE Portfolio System SHALL present career stage and job readiness with clear justification
5. THE Portfolio System SHALL include a summary section that gives a quick overview of the developer's profile
