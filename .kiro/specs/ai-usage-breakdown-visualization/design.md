# Design Document

## Overview

This feature redesigns the AI vs Human code analysis to provide a motivating, context-aware breakdown that shows WHERE developers use AI rather than just showing a demotivating overall percentage. The system will categorize AI usage into Core Skills (where developers should write code themselves) and Supporting Tasks (where AI assistance is smart and efficient), then visualize this breakdown in an encouraging way.

## Architecture

### High-Level Flow

```
User Profile Data (expertise, core_skills, weaknesses)
    ↓
GitHub Analysis (commits, repos, languages)
    ↓
AI Usage Categorization Engine
    ↓
Category-Based Breakdown (Core vs Supporting)
    ↓
Visualization Generator (Charts, Badges, Summaries)
    ↓
Portfolio Display (Motivating, Context-Aware)
```

### Key Components

1. **AI Usage Categorizer** - Analyzes code and categorizes AI usage by task type
2. **Breakdown Calculator** - Calculates AI% for each category separately
3. **Visualization Generator** - Creates charts and visual representations
4. **Messaging Engine** - Generates positive, context-aware messages
5. **Template Renderer** - Displays the breakdown in the portfolio view

## Components and Interfaces

### 1. AI Usage Categorizer (`haunted_profiles/ai_usage_categorizer.py`)

**Purpose**: Categorize code/commits into task types based on user profile and code analysis

**Interface**:
```python
class AIUsageCategorizer:
    def __init__(self, user_profile, github_data):
        """
        Args:
            user_profile: Dict with expertise_area, core_skills, weaknesses, etc.
            github_data: Dict with repos, commits, languages
        """
        
    def categorize_by_task_type(self):
        """
        Categorize AI usage into task types
        
        Returns: {
            'core_algorithms': {'ai_percentage': 10, 'human_percentage': 90, 'examples': [...]},
            'api_integration': {'ai_percentage': 40, 'human_percentage': 60, 'examples': [...]},
            'ui_ux': {'ai_percentage': 85, 'human_percentage': 15, 'examples': [...]},
            'documentation': {'ai_percentage': 90, 'human_percentage': 10, 'examples': [...]},
            'boilerplate': {'ai_percentage': 70, 'human_percentage': 30, 'examples': [...]}
        }
        """
        
    def identify_core_vs_supporting(self):
        """
        Separate core skills from supporting tasks
        
        Returns: {
            'core': {
                'categories': ['core_algorithms', 'api_integration'],
                'ai_percentage': 15,
                'human_percentage': 85,
                'skills': ['Object Detection', 'SGAN', 'AdaIN']
            },
            'supporting': {
                'categories': ['ui_ux', 'documentation', 'boilerplate'],
                'ai_percentage': 80,
                'human_percentage': 20,
                'tasks': ['UI/UX', 'Streamlit', 'Documentation']
            }
        }
        """
```

### 2. Breakdown Calculator (`haunted_profiles/breakdown_calculator.py`)

**Purpose**: Calculate detailed AI usage statistics for each category

**Interface**:
```python
class BreakdownCalculator:
    def __init__(self, categorized_data, user_profile):
        """
        Args:
            categorized_data: Output from AIUsageCategorizer
            user_profile: User's self-description
        """
        
    def calculate_category_breakdown(self):
        """
        Calculate AI% for each category with context
        
        Returns: {
            'categories': [
                {
                    'name': 'Core ML/CV Algorithms',
                    'ai_percentage': 10,
                    'human_percentage': 90,
                    'is_core': True,
                    'status': 'excellent',  # excellent/good/needs_improvement
                    'examples': ['Object Detection', 'SGAN training'],
                    'message': 'You write your core algorithms independently! 🔥'
                },
                {
                    'name': 'UI/UX & Styling',
                    'ai_percentage': 85,
                    'human_percentage': 15,
                    'is_core': False,
                    'status': 'smart',
                    'examples': ['Streamlit dashboards', 'CSS styling'],
                    'message': 'Smart use of AI for non-core tasks ✅'
                }
            ],
            'overall_assessment': 'smart_ai_user',
            'core_independence_score': 90
        }
        """
        
    def calculate_self_awareness_score(self):
        """
        Calculate how self-aware the developer is about their AI usage
        
        Returns: {
            'score': 85,
            'level': 'highly_self_aware',
            'indicators': ['honest_about_weaknesses', 'clear_expertise', 'strategic_ai_use']
        }
        """
```

### 3. Visualization Generator (`haunted_profiles/visualization_generator.py`)

**Purpose**: Generate chart data and visual elements for the breakdown

**Interface**:
```python
class VisualizationGenerator:
    def __init__(self, breakdown_data):
        """
        Args:
            breakdown_data: Output from BreakdownCalculator
        """
        
    def generate_stacked_bar_data(self):
        """
        Generate data for stacked bar chart
        
        Returns: {
            'labels': ['Core Skills', 'Supporting Tasks'],
            'human_data': [90, 20],
            'ai_data': [10, 80],
            'colors': {
                'human': '#39FF14',  # neon green
                'ai': '#9D4EDD'      # neon purple
            }
        }
        """
        
    def generate_category_cards(self):
        """
        Generate visual cards for each category
        
        Returns: [
            {
                'title': 'Core ML/CV Algorithms',
                'icon': '🔥',
                'human_percentage': 90,
                'ai_percentage': 10,
                'status': 'excellent',
                'color': 'green',
                'examples': ['Object Detection', 'SGAN'],
                'message': 'You write your core code independently!'
            },
            ...
        ]
        """
        
    def generate_employer_summary(self):
        """
        Generate employer-friendly summary
        
        Returns: {
            'headline': 'Computer Vision Developer - Writes Core Algorithms Independently',
            'key_points': [
                'Independently develops ML/CV algorithms (90% human-written)',
                'Proficient in Object Detection, SGAN, AdaIN style transfer',
                'Efficiently uses AI for UI/UX and documentation (smart workflow)'
            ],
            'technical_depth': 'Advanced - 5 complex CV projects',
            'recommendation': 'Strong technical foundation with strategic AI usage'
        }
        """
```

### 4. Messaging Engine (`haunted_profiles/messaging_engine.py`)

**Purpose**: Generate positive, context-aware messages based on AI usage patterns

**Interface**:
```python
class MessagingEngine:
    def __init__(self, breakdown_data, user_profile):
        """
        Args:
            breakdown_data: Output from BreakdownCalculator
            user_profile: User's self-description
        """
        
    def generate_motivational_message(self):
        """
        Generate main motivational message
        
        Returns: {
            'title': 'Smart AI User 🔥',
            'message': 'You write your core ML/CV algorithms yourself and use AI strategically for UI/UX and documentation. This is exactly how professional developers work!',
            'tone': 'encouraging'
        }
        """
        
    def generate_category_messages(self, category):
        """
        Generate message for specific category
        
        Args:
            category: Category name (e.g., 'core_algorithms')
            
        Returns: {
            'message': 'You write your core algorithms independently! 🔥',
            'icon': '✅',
            'color': 'green'
        }
        """
        
    def generate_improvement_suggestions(self):
        """
        Generate actionable improvement suggestions
        
        Returns: [
            {
                'area': 'Core Skills',
                'suggestion': 'Keep writing your ML algorithms yourself - you\'re doing great!',
                'priority': 'maintain',
                'icon': '🔥'
            },
            {
                'area': 'Commit Messages',
                'suggestion': 'Add more technical details to show your understanding',
                'priority': 'improve',
                'icon': '📈'
            }
        ]
        """
```

## Data Models

### Enhanced Portfolio Data Structure

```python
portfolio_data = {
    'ai_usage_breakdown': {
        'overall': {
            'ai_percentage': 75,
            'human_percentage': 25,
            'assessment': 'smart_ai_user'
        },
        'core_vs_supporting': {
            'core': {
                'ai_percentage': 10,
                'human_percentage': 90,
                'skills': ['Object Detection', 'SGAN', 'AdaIN'],
                'status': 'excellent'
            },
            'supporting': {
                'ai_percentage': 80,
                'human_percentage': 20,
                'tasks': ['UI/UX', 'Streamlit', 'Documentation'],
                'status': 'smart'
            }
        },
        'categories': [
            {
                'name': 'Core ML/CV Algorithms',
                'ai_percentage': 10,
                'human_percentage': 90,
                'is_core': True,
                'examples': ['Object Detection', 'SGAN training'],
                'message': 'You write your core algorithms independently! 🔥',
                'status': 'excellent'
            },
            {
                'name': 'API & Integration',
                'ai_percentage': 30,
                'human_percentage': 70,
                'is_core': True,
                'examples': ['Model integration', 'Pipeline setup'],
                'message': 'Good technical implementation',
                'status': 'good'
            },
            {
                'name': 'UI/UX & Styling',
                'ai_percentage': 85,
                'human_percentage': 15,
                'is_core': False,
                'examples': ['Streamlit dashboards', 'CSS styling'],
                'message': 'Smart use of AI for non-core tasks ✅',
                'status': 'smart'
            },
            {
                'name': 'Documentation',
                'ai_percentage': 90,
                'human_percentage': 10,
                'is_core': False,
                'examples': ['README files', 'Code comments'],
                'message': 'Efficient documentation with AI',
                'status': 'smart'
            }
        ],
        'self_awareness': {
            'score': 85,
            'level': 'highly_self_aware',
            'badge': '✅ Self-Aware Developer'
        },
        'employer_summary': {
            'headline': 'Computer Vision Developer - Writes Core Algorithms Independently',
            'key_points': [...],
            'recommendation': 'Strong technical foundation with strategic AI usage'
        }
    }
}
```

## Error Handling

1. **Missing User Profile Data**
   - Fallback to GitHub-only analysis
   - Show message encouraging user to complete profile

2. **Insufficient GitHub Data**
   - Show partial breakdown with available data
   - Suggest adding more projects

3. **Categorization Uncertainty**
   - Default to neutral assessment
   - Show "Unable to determine" with explanation

## Testing Strategy

### Unit Tests
- Test AIUsageCategorizer with various user profiles
- Test BreakdownCalculator with different AI usage patterns
- Test MessagingEngine message generation
- Test VisualizationGenerator data formatting

### Integration Tests
- Test full flow from user profile to visualization
- Test with real GitHub data samples
- Test edge cases (no user profile, minimal GitHub data)

### Visual Tests
- Verify chart rendering with different breakdowns
- Test responsive design on mobile/desktop
- Verify color schemes and accessibility

## UI/UX Design

### Layout Structure

```
┌─────────────────────────────────────────────────────┐
│  🤖 Code Intelligence Analysis                      │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  Smart AI User 🔥                            │  │
│  │  You write your core ML/CV algorithms        │  │
│  │  yourself and use AI strategically for       │  │
│  │  UI/UX and documentation!                    │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌─────────────────┬─────────────────────────────┐ │
│  │ Core Skills     │ ████████████░░ 90% Human    │ │
│  │ 🔥              │ ░░░░░░░░░░░░░░ 10% AI       │ │
│  └─────────────────┴─────────────────────────────┘ │
│                                                      │
│  ┌─────────────────┬─────────────────────────────┐ │
│  │ Supporting      │ ████░░░░░░░░░░ 20% Human    │ │
│  │ ✅              │ ░░░░░░░░░░░░░░ 80% AI       │ │
│  └─────────────────┴─────────────────────────────┘ │
│                                                      │
│  📊 Detailed Breakdown:                             │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ 🔥 Core ML/CV Algorithms                     │  │
│  │ ████████████████████ 90% Human-Written       │  │
│  │ Examples: Object Detection, SGAN, AdaIN      │  │
│  │ ✅ You write your core code independently!   │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ 🎨 UI/UX & Styling                           │  │
│  │ ███░░░░░░░░░░░░░░░░░ 15% Human-Written       │  │
│  │ Examples: Streamlit dashboards, CSS          │  │
│  │ ✅ Smart use of AI for non-core tasks        │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  👔 Employer View:                                  │
│  "Computer Vision Developer - Writes Core           │
│  Algorithms Independently"                          │
│  • Independently develops ML/CV algorithms          │
│  • Proficient in Object Detection, SGAN, AdaIN     │
│  • Efficiently uses AI for UI/UX (smart workflow)  │
└─────────────────────────────────────────────────────┘
```

### Color Scheme

- **Core Skills (High Human%)**: Neon Green (#39FF14) - Excellent
- **Supporting Tasks (High AI%)**: Neon Purple (#9D4EDD) - Smart
- **Needs Improvement**: Orange (#FF6B35) - Actionable
- **Neutral**: Gray (#8B8B8B)

### Visual Indicators

- 🔥 = Core skills, excellent performance
- ✅ = Smart AI usage, appropriate
- 📈 = Area for improvement
- 👔 = Employer perspective
- 🎯 = Strategic focus area

## Implementation Notes

1. **Backward Compatibility**: Existing portfolios without detailed user profiles should still work with GitHub-only analysis

2. **Performance**: Categorization should happen during portfolio refresh, not on every page load

3. **Caching**: Cache breakdown calculations in `portfolio_data` JSON field

4. **Progressive Enhancement**: Show basic breakdown first, then load detailed charts

5. **Mobile Optimization**: Stack category cards vertically on mobile devices
