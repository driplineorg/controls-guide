First Mesh Walkthrough
======================
In this walkthrough, we will go through the process of creating a new and fairly minimal slow controls system.
We will try to call attention to places where decisions made here are for convenience of example, vs decisions recommended practice.

Our first big decision comes before we get started and is a question of how we will deploy and manage our software.
In this example, we will use ``docker-compose`` to define and deploy our collection of applications.
If you're not familiar with compose, please review the `official documentation <https://docs.docker.com/compose/gettingstarted/>`_ and work through the examples there.
You should also be familiar with `exec <https://docs.docker.com/compose/reference/exec/>`_ and `logs <https://docs.docker.com/compose/reference/logs/>`_ subcommands, all of these will be useful throughout this guide.

If you are working through this walkthrough, you're strongly encouraged to create a directory and write all of the files yourself, exploring the options or configurable parameters, etc.
For reference, you can find a completed set of files for this example in the `github repo for this documentation <https://github.com/driplineorg/controls-guide/tree/master/examples/first-mesh>`_.


Configure the message broker
----------------------------
The core to any dripline mesh is the AMQP message broker.
In principle, dripline-compliant messages could be sent over any transport protocol you want, but in practice all available libraries are written for, and tested with AMQP (specifically RabbitMQ), so you should probably just use that.
We'll set the username and password for the default role in RabbitMQ, to be used by all of our services.
In principle, RabbitMQ provides interesting and sophisticated role-based access controls features which could be leveraged, but this is not currently done.
This is done with the following service block in the docker-compose file:

.. literalinclude:: ../../examples/first-mesh/docker-compose.yaml
   :caption: docker-compose.yaml
   :language: yaml
   :lines: 3-9
   :linenos:
   :lineno-start: 3

In order for services to connect to the broker, they will need to authenticate using the username and password indicated above.
The dripline libraries typically retrieve this information from an authentications file, we'll go ahead and create that now:

.. literalinclude:: ../../examples/first-mesh/authentications.json
   :language: json
   :caption: authentications.json
   :name: authentications-file
   :linenos:


Add a dripline service
----------------------
Now that we have a broker running, we will go ahead and create our first dripline service.
We won't do anythng fancy, we'll use the built-in ``KeyValueStore`` class to create some endpoints which simply remember a value and report it back.
In a more realistic use-case, the remembered value may be replaced by an interaction with some hardware, but this is nice because it runs without requiring equipment, and still demonstrates the interactions between the software components.


The compose entry
+++++++++++++++++

To create our dripline service, we add another object to the docker-compose definition file (under the ``services:`` block) that looks like the following:

.. literalinclude:: ../../examples/first-mesh/docker-compose.yaml
   :caption: docker-compose.yaml
   :language: yaml
   :lines: 11-21
   :linenos:
   :lineno-start: 11

Here we're running a container with two files mounted in, the authentications file from the previous section, and a runtime configuration file to be discussed next.
We also specify the command to run in the container (review the docker compose documentation linked above if you need help understanding the syntax).

The runtime configuration file
++++++++++++++++++++++++++++++

The configuration file is used to define the classes which need to be created to do the work of the service.
The file lists those, including the configurable parameters that are passed to the ``__init__`` functions for those classes.
If you're ever not sure what configurable parameters a class takes, you can check that function definition in the class and its base classes.

There are several important patterns for a runtime configuration file:

#. The description of classes goes in a section of the yaml file named ``runtime-config``
#. Every class is a dictionary block, with the required keys ``name`` (uniquely naming the instance) and ``module`` (naming the class)
#. A class may include a ``module_path`` key, which indicates the path to a python source file implementing that class
#. The top-level of the runtime-config should have a class which is either a ``Service`` or a class derived from it, this class is responsible for connecting to AMQP and sending and receiving dripline messsages.
#. The ``Service`` may have an ``endpoints`` key which contains a list of dictionary blocks defining other class instances

In this case, our key-value storage service has a vanilla ``Service`` for consuming messages, and three endpoints for storing values.
Taking the "peaches" endpoint as an example, we see that we're creating an instance of the ``KeyValueStore`` class and "peaches" is its name.
We're passing in an ``initial_value`` (defined in the ``KeyValueStore`` class itself), ``get_on_set``, ``log_on_set``, and ``log_interval`` (from the ``Entity`` base class), and ``calibration`` (from the ``Endpoint`` base class inherited through ``Entity``).
Any other arguments those classes take in their ``__init__`` are being left at the default values.
The full configuration looks like:

.. literalinclude:: ../../examples/first-mesh/key-value-store.yaml
   :caption: key-value-store.yaml
   :language: yaml
   :linenos:


Running and interacting
+++++++++++++++++++++++

Having create the runtime configuration and added it to the compose environment, bring the the compose environment up to launch your containers.
Probably the best option is to bring it up in daemon mode (with ``-d``), but that's up to you; I typically launch as a daemon, then use the ``logs`` subcommand with ``-f`` to follow the activity of any service I'm actively trying to debug.
If you do this, you should see new output every 10 seconds when the peaches endpoints logs a new value (per the configured ``log_interval`` value).

With that working, use the ``exec`` subcommand to run a second bash shell in the key-value-store container.
From here, we'll use the command line interface to interact with our new service (note that you can use the ``--help`` flag with any of these tools to find out about the full set of available options).

Use the ``dl-mon`` command (from ``dripline-cpp`` to watch the logs).
The full command could be ``dl-mon --auth-file /root/authentications.json -b rabbit-broker -a sensor_value.#``.
You could similarly bind to ``heartbeat.#`` to see the regular heartbeat messages from all running services (for now we just have the one).

Use the ``dl-agent`` command to interact with an endpoint.
First, we'll check the current value of the peaches endpoing, with ``dl-agent --auth-file /root/authentications.json -b rabbit-broker get peaches``.
You should see a verbose output that includes a payload section with the current value.
Now try to use the ``set`` subcommand to change the value and get it again, you should see your new value.
You should also see that a new value gets logged whenever you use ``set``, and that time-based logs have your newly assinged value.


Add historical data storage
---------------------------

This has all been nice for allowing us to interact with the key-value-store service.
Hopefully you can see that if instead of the trivial implementations of the ``on_get`` and ``on_set`` methods in the ``KeyValueStore`` class, we could implement those methods with arbitrarily complex logic and still interact with them in the same way.
For this tutorial however, we set aside the question of implementing more complex interactions with hardware and focus back on software issues.
In particular, as built we have a way to find out what the current value of peaches is, but not what it has been.
Normally we want to catch the value logs produced and record them in a database or other long-term storage system so that they can be referenced or processed later.

The details of the logging system are discussed in the :ref:`logging system <logging-data>` section so here we jump ahead with spinning it up.

... the logging code has not yet been ported from dripline v2 to v3.
The very-brief overview of how it works is that it listens to messages similar to what was done with ``dl-mon`` in the prior section.
When a message is received, it unpacks the message's payload data and uses that to insert a new record into the database.
Our example adds data to postgres, but one could construct a similar system for logging to other databases.

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
Here, we use `grafana <https://grafana.com>`_.
It makes it easy to query a large number of data sources, including postgreSQL as configured in the previous section.
It supports many visualizations (plots, tables, etc.), as well as setting alarm conditions (such as value out of bounds) and even external alarm integrations (such as sending messages to slack).

ToDo Notes:
+++++++++++

#. Create a grafana service

   #. configure to enable anyonmyous login? (or simple/default user/password)
   #. configure provisioning for datasource pointing to postgres above

#. Go through interactively creating a dashboard to plot one sensor's time series & a table of aggregate values
   #. Export and add the dashboard to the provisioning system
