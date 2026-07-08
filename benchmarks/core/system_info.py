"""
System Information for Benchmark Reproducibility.
"""

import platform
import subprocess
import psutil
from typing import Dict, Any

def get_git_commit() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    except Exception:
        return "unknown"

def get_system_info() -> Dict[str, Any]:
    """Capture environmental information for reproducibility."""
    
    cpu_info = "unknown"
    try:
        if platform.system() == "Windows":
            cpu_info = subprocess.check_output(["wmic", "cpu", "get", "name"]).decode().split("\n")[1].strip()
        elif platform.system() == "Darwin":
            cpu_info = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
        elif platform.system() == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        cpu_info = line.split(":")[1].strip()
                        break
    except Exception:
        cpu_info = platform.processor()

    ram_total = psutil.virtual_memory().total / (1024 ** 3)  # GB
    
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "python_version": platform.python_version(),
        "cpu": cpu_info,
        "ram_gb": round(ram_total, 2),
        "git_commit": get_git_commit()
    }
