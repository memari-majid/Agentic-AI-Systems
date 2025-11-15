#!/usr/bin/env python3
"""
Test script for the update agent - runs a quick validation without heavy API calls
"""

import os
import sys
from pathlib import Path

def test_environment():
    """Test that environment is set up correctly."""
    print("🧪 Testing Update Agent Environment\n")
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OPENAI_API_KEY is set")
        print(f"   Key prefix: {api_key[:10]}...")
    else:
        print("❌ OPENAI_API_KEY is not set")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
        return False
    
    # Check required files
    required_files = [
        'scripts/update_agent.py',
        'arxiv-paper/SEARCH-PROMPTS-FOR-IMPROVEMENT.md',
        'README.md',
    ]
    
    print("\n📁 Checking required files:")
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            return False
    
    # Check dependencies
    print("\n📦 Checking dependencies:")
    required_modules = [
        'openai',
        'requests',
        'aiohttp',
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - NOT INSTALLED")
            print(f"   Install with: pip install {module}")
            return False
    
    return True


def test_search_prompts():
    """Test loading search prompts."""
    print("\n🔍 Testing search prompts loading:")
    
    prompts_file = Path('arxiv-paper/SEARCH-PROMPTS-FOR-IMPROVEMENT.md')
    if not prompts_file.exists():
        print("❌ Prompts file not found")
        return False
    
    with open(prompts_file, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        prompts = [line.split('**Prompt**:')[1].strip().strip('"') 
                  for line in lines if line.strip().startswith('**Prompt**:')]
    
    print(f"✅ Loaded {len(prompts)} search prompts")
    print(f"   First prompt: {prompts[0][:60]}...")
    
    return True


def quick_api_test():
    """Quick OpenAI API test."""
    print("\n🤖 Testing OpenAI API connection:")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Simple API test
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Reply with just 'OK'"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API connection successful")
        print(f"   Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Update Agent Test Suite")
    print("=" * 60)
    
    tests = [
        ("Environment Setup", test_environment),
        ("Search Prompts", test_search_prompts),
        ("OpenAI API", quick_api_test),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! You can run the full update agent:")
        print("   python scripts/update_agent.py")
    else:
        print("\n⚠️  Some tests failed. Fix the issues above before running the agent.")
        sys.exit(1)


if __name__ == '__main__':
    main()

