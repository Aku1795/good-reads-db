pytest ./tests || { echo 'tests failed not launching app' ; exit 1; }
python3 main.py