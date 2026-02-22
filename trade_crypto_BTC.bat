@echo off
title Athena Crypto Scheduler

cd /d D:\MyWorkspace\AthenaProjectV2\app

call ..\venv\Scripts\activate.bat

python -m portfolios.crypto_port.scheduler
