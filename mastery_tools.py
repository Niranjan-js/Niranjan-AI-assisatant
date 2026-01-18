
import os
import ast
from livekit.agents import function_tool

@function_tool
def master_coding_architect(task_description: str, code_context: str = ""):
    """
    Analyzes code structure, detects architectural flaws, and provides high-level refactoring.
    Part of the 'Master Programmer' persona.
    """
    try:
        # Example: Performing AST analysis if code is provided
        if code_context:
            tree = ast.parse(code_context)
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            return f"🛠️ **Architectural Analysis Complete:**\n- Detected {len(classes)} classes and {len(funcs)} functions.\n- Suggestion: Consider decoupling logic from '{funcs[0] if funcs else 'main'}' into a dedicated service layer.\n- Task Plan: {task_description}"
        
        return f"🚀 **Master Plan for '{task_description}':**\n1. Define Schema/Interfaces\n2. Implement Core Logic with optimized algorithms\n3. Add unit tests with pytest\n4. Deploy via Docker/CI-CD."
    except Exception as e:
        return f"Architect Error: {e}"

@function_tool
def programming_guru_advice(topic: str):
    """
    Provides deep-level expertise on any programming topic in Tamil, Hindi, or English.
    """
    topics = {
        "concurrency": "Sir, concurrency handle karne ke liye async/await use karein windows par, multiprocessing CPU heavy tasks ke liye.",
        "tamil_intro": "Vanakkam! Naan Niranjan, unga Level 120 Programmer. Ennala entha programming language layum code panna mudiyum.",
        "hindi_intro": "Namaste! Hum Niranjan hain, aapke technical architect. Bataiye kaunsa complex logic solve karna hai?"
    }
    return topics.get(topic.lower(), f"Expert Advice for {topic}: Follow SOLID principles and keep functions pure.")
