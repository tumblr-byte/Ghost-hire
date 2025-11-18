# Design Document

## Overview

The Haunted Portfolio Enhancement transforms the existing portfolio into an intelligent, honest career showcase. The system combines user self-declaration with deep GitHub analysis to provide employers with a transparent view of a developer's true capabilities, including their expertise area, AI usage patterns, career stage, and job readiness.

The design builds upon the existing Django application structure, extending the User model, enhancing the portfolio analyzer, and creating new assessment modules while maintaining the haunted theme aesthetic.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  (haunted_portfolio.html with enhanced sections)            │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                    Django Views Layer                        │
│  - haunted_portfolio view (enhanced)                        │
│  - tell_kiro_about_you view (enhanced)                      │
│  - refresh_portfolio view (enhanced)                        │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                   Business Logic Layer                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Enhanced Portfolio Analyzer                          │  │
│  │  - GitHub Deep Analysis                               │  │
│  │  - AI Detection Engine (enhanced)                     │  │
│  │  - Expertise Matcher                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Career Assessment Module (NEW)                       │  │
│  │  - Career Stage Classifier                            │  │
│  │  - Job Readiness Calculator                           │  │
│  │  - Skill Proficiency Analyzer                         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Journey Extractor (NEW)                              │  │
│  │  - Timeline Builder                                   │  │
│  │  - Milestone Detector                                 │  │
│  │  - Growth Narrative Generator                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                      Data Layer                              │
│  - User Model (extended with new fields)                    │
│  - portfolio_data JSONField (enhanced structure)            │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
User fills expertise form
         │
         ▼
System stores user profile data
         │
         ▼
User triggers portfolio analysis
         │
         ▼
GitHub Analyzer fetches repos + commits
         │
         ├──────────────────────────────────┐
         │                                   │
         ▼                                   ▼
AI Detection Engine              Expertise Matcher
(analyzes code patterns)         (matches skills to repos)
         │                                   │
         └──────────────┬────────────────────┘
                        │
                        ▼
         Career Assessment Module
         (evaluates stage + readiness)
                        │
                        ▼
            Journey Extractor
         (builds timeline + narrative)
                        │
                        ▼
         Store enhanced portfolio_data
                        │
                        ▼
         Render beautiful portfolio
```

## Components and Interfaces

### 1. Enhanced User Model

**Location**: `haunted_profiles/models.py`

**New/Modified Fields**:
```python
class User(AbstractBaseUser, PermissionsMixin):
    # Existing fields...
    
    # Enhanced self-description fields
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
```

**Enhanced portfolio_data Structure**:
```python
{
    'analyzed_at': '2025-11-14T10:30:00',
    'user_profile': {
        'expertise_area': 'Computer Vision Developer',
        'expertise_details': '...',
        'learning_journey': '...',
        'ai_usage_context': '...'
    },
    'github': {
        # Existing fields...
        'expertise_analysis': {
            'core_repos': [...],  # Repos in expertise area
            'supporting_repos': [...],  # Related repos
            'exploratory_repos': [...],  # Learning/experimental
            'core_ai_percentage': 15,  # AI usage in core work
            'supporting_ai_percentage': 45,  # AI usage in supporting work
            'smart_delegation': True  # Uses AI appropriately
        },
        'unique_projects': [
            {
                'name': '...',
                'description': '...',
                'relevance_to_expertise': 'high|medium|low',
                'ai_human_ratio': {'ai': 20, 'human': 80},
                'complexity_score': 8.5,
                'innovation_score': 7.0
            }
        ]
    },
    'career_assessment': {
        'stage': 'intermediate',  # beginner|intermediate|advanced|expert
        'stage_evidence': [...],  # Reasons for classification
        'years_active': 2.5,
        'project_complexity_avg': 7.2,
        'code_quality_score': 75,
        'consistency_score': 85
    },
    'job_readiness': {
        'overall_score': 78,  # 0-100
        'technical_skills_score': 80,
        'portfolio_quality_score': 75,
        'code_quality_score': 75,
        'communication_score': 80,
        'recommendations': [...]
    },
    'skills_analysis': {
        'core_skills': [
            {'name': 'PyTorch', 'proficiency': 85, 'human_developed': True},
            {'name': 'OpenCV', 'proficiency': 90, 'human_developed': True}
        ],
        'supporting_skills': [...],
        'exploratory_skills': [...]
    },
    'journey': {
        'timeline': [
            {
                'date': '2023-01',
                'event': 'Started learning Python',
                'type': 'learning'
            },
            {
                'date': '2023-06',
                'event': 'First ML project',
                'type': 'milestone',
                'project': 'object-detection-yolo'
            }
        ],
        'key_milestones': [...],
        'growth_metrics': {
            'code_quality_progression': [60, 65, 70, 75, 80],
            'complexity_progression': [4, 5, 6, 7, 8]
        }
    }
}
```

### 2. Enhanced Portfolio Analyzer

**Location**: `haunted_profiles/portfolio_analyzer.py`

**New Functions**:

```python
def analyze_expertise_match(repos_data, user_expertise, username):
    """
    Match repositories to user's declared expertise area.
    Categorize repos as: core, supporting, or exploratory.
    Calculate AI usage separately for each category.
    """
    pass

def analyze_project_relevance(repo, user_expertise):
    """
    Determine how relevant a project is to user's expertise.
    Returns: 'high', 'medium', or 'low' relevance score.
    """
    pass

def calculate_project_complexity(repo, commits_data):
    """
    Analyze project complexity based on:
    - Code structure
    - Commit patterns
    - File organization
    - Technical depth
    Returns: complexity_score (0-10)
    """
    pass

def detect_innovation(repo, all_repos):
    """
    Detect if a project is innovative/unique:
    - Novel tech stack combinations
    - Original problem-solving
    - Unique approach
    Returns: innovation_score (0-10)
    """
    pass
```

### 3. Career Assessment Module (NEW)

**Location**: `haunted_profiles/career_assessor.py`

**Interface**:

```python
class CareerAssessor:
    """Assesses developer's career stage and job readiness"""
    
    def __init__(self, github_data, user_profile):
        self.github_data = github_data
        self.user_profile = user_profile
    
    def assess_career_stage(self):
        """
        Classify career stage: beginner, intermediate, advanced, expert
        Based on:
        - Years of activity
        - Project complexity
        - Code quality patterns
        - Contribution consistency
        - Technical depth
        
        Returns: {
            'stage': 'intermediate',
            'confidence': 0.85,
            'evidence': [...]
        }
        """
        pass
    
    def calculate_job_readiness(self):
        """
        Calculate job readiness score (0-100)
        Factors:
        - Technical skills breadth (25%)
        - Technical skills depth (25%)
        - Portfolio quality (20%)
        - Code quality (15%)
        - Communication (10%)
        - Consistency (5%)
        
        Returns: {
            'overall_score': 78,
            'breakdown': {...},
            'recommendations': [...]
        }
        """
        pass
    
    def analyze_skill_proficiency(self):
        """
        Analyze proficiency level for each skill
        Based on:
        - Usage frequency
        - Code quality in that skill
        - Project complexity using that skill
        - Recency of use
        
        Returns: {
            'core_skills': [...],
            'supporting_skills': [...],
            'exploratory_skills': [...]
        }
        """
        pass
```

### 4. Journey Extractor (NEW)

**Location**: `haunted_profiles/journey_extractor.py`

**Interface**:

```python
class JourneyExtractor:
    """Builds developer's learning journey and growth narrative"""
    
    def __init__(self, github_data, user_narrative):
        self.github_data = github_data
        self.user_narrative = user_narrative
    
    def build_timeline(self):
        """
        Create chronological timeline of:
        - First commits
        - New skills acquired
        - Project milestones
        - Complexity increases
        - Key achievements
        
        Returns: [
            {'date': '2023-01', 'event': '...', 'type': 'learning'},
            ...
        ]
        """
        pass
    
    def detect_milestones(self):
        """
        Identify key milestones:
        - First project in expertise area
        - Breakthrough projects (high stars/complexity)
        - Skill mastery moments
        - Contribution spikes
        
        Returns: [...]
        """
        pass
    
    def calculate_growth_metrics(self):
        """
        Track growth over time:
        - Code quality progression
        - Complexity progression
        - Skill acquisition rate
        - Consistency improvements
        
        Returns: {
            'code_quality_progression': [60, 65, 70, 75, 80],
            'complexity_progression': [4, 5, 6, 7, 8],
            'skill_acquisition_timeline': {...}
        }
        """
        pass
    
    def generate_narrative(self):
        """
        Combine user's written journey with GitHub evidence
        Create engaging story format
        
        Returns: {
            'intro': '...',
            'key_moments': [...],
            'current_state': '...',
            'future_direction': '...'
        }
        """
        pass
```

### 5. Enhanced Views

**Location**: `haunted_profiles/views.py`

**Modified Functions**:

```python
@login_required
def tell_kiro_about_you(request):
    """
    Enhanced form to capture:
    - Expertise area
    - Expertise details
    - Learning journey
    - AI usage context
    - Non-expertise areas
    """
    pass

@login_required
def haunted_portfolio(request, username=None):
    """
    Enhanced portfolio view with new sections:
    - Expertise declaration
    - AI usage intelligence
    - Career stage
    - Job readiness
    - Enhanced projects
    - Skills categorization
    - Journey timeline
    """
    pass
```

## Data Models

### Enhanced portfolio_data JSON Structure

```json
{
  "analyzed_at": "2025-11-14T10:30:00",
  "user_profile": {
    "expertise_area": "Computer Vision Developer",
    "expertise_details": "Specializing in object detection...",
    "learning_journey": "Started with Python basics...",
    "ai_usage_context": "Use AI for UI/UX and boilerplate..."
  },
  "github": {
    "username": "johndoe",
    "public_repos": 25,
    "expertise_analysis": {
      "core_repos": [
        {
          "name": "yolo-custom-detector",
          "relevance": "high",
          "ai_percentage": 10,
          "human_percentage": 90,
          "complexity_score": 8.5
        }
      ],
      "core_ai_percentage": 15,
      "supporting_ai_percentage": 45,
      "smart_delegation": true,
      "delegation_examples": [
        "Uses AI for Streamlit UI generation",
        "Human code for core CV algorithms"
      ]
    },
    "unique_projects": [
      {
        "name": "real-time-face-detection",
        "description": "Custom YOLO implementation...",
        "stars": 45,
        "language": "Python",
        "url": "https://github.com/...",
        "relevance_to_expertise": "high",
        "ai_human_ratio": {"ai": 15, "human": 85},
        "complexity_score": 8.5,
        "innovation_score": 7.5,
        "tech_stack": ["PyTorch", "OpenCV", "CUDA"]
      }
    ]
  },
  "career_assessment": {
    "stage": "intermediate",
    "stage_confidence": 0.85,
    "stage_evidence": [
      "2+ years of consistent activity",
      "Average project complexity: 7.2/10",
      "Demonstrates understanding of advanced concepts",
      "Iterative improvement in code quality"
    ],
    "years_active": 2.5,
    "project_complexity_avg": 7.2,
    "code_quality_score": 75,
    "consistency_score": 85
  },
  "job_readiness": {
    "overall_score": 78,
    "breakdown": {
      "technical_breadth": 80,
      "technical_depth": 85,
      "portfolio_quality": 75,
      "code_quality": 75,
      "communication": 70,
      "consistency": 85
    },
    "strengths": [
      "Strong technical depth in Computer Vision",
      "Consistent project delivery",
      "Good code quality practices"
    ],
    "areas_for_improvement": [
      "Expand portfolio with more diverse projects",
      "Improve documentation and commit messages",
      "Contribute to open source projects"
    ],
    "recommendations": [
      "Ready for junior-to-mid level CV roles",
      "Consider building 1-2 more complex projects",
      "Focus on production-ready code practices"
    ]
  },
  "skills_analysis": {
    "core_skills": [
      {
        "name": "PyTorch",
        "proficiency": 85,
        "human_developed": true,
        "usage_count": 12,
        "avg_complexity": 8.0,
        "last_used": "2025-11-10"
      },
      {
        "name": "OpenCV",
        "proficiency": 90,
        "human_developed": true,
        "usage_count": 15,
        "avg_complexity": 7.5,
        "last_used": "2025-11-12"
      }
    ],
    "supporting_skills": [
      {
        "name": "Flask",
        "proficiency": 65,
        "human_developed": false,
        "ai_assisted": true,
        "usage_count": 5
      }
    ],
    "exploratory_skills": [
      {
        "name": "React",
        "proficiency": 40,
        "human_developed": false,
        "ai_assisted": true,
        "usage_count": 2
      }
    ]
  },
  "journey": {
    "timeline": [
      {
        "date": "2023-01",
        "event": "Started learning Python",
        "type": "learning",
        "evidence": "First Python commits"
      },
      {
        "date": "2023-06",
        "event": "First ML project",
        "type": "milestone",
        "project": "mnist-classifier",
        "significance": "Entry into machine learning"
      },
      {
        "date": "2024-02",
        "event": "Mastered YOLO architecture",
        "type": "skill_mastery",
        "project": "yolo-custom-detector",
        "significance": "Deep understanding of object detection"
      }
    ],
    "key_milestones": [
      {
        "title": "First Computer Vision Project",
        "date": "2023-08",
        "description": "Built face detection system",
        "impact": "Discovered passion for CV"
      }
    ],
    "growth_metrics": {
      "code_quality_progression": [60, 65, 70, 75, 80],
      "complexity_progression": [4, 5, 6, 7, 8],
      "skill_count_progression": [3, 5, 8, 10, 12]
    },
    "narrative": {
      "intro": "Started coding journey in early 2023...",
      "key_moments": [
        "Discovered computer vision through online course",
        "Built first object detection project",
        "Contributed to open source CV library"
      ],
      "current_state": "Intermediate CV developer with strong fundamentals",
      "future_direction": "Aiming for advanced CV roles, exploring 3D vision"
    }
  }
}
```

## Error Handling

### GitHub API Rate Limiting
- Implement exponential backoff
- Cache results for 24 hours
- Show user-friendly messages when rate limited
- Provide option to retry later

### Invalid User Input
- Validate expertise area against known domains
- Provide suggestions for common expertise areas
- Allow free-form text but guide users

### Analysis Failures
- Graceful degradation: show partial results
- Log errors for debugging
- Provide clear error messages to users
- Offer manual refresh option

### Missing Data
- Handle users with few repos gracefully
- Provide constructive feedback for beginners
- Don't penalize new developers

## Testing Strategy

### Unit Tests

**Test Coverage**:
1. **Portfolio Analyzer Tests** (`test_portfolio_analyzer.py`)
   - Test expertise matching logic
   - Test AI detection accuracy
   - Test project complexity calculation
   - Test innovation detection

2. **Career Assessor Tests** (`test_career_assessor.py`)
   - Test career stage classification
   - Test job readiness calculation
   - Test skill proficiency analysis
   - Test edge cases (new developers, experts)

3. **Journey Extractor Tests** (`test_journey_extractor.py`)
   - Test timeline building
   - Test milestone detection
   - Test growth metrics calculation
   - Test narrative generation

### Integration Tests

1. **End-to-End Portfolio Analysis**
   - Test full flow from user input to portfolio display
   - Test with real GitHub profiles (test accounts)
   - Verify data persistence

2. **View Tests**
   - Test form submissions
   - Test portfolio rendering
   - Test error handling

### Manual Testing

1. **Visual Testing**
   - Verify haunted theme consistency
   - Test responsive design
   - Test animations and interactions

2. **User Experience Testing**
   - Test with different user profiles (beginner, intermediate, advanced)
   - Verify clarity of assessments
   - Test with various expertise areas

## Performance Considerations

### Optimization Strategies

1. **Caching**
   - Cache GitHub API responses for 24 hours
   - Cache analysis results in database
   - Implement Redis caching for frequently accessed portfolios

2. **Async Processing**
   - Move portfolio analysis to background task (Celery)
   - Show loading state to user
   - Send notification when analysis complete

3. **Pagination**
   - Limit initial repo analysis to 30 most recent
   - Load more on demand

4. **Database Indexing**
   - Index on `last_portfolio_update`
   - Index on `expertise_area` for search

## Security Considerations

1. **API Key Management**
   - Store GitHub API tokens securely in environment variables
   - Rotate tokens regularly
   - Use rate limiting to prevent abuse

2. **User Data Privacy**
   - Only analyze public GitHub data
   - Allow users to delete their analysis
   - Don't store sensitive information

3. **Input Validation**
   - Sanitize all user inputs
   - Validate URLs before fetching
   - Prevent injection attacks

## UI/UX Design

### Visual Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│  Header: Avatar, Username, Verified Badge               │
├─────────────────────────────────────────────────────────┤
│  Expertise Declaration Section                          │
│  - Role, Skills, Journey (user's words)                 │
├─────────────────────────────────────────────────────────┤
│  AI Usage Intelligence Section                          │
│  - Core vs Supporting AI usage                          │
│  - Smart delegation examples                            │
│  - Visual bars showing percentages                      │
├─────────────────────────────────────────────────────────┤
│  Career Stage & Job Readiness                           │
│  - Stage badge (Beginner/Intermediate/Advanced/Expert)  │
│  - Job readiness score with breakdown                   │
│  - Recommendations                                      │
├─────────────────────────────────────────────────────────┤
│  Unique Projects Section                                │
│  - Project cards with relevance indicators              │
│  - AI/Human ratio per project                           │
│  - Complexity and innovation scores                     │
├─────────────────────────────────────────────────────────┤
│  Skills & Tech Stack                                    │
│  - Categorized: Core, Supporting, Exploratory           │
│  - Proficiency indicators                               │
│  - Human vs AI-assisted badges                          │
├─────────────────────────────────────────────────────────┤
│  Journey Timeline                                       │
│  - Visual timeline with milestones                      │
│  - Growth charts                                        │
│  - Narrative story                                      │
├─────────────────────────────────────────────────────────┤
│  GitHub Stats (existing)                                │
└─────────────────────────────────────────────────────────┘
```

### Color Coding

- **Neon Green (#39ff14)**: Strengths, high scores, human code
- **Neon Purple (#9d4edd)**: Neutral info, section headers
- **Yellow (#ffc107)**: Areas for improvement, warnings
- **Red (#ff0055)**: Critical issues (if any)

### Interactive Elements

- Hover effects on project cards
- Expandable sections for detailed info
- Animated progress bars
- Tooltips for explanations
- Click to view GitHub repos

## Migration Strategy

### Phase 1: Database Migration
1. Add new fields to User model
2. Run Django migrations
3. Existing users have blank values (no breaking changes)

### Phase 2: Code Deployment
1. Deploy new analyzer modules
2. Deploy enhanced views
3. Deploy new templates

### Phase 3: User Onboarding
1. Prompt existing users to fill expertise form
2. Offer to re-analyze portfolios
3. Show benefits of new features

### Backward Compatibility
- Existing portfolio_data structure still works
- New fields are optional
- Graceful degradation if analysis fails
