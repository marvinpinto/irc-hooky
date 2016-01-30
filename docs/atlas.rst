Atlas Notifications
===================

Atlas is able to send out webhook notifications for Consul Alerts, Packer
Builds, and Terraform Runs. IRC Hooky supports the following subset:

- `Packer Builds`__
- `Terraform Runs`__

__ https://atlas.hashicorp.com/help/packer/builds/notifications
__ https://atlas.hashicorp.com/help/terraform/runs/notifications

This page will walk you through setting up webhook notifications in your Atlas
account globally.

To start off with, if you haven't already done so, create an ``/atlas``
endpoint in your API Gateway instance following the :doc:`deployment
<deployment>` instructions.

Your API Gateway webhook URL should look something like:

.. code-block:: text

    https://xxxxxxx.execute-api.us-east-1.amazonaws.com/prod/atlas

To bring up the webhooks settings page, navigate over to:

.. code-block:: text

    https://atlas.hashicorp.com/settings/organizations/<USERNAME>/configuration

In the **Notification Methods** section, set the **Webhook URL** value to:

.. code-block:: text

    https://xxxxxxx.execute-api.us-east-1.amazonaws.com/prod/atlas

Click the green **Save** button.

Now within the **Integrations** settings for a project, you should be able to
check/uncheck the notification events that you would like to receive.
