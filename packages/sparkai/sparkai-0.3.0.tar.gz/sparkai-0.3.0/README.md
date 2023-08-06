# sparkai-python-client

The official [SparkAI](https://www.spark.ai) Python client

## Installation

$ pip install --upgrade sparkai

## Usage

```
import sparkai.SparkAIClient
client = SparkAIClient('PROVIDED_API_KEY')
url = https://picsum.photos/200/300
instructions = 'Annotate any object in the photo'
token = client.create_engagement_from_image_url(url, instructions=instructions)
```

### Validating webhook signature

```
client.validate_webhook_secret(request_secret_header, request_body, self_secret)
```

- `request_secret_header`: the whole header Spark-Signature sent with the webhook request
- `request_body`: the whole JSON object body sent witth the webhook request
- `self_secret`: customer's webhook token

Returns True if the signature is valid
