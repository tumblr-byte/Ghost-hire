# Requirements Document

## Introduction

This feature enhances the AI vs Human code analysis visualization to provide a more nuanced, motivating, and accurate representation of how developers use AI. Instead of showing a single demotivating percentage (e.g., "75% AI-Assisted"), the system will break down AI usage by category (Core Skills vs Supporting Tasks) and show WHERE AI is used, making it clear that using AI for UI/UX or documentation while writing core algorithms yourself is smart, not a weakness.

## Glossary

- **System**: The Ghost Hire portfolio analysis and visualization system
- **User**: A developer viewing their portfolio analysis
- **Core Skills**: The developer's primary expertise area where they write code themselves (e.g., ML algorithms, backend logic, CV models)
- **Supporting Tasks**: Non-core areas where AI assistance is used (e.g., UI/UX, documentation, boilerplate, syntax)
- **AI Usage Breakdown**: A categorized visualization showing where AI is used vs where human code is written
- **Motivating Visualization**: A chart/display that encourages developers by highlighting their strengths rather than focusing on raw AI percentage

## Requirements

### Requirement 1

**User Story:** As a developer who writes core algorithms myself but uses AI for UI/UX, I want to see a breakdown of WHERE I use AI, so that I don't feel demotivated by a high AI percentage that lacks context

#### Acceptance Criteria

1. WHEN THE System displays AI usage analysis, THE System SHALL show a categorized breakdown with at least two categories: "Core Skills (Human-Written)" and "Supporting Tasks (AI-Assisted)"
2. WHEN THE System calculates AI usage, THE System SHALL use the user's self-described expertise area and core skills to determine which code is core vs supporting
3. WHEN THE System displays the breakdown, THE System SHALL show specific examples of what falls into each category based on user input (e.g., "Core: Object Detection, SGAN" vs "Supporting: UI/UX, Streamlit")
4. WHEN a developer has high AI usage in supporting tasks but low AI usage in core skills, THE System SHALL display a positive message emphasizing smart AI usage
5. WHEN THE System presents the visualization, THE System SHALL use visual indicators (icons, colors, charts) to make the distinction between core and supporting work clear

### Requirement 2

**User Story:** As a developer viewing my portfolio, I want to see a visual chart that breaks down my AI usage by task type, so that employers and I can understand my actual coding abilities

#### Acceptance Criteria

1. WHEN THE System renders the AI usage section, THE System SHALL display a stacked bar chart or segmented visualization showing AI usage across different categories
2. WHEN THE System creates the visualization, THE System SHALL include at least these categories: "Core Algorithms/Logic", "API/Integration", "UI/UX", "Documentation", "Boilerplate/Setup"
3. WHEN THE System displays each category, THE System SHALL show the percentage of AI assistance for that specific category
4. WHEN a category has low AI usage, THE System SHALL highlight it with a positive indicator (e.g., green color, checkmark)
5. WHEN a category has high AI usage in non-core areas, THE System SHALL display it neutrally without negative connotation

### Requirement 3

**User Story:** As a developer who is self-aware about my AI usage, I want the system to recognize and reward my honesty about where I use AI help, so that I feel encouraged rather than penalized

#### Acceptance Criteria

1. WHEN a user provides detailed information about their AI usage context, THE System SHALL calculate a "Self-Awareness Score" or similar positive metric
2. WHEN THE System detects that a user is honest about weaknesses, THE System SHALL display a positive badge or indicator (e.g., "✅ Self-Aware Developer")
3. WHEN THE System shows AI usage statistics, THE System SHALL include a section titled "Smart AI Usage" that explains how the developer uses AI strategically
4. WHEN a developer uses AI primarily for non-core tasks, THE System SHALL display messaging like "Uses AI smartly for supporting tasks while writing core code independently"
5. WHEN THE System calculates the overall assessment, THE System SHALL weight core skill proficiency higher than supporting task proficiency

### Requirement 4

**User Story:** As a developer concerned about how employers perceive my AI usage, I want to see an "Employer View" summary that frames my AI usage positively, so that I can confidently share my profile

#### Acceptance Criteria

1. WHEN THE System generates the portfolio summary, THE System SHALL include an "Employer Perspective" section that reframes AI usage in professional terms
2. WHEN a developer has high AI usage overall but low AI usage in core skills, THE System SHALL emphasize the core skills in the employer summary
3. WHEN THE System creates the employer view, THE System SHALL include statements like "Writes [Core Skill] algorithms independently" and "Efficiently uses AI for [Supporting Tasks]"
4. WHEN THE System displays technical depth, THE System SHALL show specific examples of complex work done without AI assistance
5. WHEN a developer has advanced code complexity, THE System SHALL prominently display this in the employer view regardless of overall AI percentage

### Requirement 5

**User Story:** As a developer who wants to improve, I want to see actionable recommendations based on my AI usage breakdown, so that I know exactly what to work on

#### Acceptance Criteria

1. WHEN THE System analyzes AI usage patterns, THE System SHALL generate specific recommendations based on the category breakdown
2. WHEN a developer has high AI usage in core skills, THE System SHALL suggest specific exercises or projects to build those skills independently
3. WHEN a developer has appropriate AI usage patterns, THE System SHALL provide encouragement and suggest next-level challenges
4. WHEN THE System displays recommendations, THE System SHALL prioritize improvements in core skills over supporting tasks
5. WHEN a developer has low AI usage in core skills, THE System SHALL acknowledge this strength and suggest ways to showcase it better

### Requirement 6

**User Story:** As a developer, I want to see my AI usage trend over time, so that I can track whether I'm becoming more independent in my core skills

#### Acceptance Criteria

1. WHEN THE System has historical portfolio data, THE System SHALL display a trend chart showing AI usage changes over time
2. WHEN THE System shows the trend, THE System SHALL separate core skills from supporting tasks in the visualization
3. WHEN a developer's core skill independence is improving, THE System SHALL highlight this positive trend
4. WHEN THE System displays the trend, THE System SHALL show at least three time periods if data is available
5. WHEN historical data is insufficient, THE System SHALL display a message encouraging the user to refresh their portfolio regularly to track progress
