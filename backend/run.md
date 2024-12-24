
# Run with virtualenv on ubuntu

## prepare virtual environment
``` bash
virtualenv -p /usr/bin/python3.8 venv
source venv/bin/activate
python3.8 -m pip install -r requirements.txt
```

## Run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000





