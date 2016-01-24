Initial Lambda Setup
====================

This is where we're going to do all the work to setup the IRC Hooky Lambda
function for the first time. The good news here is that you will only need to
go through this once because updating the Lambda Function (for new releases) is
much simpler! (see :doc:`lambda_update`)


Preparation
-----------

Let's get started with a bit of prep-work. Set the following environment
variables which we'll use for all the subsequent steps.

.. code-block:: bash

    export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
    export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET KEY>
    export AWS_DEFAULT_REGION=us-east-1
    export LAMBDA_FUNCTION_NAME=irc-hooky


Lambda Basic Execution Role
---------------------------

Now let's create a Lambda Basic Execution IAM role which will give the Lambda
function all the basic permissions it needs (for logging, etc).

First, the policy for our Lambda role:

.. code-block:: bash

    aws iam create-policy \
        --policy-name "Lambda-Basic-Execution-Role-Policy" \
        --policy-document '{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
              ],
              "Resource": "arn:aws:logs:*:*:*"
            }
          ]
        }'

Take note of the ``Policy['Arn']`` value from the above command's output and
export it as an environment variable.

.. code-block:: bash

    export LAMBDA_BASIC_POLICY_ARN="arn:aws:iam..."

Now create the actual role itself:

.. code-block:: bash

    aws iam create-role \
        --role-name "Lambda-Basic-Execution-Role" \
        --assume-role-policy-document '{
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
        }'

Take note of the ``Role['Arn']`` value from the above command's output and
export it as an environment variable.

.. code-block:: bash

    export LAMBDA_BASIC_ROLE_ARN="arn:aws:iam..."

Now that we have both the policy and role in place, let's attach the policy to
the role:

.. code-block:: bash

    aws iam attach-role-policy \
        --role-name "Lambda-Basic-Execution-Role" \
        --policy-arn "$LAMBDA_BASIC_POLICY_ARN"

And that's it! We have a Lambda role and policy that will fit our needs just
fine. Let's move on to setting up the Lambda function.


Lambda Function
---------------

Before creating the Lambda function, head on over to `IRC Hooky Releases`__
page and download the the ``lambda.zip`` that corresponds to the most recent
release.

__ https://github.com/marvinpinto/irc-hooky/releases

Create the Lambda function in a 128MB container and a 10-second timeout.

.. code-block:: bash

    aws lambda create-function \
        --function-name "irc-hooky" \
        --runtime "python2.7" \
        --role "$LAMBDA_BASIC_ROLE_ARN" \
        --handler "irc_hooky.github.main" \
        --timeout 10 \
        --memory-size 128 \
        --publish \
        --zip-file "fileb://lambda.zip"

And that's it! You now have a fully deployed and working Lambda function!
