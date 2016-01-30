GitHub Webhooks
===============

GitHub has a full featured webhook system that's able to notify you of a `wide
variety`__ of events. IRC Hooky supports the following subset:

- `Issues`__
- `Pull Request`__

__ https://developer.github.com/webhooks/#events
__ https://developer.github.com/v3/activity/events/types/#issuesevent
__ https://developer.github.com/v3/activity/events/types/#pullrequestevent

This page will walk you through setting up webhooks on a GitHub repository and
getting related notifications in IRC.

To start off with, if you haven't already done so, create a ``/github``
endpoint in your API Gateway instance following the :doc:`deployment
<deployment>` instructions.

Your API Gateway webhook URL should look something like:

.. code-block:: text

    https://xxxxxxx.execute-api.us-east-1.amazonaws.com/prod/github

To bring up the webhooks settings page, navigate over to:

.. code-block:: text

    https://github.com/<USERNAME>/<REPOSITORY>/settings/hooks/new

And fill in the following fields:

============  ============
Payload URL   https://xxxxxxx.execute-api.us-east-1.amazonaws.com/prod/github
Content Type  ``application/json``
Secret        *blank*
Which events  Send me **everything**
Active        *checkmark*
============  ============

Click the green **Add webhook** button and you're done!
