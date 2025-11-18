"""
Journey Extractor Module
Builds developer's learning journey and growth narrative from GitHub data and user input
"""
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JourneyExtractor:
    """Builds developer's learning journey and growth narrative"""
    
    def __init__(self, github_data, user_narrative):
        """
        Initialize with GitHub data and user's narrative
        
        Args:
            github_data: Dict containing GitHub analysis results
            user_narrative: Dict containing user's learning journey text
        """
        self.github_data = github_data
        self.user_narrative = user_narrative or {}
    
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
        timeline = []
        
        # Add user's learning journey as first event
        if self.user_narrative.get('learning_journey'):
            timeline.append({
                'date': 'Start',
                'event': 'Started coding journey',
                'type': 'learning',
                'description': self.user_narrative['learning_journey'][:200]
            })
        
        # Add skill acquisition events
        skills = self.github_data.get('skills', [])
        for i, skill in enumerate(skills[:5]):
            timeline.append({
                'date': f'Phase {i+1}',
                'event': f'Learned {skill}',
                'type': 'skill_acquisition',
                'skill': skill
            })
        
        # Add project milestones
        unique_projects = self.github_data.get('unique_projects', [])
        for project in unique_projects[:3]:
            timeline.append({
                'date': 'Recent',
                'event': f'Built {project["name"]}',
                'type': 'milestone',
                'project': project['name'],
                'description': project.get('description', ''),
                'stars': project.get('stars', 0)
            })
        
        return timeline
    
    def detect_milestones(self):
        """
        Identify key milestones:
        - First project in expertise area
        - Breakthrough projects (high stars/complexity)
        - Skill mastery moments
        - Contribution spikes
        
        Returns: [...]
        """
        milestones = []
        unique_projects = self.github_data.get('unique_projects', [])
        
        # Breakthrough projects (with stars)
        for project in unique_projects:
            if project.get('stars', 0) >= 5:
                milestones.append({
                    'title': f'Breakthrough: {project["name"]}',
                    'description': project.get('description', 'Notable project'),
                    'impact': f'{project["stars"]} stars - community recognition',
                    'type': 'breakthrough'
                })
        
        # First project in expertise area
        if unique_projects:
            first_project = unique_projects[0]
            milestones.append({
                'title': f'First Major Project: {first_project["name"]}',
                'description': first_project.get('description', ''),
                'impact': 'Started building portfolio',
                'type': 'first_project'
            })
        
        # Skill mastery (based on proficiency)
        domains = self.github_data.get('domains', [])
        if domains:
            milestones.append({
                'title': f'Domain Expertise: {domains[0]}',
                'description': f'Specialized in {domains[0]}',
                'impact': 'Developed focused expertise',
                'type': 'skill_mastery'
            })
        
        return milestones[:5]  # Top 5 milestones
    
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
            'skill_count_progression': [1, 2, 3, 5, 7]
        }
        """
        # Simplified growth metrics based on current state
        human_percentage = self.github_data.get('human_code_percentage', 50)
        complexity_level = self.github_data.get('complexity_level', 'intermediate')
        skills_count = len(self.github_data.get('skills', []))
        
        # Simulate progression (in real implementation, would analyze commit history)
        complexity_map = {'basic': 5, 'intermediate': 7, 'advanced': 9}
        current_complexity = complexity_map.get(complexity_level, 7)
        
        return {
            'code_quality_progression': [
                max(30, human_percentage - 20),
                max(40, human_percentage - 15),
                max(50, human_percentage - 10),
                max(60, human_percentage - 5),
                human_percentage
            ],
            'complexity_progression': [
                max(3, current_complexity - 4),
                max(4, current_complexity - 3),
                max(5, current_complexity - 2),
                max(6, current_complexity - 1),
                current_complexity
            ],
            'skill_count_progression': [
                max(1, skills_count - 4),
                max(2, skills_count - 3),
                max(3, skills_count - 2),
                max(4, skills_count - 1),
                skills_count
            ]
        }
    
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
        # Intro from user's journey
        intro = self.user_narrative.get('learning_journey', '')
        if not intro:
            # Generate default intro based on GitHub data
            domains = self.github_data.get('domains', [])
            repos_count = self.github_data.get('public_repos', 0)
            if domains:
                intro = f"A passionate developer specializing in {domains[0]}, with {repos_count} projects showcasing technical skills and continuous learning."
            else:
                intro = f"A dedicated developer with {repos_count} projects, constantly learning and building new skills through hands-on experience."
        
        # Key moments from milestones
        milestones = self.detect_milestones()
        key_moments = [m['title'] for m in milestones[:3]]
        
        # Current state from GitHub analysis
        domains = self.github_data.get('domains', [])
        complexity_level = self.github_data.get('complexity_level', 'intermediate')
        
        if domains:
            current_state = f"Currently specializing in {domains[0]} with {complexity_level} level expertise"
        else:
            current_state = f"Building skills with {complexity_level} level projects"
        
        # Future direction from user's context
        future_direction = self.user_narrative.get('ai_usage_context', '')
        if not future_direction:
            future_direction = "Continuing to grow technical skills and take on more complex challenges"
        
        return {
            'intro': intro[:300],
            'key_moments': key_moments,
            'current_state': current_state,
            'future_direction': future_direction[:200]
        }
