@echo off
title Athena Trend Port

cd /d D:\MyWorkspace\AthenaProjectV2\app

call ..\venv\Scripts\activate.bat

python -m portfolios.trend_port.main