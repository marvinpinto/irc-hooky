Welcome to IRC Hooky!
=====================

IRC Hooky makes it easy to send custom webhook-triggered notifications to IRC
using an entirely serverless architecture.

Using a combination of `AWS Lambda`__ and `API Gateway`__, listening for and
delivering webhooks could cost pennies per month compared to an actual server
and all the maintenance that comes with it.

The Lambda and API Gateway **pay-only-for-what-you-use** model seems to fit
perfectly for this use case!

The blog post `Using a Serverless Architecture to deliver IRC Webhook
Notifications`__ talks a bit more about the *why* of IRC Hooky and explains
some of the design decisions behind it. I encourage you to read it!

__ https://aws.amazon.com/lambda
__ https://aws.amazon.com/api-gateway
__ https://disjoint.ca/posts/2016/02/28/using-a-serverless-architecture-to-deliver-irc-webhook-notifications

Features
--------

- :doc:`GitHub webhook events <github>`
- :doc:`Hashicorp Atlas notifications <atlas>`

More Info
---------

This website covers the project information for IRC Hooky such as installation,
development, and so forth.

Please use `GitHub Issues`__ for filing bug or feature requests, and `Pull
Requests`__ for submitting code patches.

__ https://github.com/marvinpinto/irc-hooky/issues
__ https://github.com/marvinpinto/irc-hooky/pulls

----

Have a look through the left sidebar to get started, and thank you for checking
this out!

.. toctree::
   :hidden:
   :maxdepth: 2

   overview
   deployment
   github
   atlas
   faq
   Home Page <https://disjoint.ca>
