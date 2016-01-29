Deployment
==========

In the example below, we're going to use the ``deploy.py`` tool to create an
API Gateway instance called ``irc-hooky`` and add a ``/github`` endpoint to
this API. We'll then deploy the IRC Hooky Lambda function and wire it all up!

Keep in mind that that the ``deploy.py`` tool was intended to be idempotent.
This means that it should not matter if you run it more than once. This also
means that these same instructions also apply to deploying **updated** versions
of IRC Hooky.

With all that, here are the base pre-requisites you'll need in order to get
going:

- AWS account + credentials
- Python 2.7.9+
- Virtualenv
- `lambda.zip`__
- `deploy.py`__

__ https://github.com/marvinpinto/irc-hooky/releases/latest
__ https://raw.githubusercontent.com/marvinpinto/irc-hooky/master/scripts/deploy.py

Save a copy of both ``lambda.zip`` and ``deploy.py`` in a local directory.

``deploy.py`` needs a few parameters set via environment variables, so let's do
that now:

.. code-block:: bash

    export AWS_ACCESS_KEY_ID="<YOUR AWS ACCESS KEY>"
    export AWS_SECRET_ACCESS_KEY="<YOUR AWS SECRET ACCESS KEY>"
    export AWS_DEFAULT_REGION="us-east-1"
    export LAMBDA_FUNCTION_NAME="irc-hooky"
    export REST_ENDPOINT_NAME="github"
    export IRCHOOKY_IRC_SERVER="chat.freenode.net"
    export IRCHOOKY_IRC_PORT="6667"
    export IRCHOOKY_IRC_CHANNEL="##testtest"

Do pay attention to the region and other parameters above and set them to
whatever works best for you.

Now let's create the virtualenv and install the dependencies we're going to
need:

.. code-block:: bash

    rm -rf deploy-env
    virtualenv deploy-env
    deploy-env/bin/pip install requests
    deploy-env/bin/pip install boto3

And the last thing we need to do here is wire everything up!

.. code-block:: bash

    deploy-env/bin/python deploy.py

And you're done! You should then see an output line that looks something like:

.. code-block:: text

    INFO:irchooky:IRC Hooky has been successfully deployed to: https://1234556x.execute-api.us-east-1.amazonaws.com/prod/github
