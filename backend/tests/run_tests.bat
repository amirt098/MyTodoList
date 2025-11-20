@echo off
REM Simple test runner script for Windows

echo Running Project End-to-End Tests...
echo ====================================
echo.

python manage.py test tests.test_project_e2e --verbosity=2

echo.
echo Tests completed!
pause

