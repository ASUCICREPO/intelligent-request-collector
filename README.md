# intelligent-request-collector

** setup **
```
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

**You must enable Claude Sonnet Model Access on AWS Console.**

** execution **
```
export AWS_ACCESS_KEY_ID={REDACT}
export AWS_SECRET_ACCESS_KEY={REDACT}
export AWS_SESSION_TOKEN={REDACT}

streamlit run main.py
```

**Sample .env**
```
REGION_NAME=""
BUCKET_NAME=""
DYNAMODB_TABLE_NAME=""
```