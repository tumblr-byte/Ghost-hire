"""
Visualization Generator Module
Generates chart data and visual elements for the breakdown
"""
import logging

logger = logging.getLogger(__name__)


class VisualizationGenerator:
    """Generates visualization data for AI usage breakdown"""
    
    def __init__(self, breakdown_data):
        """
        Args:
            breakdown_data: Output from BreakdownCalculator
        """
        self.breakdown_data = breakdown_data
        
    def generate_stacked_bar_data(self):
        """
        Generate data for stacked bar chart
        
        Returns: {
            'labels': ['Core Skills', 'Supporting Tasks'],
            'human_data': [90, 20],
            'ai_data': [10, 80],
            'colors': {...}
        }
        """
        core_independence = self.breakdown_data.get('core_independence_score', 50)
        
        # Calculate supporting tasks percentage (inverse of core for simplicity)
        supporting_human = max(10, 100 - (core_independence + 30))
        
        return {
            'labels': ['Core Skills', 'Supporting Tasks'],
            'human_data': [core_independence, supporting_human],
            'ai_data': [100 - core_independence, 100 - supporting_human],
            'colors': {
                'human': '#39FF14',  # neon green
                'ai': '#9D4EDD'      # neon purple
            }
        }
    
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
        categories = self.breakdown_data.get('categories', [])
        cards = []
        
        for category in categories:
            # Determine icon and color based on status
            if category['status'] == 'excellent':
                icon = '🔥'
                color = 'green'
            elif category['status'] == 'good':
                icon = '✅'
                color = 'green'
            elif category['status'] == 'smart':
                icon = '✅'
                color = 'purple'
            else:
                icon = '📈'
                color = 'orange'
            
            cards.append({
                'title': category['name'],
                'icon': icon,
                'human_percentage': category['human_percentage'],
                'ai_percentage': category['ai_percentage'],
                'status': category['status'],
                'color': color,
                'examples': category.get('examples', []),
                'message': category.get('message', '')
            })
        
        return cards
    
    def generate_employer_summary(self):
        """
        Generate employer-friendly summary
        
        Returns: {
            'headline': 'Computer Vision Developer - Writes Core Algorithms Independently',
            'key_points': [...],
            'technical_depth': 'Advanced - 5 complex CV projects',
            'recommendation': 'Strong technical foundation with strategic AI usage'
        }
        """
        categories = self.breakdown_data.get('categories', [])
        core_independence = self.breakdown_data.get('core_independence_score', 50)
        overall_assessment = self.breakdown_data.get('overall_assessment', 'smart_ai_user')
        
        # Find core category for headline
        core_category = next((c for c in categories if c['is_core']), None)
        
        headline = 'Developer - Writes Code Independently'
        if core_category and core_category['human_percentage'] >= 80:
            headline = f"{core_category['name']} Developer - Writes Core Algorithms Independently"
        
        # Generate key points
        key_points = []
        
        # Core skills point
        if core_independence >= 80:
            key_points.append(f'Independently develops core algorithms ({core_independence}% human-written)')
        elif core_independence >= 60:
            key_points.append(f'Develops core algorithms with some AI assistance ({core_independence}% human-written)')
        
        # Skills proficiency
        if core_category and core_category.get('examples'):
            skills_str = ', '.join(core_category['examples'][:3])
            key_points.append(f'Proficient in {skills_str}')
        
        # AI usage point
        supporting_category = next((c for c in categories if not c['is_core']), None)
        if supporting_category:
            key_points.append(f'Efficiently uses AI for {supporting_category["name"].lower()} (smart workflow)')
        
        # Technical depth
        technical_depth = 'Intermediate level'
        if core_independence >= 80:
            technical_depth = 'Advanced - Strong technical foundation'
        elif core_independence >= 60:
            technical_depth = 'Intermediate - Growing technical skills'
        
        # Recommendation
        recommendation = 'Developing technical skills'
        if overall_assessment == 'excellent':
            recommendation = 'Strong technical foundation with strategic AI usage'
        elif overall_assessment == 'smart_ai_user':
            recommendation = 'Good technical skills with smart AI assistance'
        else:
            recommendation = 'Building technical foundation, consider more hands-on coding'
        
        return {
            'headline': headline,
            'key_points': key_points,
            'technical_depth': technical_depth,
            'recommendation': recommendation
        }
