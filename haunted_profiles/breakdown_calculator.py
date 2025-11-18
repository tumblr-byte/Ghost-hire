"""
Breakdown Calculator Module
Calculates detailed AI usage statistics for each category
"""
import logging

logger = logging.getLogger(__name__)


class BreakdownCalculator:
    """Calculates AI usage breakdown with context-aware messages"""
    
    def __init__(self, categorized_data, user_profile):
        """
        Args:
            categorized_data: Output from AIUsageCategorizer
            user_profile: User's self-description
        """
        self.categorized_data = categorized_data
        self.user_profile = user_profile or {}
        
    def calculate_category_breakdown(self):
        """
        Calculate AI% for each category with context
        
        Returns: {
            'categories': [...],
            'overall_assessment': 'smart_ai_user',
            'core_independence_score': 90
        }
        """
        categories_data = self.categorized_data.get('categories', {})
        core_vs_supporting = self.categorized_data.get('core_vs_supporting', {})
        
        categories = []
        
        # Core ML/CV Algorithms
        if 'core_algorithms' in categories_data:
            core_data = categories_data['core_algorithms']
            categories.append({
                'name': 'Core ML/CV Algorithms',
                'ai_percentage': core_data['ai_percentage'],
                'human_percentage': core_data['human_percentage'],
                'is_core': True,
                'status': self._get_status(core_data['human_percentage'], True),
                'examples': core_data['examples'],
                'message': self._get_message(core_data['human_percentage'], True)
            })
        
        # API & Integration
        if 'api_integration' in categories_data:
            api_data = categories_data['api_integration']
            categories.append({
                'name': 'API & Integration',
                'ai_percentage': api_data['ai_percentage'],
                'human_percentage': api_data['human_percentage'],
                'is_core': True,
                'status': self._get_status(api_data['human_percentage'], True),
                'examples': api_data['examples'],
                'message': self._get_message(api_data['human_percentage'], True)
            })
        
        # UI/UX & Styling
        if 'ui_ux' in categories_data:
            ui_data = categories_data['ui_ux']
            categories.append({
                'name': 'UI/UX & Styling',
                'ai_percentage': ui_data['ai_percentage'],
                'human_percentage': ui_data['human_percentage'],
                'is_core': False,
                'status': 'smart',
                'examples': ui_data['examples'],
                'message': 'Smart use of AI for non-core tasks ✅'
            })
        
        # Documentation
        if 'documentation' in categories_data:
            doc_data = categories_data['documentation']
            categories.append({
                'name': 'Documentation',
                'ai_percentage': doc_data['ai_percentage'],
                'human_percentage': doc_data['human_percentage'],
                'is_core': False,
                'status': 'smart',
                'examples': doc_data['examples'],
                'message': 'Efficient documentation with AI'
            })
        
        # Calculate core independence score
        core_data = core_vs_supporting.get('core', {})
        core_independence_score = core_data.get('human_percentage', 50)
        
        # Overall assessment
        overall_assessment = 'smart_ai_user'
        if core_independence_score >= 80:
            overall_assessment = 'excellent'
        elif core_independence_score >= 60:
            overall_assessment = 'smart_ai_user'
        else:
            overall_assessment = 'needs_improvement'
        
        return {
            'categories': categories,
            'overall_assessment': overall_assessment,
            'core_independence_score': core_independence_score
        }
    
    def calculate_self_awareness_score(self):
        """
        Calculate how self-aware the developer is about their AI usage
        
        Returns: {
            'score': 85,
            'level': 'highly_self_aware',
            'indicators': ['honest_about_weaknesses', 'clear_expertise', 'strategic_ai_use']
        }
        """
        score = 0
        indicators = []
        
        # Check if user provided detailed profile
        if self.user_profile.get('developer_role'):
            score += 20
            indicators.append('clear_role_definition')
        
        if self.user_profile.get('core_skills'):
            score += 20
            indicators.append('clear_expertise')
        
        if self.user_profile.get('weaknesses'):
            score += 25
            indicators.append('honest_about_weaknesses')
        
        if self.user_profile.get('expertise_area'):
            score += 15
            indicators.append('domain_awareness')
        
        if self.user_profile.get('ai_usage_context'):
            score += 20
            indicators.append('strategic_ai_use')
        
        # Determine level
        if score >= 80:
            level = 'highly_self_aware'
        elif score >= 60:
            level = 'self_aware'
        elif score >= 40:
            level = 'somewhat_aware'
        else:
            level = 'needs_reflection'
        
        return {
            'score': score,
            'level': level,
            'indicators': indicators
        }
    
    def _get_status(self, human_percentage, is_core):
        """Determine status based on human percentage"""
        if is_core:
            if human_percentage >= 80:
                return 'excellent'
            elif human_percentage >= 60:
                return 'good'
            else:
                return 'needs_improvement'
        else:
            return 'smart'
    
    def _get_message(self, human_percentage, is_core):
        """Generate message based on human percentage"""
        if is_core:
            if human_percentage >= 80:
                return 'You write your core code independently! 🔥'
            elif human_percentage >= 60:
                return 'Good technical implementation'
            else:
                return 'Consider writing more core code yourself'
        else:
            return 'Smart use of AI for non-core tasks ✅'
