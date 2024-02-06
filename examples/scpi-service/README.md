# SCPI Service

## Introduction: ``ASCPIDevice``

The class `ASCPIDevice` (in scpi_device.py) is a simulation of a semi-SCPI-compliant device.  
The SCPI queries to which the devicer responds can be configured at runtime via an init argument.  

This service is intended to enable users to learn how to create a configuration file to run a 
dripline service that communicates with the device.  
The service can use out-of-the-box `EthernetSCPIService`.

## Usage

The `scpi_device.py` module can be run as an executable script, which will start up an example version of the service.
The following SCPI queries will be available:

* `IDN?`
* `OPT?`
* `READ?` and `READ [value]`
* `VOLTage?` and `VOLTage [value]`
* `FREQuency?` and `FREQuency [value]`

Command-line usage:

    > ./scpi_device.py

## Test Client

A client module is provided that communicates with `ASCPIDevice` without using dripline features.  
The `test_scpi_client.py` module can be run as a script after starting the device as above:

    > ./test_scpi_client.py

The executable element of the macro will call the default commands that the `scpi_device.py` module provides.

## Use in a Dripline Mesh

A docker-compose file is provided that sets up the device and service in a mesh, along with a broker.  
The following services are included:

* `rabbit-broker` -- The AMQP broker for the mesh
* `scpi-device` -- The simulated device
* `scpi-client` (commented out) -- A test container that can be used to query the device without dripline
* `scpi-service` -- The dripline service that talks to the SCPI device

You can start each container in a separate terminal/terminal tab:

First start the rabbit broker in terminal 1:
    > docker-compose up rabbit-broker

Second, start the SCPI device in terminal 2:
    > docker-compose up scpi-device

Third, start the driplien service for the SCPI device in terminal 3:
    > docker-compose up scpi-service

Finally, use a fourth terminal to make a dripline query:
```
  > docker-compose exec scpi-service bash
  \# dl-agent get --auth-file /root/authentications.json opt
  [...]
  Routing key: amq.gen-lFdABKMsmjpvDpN7bAG-bQ
  Correlation ID: 8238bd83-8ff5-48b5-96cb-8c6ef66a6308
  Reply To: 
  Message Type: 2
  Encoding: json
  Timestamp: 2024-02-06T02:08:38.525721Z
  Sender Info:
      Executable: /usr/local/bin/python3.8
      Hostname: 06019eed80ae
      Username: root
      Service: my_device
      Versions:
          dripline:
              Version: 3.0.0
              Commit: 
              Package: 
          dripline-cpp:
              Version: 2.8.4
              Commit: 4f6490226eefc16a880ae5b342014b590f6115af
              Package: driplineorg/dripline-cpp
          dripline-python:
              Version: 0.0.0
              Commit: na
              Package: driplineorg/dripline-python
  Specifier: 
  Payload: 
  {
      value_raw : Option1,Option2,Option3
  }

  Return Code: 0
  Return Message: 
```
