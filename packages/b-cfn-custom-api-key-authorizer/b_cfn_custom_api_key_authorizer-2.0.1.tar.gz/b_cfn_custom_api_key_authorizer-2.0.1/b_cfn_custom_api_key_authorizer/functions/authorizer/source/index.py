import json
import logging
import os

# These imports come from a layer.
from api_keys_verification import ApiKeysVerification
from auth_exception import AuthException

from policy_document import PolicyDocument

# Allow extensive logging even with other file and other layer levels.
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
for handler in root_logger.handlers:
    handler.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info(f'Received event:\n{json.dumps(event)}.')

    # Custom authorizer resource specifies header/ApiKey attribute:
    # identity_source=['$request.header.ApiKey', '$request.header.ApiSecret'].
    # They are converted to lowercase by apigateway/lambda services.
    api_key = event.get('headers', {}).get('apikey')
    api_secret = event.get('headers', {}).get('apisecret')

    document = PolicyDocument(
        region=os.environ['AWS_REGION'],
        account_id=os.environ['AWS_ACCOUNT'],
        api_id=os.environ['AWS_API_ID'],
        api_key=api_key
    )

    logger.info('Attempting to verify api keys...')

    # Verify the authorization token.
    try:
        ApiKeysVerification(api_key, api_secret).verify()
        logger.info(f'Authentication succeeded for api key: {api_key}.')
        # Authorization was successful. Return "Allow".
        return document.create_policy_statement(allow=True)
    except AuthException as ex:
        # Log the error.
        logger.info(f'Authentication failed for api key: {api_key}. Message: {repr(ex)}.')
        # Authorization has failed. Return "Deny".
        return document.create_policy_statement(allow=False)
