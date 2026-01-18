
import os
import re
from livekit.agents import function_tool

# --- Global Knowledge Repositories (Simulation) ---
KNOWLEDGE_HUB_DIR = "knowledge_hub"

class SkillManager:
    """
    Manages the 'Master Programmer' skills. 
    Actually scans the project directory for files containing @function_tool.
    """
    @staticmethod
    def discover_skills():
        skills = []
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        for file in os.listdir(project_dir):
            if file.endswith("_tools.py") or file == "agent.py" or file == "skills_manager.py":
                path = os.path.join(project_dir, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Simple regex to find function tool names
                        matches = re.findall(r'@function_tool\ndef\s+(\w+)', content)
                        if matches:
                            skills.append({
                                "module": file,
                                "functions": matches
                            })
                except:
                    pass
        return skills

@function_tool
def list_available_skills():
    """
    Lists all integrated AI facilities by scanning the project for @function_tool decorators.
    Shows the 'Master Programmer' awareness of its own abilities.
    """
    discovered = SkillManager.discover_skills()
    if not discovered:
        return "💡 No additional skills detected in current modules."
    
    report = "💡 **Niranjan v3.0 Integrated Capabilities:**\n"
    for item in discovered:
        funcs = ", ".join([f"`{f}`" for f in item['functions']])
        report += f"- **{item['module']}**: {funcs}\n"
        
    return report

@function_tool
def publish_to_knowledge_hub(title: str, content: str):
    """
    Publishes content to the internal knowledge portal (CMS inspired by Wagtail).
    """
    if not os.path.exists(KNOWLEDGE_HUB_DIR):
        os.makedirs(KNOWLEDGE_HUB_DIR)
        
    filename = f"{title.lower().replace(' ', '_')}.md"
    path = os.path.join(KNOWLEDGE_HUB_DIR, filename)
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nPublished on: {os.path.getctime(KNOWLEDGE_HUB_DIR)}\n\n{content}")
        return f"📝 Article Published: {KNOWLEDGE_HUB_DIR}\\{filename}"
    except Exception as e:
        return f"Wagtail publishing error: {e}"
