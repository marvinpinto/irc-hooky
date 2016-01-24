Lambda Function Updates
=======================

**Scenario**: There is an new version of IRC Hooky released and you want to get
all up in that goodness. What do you do?!


First head over to the `IRC Hooky Releases`__ page and download the
``lambda.zip`` that corresponds to the most recent release.

Then set the following environment variables pertaining to `aws cli`__.

.. code-block:: bash

    export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
    export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET KEY>
    export AWS_DEFAULT_REGION=us-east-1
    export LAMBDA_FUNCTION_NAME=irc-hooky

Finally update and deploy the new version of the Lambda function!

.. code-block:: bash

    aws lambda update-function-code \
        --region "$AWS_DEFAULT_REGION" \
        --function-name "$LAMBDA_FUNCTION_NAME" \
        --publish \
        --zip-file "fileb://lambda.zip"

__ https://github.com/marvinpinto/irc-hooky/releases
__ https://aws.amazon.com/cli
