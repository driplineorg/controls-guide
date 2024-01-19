API Overview
=============

C++
---

The following classes can be used by client code:

* ``agent`` -- sending messages
* ``endpoint`` -- basic receiving and processing messages
* ``hub`` -- adding a dripline API to an existing codebase
* ``monitor`` -- monitor message traffic
* ``relayer`` -- perform asyncronous message sending
* ``scheduler`` -- schedule and execute one-off or repeating scheduled events
* ``service`` -- main dripline microservice potentially with child endpoints

Python
------

The following classes can be used by client code:

* Core -- :py:mod:`dripline.core`
    * :py:mod:`dripline.core.alert_consumer` -- Receive alert messages
    * ``Endpoint`` -- Basic receiving and processing messages
    * ``Entity`` -- An endpoint that 
    * ``Interface`` -- Client interface for sending messages
    * ``Scheduler`` -- Schedule and execute one-off or repeating scheduled events
    * ``Service`` -- Main dripline microservice potentially with child endpoints
* Implementations -- ``dripline.implementations``
    * ``SimpleSCPIEntity`` and others -- Endpoints that handle SCPI requests
    * ``EthernetSCPIService`` -- Service that communicates with a SCPI device
    * ``KeyValueStore`` -- Example service, storing values in a dictionary structure
    * ``PostgresSQLInterface`` -- Service that interacts with a PostgresQL database
    * ``PostgresSensorLogger`` -- Receives messages that should be logged into a database
