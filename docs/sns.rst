SNS Topic Setup
===============

Let's get started with a bit of prep-work. Set the following environment
variables which we'll use for all the subsequent steps.

.. code-block:: bash

    export AWS_ACCESS_KEY_ID=<YOUR AWS ACCESS KEY>
    export AWS_SECRET_ACCESS_KEY=<YOUR AWS SECRET KEY>
    export AWS_DEFAULT_REGION=us-east-1
    LAMBDA_FUNCTION_ARN="<YOUR LAMBDA FUNCTION ARN>"

Note that if you don't have the ARN for your Lambda function handy, you should
be able to find it using the following:

.. code-block:: bash

    aws lambda list-functions

Create a new SNS topic called ``irc-hooky``. We'll use this topic as the
trigger for the asynchronous invocations.

.. code-block:: bash

    aws sns create-topic \
        --name "irc-hooky"

Take note of the ``TopicArn`` value from the above command's output and export
it as an environment variable.

.. code-block:: bash

    SNS_TOPIC_ARN="arn:aws:sns..."

Now subscribe the Lambda function you created to this SNS topic:

.. code-block:: bash

    aws sns subscribe \
        --topic-arn "$SNS_TOPIC_ARN" \
        --protocol lambda \
        --notification-endpoint "$LAMBDA_FUNCTION_ARN"
