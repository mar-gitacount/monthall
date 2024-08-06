@echo off
setlocal enabledelayedexpansion

:: Conda 環境をアクティベート
CALL conda activate myenv

:: Python スクリプトを実行し、stdout と stderr を error.log にキャプチャ
python scriping.py > error.log 2>&1

:: Python スクリプトの実行結果をチェック
if %errorlevel% == 0 (
    echo Python スクリプトが正常に完了しました。
    goto end
)

:: エラー処理
echo エラーが発生しました。不足しているモジュールをチェックしています...
set /p error=<error.log

:: エラーメッセージを解析して特定のエラーを探す
echo !error! | findstr /C:"No module named" > nul
if not errorlevel 1 (
    set modulename=!error:*named =!
    set modulename=!modulename:'=!
    echo 不足しているモジュールをインストールします: !modulename!
    python -m pip install !modulename!
    goto run_python
)

echo 関連するエラーが見つからないか、モジュール名が解析できませんでした。
pause
goto end

:run_python
python scripting.py > error.log 2>&1
if %errorlevel% == 0 (
    echo モジュールをインストールした後、Python スクリプトが正常に完了しました。
) else (
    echo モジュールを試みた後も Python スクリプトが失敗しました。
)
pause

:end
echo バッチスクリプトを終了します。
endlocal
