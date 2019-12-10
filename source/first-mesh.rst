First Mesh Walkthrough
======================
In this walkthrough, we will go through the process of creating a new and fairly minimal slow controls system.
We will try to call attention to places where decisions made here are for convenience of example, vs decisions recommended practice.

Our first big decision comes before we get started and is a question of how we will deploy and manage our software.
In this example, we will use ``docker-compose`` to define and deploy our collection of applications.
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

ToDo Notes:
+++++++++++

#. Add content for a very simple service, probably our classic key-value store thing
#. Demo that you can get and set it using exec
#. Demo that you can see sensor logs with dl-monitor


Add historical data storage
---------------------------

ToDo Notes:
+++++++++++

#. Create a postgres service in the compose (with volume & initialization directory)
#. Create an ``endpoint_id_map`` table, an ``endpoints_logs_double`` table, an ``endpoint_values`` view
#. *Stretch:* Add a view that combines data types and resolves inserts to the correct tables.
#. Create a sensor-logger service to record sensor values into the above
#. can we just enable and use annonymous access (and add a comment on the lack of security)?


Add historical data visualizer
------------------------------
If historical storage of data is out-of-scope for dripline, then visualization of historical data is obviously more so.
Nevertheless, a control system is not very useful unless it is easy to quickly view and understand the information being collected.
For most use cases, we recommend leveraging third-party, open-source, solutions, as they tend to be much easier to manage and much more powerful than custom solutions (unless you have significant human resources to throw at the problem).
Here, we use `grafana <https://grafana.com>`_

ToDo Notes:
+++++++++++

#. Create a grafana service

   #. configure to enable anyonmyous login? (or simple/default user/password)
   #. configure provisioning for datasource pointing to postgres above

#. Go through interactively creating a dashboard to plot one sensor's time series & a table of aggregate values
   #. Export and add the dashboard to the provisioning system
