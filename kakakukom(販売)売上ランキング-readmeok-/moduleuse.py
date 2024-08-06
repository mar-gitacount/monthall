import subprocess
import sys

def install_missing_module(error_message):
    # "No module named 'xyz'" というエラーメッセージからモジュール名を抽出
    prefix = "No module named '"
    if prefix in error_message:
        module_name = error_message.split(prefix)[1].split("'")[0]
        print(f"Detected missing module: {module_name}. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            print(f"Module '{module_name}' installed successfully.")
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to install '{module_name}'.")
    return False