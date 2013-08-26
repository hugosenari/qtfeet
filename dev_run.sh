find ./ -name \*.pyc -delete &&
flake8 qtfeet tests &&
python -m unittest tests.test_qtfeet &&
python -m qtfeet -o '{"loglevel": "DEBUG"}'

