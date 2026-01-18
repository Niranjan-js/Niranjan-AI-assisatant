
import os
from livekit.agents import function_tool

@function_tool
def generate_prp_tool(task_name: str, requirement_desc: str):
    """
    Generates a Product Requirement Prompt (PRP) blueprint for a complex coding task.
    Inspired by 'Wirasm/PRPs-agentic-eng'.
    Includes: Context, Patterns, and Execution plan.
    """
    prp_content = f"""# PRP: {task_name}
## Context
- Primary Files: [Auto-selected based on task]
- Dependencies: Python 3.10+, LiveKit
- Architecture: Agentic Sub-modules

## Requirement
{requirement_desc}

## Implementation Patterns
- Use @function_tool for all new capabilities.
- Implement robust try-except blocks.
- Follow PEP8 styling.

## Validation Plan
1. Run local unit test.
2. Verify integration in agent.py.
3. Live session check.
"""
    # Create PRPs directory if not exists
    prp_dir = "PRPs"
    if not os.path.exists(prp_dir):
        os.makedirs(prp_dir)
    
    file_path = os.path.join(prp_dir, f"{task_name.lower().replace(' ', '_')}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(prp_content)
        
    return f"🚀 PRP Generated: {file_path}\nUse this blueprint for a 'vertical slice' implementation of the feature."

@function_tool
def execute_prp_tool(prp_path: str):
    """
    Reads a PRP blueprint and initiates the autonomous coding flow to implement it.
    """
    if not os.path.exists(prp_path):
        return f"❌ Error: PRP file not found at {prp_path}"
        
    with open(prp_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Analysis of the PRP logic
    requirement = content.split('## Requirement')[1].split('##')[0].strip()
    
    analysis = "🔬 **Master Programmer Technical Analysis:**\n"
    if "scrape" in requirement.lower():
        analysis += "- Recommend using `BeautifulSoup` or `Selenium` for JS-heavy sites.\n- Pattern: Singleton Scraper Instance.\n"
    elif "db" in requirement.lower() or "database" in requirement.lower():
        analysis += "- Use `SQLAlchemy` ORM for type safety.\n- Pattern: Repository Pattern.\n"
    
    return f"🛠️ **PRP Execution Started:**\n- Task: {requirement}\n{analysis}"
