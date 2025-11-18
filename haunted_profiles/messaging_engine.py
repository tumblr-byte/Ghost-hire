"""
Messaging Engine Module
Generates positive, context-aware messages based on AI usage patterns
"""
import logging

logger = logging.getLogger(__name__)


class MessagingEngine:
    """Generates motivational and context-aware messages"""
    
    def __init__(self, breakdown_data, user_profile):
        """
        Args:
            breakdown_data: Output from BreakdownCalculator
            user_profile: User's self-description
        """
        self.breakdown_data = breakdown_data
        self.user_profile = user_profile or {}
        
    def generate_motivational_message(self):
        """
        Generate main motivational message
        
        Returns: {
            'title': 'Smart AI User 🔥',
            'message': '...',
            'tone': 'encouraging'
        }
        """
        core_independence = self.breakdown_data.get('core_independence_score', 50)
        overall_assessment = self.breakdown_data.get('overall_assessment', 'smart_ai_user')
        
        title = 'Smart AI User 🔥'
        message = ''
        tone = 'encouraging'
        
        if overall_assessment == 'excellent':
            title = '🧠 AI Strategy Analysis - You\'re doing it RIGHT'
            message = 'You write your core algorithms independently and use AI strategically for supporting tasks. This is exactly how professional developers work!'
            tone = 'celebrating'
        elif overall_assessment == 'smart_ai_user':
            title = '🧠 AI Strategy Analysis - You\'re doing it RIGHT'
            message = 'Strategic AI usage - You write your core code yourself and use AI for efficiency on supporting tasks. This is the smart way to work!'
            tone = 'encouraging'
        else:
            title = '🚀 Level Up Your Skills'
            message = 'Build more complex projects to reach Ghost Level 100! Focus on writing core algorithms yourself while using AI for supporting tasks.'
            tone = 'constructive'
        
        return {
            'title': title,
            'message': message,
            'tone': tone
        }
    
    def generate_category_messages(self, category):
        """
        Generate message for specific category
        
        Args:
            category: Category dict with name, status, human_percentage
            
        Returns: {
            'message': 'You write your core algorithms independently! 🔥',
            'icon': '✅',
            'color': 'green'
        }
        """
        status = category.get('status', 'good')
        is_core = category.get('is_core', False)
        human_percentage = category.get('human_percentage', 50)
        
        if status == 'excellent':
            return {
                'message': 'You write your core code independently! 🔥',
                'icon': '🔥',
                'color': 'green'
            }
        elif status == 'good':
            return {
                'message': 'Good technical implementation',
                'icon': '✅',
                'color': 'green'
            }
        elif status == 'smart':
            return {
                'message': 'Smart use of AI for non-core tasks ✅',
                'icon': '✅',
                'color': 'purple'
            }
        else:
            return {
                'message': 'Consider writing more code yourself',
                'icon': '📈',
                'color': 'orange'
            }
    
    def generate_improvement_suggestions(self):
        """
        Generate actionable improvement suggestions (Next Level Unlocks)
        
        Returns: [
            {
                'area': 'Core Skills Mastery',
                'suggestion': 'Keep writing your ML algorithms yourself - you\'re doing great!',
                'priority': 'maintain',
                'icon': '🏆'
            },
            ...
        ]
        """
        suggestions = []
        core_independence = self.breakdown_data.get('core_independence_score', 50)
        categories = self.breakdown_data.get('categories', [])
        
        # Core skills suggestions
        if core_independence >= 80:
            suggestions.append({
                'area': '🏆 Core Skills Mastery',
                'suggestion': 'You\'re crushing it! Keep writing your core algorithms yourself. Next: Mentor others!',
                'priority': 'maintain',
                'icon': '🏆'
            })
        elif core_independence >= 60:
            suggestions.append({
                'area': '⭐ Level Up Core Skills',
                'suggestion': 'Try implementing more complex features from scratch. You\'re almost there!',
                'priority': 'improve',
                'icon': '⭐'
            })
        else:
            suggestions.append({
                'area': '🚀 Build Core Foundation',
                'suggestion': 'Focus on writing core algorithms yourself - start with smaller features and level up!',
                'priority': 'critical',
                'icon': '🚀'
            })
        
        # Commit message suggestions
        suggestions.append({
            'area': '📝 Better Documentation',
            'suggestion': 'Write detailed commit messages explaining your technical decisions. Unlock: Team Lead badge!',
            'priority': 'improve',
            'icon': '📝'
        })
        
        # Project suggestions
        suggestions.append({
            'area': '💎 Showcase Projects',
            'suggestion': 'Build 2-3 projects that showcase your core skills without AI. Unlock: Portfolio Master!',
            'priority': 'improve',
            'icon': '💎'
        })
        
        # Bonus unlock
        if core_independence >= 70:
            suggestions.append({
                'area': '🎯 Open Source Contribution',
                'suggestion': 'Contribute to open source projects in your domain. Unlock: Community Champion!',
                'priority': 'improve',
                'icon': '🎯'
            })
        
        return suggestions
