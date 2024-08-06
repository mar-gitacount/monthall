import subprocess
# アップロード時に実行
# Gitコマンドを実行する関数
def run_git_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

# コミットメッセージ
commit_message = "Your commit message"

# ブランチ名
branch_name = "main"

# コマンドのリスト
commands = [
    ["git", "add", "."],
    ["git", "commit", "-m", commit_message],
    ["git", "push", "origin", branch_name]
]

# 各コマンドを実行
for command in commands:
    run_git_command(command)
