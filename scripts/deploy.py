import os
import sys
import logging
import boto3
import botocore.exceptions
import json
import requests
import time

logging.basicConfig()
logging.captureWarnings(True)


class DeployIRCHooky(object):

    def __init__(self):
        self.log = logging.getLogger("irchooky")
        self.log.setLevel(logging.DEBUG)

    def validate_env_vars(self):
        env_vars = [
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'AWS_DEFAULT_REGION',
            'LAMBDA_FUNCTION_NAME',
            'REST_ENDPOINT_NAME',
            'IRCHOOKY_IRC_SERVER',
            'IRCHOOKY_IRC_PORT',
            'IRCHOOKY_IRC_CHANNEL'
        ]
        for var in env_vars:
            if not os.environ.get(var):
                self.log.error("Could not find environment variable %s" % var)
                sys.exit(1)
        self.lambda_func_name = os.environ['LAMBDA_FUNCTION_NAME']
        self.rest_endpoint_name = os.environ['REST_ENDPOINT_NAME']
        self.region = os.environ['AWS_DEFAULT_REGION']
        self.irc_server = os.environ['IRCHOOKY_IRC_SERVER']
        self.irc_port = os.environ['IRCHOOKY_IRC_PORT']
        self.irc_channel = os.environ['IRCHOOKY_IRC_CHANNEL']

    def create_lambda_policy(self):
        policy_name = "%s-lambda-basic-execution-role-policy" % self.lambda_func_name  # NOQA
        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                        "sns:Publish",
                        "sns:Subscribe"
                    ],
                    "Resource": [
                        "arn:aws:logs:*:*:*",
                        "arn:aws:sns:*"
                    ]
                }
            ]
        }
        client = boto3.client('iam')
        self.lambda_policy_arn = ""
        try:
            response = client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_doc)
            )
            self.lambda_policy_arn = response['Policy']['Arn']
            self.log.info("Policy %s successfully created." % self.lambda_policy_arn)  # NOQA
        except botocore.exceptions.ClientError:
            self.log.info("Policy %s already exists, searching for ARN" % policy_name)  # NOQA
            response = client.list_policies(Scope='Local')
            for policy in response['Policies']:
                if policy['PolicyName'] == policy_name:
                    self.lambda_policy_arn = policy['Arn']
                    self.log.info("Lambda Policy ARN found: %s" % self.lambda_policy_arn)  # NOQA
            if not self.lambda_policy_arn:
                self.log.error("Could not find Lambda policy ARN, manual cleanup needed.")  # NOQA
                sys.exit(1)

    def create_lambda_role(self):
        self.lambda_role_name = "%s-lambda-basic-execution-role" % self.lambda_func_name  # NOQA
        role_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        client = boto3.client('iam')
        self.lambda_role_arn = ""
        try:
            response = client.create_role(
                RoleName=self.lambda_role_name,
                AssumeRolePolicyDocument=json.dumps(role_doc)
            )
            self.lambda_role_arn = response['Role']['Arn']
            self.log.info("Role %s successfully created." % self.lambda_role_arn)  # NOQA
        except botocore.exceptions.ClientError:
            self.log.info("Role %s already exists, searching for ARN" % self.lambda_role_name)  # NOQA
            response = client.list_roles()
            for role in response['Roles']:
                if role['RoleName'] == self.lambda_role_name:
                    self.lambda_role_arn = role['Arn']
                    self.log.info("Lambda Role ARN found: %s" % self.lambda_role_arn)  # NOQA
            if not self.lambda_role_arn:
                self.log.error("Could not find Lambda role ARN, manual cleanup needed")  # NOQA
                sys.exit(1)

    def attach_lambda_role_policy(self):
        client = boto3.client('iam')
        client.attach_role_policy(
            RoleName=self.lambda_role_name,
            PolicyArn=self.lambda_policy_arn
        )

    def create_lambda_function(self):
        client = boto3.client('lambda')
        self.lambda_function_arn = ""
        encoded_zip = None
        try:
            with open("./lambda.zip", 'rb') as f:
                encoded_zip = f.read()
        except IOError as e:
            self.log.error(e)
            sys.exit(1)

        # If the function does not exist, create it. If it does exist, update
        # its code and configuration.
        response = client.list_functions()
        for function in response['Functions']:
            if function['FunctionName'] == self.lambda_func_name:
                self.lambda_function_arn = function['FunctionArn']
                self.log.info("Lambda Function ARN found: %s" % self.lambda_function_arn)  # NOQA

        if not self.lambda_function_arn:
            # function does not exist
            response = client.create_function(
                FunctionName=self.lambda_func_name,
                Runtime="python2.7",
                Role=self.lambda_role_arn,
                Handler="irc_hooky/entrypoint.handler",
                Timeout=60,
                MemorySize=128,
                Publish=True,
                Code={'ZipFile': encoded_zip}
            )
            self.lambda_function_arn = response['FunctionArn']
            self.log.info("Function %s successfully created." % self.lambda_function_arn)  # NOQA
            return

        # function already exists so update its configuration
        self.log.info("Function %s already exists, updating configuration." % self.lambda_func_name)  # NOQA
        response = client.update_function_configuration(
            FunctionName=self.lambda_func_name,
            Role=self.lambda_role_arn,
            Handler="irc_hooky/entrypoint.handler",
            Timeout=60,
            MemorySize=128
        )

        # Then update the function code
        self.log.info("Updating Lambda function code for %s." % self.lambda_func_name)  # NOQA
        response = client.update_function_code(
            FunctionName=self.lambda_func_name,
            ZipFile=encoded_zip,
            Publish=True
        )

    def wire_sns_notifications(self):
        self.log.info("Wiring up Lambda SNS subscriptions")
        client = boto3.client('sns')
        response = client.create_topic(Name=self.lambda_func_name)
        self.sns_topic_arn = response['TopicArn']
        client.subscribe(
            TopicArn=self.sns_topic_arn,
            Protocol="lambda",
            Endpoint=self.lambda_function_arn
        )

    def sns_lambda_permission(self):
        client = boto3.client('lambda')
        try:
            client.add_permission(
                FunctionName=self.lambda_function_arn,
                StatementId="%s-sns-lambda-permission-id" % self.lambda_func_name,  # NOQA
                Action="lambda:*",
                Principal="sns.amazonaws.com"
            )
            self.log.info("SNS -> Lambda permissions added")
        except botocore.exceptions.ClientError:
            self.log.info("SNS -> Lambda permissions already in place")

    def create_api_gateway(self):
        client = boto3.client('apigateway')
        response = client.get_rest_apis()
        self.rest_api_id = ""
        self.rest_api_root_resource_id = ""

        for item in response['items']:
            if item['name'] == self.lambda_func_name:
                self.rest_api_id = item['id']
                self.log.info("Found existing API Gateway instance: %s" % self.rest_api_id)  # NOQA

        if not self.rest_api_id:
            response = client.create_rest_api(name=self.lambda_func_name)
            self.rest_api_id = response['id']
            self.log.info("Created new API Gateway instance: %s" % self.rest_api_id)  # NOQA

        response = client.get_resources(restApiId=self.rest_api_id)
        for item in response['items']:
            if item['path'] == "/":
                self.rest_api_root_resource_id = item['id']

    def create_api_gateway_endpoint(self):
        client = boto3.client('apigateway')
        self.rest_endpoint_resource_id = ""

        response = client.get_resources(restApiId=self.rest_api_id)
        for item in response['items']:
            if item.get('pathPart') == self.rest_endpoint_name:
                self.log.info("Found existing endpoint for %s" % self.rest_endpoint_name)  # NOQA
                self.rest_endpoint_resource_id = item['id']

        if not self.rest_endpoint_resource_id:
            self.log.info("Creating new %s endpoint" % self.rest_endpoint_name)
            response = client.create_resource(
                restApiId=self.rest_api_id,
                parentId=self.rest_api_root_resource_id,
                pathPart=self.rest_endpoint_name
            )
            self.rest_endpoint_resource_id = response['id']

    def accept_post_requests_on_endpoint(self):
        client = boto3.client('apigateway')
        try:
            client.put_method(
                restApiId=self.rest_api_id,
                resourceId=self.rest_endpoint_resource_id,
                httpMethod="POST",
                authorizationType="NONE"
            )
            self.log.info("Setup the new endpoint to accept POST requests")
        except botocore.exceptions.ClientError:
            self.log.info("POST method already exists for this endpoint")

    def api_gateway_input_mapping_tamplate(self):
        client = boto3.client('apigateway')
        t = []
        t.append("{\"X-Hub-Signature\": \"$input.params().header.get('X-Hub-Signature')\"")  # NOQA
        t.append("\"X-Github-Event\": \"$input.params().header.get('X-Github-Event')\"")  # NOQA
        t.append("\"resource-path\": \"$context.resourcePath\"")
        t.append("\"irc-server\": \"${stageVariables.irc_server}\"")
        t.append("\"irc-port\": \"${stageVariables.irc_port}\"")
        t.append("\"irc-channel\": \"${stageVariables.irc_channel}\"")
        t.append("\"irchooky-sns-arn\": \"${stageVariables.irchooky_sns_arn}\"")  # NOQA
        t.append("\"payload\": $input.json('$')}")
        uri = "arn:aws:apigateway:%s:lambda:path/2015-03-31/functions/%s/invocations" % (self.region, self.lambda_function_arn)  # NOQA
        client.put_integration(
            restApiId=self.rest_api_id,
            resourceId=self.rest_endpoint_resource_id,
            httpMethod="POST",
            integrationHttpMethod="POST",
            uri=uri,
            type="AWS",
            requestTemplates={"application/json": ",".join(t)}
        )
        self.log.info("Input request mapping template complete")

    def api_gateway_method_response(self):
        client = boto3.client('apigateway')
        try:
            client.put_method_response(
                restApiId=self.rest_api_id,
                resourceId=self.rest_endpoint_resource_id,
                httpMethod="POST",
                statusCode="200",
                responseModels={"application/json": "Empty"}
            )
            self.log.info("200 Method response creation successful")
        except botocore.exceptions.ClientError:
            self.log.info("200 Method response already exists, nothing to do")

    def api_gateway_integration_response(self):
        client = boto3.client('apigateway')
        client.put_integration_response(
            restApiId=self.rest_api_id,
            resourceId=self.rest_endpoint_resource_id,
            httpMethod="POST",
            statusCode="200",
            responseTemplates={"application/json": ""}
        )
        self.log.info("200 integration response creation successful")

    def api_gateway_lambda_permission(self):
        client = boto3.client('lambda')
        try:
            client.add_permission(
                FunctionName=self.lambda_function_arn,
                StatementId="%s-lambda-permission-id" % self.lambda_func_name,
                Action="lambda:*",
                Principal="apigateway.amazonaws.com"
            )
            self.log.info("API Gateway -> Lambda permissions added")
        except botocore.exceptions.ClientError:
            self.log.info("API Gateway -> Lambda permissions already in place")

    def deploy_api_gateway(self):
        client = boto3.client('apigateway')
        gateway_vars = {
            "irc_server": self.irc_server,
            "irc_port": self.irc_port,
            "irc_channel": self.irc_channel,
            "irchooky_sns_arn": self.sns_topic_arn
        }
        client.create_deployment(
            restApiId=self.rest_api_id,
            variables=gateway_vars,
            stageName="prod"
        )
        self.log.info("API Gateway successfully deployed!")

    def get_api_gateway_url(self):
        url = "https://%s.execute-api.%s.amazonaws.com/prod" % (self.rest_api_id, self.region)  # NOQA
        return url

    def test_gateway_endpoint(self):
        endpoint = "%s/%s" % (self.get_api_gateway_url(), self.rest_endpoint_name)  # NOQA
        self.log.info("IRC Hooky has been successfully deployed to: %s" % endpoint)  # NOQA
        payload = {"foo": "bar"}
        r = requests.post(endpoint, data=json.dumps(payload))
        if r.status_code == requests.codes.ok:
            self.log.info("Sending a POST request to the %s endpoint resulted in: %s" % (self.rest_endpoint_name, r.text))  # NOQA
        else:
            self.log.error("There was an error communicating with: %s" % endpoint)  # NOQA
            self.log.error("Response status code: %s" % r.status_code)
            self.log.error("Response headers: %s" % r.headers)
            self.log.error("Response output: %s" % r.text)
            sys.exit(1)


if __name__ == "__main__":
    dpl = DeployIRCHooky()
    dpl.validate_env_vars()
    dpl.create_lambda_policy()
    dpl.create_lambda_role()
    dpl.attach_lambda_role_policy()
    time.sleep(5)                     # Wait for role policy to take effect before creating lambda function,
                                      # see https://stackoverflow.com/a/37438525/305559
    dpl.create_lambda_function()
    dpl.wire_sns_notifications()
    dpl.sns_lambda_permission()
    dpl.create_api_gateway()
    dpl.create_api_gateway_endpoint()
    dpl.accept_post_requests_on_endpoint()
    dpl.api_gateway_input_mapping_tamplate()
    dpl.api_gateway_method_response()
    dpl.api_gateway_integration_response()
    dpl.api_gateway_lambda_permission()
    dpl.deploy_api_gateway()
    dpl.test_gateway_endpoint()
