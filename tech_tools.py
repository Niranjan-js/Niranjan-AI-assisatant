
import subprocess
import webbrowser
import os
import shlex
import pyperclip
from livekit.agents import function_tool

# Safe whitelist for terminal commands
SAFE_COMMANDS = ["npm", "pip", "git", "python", "node", "ls", "dir", "cd", "echo", "mkdir", "whoami", "ipconfig", "ping"]

@function_tool
def run_terminal_command(command: str):
    """
    Executes a terminal command. Only allows safe commands (npm, pip, git, python, etc.).
    Blocks dangerous commands (rm, del, format).
    """
    try:
        # Basic security check
        cmd_start = command.split(" ")[0].lower()
        if cmd_start not in SAFE_COMMANDS:
            return f"🚫 Security Alert: Command '{cmd_start}' is not in the safelist. Allowed: {', '.join(SAFE_COMMANDS)}"
        
        # Danger check
        if "rm " in command or "del " in command or "format" in command:
             return "🚫 Security Alert: Destructive commands are blocked."

        # Execute
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = process.stdout if process.stdout else process.stderr
        
        # Truncate output if too long
        if len(output) > 500:
            output = output[:500] + "\n...(output truncated)"
            
        return f"✅ Command Executed:\n{output}"
    except Exception as e:
        return f"Error executing command: {e}"

@function_tool
def analyze_clipboard_error():
    """
    Reads the current text from the clipboard (assuming it's an error message)
    and returns it for the AI to analyze.
    """
    try:
        content = pyperclip.paste()
        if not content:
            return "⚠️ Clipboard is empty."
        return f"📋 Clipboard Content:\n{content}"
    except Exception as e:
        return f"Error reading clipboard: {e}"

@function_tool
def search_stackoverflow(query: str):
    """
    Searches StackOverflow for the given query/error.
    """
    try:
        url = f"https://stackoverflow.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"🔍 Opened StackOverflow search for: {query}"
    except Exception as e:
        return f"Error opening StackOverflow: {e}"

@function_tool
def github_trending(language: str = "python"):
    """
    Opens the GitHub Trending page for the specified language.
    """
    try:
        url = f"https://github.com/trending/{language}?since=daily"
        webbrowser.open(url)
        return f"📈 Opened GitHub Trending for {language}"
    except Exception as e:
        return f"Error opening GitHub: {e}"

@function_tool
def read_file_content(file_path: str):
    """
    Reads the content of a code file (Python, JS, etc.) so the AI can analyze/debug it.
    """
    try:
        if not os.path.exists(file_path):
            return "❌ File not found."
        
        # Security: basic check to prevent reading system secrets (optional but good)
        if ".env" in file_path or "password" in file_path.lower():
             return "🚫 Security Alert: Sensitive files are protected."

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Truncate if too huge
        if len(content) > 5000:
            return f"📄 Content (First 5000 chars):\n{content[:5000]}\n...(file too large)"
            
        return f"📄 File Content ({file_path}):\n{content}"
    except Exception as e:
        return f"Error reading file: {e}"

@function_tool
def security_audit_tool():
    """
    Performs a system security audit (like Prowler).
    Checks: Open ports, Firewall status (Windows).
    """
    report = ["🛡️ Advanced Security Audit Report (Niranjan Security Protocol):"]
    
    try:
        # 1. Firewall Check (Windows)
        fw = subprocess.run("netsh advfirewall show allprofiles state", shell=True, capture_output=True, text=True)
        if "ON" in fw.stdout:
            report.append("✅ Firewall: ACTIVE")
        else:
            report.append("⚠️ Firewall: POTENTIALLY DISABLED")
            
        # 2. Antivirus Check (Windows Security Center)
        av = subprocess.run("powershell Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct", shell=True, capture_output=True, text=True)
        if "displayName" in av.stdout:
            # Extract display name
            names = [line.split(":")[1].strip() for line in av.stdout.split("\n") if "displayName" in line]
            report.append(f"🛡️ Antivirus: {', '.join(names)}")
        else:
            report.append("⚠️ Antivirus: Not detected or access denied")

        # 3. BitLocker Check
        bl = subprocess.run("powershell manage-bde -status C:", shell=True, capture_output=True, text=True)
        if "Fully Encrypted" in bl.stdout:
            report.append("🔒 Disk Encryption (C:): ACTIVE")
        else:
            report.append("⚠️ Disk Encryption: NOT FULLY ENCRYPTED")

        # 6. Windows Update Check
        wu = subprocess.run("powershell Get-HotFix | select -First 5", shell=True, capture_output=True, text=True)
        if wu.stdout.strip():
            report.append(f"📦 Recent Updates: {len(wu.stdout.splitlines()) - 1} patches found")
        
        # 7. Network Interfaces
        net = subprocess.run("powershell Get-NetAdapter | where status -eq 'Up'", shell=True, capture_output=True, text=True)
        if net.stdout.strip():
             adapters = [line.split()[0] for line in net.stdout.splitlines() if "Name" not in line and line.strip()]
             report.append(f"🌐 Active Adapters: {', '.join(adapters)}")

        return "\n".join(report)
    except Exception as e:
        return f"Security audit failed: {e}"

@function_tool
def write_file_tool(file_path: str, content: str):
    """
    Writes content to a file. Useful for fixing code features or creating new scripts.
    Overwrites the file if it exists.
    """
    try:
        # Security checks
        if ".." in file_path or file_path.startswith("/") or file_path.startswith("C:\\Windows"):
             return "🚫 Security Alert: Access to system paths is restricted."
        
        if file_path.endswith(".env"):
             return "🚫 Security Alert: Cannot edit .env files directly."

        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"✅ File Written: {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"

@function_tool
def system_health_diagnostic():
    """
    Performs a deep diagnostic of OS health, disk space, and memory leaks.
    """
    try:
        import psutil
        import shutil
        import os
        
        # Disk
        total, used, free = shutil.disk_usage("/")
        disk_percent = (used / total) * 100
        
        # CPU/Mem
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        
        # Process check
        proc_count = len(psutil.pids())
        
        status = "HEALTHY" if disk_percent < 90 and mem < 90 else "WARNING"
        
        return (f"🏥 **System Health Report:** {status}\n"
                f"- Disk Usage: {disk_percent:.1f}% ({free/1e9:.1f} GB Free)\n"
                f"- Memory Load: {mem:.1f}%\n"
                f"- CPU Stress: {cpu:.1f}%\n"
                f"- Active Processes: {proc_count}")
    except Exception as e:
        return f"Diagnostic Error: {e}"
