API Gateway Setup
=================

This section might come across as a bit intense, what will all the copy-pasta
and all but I assure you it will be well worth it!

The good news is that you will only need to go through this once (for each
endpoint) as updating the Lambda Function for new releases is much simpler!
(see :doc:`lambda_update`)


Preparation
-----------

Let's get started with a bit of prep-work. Set the following environment
variables which we'll use for all the subsequent steps.

.. code-block:: bash

    export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
    export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET KEY>
    export AWS_DEFAULT_REGION=us-east-1
    export LAMBDA_FUNCTION_ARN=<YOUR LAMBDA FUNCTION ARN>

Note that if you don't have the ARN for your Lambda function handy, you should
be able to find it using the following:

.. code-block:: bash

    aws lambda list-functions


API Gateway Setup
-----------------

Let's get started by creating a new API Gateway instance.

.. code-block:: bash

    aws apigateway create-rest-api \
        --name irc-hooky-api

Take note of the ``id`` value from the above command's output and export it as
an environment variable.

.. code-block:: bash

    export REST_API_ID="..."

Use the following to get all the Resource IDs and make note of root's (``/``)
resource ID.

.. code-block:: bash

    aws apigateway get-resources \
        --rest-api-id "$REST_API_ID"

Take note of the ``items[0]['id']`` value from the above command's output and
export it as an environment variable.

.. code-block:: bash

    export REST_ROOT_RESOURCE_ID="..."

Create a ``/github`` Resource endpoint:

.. code-block:: bash

    aws apigateway create-resource \
        --rest-api-id "$REST_API_ID" \
        --parent-id "$REST_ROOT_RESOURCE_ID" \
        --path-part "github"

Take note of the ``id`` value from the above command's output and export it as
an environment variable.

.. code-block:: bash

    export REST_GITHUB_RESOURCE_ID="..."

Now that we have a ``/github`` endpoint, let's make sure that we can accept
POST requests on it.

.. code-block:: bash

    aws apigateway put-method \
        --rest-api-id "$REST_API_ID" \
        --resource-id "$REST_GITHUB_RESOURCE_ID" \
        --http-method "POST" \
        --authorization-type "none"

Awesome! Let's recap where we're at:

- We have an API Gateway instance configured and ready to use
- We've created a ``/github`` endpoint that is ready to accept POST requests

The next thing we have to do here is to have API Gateway trigger the Lambda
function every time we receive a POST request on the ``/github`` endpoint.

Moving on.

One of the things that API Gateway will need to do is to pass in a few
parameters into the Lambda function. API Gateway accomplishes this with a
`mapping template`__. In our case, the mapping template will need to look
something like:

.. code-block:: json

    {
        "X-Hub-Signature": $input.params().header.get("X-Hub-Signature"),
        "X-Github-Event": $input.params().header.get("X-Github-Event"),
        "gh-payload": $input.json("$")
    }

__ http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html

Since the ``put-integration`` sub-command only accepts strings, the mapping
template above needs to be converted and supplied into the
``request-templates`` parameter as follows:

.. code-block:: bash

    aws apigateway put-integration \
        --region "$AWS_DEFAULT_REGION" \
        --rest-api-id "$REST_API_ID" \
        --resource-id "$REST_GITHUB_RESOURCE_ID" \
        --http-method "POST" \
        --integration-http-method "POST" \
        --type "AWS" \
        --uri "arn:aws:apigateway:${AWS_DEFAULT_REGION}:lambda:path/2015-03-31/functions/${LAMBDA_FUNCTION_ARN}/invocations" \
        --request-templates '{
            "application/json": "{ \"X-Hub-Signature\": \"$input.params().header.get(\"X-Hub-Signature\")\", \"X-Github-Event\": \"$input.params().header.get(\"X-Github-Event\")\", \"gh-payload\": $input.json(\"$\") }"
        }'

With that in place, the next thing we need to do here is to create a 200 method
response:

.. code-block:: bash

    aws apigateway put-method-response \
        --region "$AWS_DEFAULT_REGION" \
        --rest-api-id "$REST_API_ID" \
        --resource-id "$REST_GITHUB_RESOURCE_ID" \
        --http-method "POST" \
        --status-code 200 \
        --response-models '{"application/json":"Empty"}'

And then return that 200 back to the caller:

.. code-block:: bash

    aws apigateway put-integration-response \
        --region "$AWS_DEFAULT_REGION" \
        --rest-api-id "$REST_API_ID" \
        --resource-id "$REST_GITHUB_RESOURCE_ID" \
        --http-method "POST" \
        --status-code 200 \
        --response-templates '{"application/json": ""}'


API Gateway Deployment
----------------------

Let's recap where we are at:

- All the needed roles are in place for the Lambda function
- Our Lambda function is deployed and ready to go
- API Gateway is configured and ready to hit the button

The last two things we need to do here are to give API Gateway permission to
execute our Lambda function, and then deploy our API!

Let's get started. First, let's give API gateway the permission it needs in
order to invoke the Lambda function.

.. code-block:: bash

    aws lambda add-permission \
        --region "$AWS_DEFAULT_REGION" \
        --function-name "$LAMBDA_FUNCTION_ARN" \
        --statement-id "$(cat /proc/sys/kernel/random/uuid)" \
        --action "lambda:*" \
        --principal "apigateway.amazonaws.com"

And now create a `deployment stage`__ called ``prod`` and deploy our API to it!

__ http://docs.aws.amazon.com/apigateway/latest/developerguide/stages.html

.. code-block:: bash

    aws apigateway create-deployment \
        --region "$AWS_DEFAULT_REGION" \
        --rest-api-id "$REST_API_ID" \
        --stage-name "prod"

And that should be it! Your new Lambda-backed API should be available at:

.. code-block:: bash

    echo "https://${REST_API_ID}.execute-api.${AWS_DEFAULT_REGION}.amazonaws.com/prod"

You should be able to test it with a POST request with something like:

.. code-block:: bash

    curl -X POST \
        -d '{"hello": "hi"}' \
        https://${REST_API_ID}.execute-api.${AWS_DEFAULT_REGION}.amazonaws.com/prod/github
