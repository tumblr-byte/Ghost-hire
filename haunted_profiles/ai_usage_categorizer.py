"""
AI Usage Categorizer Module
Categorizes code/commits into task types based on user profile and code analysis
"""
import logging

logger = logging.getLogger(__name__)


class AIUsageCategorizer:
    """Categorizes AI usage into task types (core vs supporting)"""
    
    def __init__(self, user_profile, github_data):
        """
        Args:
            user_profile: Dict with expertise_area, core_skills, weaknesses, etc.
            github_data: Dict with repos, commits, languages, ai_percentage
        """
        self.user_profile = user_profile or {}
        self.github_data = github_data or {}
        
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
        # Get user's core skills and weaknesses
        core_skills = self.user_profile.get('core_skills', '').lower()
        weaknesses = self.user_profile.get('weaknesses', '').lower()
        expertise_area = self.user_profile.get('expertise_area', '').lower()
        
        # Default AI percentages based on typical patterns
        overall_ai = self.github_data.get('ai_code_percentage', 50)
        
        # Core algorithms - if user has ML/CV expertise, they likely write this themselves
        core_ai_percentage = 10
        if any(term in expertise_area or term in core_skills for term in ['ml', 'ai', 'vision', 'computer vision', 'machine learning']):
            core_ai_percentage = 10  # Very low AI usage in core skills
        else:
            core_ai_percentage = max(10, overall_ai - 30)  # Lower than overall
        
        # UI/UX - if mentioned in weaknesses, high AI usage
        ui_ai_percentage = 85
        if any(term in weaknesses for term in ['ui', 'ux', 'css', 'styling', 'streamlit', 'frontend']):
            ui_ai_percentage = 85
        else:
            ui_ai_percentage = max(40, overall_ai)
        
        # Documentation - typically high AI usage
        doc_ai_percentage = 90
        if 'documentation' in weaknesses or 'readme' in weaknesses:
            doc_ai_percentage = 90
        else:
            doc_ai_percentage = 70
        
        # API/Integration - moderate AI usage
        api_ai_percentage = max(30, min(70, overall_ai))
        
        # Boilerplate - moderate to high AI usage
        boilerplate_ai_percentage = max(60, min(80, overall_ai + 10))
        
        # Extract examples from user profile
        core_examples = self._extract_core_examples()
        ui_examples = self._extract_ui_examples()
        
        return {
            'core_algorithms': {
                'ai_percentage': core_ai_percentage,
                'human_percentage': 100 - core_ai_percentage,
                'examples': core_examples
            },
            'api_integration': {
                'ai_percentage': api_ai_percentage,
                'human_percentage': 100 - api_ai_percentage,
                'examples': ['Model integration', 'Pipeline setup', 'API endpoints']
            },
            'ui_ux': {
                'ai_percentage': ui_ai_percentage,
                'human_percentage': 100 - ui_ai_percentage,
                'examples': ui_examples
            },
            'documentation': {
                'ai_percentage': doc_ai_percentage,
                'human_percentage': 100 - doc_ai_percentage,
                'examples': ['README files', 'Code comments', 'Documentation']
            },
            'boilerplate': {
                'ai_percentage': boilerplate_ai_percentage,
                'human_percentage': 100 - boilerplate_ai_percentage,
                'examples': ['Project setup', 'Configuration files', 'Boilerplate code']
            }
        }
    
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
        categories = self.categorize_by_task_type()
        
        # Core categories (where developer should write code themselves)
        core_categories = ['core_algorithms', 'api_integration']
        core_ai_sum = sum(categories[cat]['ai_percentage'] for cat in core_categories)
        core_ai_avg = core_ai_sum / len(core_categories)
        
        # Supporting categories (where AI assistance is smart)
        supporting_categories = ['ui_ux', 'documentation', 'boilerplate']
        supporting_ai_sum = sum(categories[cat]['ai_percentage'] for cat in supporting_categories)
        supporting_ai_avg = supporting_ai_sum / len(supporting_categories)
        
        # Extract skills and tasks
        core_skills = self._extract_core_examples()
        supporting_tasks = self._extract_ui_examples()
        
        return {
            'core': {
                'categories': core_categories,
                'ai_percentage': round(core_ai_avg),
                'human_percentage': round(100 - core_ai_avg),
                'skills': core_skills
            },
            'supporting': {
                'categories': supporting_categories,
                'ai_percentage': round(supporting_ai_avg),
                'human_percentage': round(100 - supporting_ai_avg),
                'tasks': supporting_tasks
            }
        }
    
    def _extract_core_examples(self):
        """Extract core skill examples from user profile"""
        core_skills = self.user_profile.get('core_skills', '')
        expertise_details = self.user_profile.get('expertise_details', '')
        
        examples = []
        
        # Parse core skills
        if core_skills:
            skills_list = [s.strip() for s in core_skills.split(',')]
            examples.extend(skills_list[:5])  # Top 5
        
        # Add from expertise details
        if expertise_details and not examples:
            details_list = [s.strip() for s in expertise_details.split(',')]
            examples.extend(details_list[:3])
        
        # Fallback to GitHub domains
        if not examples:
            domains = self.github_data.get('domains', [])
            if domains:
                examples = [domains[0]]
        
        return examples[:5] if examples else ['Core development']
    
    def _extract_ui_examples(self):
        """Extract UI/supporting task examples from user profile"""
        weaknesses = self.user_profile.get('weaknesses', '')
        non_expertise = self.user_profile.get('non_expertise_areas', '')
        
        examples = []
        
        # Parse weaknesses
        if weaknesses:
            weak_list = [s.strip() for s in weaknesses.split(',')]
            examples.extend(weak_list[:5])
        
        # Add from non-expertise areas
        if non_expertise and len(examples) < 3:
            non_exp_list = [s.strip() for s in non_expertise.split(',')]
            examples.extend(non_exp_list[:3])
        
        return examples[:5] if examples else ['UI/UX', 'Styling', 'Documentation']
