Dripline v3 Release
=====================================

Dripline v3 introduces some new features and make a number of changes that should make life easier in building a controls system relative to v2.

Note that some features from project8/dragonfly were imported into dripline-python.

New Features and Changes
-------------------------

* The core features of the Dripline standard are now all implemented in dripline-cpp, and dripline-python wraps and extends the C++ code.
* The C++ code is multithreaded, allowing services to process messages and listen for new messages simultaneously (in both C++ and Python).
* dripline-python is organized to enable easy extension of the dripline namespace with plugins.
* Several classes are imported from project8/dragonfly as official dripline-python implementations.
* dripline-cpp includes executables ``dl-agent`` (for sending messages), and ``dl-mon`` (for monitoring message traffic).
* dripline-python includes executable ``dl-serve`` (for running services).
* Large requests can be split into multiple individual messages.
* An automatic heartbeat (in the form of an alert message) has been added to each service.
* Exceptions raised in Python or thrown in C++ result in reply messages being sent using ``ThrowReply`` and ``throw_reply`` in Python and C++, respectively.
* In C++, the following classes can be used by client code:
    * ``agent`` -- sending messages
    * ``endpoint`` -- basic receiving and processing messages
    * ``hub`` -- adding a dripline API to an existing codebase
    * ``monitor`` -- monitor message traffic
    * ``relayer`` -- perform asyncronous message sending
    * ``scheduler`` -- schedule and execute one-off or repeating scheduled events
    * ``service`` -- main dripline microservice potentially with child endpoints
* In Python, the following classes can be used by client code:
    * Core
        * ``AlertConsumer`` -- Receive alert messages
        * ``Endpoint`` -- Basic receiving and processing messages
        * ``Entity`` -- An endpoint that 
        * ``Interface`` -- Client interface for sending messages
        * ``Scheduler`` -- Schedule and execute one-off or repeating scheduled events
        * ``Service`` -- Main dripline microservice potentially with child endpoints
    * Implementations
        * ``SimpleSCPIEntity`` and others -- Endpoints that handle SCPI requests
        * ``EthernetSCPIService`` -- Service that communicates with a SCPI device
        * ``KeyValueStore`` -- Example service, storing values in a dictionary structure
        * ``PostgresSQLInterface`` -- Service that interacts with a PostgresQL database
        * ``PostgresSensorLogger`` -- Receives messages that should be logged into a database

Moving from Dripline v2 to v3
------------------------------

The message structure and overall API (especially in Python) changed very little, so hopefully the effort to upgrade a system to the new version will be minimal.

That said, the two versions are not compatible, so you cannot run a mixed-version system.

You'll need to make at least the following changes:

.. list-table:: Command Line Interface
   :widths: 50 25 25
   :header-rows: 1

   * - Description
     - Dripline v2 / Dragonfly
     - Dripline v3
   * - Starting a service
     - ``dragonfly serve`` (dragonfly)
     - ``dl-serve``
   * - Sending a request
     - ``dragonfly [get/set/cmd]`` (dragonfly)
     - ``dl-agent [get/set/cmd]``
   * - Monitoring message traffic
     - ``dragonfly monitor`` (dragonfly)
     - ``dl-mon``

.. list-table:: Python Classes
   :widths: 50 25 25
   :header-rows: 1

   * - Description
     - Dripline v2 / Dragonfly
     - Dripline v3
   * - The aspect of a service that communicates with an instrument
     - ``Provider``
     - ``Service``
   * - The main type of service used to interact with instruments
     - ``Spimescape``
     - ``Service``
   * - A service that listens on the alerts queue for broadcasts from other services
     - ``Gogol``
     - ``AlertConsumer``
   * - An endpoint that logs at regular intervals
     - ``Spime``
     - ``Entity``
   * - SCPI communication with an instrument over ethernet
     - ``EthernetProvider`` (dragonfly)
     - ``EthernetSCPIService``
   * - Endpoints for SCPI communication
     - ``SimpleSCPI*Spime``, ``FormatSpime`` (dragonfly)
     - ``SimpleSCPI*Entity``, ``FormatEntity``
   * - Communication with a PostgresQL database
     - ``PostgresQLInterface`` (dragonfly)
     - ``PostgresQLInterface``
   * - Logging to a PostgresQL database
     - ``SensorLogger`` (dragonfly)
     - ``PostgresSensorLogger``
   * - Example service that stores values in a dictionary
     - ``kv_store`` (dragonfly)
     - ``KeyValueStore``
