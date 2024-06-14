# intelligent-request-collector

**Prerequisites**
```
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

**AWS Console Setup**
1) Create a bucket with default policies, make note of the name
2) Go to SES and verify the identity of the email address you will be sending to/from
3) *ou must enable Claude Sonnet Model Access on AWS Console.

**Set your access information**
_You can obtain this from your AWS Apps Portal._
```
export AWS_ACCESS_KEY_ID={REDACT}
export AWS_SECRET_ACCESS_KEY={REDACT}
export AWS_SESSION_TOKEN={REDACT}
```

**Create a .env file**

_Create a .env file with the appropriate values. BUCKET_NAME and FROM_EMAIL are the only required ones; region name should default to us-east-1._
```
REGION_NAME=""
BUCKET_NAME=""
FROM_EMAIL=""
DYNAMODB_TABLE_NAME=""
```

**Run it**

`streamlit run main.py`