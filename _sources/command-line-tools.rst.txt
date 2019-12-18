.. _command-line-tools:

Command Line Tools
==================

The primary dripline libraryes ship with several command line tools which will describe here.
The ``dripline-cpp`` software repo provides the ``dl-agent`` and ``dl-mon`` commands, which are used for generic interactions with a dripline mesh.
The ``dripline-python`` repo (which s built on top of the ``dripline-cpp`` repo) adds the ``dl-serve`` command which is used to start up services.
Each of the programs has extensive built-in documentation of its command line usage and behavior, which can be accessed by calling it with the ``--help`` flag.
Here we will summarize when you might use each program and any key behaviors or features from the command line interface.

dl-agent
--------
This command is used to construct and send dripline messages and to collect the generated reply.
Note that are subcommands corresponding to the various operations (get, set, cmd), and that in addition to providing details related to the request you are sending, you must provide the details required for making a connection to the message broker.
It may be tempting to use this command in shell scripting to combine repeated or multi-step tasks.
While this certainly works, it is often better to script in python, where the API is more directly available.

dl-mon
------
This command is used to passively collect and print messages sent via the AMQP broker.
It can be very useful for monitoring to see if a service is producing expected messages.
Be warned that if the monitor is running on the requests exchange, it counts as a consumer, and requests sent to a crashed service will not produce to normal error (which indicates that the message is undeliverable becuase there is no consumer).

dl-serve
--------
This command is used to run a new dripline service.
It parses a configuration file and uses the contents to instantiate the classes which do the work of the service.
The top-level class must be a ``Service`` (or derived from it), this class is responsible for making the connection to AMQP and processing messages as they are delivered.
Other classes must be instances of ``Endpoint`` (or derived from it).
The ``dl-serve`` command can create instances of any classes in the dripline python package, including those added to its namespace using plugin packages (see, for example the :ref:`plugin tutorial<python-plugin>`.
After creating all of the class instances, this command starts the infinite message consuming loop to process incoming request messages.
