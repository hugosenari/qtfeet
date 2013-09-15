find ./ -name \*.pyc -delete &&
flake8 qtfeet tests &&
python dev_run.py -o '{"loglevel": "DEBUG"}'
