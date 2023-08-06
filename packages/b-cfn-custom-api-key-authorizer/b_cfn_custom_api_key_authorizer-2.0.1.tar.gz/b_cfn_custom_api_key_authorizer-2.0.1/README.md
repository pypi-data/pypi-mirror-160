# B.CfnCustomApiKeyAuthorizer

![Pipeline](https://github.com/Biomapas/B.CfnCustomApiKeyAuthorizer/workflows/Pipeline/badge.svg?branch=master)

An AWS CDK resource that enables protection of your public APIs by 
using Api Keys (ApiKey and Secret).

### Description

This custom authorizer enables Api Key functionality 
(something similar to ApiGateway V1 version: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-setup-api-key-with-console.html)

APIs created via ApiGateway V2 do not have Api Key authorization functionality out-of-the-box. 
If you want to protect your V2 API by generating a secret key and giving only for the 
intended clients - this library is just for you. This library allows you to protect you
ApiGatewayV2-based endpoints with a combination of ApiKey and ApiSecret. Refer to usages & examples 
to understand how to use this library. 

The authorizer library exposes these lambda functions that can be called directly:
- `authorizer` - _ApiKeysAuthorizerFunction_ - used by a custom (this) authorizer that is attached to your API.
- `deleter` - _ApiKeysDeleterFunction_ - allows revoking access to your API i.e. deletes api keys.
- `exists` - _ApiKeysExistsFunction_ - allows you to check whether a given API key exists in the database.
- `generator` - _ApiKeysGeneratorFunction_ - generates api key and api secret pair and saves in an internal database.
- `validator` - _ApiKeysValidatorFunction_ - validates given api key and api secret against the ones in the database.

### Remarks

[Biomapas](https://www.biomapas.com/) aims to modernise life-science industry by sharing its IT knowledge with other
companies and the community. This is an open source library intended to be used by anyone. Improvements and pull
requests are welcome.

### Related technology

- Python3
- AWS CDK
- AWS CloudFormation
- AWS API Gateway
- AWS API Gateway Authorizer
- AWS Lambda

### Assumptions

This project assumes you are an expert in infrastructure-as-code via AWS CloudFormation and AWS CDK. You must clearly
understand how AWS API Gateway endpoints are protected with Authorizers / Custom Authorizers and how it is managed via
CloudFormation or CDK.

- Excellent knowledge in IaaC (Infrastructure as a Code) principles.
- Excellent knowledge in API Gateway, Authorizers.
- Good experience in AWS CDK and AWS CloudFormation.
- Good Python skills and basics of OOP.

### Useful sources

- AWS CDK:<br>https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html
- AWS CloudFormation:<br>https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html
- API Gateway with
  CloudFormation:<br>https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
- AWS Custom
  Authorizers:<br>https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html

### Install

Before installing this library, ensure you have these tools setup:

- Python / Pip
- AWS CDK

To install this project from source run:

```
pip install .
```

Or you can install it from a PyPi repository:

```
pip install b-cfn-custom-api-key-authorizer
```

### Usage & Examples

Firstly, create an api and stage:

```python
from aws_cdk.aws_apigatewayv2 import CfnApi, CfnStage

api = CfnApi(...)
api_stage = CfnStage(...)
```

Create api key custom authorizer:

```python
from b_cfn_custom_api_key_authorizer.custom_authorizer import ApiKeyCustomAuthorizer

authorizer = ApiKeyCustomAuthorizer(
    scope=Stack(...),
    resource_name_prefix='MyCool',
    api=api,
)
```

Use that authorizer to protect your routes (endpoints):

```python
from aws_cdk.aws_apigatewayv2 import CfnRoute

route = CfnRoute(
    scope=Stack(...),
    id='DummyRoute',
    api_id=api.ref,
    route_key='GET /dummy/endpoint',
    authorization_type='CUSTOM',
    target=f'integrations/{integration.ref}',
    authorizer_id=authorizer.ref
)
```

Once your infrastructure is deployed, try calling your api endpoint. You will get "Unauthorized" error.

```python
import urllib3

response = urllib3.PoolManager().request(
    method='GET',
    url='https://your-api-url/dummy/endpoint',
    headers={},
)

>>> response.status
>>> 401
```

Create `ApiKey` and `ApiSecret` by invoking a dedicated api keys generator lambda function:

```python
# Your supplied prefix for the infrastrucutre.
resource_name_prefix = 'MyCool'
# Created generator lambda function name.
function_name = 'ApiKeysGeneratorFunction'
# Full function name is a combination of both.
function_name = resource_name_prefix + function_name

response = boto3.client('lambda').invoke(
    FunctionName=function_name,
    InvocationType='RequestResponse',
)

response = json.loads(response['Payload'].read())
api_key = response['ApiKey']
api_secret = response['ApiSecret']
```

Now try calling the same api with api keys:

```python
import urllib3

response = urllib3.PoolManager().request(
    method='GET',
    url='https://your-api-url/dummy/endpoint',
    headers={
        'ApiKey': api_key,
        'ApiSecret': api_secret
    },
)

>>> response.status
>>> 200
```

#### Exposed lambda functions

The authorizer exposes these lambda functions that can be called directly:
- `authorizer` - ApiKeysAuthorizerFunction
  
```python
response = boto3.client('lambda').invoke(
    FunctionName=prefix + 'ApiKeysAuthorizerFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'ApiKey': '123',
        'ApiSecret': '123'
    }).encode()
)

response = json.loads(response['Payload'].read())

# This will contain a dictionary of IAM based 
# permission either to "allow" or "deny" the request.
print(response)
```

- `deleter` - ApiKeysDeleterFunction
  
```python
# This does not produce a response.
boto3.client('lambda').invoke(
    FunctionName=prefix + 'ApiKeysDeleterFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'ApiKey': '123',
    }).encode()
)
```

- `exists` - ApiKeysExistsFunction
  
```python
response = boto3.client('lambda').invoke(
    FunctionName=prefix + 'ApiKeysExistsFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'ApiKey': '123',
    }).encode()
)

response = json.loads(response['Payload'].read())

# Check whether your ApiKey/Secret exists in the database.
assert response['Exists'] is True
```

- `generator` - ApiKeysGeneratorFunction
  
```python
response = boto3.client('lambda').invoke(
    FunctionName=prefix + 'ApiKeysGeneratorFunction',
    InvocationType='RequestResponse',
)

response = json.loads(response['Payload'].read())

api_key = response['ApiKey']
api_secret = response['ApiSecret']
```

- `validator` - ApiKeysValidatorFunction

```python
response = boto3.client('lambda').invoke(
    FunctionName=prefix + 'ApiKeysValidatorFunction',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'ApiKey': '123',
        'ApiSecret': '123',
    }).encode()
)

response = json.loads(response['Payload'].read())

# Check whether your ApiKey/Secret is valid.
assert response['Valid'] is True
```

### Testing

This package has integration tests based on **pytest**. To run tests simply run:

```

pytest b_cfn_custom_api_key_authorizer_test/integration/tests

```

### Contribution

Found a bug? Want to add or suggest a new feature? Contributions of any kind are gladly welcome. You may contact us
directly, create a pull-request or an issue in github platform. Lets modernize the world together.
