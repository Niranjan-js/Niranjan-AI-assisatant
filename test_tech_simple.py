
import subprocess
import webbrowser
import os
import pyperclip

# --- Mocking Logic ---
SAFE_COMMANDS = ["npm", "pip", "git", "python", "node", "ls", "dir", "cd", "echo", "mkdir", "whoami", "ipconfig", "ping"]

def run_terminal_command(command: str):
    try:
        cmd_start = command.split(" ")[0].lower()
        if cmd_start not in SAFE_COMMANDS:
            return f"🚫 Security Alert: Command '{cmd_start}' is not in the safelist. Allowed: {', '.join(SAFE_COMMANDS)}"
        
        if "rm " in command or "del " in command or "format" in command:
             return "🚫 Security Alert: Destructive commands are blocked."

        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = process.stdout if process.stdout else process.stderr
        
        if len(output) > 500:
            output = output[:500] + "\n...(output truncated)"
            
        return f"✅ Command Executed:\n{output}"
    except Exception as e:
        return f"Error executing command: {e}"

def search_stackoverflow(query: str):
    try:
        url = f"https://stackoverflow.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"🔍 Opened StackOverflow search for: {query}"
    except Exception as e:
        return f"Error opening StackOverflow: {e}"

def github_trending(language: str = "python"):
    try:
        url = f"https://github.com/trending/{language}?since=daily"
        webbrowser.open(url)
        return f"📈 Opened GitHub Trending for {language}"
    except Exception as e:
        return f"Error opening GitHub: {e}"

if __name__ == "__main__":
    print("--- Running Tech Tools Logic Verification ---")
    print(run_terminal_command("echo Hello Niranjan"))
    print(run_terminal_command("del system32")) # Should fail
    print(search_stackoverflow("AttributeError: NoneType object has no attribute"))
    print(github_trending("python"))
    print("--- Verified ---")
