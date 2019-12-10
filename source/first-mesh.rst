First Mesh Walkthrough
======================
In this walkthrough, we will go through the process of creating a new and fairly minimal slow controls system.
We will try to call attention to places where decisions made here are for convenience of example, vs decisions recommended practice.

Our first big decision comes before we get started and is a question of how we will deploy and manage our software.
In this example, we will use `docker-compose` to define and deploy our collection of applications.
If you're not familiar with compose, please review the `official documentation <https://docs.docker.com/compose/gettingstarted/>`_ and work through the examples there.
You should also be familiar with `exec <https://docs.docker.com/compose/reference/exec/>`_ and `logs <https://docs.docker.com/compose/reference/logs/>`_ subcommands, all of these will be useful throughout this guide.

If you are working through this walkthrough, you're strongly encouraged to create a directory and write all of the files yourself, exploring the options or configurable parameters, etc.
For reference, you can find the complete set 


Configure the message broker
----------------------------
The core to any dripline mesh is the AMQP message broker.
In principle, dripline-compliant messages could be sent over any transport protocol you want, but in practice all available libraries are written for, and tested with AMQP (specifically RabbitMQ), so you should probably just use that.
We'll set the username and password for the default role in RabbitMQ, to be used by all of our services.
In principle, RabbitMQ provides interesting and sophisticated role-based access controls features which could be leveraged, but this is not currently done.
This is done with the following service block in the docker-compose file:

.. literalinclude:: ../examples/first-mesh/docker-compose.yaml
   :caption: docker-compose.yaml
   :language: yaml
   :lines: 3-9
   :linenos:
   :lineno-start: 3

In order for services to connect to the broker, they will need to authenticate using the username and password indicated above.
The dripline libraries typically retrieve this information from an authentications file, we'll go ahead and create that now:

.. literalinclude:: ../examples/first-mesh/authentications.json
   :language: json
   :caption: authentications.json
   :name: authentications-file
   :linenos:


Add a dripline service
----------------------
Now that we have a broker running, we will go ahead and create our first service.

