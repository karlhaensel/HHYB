@echo off

if "%1"=="cov" goto coverage
if "%1"=="pre" goto pre_commit

echo Unknown command: %1
goto end

:coverage
coverage run -m pytest
coverage report
coverage html
goto end

:pre_commit
pre-commit run --all-files
goto end

:end
