Frequently Asked Questions
==========================

An implicit requirement here is that you are somewhat familiar with AWS and
HTTP in general. Do feel free to reach out if you have any specific questions
and I'll do my best!


Is there a hosted version of IRC Hooky I could use instead?
-----------------------------------------------------------

There very well might be! But unfortunately this isn't it. The complexity of
adding user & account management on top of IRC Hooky isn't in the scope of this
project.


What options do I have besides deploy.py?
-----------------------------------------

You are than welcome to use `AWS console`__, `aws cli`__, or any tool that you
are more comfortable with.

__ https://console.aws.amazon.com/console
__ https://aws.amazon.com/cli

The reasoning behind ``deploy.py`` versus writing out the instructions manually
is because the latter got unweildy fast. Iterating on an environment where one
has to copy/paste commands into a terminal window got cumbersome and I decided
to write a python tool to take care of that aspect.

You should be able to glean all the information you need from ``deploy.py`` and
plug that back into your tool of choice.

For an idea of what the *manual* instructions previously looked like, have a look
at `this commit`__.

__ https://github.com/marvinpinto/irc-hooky/commit/eb5e7fc7769ce2dfc4d1c8f5db1e9eedff8a3f70


Where do I report bugs?
-----------------------

It would be awesome if you could open up a `Github Issue`__ with as much detail
as you can provide. Then we can talk it through and see what needs doing!

__ https://github.com/marvinpinto/irc-hooky/issues


How do I contribute to IRC Hooky?
---------------------------------

`Pull Requests`__ work best here. If you need my help with a new feature get a
hold of me (`Marvin Pinto`__) and I'll help you out!

__ https://github.com/marvinpinto/irc-hooky/pulls
__ https://www.disjoint.ca/page/about
