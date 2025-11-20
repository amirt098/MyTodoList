#!/bin/bash
# Simple test runner script

echo "Running Project End-to-End Tests..."
echo "===================================="
echo ""

python manage.py test tests.test_project_e2e --verbosity=2

echo ""
echo "Tests completed!"

