@echo off
echo Restarting Celery Worker...

REM Kill existing celery processes
taskkill /F /IM celery.exe 2>nul
timeout /t 2 /nobreak >nul

REM Start worker
cd backend
start cmd /k "celery -A task_queue.celery_app worker --loglevel=info --concurrency=3 --pool=solo --queues=audio_processing,cluster_jobs,analytics --hostname=worker@%%h"

echo Worker restarted!
echo Check the new window for worker logs.
