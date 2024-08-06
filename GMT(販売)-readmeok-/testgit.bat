@echo off
REM 変数設定
set COMMIT_MESSAGE="Your commit message"
set BRANCH_NAME=main

REM Gitコマンドの実行
@REM echo Adding changes to git...
git add .

echo Committing changes...
git commit -m %COMMIT_MESSAGE%

echo Pushing to GitHub...
git push origin %BRANCH_NAME%

echo Done!