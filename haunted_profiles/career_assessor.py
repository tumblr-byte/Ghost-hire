"""
Career Assessment Module
Assesses developer's career stage and job readiness based on GitHub analysis
"""
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CareerAssessor:
    """Assesses developer's career stage and job readiness"""
    
    def __init__(self, github_data, user_profile):
        """
        Initialize with GitHub analysis data and user profile
        
        Args:
            github_data: Dict containing GitHub analysis results
            user_profile: Dict containing user's self-description
        """
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
        evidence = []
        stage_scores = {
            'beginner': 0,
            'intermediate': 0,
            'advanced': 0,
            'expert': 0
        }
        
        # Factor 1: Repository count and quality
        original_repos = self.github_data.get('original_repos', 0)
        total_repos = self.github_data.get('public_repos', 0)
        
        if original_repos >= 20:
            stage_scores['advanced'] += 3
            stage_scores['expert'] += 2
            evidence.append(f"✅ {original_repos} original repositories - extensive portfolio")
        elif original_repos >= 10:
            stage_scores['intermediate'] += 3
            stage_scores['advanced'] += 2
            evidence.append(f"✅ {original_repos} original repositories - solid portfolio")
        elif original_repos >= 5:
            stage_scores['beginner'] += 2
            stage_scores['intermediate'] += 3
            evidence.append(f"📊 {original_repos} original repositories - building portfolio")
        else:
            stage_scores['beginner'] += 3
            evidence.append(f"📊 {original_repos} repositories - early stage portfolio")
        
        # Factor 2: Project complexity
        complexity_level = self.github_data.get('complexity_level', 'intermediate')
        
        if complexity_level == 'advanced':
            stage_scores['advanced'] += 4
            stage_scores['expert'] += 3
            evidence.append("🔬 Advanced code complexity - tackles complex problems")
        elif complexity_level == 'intermediate':
            stage_scores['intermediate'] += 3
            stage_scores['advanced'] += 1
            evidence.append("⚡ Intermediate complexity - solid technical skills")
        else:
            stage_scores['beginner'] += 3
            evidence.append("📚 Basic complexity - learning fundamentals")
        
        # Factor 3: Stars and community engagement
        total_stars = self.github_data.get('total_stars', 0)
        
        if total_stars >= 100:
            stage_scores['expert'] += 3
            stage_scores['advanced'] += 2
            evidence.append(f"⭐ {total_stars} stars - recognized by community")
        elif total_stars >= 20:
            stage_scores['advanced'] += 2
            stage_scores['intermediate'] += 1
            evidence.append(f"⭐ {total_stars} stars - gaining recognition")
        elif total_stars >= 5:
            stage_scores['intermediate'] += 1
            evidence.append(f"⭐ {total_stars} stars - some community interest")
        
        # Factor 4: Human vs AI code ratio
        human_percentage = self.github_data.get('human_code_percentage', 50)
        
        if human_percentage >= 75:
            stage_scores['advanced'] += 2
            stage_scores['intermediate'] += 1
            evidence.append(f"💪 {human_percentage}% human code - strong original work")
        elif human_percentage >= 60:
            stage_scores['intermediate'] += 2
            evidence.append(f"⚡ Strategic AI usage - {human_percentage}% human on core algorithms, AI for efficiency")
        else:
            stage_scores['beginner'] += 1
            evidence.append(f"🚀 {human_percentage}% human code - building skills with smart AI assistance")
        
        # Factor 5: Smart AI usage
        smart_ai_user = self.github_data.get('smart_ai_user', False)
        
        if smart_ai_user:
            stage_scores['intermediate'] += 1
            stage_scores['advanced'] += 1
            evidence.append("✅ Smart AI usage - uses AI as a tool, not a crutch")
        
        # Factor 6: Domain expertise
        domains = self.github_data.get('domains', [])
        
        if len(domains) >= 2:
            stage_scores['intermediate'] += 1
            stage_scores['advanced'] += 1
            evidence.append(f"🎯 Multi-domain expertise: {', '.join(domains[:2])}")
        elif len(domains) == 1:
            evidence.append(f"🎯 Focused on: {domains[0]}")
        
        # Factor 7: Unique projects
        unique_projects = self.github_data.get('unique_projects', [])
        
        if len(unique_projects) >= 5:
            stage_scores['advanced'] += 2
            evidence.append(f"🚀 {len(unique_projects)} notable projects - diverse experience")
        elif len(unique_projects) >= 3:
            stage_scores['intermediate'] += 2
            evidence.append(f"🚀 {unique_projects} notable projects - growing portfolio")
        
        # Determine final stage
        max_score = max(stage_scores.values())
        if max_score == 0:
            final_stage = 'beginner'
            confidence = 0.5
        else:
            final_stage = max(stage_scores, key=stage_scores.get)
            confidence = round(stage_scores[final_stage] / sum(stage_scores.values()), 2)
        
        # Adjust based on user's self-description
        if self.user_profile.get('expertise_area'):
            evidence.append(f"👤 Self-described expertise: {self.user_profile['expertise_area']}")
        
        return {
            'stage': final_stage,
            'confidence': confidence,
            'evidence': evidence,
            'scores': stage_scores
        }
    
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
        breakdown = {}
        recommendations = []
        strengths = []
        areas_for_improvement = []
        
        # Factor 1: Technical Skills Breadth (25%)
        skills = self.github_data.get('skills', [])
        languages = self.github_data.get('languages', {})
        
        if len(skills) >= 5:
            breadth_score = 25
            strengths.append(f"Diverse tech stack: {', '.join(skills[:5])}")
        elif len(skills) >= 3:
            breadth_score = 20
            strengths.append(f"Solid tech stack: {', '.join(skills)}")
        elif len(skills) >= 2:
            breadth_score = 15
            areas_for_improvement.append("Expand your tech stack - learn complementary technologies")
        else:
            breadth_score = 10
            areas_for_improvement.append("Limited tech stack - diversify your skills")
            recommendations.append("📈 Learn 2-3 more technologies in your domain")
        
        breakdown['technical_breadth'] = breadth_score
        
        # Factor 2: Technical Skills Depth (25%)
        complexity_level = self.github_data.get('complexity_level', 'intermediate')
        human_percentage = self.github_data.get('human_code_percentage', 50)
        
        if complexity_level == 'advanced' and human_percentage >= 70:
            depth_score = 25
            strengths.append("Deep technical expertise with strong original work")
        elif complexity_level == 'advanced' or human_percentage >= 70:
            depth_score = 20
            strengths.append("Good technical depth")
        elif complexity_level == 'intermediate' and human_percentage >= 60:
            depth_score = 18
        else:
            depth_score = 12
            areas_for_improvement.append("Build deeper expertise in your core domain")
            recommendations.append("📈 Take on more complex projects in your expertise area")
        
        breakdown['technical_depth'] = depth_score
        
        # Factor 3: Portfolio Quality (20%)
        unique_projects = self.github_data.get('unique_projects', [])
        total_stars = self.github_data.get('total_stars', 0)
        
        if len(unique_projects) >= 5 and total_stars >= 20:
            portfolio_score = 20
            strengths.append(f"{len(unique_projects)} quality projects with community recognition")
        elif len(unique_projects) >= 3:
            portfolio_score = 15
            strengths.append(f"{len(unique_projects)} notable projects")
        elif len(unique_projects) >= 1:
            portfolio_score = 10
            areas_for_improvement.append("Build more diverse projects")
            recommendations.append("📈 Create 2-3 more unique projects showcasing different skills")
        else:
            portfolio_score = 5
            areas_for_improvement.append("Limited portfolio - need more projects")
            recommendations.append("📈 Build at least 3 complete projects in your domain")
        
        breakdown['portfolio_quality'] = portfolio_score
        
        # Factor 4: Code Quality (15%)
        smart_ai_user = self.github_data.get('smart_ai_user', False)
        
        if smart_ai_user and human_percentage >= 70:
            code_quality_score = 15
            strengths.append("High code quality with smart AI usage")
        elif human_percentage >= 60:
            code_quality_score = 12
            strengths.append("Strategic AI usage - efficient workflow")
        else:
            code_quality_score = 8
            areas_for_improvement.append("Level up: Build more complex projects to reach Ghost Level 100")
            recommendations.append("🚀 Build 2-3 advanced projects showcasing your core skills")
        
        breakdown['code_quality'] = code_quality_score
        
        # Factor 5: Communication (10%)
        # Based on project descriptions and commit messages
        projects_with_desc = len([p for p in unique_projects if p.get('description') and p['description'] != 'No description'])
        
        if projects_with_desc >= 3:
            communication_score = 10
            strengths.append("Good documentation and project descriptions")
        elif projects_with_desc >= 1:
            communication_score = 7
        else:
            communication_score = 4
            areas_for_improvement.append("Improve documentation and communication")
            recommendations.append("📈 Add clear README files and project descriptions")
        
        breakdown['communication'] = communication_score
        
        # Factor 6: Consistency (5%)
        original_repos = self.github_data.get('original_repos', 0)
        
        if original_repos >= 10:
            consistency_score = 5
            strengths.append("Consistent development activity")
        elif original_repos >= 5:
            consistency_score = 4
        else:
            consistency_score = 2
            areas_for_improvement.append("Build more consistent coding habits")
            recommendations.append("📈 Commit code regularly - aim for weekly activity")
        
        breakdown['consistency'] = consistency_score
        
        # Calculate overall score
        overall_score = sum(breakdown.values())
        
        # Generate job readiness assessment
        if overall_score >= 80:
            readiness_level = "🔥 Highly Job Ready"
            readiness_desc = "Ready for mid-to-senior level positions"
        elif overall_score >= 65:
            readiness_level = "✅ Job Ready"
            readiness_desc = "Ready for junior-to-mid level positions"
        elif overall_score >= 50:
            readiness_level = "⚡ Nearly Ready"
            readiness_desc = "Close to job ready - focus on improvements"
        else:
            readiness_level = "📚 Building Skills"
            readiness_desc = "Keep building - you're on the right path"
        
        return {
            'overall_score': overall_score,
            'readiness_level': readiness_level,
            'readiness_description': readiness_desc,
            'breakdown': breakdown,
            'strengths': strengths,
            'areas_for_improvement': areas_for_improvement,
            'recommendations': recommendations
        }
    
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
        languages = self.github_data.get('languages', {})
        skills = self.github_data.get('skills', [])
        unique_projects = self.github_data.get('unique_projects', [])
        
        # Categorize skills based on usage
        skill_usage = {}
        
        for lang, count in languages.items():
            skill_usage[lang] = count
        
        # Sort by usage
        sorted_skills = sorted(skill_usage.items(), key=lambda x: x[1], reverse=True)
        
        # Categorize
        core_skills = []
        supporting_skills = []
        exploratory_skills = []
        
        for i, (skill, count) in enumerate(sorted_skills):
            # Calculate proficiency (0-100)
            if count >= 10:
                proficiency = min(90 + (count - 10), 100)
            elif count >= 5:
                proficiency = 70 + (count - 5) * 4
            else:
                proficiency = 40 + count * 6
            
            # Check if human-developed (based on overall human percentage)
            human_percentage = self.github_data.get('human_code_percentage', 50)
            human_developed = human_percentage >= 60
            
            skill_data = {
                'name': skill,
                'proficiency': proficiency,
                'human_developed': human_developed,
                'usage_count': count,
                'projects': [p['name'] for p in unique_projects if p.get('language') == skill][:3]
            }
            
            # Categorize based on position and usage
            if i < 2 and count >= 5:
                core_skills.append(skill_data)
            elif i < 5:
                supporting_skills.append(skill_data)
            else:
                exploratory_skills.append(skill_data)
        
        # Add user's self-described core skills
        if self.user_profile.get('core_skills'):
            user_skills = self.user_profile['core_skills'].split(',')
            for user_skill in user_skills[:3]:
                skill_name = user_skill.strip()
                # Check if already in core_skills
                if not any(s['name'].lower() == skill_name.lower() for s in core_skills):
                    core_skills.append({
                        'name': skill_name,
                        'proficiency': 75,  # Assume decent proficiency if user claims it
                        'human_developed': True,
                        'usage_count': 0,
                        'projects': [],
                        'self_described': True
                    })
        
        return {
            'core_skills': core_skills[:5],  # Top 5 core skills
            'supporting_skills': supporting_skills[:5],
            'exploratory_skills': exploratory_skills[:5]
        }
