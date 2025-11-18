"""
AI Portfolio Analyzer - Scrapes and analyzes GitHub, LinkedIn, Devpost
Gen Z style - no boring bios, just REAL skills! 🔥
"""
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def detect_developer_domain(repos_data):
    """
    Detect what domain the developer works in (ML/CV, Web, Mobile, etc.)
    """
    domain_keywords = {
        'ML/AI': ['neural', 'model', 'train', 'dataset', 'pytorch', 'tensorflow', 'keras', 'ml', 'ai', 'gan', 'cnn', 'rnn', 'lstm', 'detection', 'classification', 'vision', 'yolo', 'sgan', 'opencv'],
        'Computer Vision': ['opencv', 'image', 'video', 'detection', 'recognition', 'segmentation', 'yolo', 'rcnn', 'gan', 'vision', 'camera', 'face'],
        'Web Development': ['react', 'vue', 'angular', 'django', 'flask', 'express', 'api', 'frontend', 'backend', 'web', 'html', 'css'],
        'Mobile': ['android', 'ios', 'react-native', 'flutter', 'swift', 'kotlin', 'mobile', 'app'],
        'Data Science': ['pandas', 'numpy', 'analysis', 'data', 'visualization', 'jupyter', 'notebook', 'analytics'],
        'DevOps': ['docker', 'kubernetes', 'ci', 'cd', 'deploy', 'aws', 'cloud', 'infrastructure'],
        'Game Dev': ['unity', 'unreal', 'game', 'engine', '3d', 'graphics', 'shader'],
    }
    
    domain_scores = {domain: 0 for domain in domain_keywords}
    
    for repo in repos_data[:30]:
        if repo.get('fork'):
            continue
        
        repo_name = repo.get('name', '').lower()
        repo_desc = (repo.get('description') or '').lower()
        repo_text = f"{repo_name} {repo_desc}"
        
        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if keyword in repo_text:
                    domain_scores[domain] += 1
    
    # Get top domains
    top_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
    detected_domains = [domain for domain, score in top_domains if score > 0][:3]
    
    return detected_domains if detected_domains else ['General Development']


def analyze_code_complexity(repos_data, username):
    """
    Analyze code complexity to understand if developer writes advanced code
    """
    complexity_indicators = {
        'advanced': 0,
        'intermediate': 0,
        'basic': 0
    }
    
    advanced_keywords = ['algorithm', 'optimization', 'neural', 'model', 'architecture', 'pipeline', 'framework', 'engine', 'compiler', 'parser']
    intermediate_keywords = ['api', 'database', 'authentication', 'integration', 'service', 'module', 'component']
    basic_keywords = ['todo', 'simple', 'basic', 'tutorial', 'practice', 'learning', 'test']
    
    for repo in repos_data[:20]:
        if repo.get('fork'):
            continue
        
        repo_name = repo.get('name', '').lower()
        repo_desc = (repo.get('description') or '').lower()
        repo_text = f"{repo_name} {repo_desc}"
        
        # Check complexity
        if any(kw in repo_text for kw in advanced_keywords):
            complexity_indicators['advanced'] += 1
        elif any(kw in repo_text for kw in intermediate_keywords):
            complexity_indicators['intermediate'] += 1
        elif any(kw in repo_text for kw in basic_keywords):
            complexity_indicators['basic'] += 1
    
    total = sum(complexity_indicators.values())
    if total == 0:
        return 'intermediate', complexity_indicators
    
    # Determine overall complexity
    if complexity_indicators['advanced'] > complexity_indicators['intermediate']:
        return 'advanced', complexity_indicators
    elif complexity_indicators['intermediate'] > complexity_indicators['basic']:
        return 'intermediate', complexity_indicators
    else:
        return 'basic', complexity_indicators


def analyze_ai_usage_patterns(repos_data, username, user_profile=None):
    """
    ENHANCED: Analyze commit patterns with domain awareness, code complexity, and user self-description
    Returns: AI%, Human%, smart usage indicators, and clear explanations
    
    user_profile: Optional dict with user's self-description:
        - developer_role: What they do
        - core_skills: Their main skills
        - strengths: What they're good at
        - weaknesses: What they use AI help for
    """
    ai_indicators = 0
    human_indicators = 0
    smart_usage_signals = []
    explanations = []
    
    # Detect developer domain from repos
    detected_domains = detect_developer_domain(repos_data)
    
    # Use user's self-described role if available
    if user_profile and user_profile.get('developer_role'):
        user_role = user_profile['developer_role']
        explanations.append(f"👤 Self-described: {user_role}")
        
        # If user says they're ML/CV, give them domain bonus
        if any(term in user_role.lower() for term in ['ml', 'ai', 'vision', 'computer vision', 'machine learning', 'data science']):
            detected_domains = ['ML/AI', 'Computer Vision'] + detected_domains
    
    # Analyze code complexity
    complexity_level, complexity_scores = analyze_code_complexity(repos_data, username)
    
    # Adjust scoring based on domain and complexity
    domain_bonus = 0
    if any(d in ['ML/AI', 'Computer Vision', 'Data Science'] for d in detected_domains):
        domain_bonus = 3  # ML/CV developers write more complex code
        explanations.append(f"🎯 Domain: {', '.join(detected_domains[:2])} - Complex technical work")
    
    if complexity_level == 'advanced':
        domain_bonus += 2
        explanations.append(f"🔬 Advanced code complexity - {complexity_scores['advanced']} advanced projects")
    
    # Use user's self-described strengths and weaknesses
    if user_profile:
        if user_profile.get('core_skills'):
            explanations.append(f"💪 Core Skills: {user_profile['core_skills'][:100]}")
        
        if user_profile.get('weaknesses'):
            weaknesses = user_profile['weaknesses']
            explanations.append(f"💡 Uses AI help for: {weaknesses[:100]}")
            # Give bonus for being honest about weaknesses
            domain_bonus += 1
            smart_usage_signals.append('self_aware')
    
    for repo in repos_data[:20]:
        if repo.get('fork'):
            continue
            
        try:
            commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits?per_page=30"
            commits_response = requests.get(commits_url)
            
            if commits_response.status_code != 200:
                continue
                
            commits = commits_response.json()
            commit_messages = [c.get('commit', {}).get('message', '') for c in commits]
            commit_times = [c.get('commit', {}).get('author', {}).get('date', '') for c in commits]
            
            # Analyze commit patterns
            for i, msg in enumerate(commit_messages):
                msg_lower = msg.lower()
                
                # IMPROVED: Check for technical depth in commits
                technical_terms = ['implement', 'refactor', 'optimize', 'debug', 'algorithm', 'model', 'train', 'architecture', 'pipeline', 'fix bug', 'improve performance']
                
                if any(term in msg_lower for term in technical_terms):
                    human_indicators += 2  # Technical commits = human work
                    smart_usage_signals.append('technical_commits')
                
                # Generic messages (but less penalty for ML/CV devs)
                elif any(phrase in msg_lower for phrase in ['initial commit', 'update', 'fix']) and len(msg) < 20:
                    ai_indicators += 1
                
                # Detailed commits
                elif len(msg) > 30:
                    human_indicators += 1
                    smart_usage_signals.append('detailed_commits')
            
            # Iterative development
            if len(commits) > 10:
                human_indicators += 3
                smart_usage_signals.append('iterative_development')
            
            # Consistent activity
            if len(set(commit_times[:10])) > 5:
                human_indicators += 2
                smart_usage_signals.append('consistent_activity')
            
        except Exception as e:
            logger.debug(f"Error analyzing commits for {repo['name']}: {e}")
            continue
    
    # Apply domain bonus
    human_indicators += domain_bonus
    
    # Calculate percentages
    total_indicators = ai_indicators + human_indicators
    if total_indicators == 0:
        ai_percentage = 30
        human_percentage = 70
    else:
        ai_percentage = round((ai_indicators / total_indicators) * 100)
        human_percentage = round((human_indicators / total_indicators) * 100)
    
    # Generate smart usage summary
    usage_summary = []
    
    # User's self-description first
    if user_profile and user_profile.get('developer_role'):
        usage_summary.append(f"👤 {user_profile['developer_role']}")
    
    # Domain-specific insights
    if detected_domains:
        usage_summary.append(f"🎯 Specializes in: {', '.join(detected_domains[:2])}")
    
    if complexity_level == 'advanced':
        usage_summary.append("🔬 Writes advanced/complex code - not simple copy-paste")
    
    # Self-awareness bonus
    if 'self_aware' in smart_usage_signals:
        usage_summary.append("✅ Self-aware about strengths and areas using AI help")
    
    if 'technical_commits' in smart_usage_signals:
        usage_summary.append("✅ Technical commit messages - understands implementation details")
    
    if 'iterative_development' in smart_usage_signals:
        usage_summary.append("✅ Iterative development - builds and improves over time")
    
    if 'consistent_activity' in smart_usage_signals:
        usage_summary.append("✅ Consistent coding activity - regular development")
    
    # AI usage interpretation
    if human_percentage > 70:
        usage_summary.append("🔥 Strong original work - writes own code, uses AI as helper")
        explanations.append("💡 Uses AI for: syntax help, debugging, optimization suggestions")
    elif human_percentage > 50:
        usage_summary.append("⚡ Balanced AI usage - uses AI smartly as coding assistant")
        explanations.append("💡 Uses AI for: code suggestions, refactoring, problem-solving")
    else:
        usage_summary.append("⚠️ High AI assistance detected - may benefit from more hands-on coding")
        explanations.append("💡 Suggestion: Try implementing more features from scratch")
    
    # Improvement suggestions
    improvements = []
    if human_percentage < 60:
        improvements.append("📈 Improve: Write more detailed commit messages explaining your changes")
        improvements.append("📈 Improve: Break large changes into smaller, incremental commits")
    
    if complexity_level == 'basic':
        improvements.append("📈 Improve: Take on more complex projects in your domain")
    
    return {
        'ai_percentage': ai_percentage,
        'human_percentage': human_percentage,
        'usage_summary': usage_summary,
        'explanations': explanations,
        'improvements': improvements,
        'smart_usage': len(smart_usage_signals) >= 2,
        'domains': detected_domains,
        'complexity_level': complexity_level,
    }


def analyze_github(github_url, user_profile=None):
    """
    Scrape GitHub profile and analyze:
    - Languages used (skills!)
    - Unique/interesting projects
    - Commit activity
    - AI vs Human code ratio
    - Smart AI usage patterns
    
    user_profile: Optional dict with user's self-description for smarter analysis
    """
    try:
        username = github_url.rstrip('/').split('/')[-1]
        api_url = f"https://api.github.com/users/{username}"
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
        
        # Get user info
        user_response = requests.get(api_url)
        repos_response = requests.get(repos_url)
        
        if user_response.status_code != 200:
            return {'error': 'GitHub profile not found'}
        
        user_data = user_response.json()
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        # Analyze languages (these become skills!)
        languages = {}
        total_stars = 0
        total_forks = 0
        unique_projects = []
        
        for repo in repos_data:
            # Skip forks (we want original work!)
            if repo.get('fork'):
                continue
                
            # Count languages
            if repo.get('language'):
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
            
            total_stars += repo.get('stargazers_count', 0)
            total_forks += repo.get('forks_count', 0)
            
            # Find unique/interesting projects
            stars = repo.get('stargazers_count', 0)
            has_description = bool(repo.get('description'))
            is_recent = repo.get('updated_at', '')[:4] in ['2024', '2025']
            
            # Project is "unique" if it has stars, description, or is recent
            if stars > 0 or (has_description and is_recent):
                unique_projects.append({
                    'name': repo['name'],
                    'description': repo.get('description', 'No description'),
                    'stars': stars,
                    'language': repo.get('language', 'Unknown'),
                    'url': repo['html_url'],
                })
        
        # Sort unique projects by stars
        unique_projects.sort(key=lambda x: x['stars'], reverse=True)
        
        # Extract skills from languages (top 5)
        skills = list(languages.keys())[:5] if languages else []
        
        # Analyze AI usage patterns with user profile
        ai_analysis = analyze_ai_usage_patterns(repos_data, username, user_profile)
        
        return {
            'username': username,
            'public_repos': user_data.get('public_repos', 0),
            'original_repos': len([r for r in repos_data if not r.get('fork')]),
            'followers': user_data.get('followers', 0),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'languages': languages,
            'skills': skills,  # Top languages as skills
            'top_language': max(languages, key=languages.get) if languages else None,
            'unique_projects': unique_projects[:5],  # Top 5 unique projects
            'ai_code_percentage': ai_analysis['ai_percentage'],
            'human_code_percentage': ai_analysis['human_percentage'],
            'ai_usage_summary': ai_analysis['usage_summary'],
            'explanations': ai_analysis.get('explanations', []),
            'improvements': ai_analysis.get('improvements', []),
            'smart_ai_user': ai_analysis['smart_usage'],
            'domains': ai_analysis.get('domains', []),
            'complexity_level': ai_analysis.get('complexity_level', 'intermediate'),
        }
        
    except Exception as e:
        logger.error(f"Error analyzing GitHub: {e}")
        return {'error': str(e)}



def analyze_devpost(devpost_url):
    """
    Scrape Devpost profile and analyze:
    - Hackathons participated
    - Projects submitted
    - Wins/prizes
    - Submission consistency
    """
    try:
        response = requests.get(devpost_url)
        if response.status_code != 200:
            return {'error': 'Devpost profile not found'}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract hackathon count
        hackathons = len(soup.find_all('div', class_='software-entry'))
        
        # Extract wins (look for prize badges)
        wins = len(soup.find_all('span', class_='winner'))
        
        # Extract project count
        projects = len(soup.find_all('article', class_='software'))
        
        return {
            'hackathons_participated': hackathons,
            'projects_submitted': projects,
            'wins': wins,
            'win_rate': round((wins / hackathons * 100), 1) if hackathons > 0 else 0,
        }
        
    except Exception as e:
        logger.error(f"Error analyzing Devpost: {e}")
        return {'error': str(e)}


def analyze_linkedin(linkedin_url):
    """
    LinkedIn - We DON'T scrape (against their TOS)
    Just validate and store the URL
    """
    try:
        # LinkedIn blocks scraping and it's against their Terms of Service
        # We just validate the URL and store it
        
        if 'linkedin.com' in linkedin_url:
            return {
                'profile_url': linkedin_url,
                'note': 'LinkedIn profile link (not scraped - respecting TOS)',
            }
        else:
            return {'error': 'Invalid LinkedIn URL'}
        
    except Exception as e:
        logger.error(f"Error validating LinkedIn: {e}")
        return {'error': str(e)}


def analyze_full_portfolio(github_url=None, linkedin_url=None, devpost_url=None, user_profile=None):
    """
    Analyze all profiles and generate comprehensive portfolio data
    
    user_profile: Optional dict with user's self-description for smarter analysis
    """
    portfolio = {
        'analyzed_at': datetime.now().isoformat(),
        'user_profile': user_profile or {},
        'github': {},
        'linkedin': {},
        'devpost': {},
        'career_assessment': {},
        'job_readiness': {},
        'skills_analysis': {},
        'journey': {},
        'overall_score': 0,
    }
    
    # Analyze GitHub with user profile
    if github_url:
        portfolio['github'] = analyze_github(github_url, user_profile)
        
        # Only run advanced analysis if GitHub data is available
        if not portfolio['github'].get('error'):
            try:
                # Import modules here to avoid circular imports
                from .career_assessor import CareerAssessor
                from .journey_extractor import JourneyExtractor
                from .ai_usage_categorizer import AIUsageCategorizer
                from .breakdown_calculator import BreakdownCalculator
                from .visualization_generator import VisualizationGenerator
                from .messaging_engine import MessagingEngine
                
                # Career Assessment
                assessor = CareerAssessor(portfolio['github'], user_profile or {})
                portfolio['career_assessment'] = assessor.assess_career_stage()
                portfolio['job_readiness'] = assessor.calculate_job_readiness()
                portfolio['skills_analysis'] = assessor.analyze_skill_proficiency()
                
                # Journey Extraction
                extractor = JourneyExtractor(portfolio['github'], user_profile or {})
                portfolio['journey'] = {
                    'timeline': extractor.build_timeline(),
                    'key_milestones': extractor.detect_milestones(),
                    'growth_metrics': extractor.calculate_growth_metrics(),
                    'narrative': extractor.generate_narrative()
                }
                
                # AI Usage Breakdown (NEW!)
                categorizer = AIUsageCategorizer(user_profile or {}, portfolio['github'])
                categorized_data = {
                    'categories': categorizer.categorize_by_task_type(),
                    'core_vs_supporting': categorizer.identify_core_vs_supporting()
                }
                
                calculator = BreakdownCalculator(categorized_data, user_profile or {})
                breakdown_data = calculator.calculate_category_breakdown()
                self_awareness = calculator.calculate_self_awareness_score()
                
                visualizer = VisualizationGenerator(breakdown_data)
                stacked_bar_data = visualizer.generate_stacked_bar_data()
                category_cards = visualizer.generate_category_cards()
                employer_summary = visualizer.generate_employer_summary()
                
                messenger = MessagingEngine(breakdown_data, user_profile or {})
                motivational_message = messenger.generate_motivational_message()
                improvement_suggestions = messenger.generate_improvement_suggestions()
                
                portfolio['ai_usage_breakdown'] = {
                    'overall': {
                        'ai_percentage': portfolio['github'].get('ai_code_percentage', 50),
                        'human_percentage': portfolio['github'].get('human_code_percentage', 50),
                        'assessment': breakdown_data.get('overall_assessment', 'smart_ai_user')
                    },
                    'core_vs_supporting': categorized_data['core_vs_supporting'],
                    'categories': breakdown_data.get('categories', []),
                    'category_cards': category_cards,
                    'stacked_bar_data': stacked_bar_data,
                    'self_awareness': self_awareness,
                    'employer_summary': employer_summary,
                    'motivational_message': motivational_message,
                    'improvement_suggestions': improvement_suggestions
                }
                
            except Exception as e:
                logger.error(f"Error in advanced analysis: {e}")
    
    # Analyze LinkedIn
    if linkedin_url:
        portfolio['linkedin'] = analyze_linkedin(linkedin_url)
    
    # Analyze Devpost
    if devpost_url:
        portfolio['devpost'] = analyze_devpost(devpost_url)
    
    # Calculate overall score
    score = 0
    if portfolio['github'].get('public_repos', 0) > 0:
        score += min(portfolio['github']['public_repos'] * 2, 50)
    if portfolio['github'].get('total_stars', 0) > 0:
        score += min(portfolio['github']['total_stars'] * 5, 30)
    if portfolio['devpost'].get('wins', 0) > 0:
        score += portfolio['devpost']['wins'] * 10
    
    # Use job readiness score if available
    if portfolio['job_readiness'].get('overall_score'):
        score = portfolio['job_readiness']['overall_score']
    
    portfolio['overall_score'] = min(score, 100)
    
    return portfolio
