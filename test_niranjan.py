
import asyncio
from advanced_tools import shop_online_tool, play_media_tool, coding_agent_tool, download_file_tool

async def test_tools():
    print("--- Testing Niranjan Tools ---")
    
    # 1. Test Shopping (should open browser)
    print("\n1. Testing Shop Online...")
    res = shop_online_tool("iPhone 15", "amazon")
    print(f"Result: {res}")
    
    # 2. Test Media (should open browser/youtube)
    print("\n2. Testing Media Player...")
    res = play_media_tool("Niranjan AI Theme")
    print(f"Result: {res}")
    
    # 3. Test Coding Agent (should create folder)
    print("\n3. Testing Coding Agent...")
    res = coding_agent_tool("Test_Project_Niranjan", "Create a simple calculator")
    print(f"Result: {res}")
    
    print("\n--- Tests Completed ---")

if __name__ == "__main__":
    asyncio.run(test_tools())
