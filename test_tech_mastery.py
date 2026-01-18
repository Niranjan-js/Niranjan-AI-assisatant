
import asyncio
from tech_tools import run_terminal_command, search_stackoverflow, github_trending

async def test_tech_tools():
    print("--- Testing Tech Mastery Tools ---")
    
    # 1. Test Safe Terminal Command
    print("\n1. Testing 'dir' command...")
    res = run_terminal_command("dir")
    print(f"Result (truncated): {res[:200]}...")

    # 2. Test Blocked Command
    print("\n2. Testing 'rm' command (should be blocked)...")
    res = run_terminal_command("rm -rf folder")
    print(f"Result: {res}")

    # 3. Test StackOverflow
    print("\n3. Testing StackOverflow Search...")
    res = search_stackoverflow("Python recursive recursiondepth exceeded")
    print(f"Result: {res}")
    
    # 4. Test GitHub Trending
    print("\n4. Testing GitHub Trending...")
    res = github_trending("javascript")
    print(f"Result: {res}")

    print("\n--- Tests Completed ---")

if __name__ == "__main__":
    asyncio.run(test_tech_tools())
