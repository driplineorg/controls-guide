Transitioning from Dripline v2 to v3
=====================================

The change from Dripline v2 to Dripline v3 was made to bring in new features and make changes that had been found wanting since the original setting up of v2.  

The changes and new features include:

* The core features of the Dripline standard are now all implemented in dripline-cpp, and dripline-python wraps and extends the C++ code.
* The C++ code is multithreaded, allowing services to process messages and listen for new messages simultaneously.
* dripline-python is organized to enable easy extension of the dripline namespace with plugins.
* Several classes are imported from Project 8's dragonfly as official implementations.
* dripline-cpp includes executables dl-agent (for sending messages), and dl-mon (for monitoring message traffic).
* dripline-python includes executable dl-serve (for running services).
* Large requests can be split into multiple individual messages.
* An automatic heartbeat (in the form of an alert message) has been added to each service.
* In C++, the following classes can be used by client code:
    * agent -- sending messages
    * endpoint -- basic receiving and processing messages
    * hub -- adding a dripline API to an existing codebase
    * monitor -- monitor message traffic
    * relayer -- perform asyncronous message sending
    * scheduler -- schedule and execute one-off or repeating scheduled events
    * service -- main dripline microservice potentially with child endpoints
* In Python, the following classes can be used by client code:
    * Core
        * AlertConsumer -- Receive alert messages
        * Endpoint -- Basic receiving and processing messages
        * Entity -- An endpoint that 
        * Interface -- Client interface for sending messages
        * Scheduler -- Schedule and execute one-off or repeating scheduled events
        * Service -- Main dripline microservice potentially with child endpoints
    * Implementations
        * SimpleSCPIEntity and others -- Endpoints that handle SCPI requests
        * EthernetSCPIService -- Service that communicates with a SCPI device
        * KeyValueStore -- Example service, storing values in a dictionary structure
        * PostgresSQLInterface -- Service that interacts with a PostgresQL database
        * PostgresSensorLogger -- Receives messages that should be logged into a database
