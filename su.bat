@echo off

rem 管理者権限を持ったコマンドプロンプトを起動
rem 実行側のコマンドプロンプトは終了
rem 作業フォルダは引き継ぐ

rem 必要ファイル
rem 無し

powershell start-process -FilePath cmd -ArgumentList '/c wt -d ""%CD%"" -p CommandPrompt' -verb runas
\
rem exit
