Demo
====

The spirit of this demo is for you to get a feel for IRC Hooky without
investing any time in setting it up and deploying it yourself.

It basically works as follows:

- Add the **demo** endpoint URL as a webhook to your application of choice (e.g. Atlas or Github)

- Send some relevant events (Pull Requests, Deployments, etc)

- Sign in to the ``#irchooky`` channel on Freenode__ and and watch for your
  event notifications!

__ https://webchat.freenode.net

Sound good?

Okay, here's what you need to know.

Endpoint URL
------------

The API Gateway base URL for the demo application is:

.. code-block:: text

    https://accti8wx4f.execute-api.us-east-1.amazonaws.com/prod

You will need to append the feature-specific endpoint to the URL. E.g.

.. code-block:: text

    https://accti8wx4f.execute-api.us-east-1.amazonaws.com/prod/github

for GitHub events, `/atlas` for Hashicorp Atlas events, and so on.

And that's it! I would love to hear any feedback you may have on how to improve
this or make it easier for folks!

More Info
---------

If you would like more information on how this endpoint is setup, have a look
at the ``deploy-demo`` target in the Makefile__. It essentially follows the
same procedure outlined in the :doc:`deployment <deployment>` instructions.

__ https://github.com/marvinpinto/irc-hooky/blob/master/Makefile
