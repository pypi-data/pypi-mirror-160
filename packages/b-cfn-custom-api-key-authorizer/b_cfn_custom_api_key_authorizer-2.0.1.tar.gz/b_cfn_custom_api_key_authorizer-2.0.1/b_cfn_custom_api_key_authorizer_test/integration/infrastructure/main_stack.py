from aws_cdk.aws_apigatewayv2 import CfnApi, CfnStage
from aws_cdk.core import Construct
from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack

from b_cfn_custom_api_key_authorizer.custom_authorizer import ApiKeyCustomAuthorizer
from b_cfn_custom_api_key_authorizer_test.integration.infrastructure import authorized_endpoint_stack


class MainStack(TestingStack):
    API_ENDPOINT = 'ApiEndpoint'
    AUTHORIZER_FUNCTION = 'AuthorizerFunction'
    DELETER_FUNCTION = 'DeleterFunction'
    EXISTS_FUNCTION = 'ExistsFunction'
    GENERATOR_FUNCTION = 'GeneratorFunction'
    VALIDATOR_FUNCTION = 'ValidatorFunction'

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope=scope)

        prefix = TestingStack.global_prefix()

        self.api = CfnApi(
            scope=self,
            id='Api',
            name=f'{prefix}Api',
            description='Sample description.',
            protocol_type='HTTP',
            cors_configuration=CfnApi.CorsProperty(
                allow_methods=['GET', 'PUT', 'POST', 'OPTIONS', 'DELETE'],
                allow_origins=['*'],
                allow_headers=[
                    'Content-Type',
                    'Authorization'
                ],
                max_age=300
            )
        )

        self.authorizer = ApiKeyCustomAuthorizer(
            scope=self,
            resource_name_prefix=prefix,
            api=self.api,
        )

        self.stage: CfnStage = CfnStage(
            scope=self,
            id='Stage',
            stage_name='test',
            api_id=self.api.ref,
            auto_deploy=True,
        )

        self.endpoint_stack = authorized_endpoint_stack.AuthorizedEndpointStack(self, self.api, self.authorizer)
        self.dummy_endpoint = f'{self.api.attr_api_endpoint}/{self.stage.stage_name}/{self.endpoint_stack.path}'

        self.add_output(self.API_ENDPOINT, value=self.dummy_endpoint)
        self.add_output(self.AUTHORIZER_FUNCTION, value=self.authorizer.authorizer_function.function_name)
        self.add_output(self.DELETER_FUNCTION, value=self.authorizer.deleter_function.function_name)
        self.add_output(self.EXISTS_FUNCTION, value=self.authorizer.exists_function.function_name)
        self.add_output(self.GENERATOR_FUNCTION, value=self.authorizer.generator_function.function_name)
        self.add_output(self.VALIDATOR_FUNCTION, value=self.authorizer.validator_function.function_name)
