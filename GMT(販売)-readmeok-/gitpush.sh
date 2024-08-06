#!/bin/bash

# 変数設定
COMMIT_MESSAGE="Your commit message"
BRANCH_NAME="main"

# Gitコマンドの実行
echo "Adding changes to git..."
git add .

echo "Committing changes..."
git commit -m "$COMMIT_MESSAGE"

echo "Pushing to GitHub..."
git push origin "$BRANCH_NAME"

echo "Done!"
