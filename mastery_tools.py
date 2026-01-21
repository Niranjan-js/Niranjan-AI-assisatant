
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
@function_tool
def master_ecommerce_builder(store_name: str, niche: str = "Electronics"):
    """
    Advanced Industry-Level E-commerce Site Generator.
    Creates a full-stack feel UI with Dark Mode, Glassmorphism, and responsive grid.
    """
    try:
        import subprocess
        base_path = os.path.join(os.path.expanduser("~"), "Documents", "Niranjan_Ecommerce_Projects", store_name.lower().replace(" ", "_"))
        if not os.path.exists(base_path): os.makedirs(base_path)
        
        # Premium CSS with Glassmorphism and Animations
        css = """
        :root { --primary: #3cc8ff; --bg: #0a0e14; --glass: rgba(20, 35, 50, 0.8); }
        body { margin: 0; background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .nav { display: flex; justify-content: space-between; padding: 20px 50px; background: var(--glass); backdrop-filter: blur(10px); sticky; top: 0; z-index: 100; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .hero { height: 80vh; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #1a2a3a, #0a0e14); text-align: center; }
        .hero h1 { font-size: 4rem; margin-bottom: 10px; color: var(--primary); text-shadow: 0 0 20px rgba(60,200,255,0.4); }
        .products { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; padding: 50px; }
        .card { background: var(--glass); border-radius: 20px; padding: 20px; transition: transform 0.3s; border: 1px solid rgba(255,255,255,0.05); }
        .card:hover { transform: translateY(-10px); border-color: var(--primary); }
        .card img { width: 100%; border-radius: 15px; background: #1a2a3a; height: 200px; object-fit: cover; }
        .btn { background: var(--primary); color: #000; border: none; padding: 12px 25px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn:hover { box-shadow: 0 0 20px var(--primary); transform: scale(1.05); }
        """
        
        html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8"><title>{store_name} | Premium {niche}</title>
            <link rel="stylesheet" href="style.css">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
        </head>
        <body>
            <nav class="nav"><h2>{store_name}</h2><div>Cart (0)</div></nav>
            <section class="hero">
                <div><h1>{store_name}</h1><p>Luxury {niche} for the Modern Era.</p><br><button class="btn">Explore Collection</button></div>
            </section>
            <section class="products">
                {' '.join([f'<div class="card"><img><h3>Premium Product {i}</h3><p>Elite performance and design.</p><br><button class="btn">$999</button></div>' for i in range(1, 9)])}
            </section>
        </body></html>"""
        
        with open(os.path.join(base_path, "index.html"), "w", encoding="utf-8") as f: f.write(html)
        with open(os.path.join(base_path, "style.css"), "w", encoding="utf-8") as f: f.write(css)
        
        # Sync with VS Code
        subprocess.Popen(["code", base_path], shell=True)
        return f"✅ **E-commerce Platform '{store_name}' Created!**\n- Location: {base_path}\n- Design: Premium Glassmorphism\n- Status: Synced with VS Code."
    except Exception as e:
        return f"Ecommerce Builder Error: {e}"
