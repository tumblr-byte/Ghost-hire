"""
Quick test to verify AI code analyzer works
"""
from haunted_profiles.portfolio_analyzer import analyze_github

# Test with a real GitHub profile
test_url = "https://github.com/torvalds"  # Linus Torvalds as example

print("🔍 Testing AI Code Analyzer...")
print(f"Analyzing: {test_url}\n")

result = analyze_github(test_url)

if 'error' in result:
    print(f"❌ Error: {result['error']}")
else:
    print("✅ Analysis Complete!\n")
    print(f"Username: {result['username']}")
    print(f"Public Repos: {result['public_repos']}")
    print(f"Original Repos: {result['original_repos']}")
    print(f"Total Stars: {result['total_stars']}")
    print(f"\n🤖 AI Code Analysis:")
    print(f"AI Code: {result.get('ai_code_percentage', 'N/A')}%")
    print(f"Human Code: {result.get('human_code_percentage', 'N/A')}%")
    print(f"Smart AI User: {result.get('smart_ai_user', False)}")
    print(f"\n📊 Usage Summary:")
    for point in result.get('ai_usage_summary', []):
        print(f"  {point}")
    print(f"\n💻 Top Languages:")
    for lang in result.get('skills', [])[:5]:
        print(f"  - {lang}")
