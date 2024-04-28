pytest ./tests || { echo 'Tests failed ... app launch cancelled' ; exit 1; }
python3 main.py
