Process Management
==================

In order to have a robust controls system it is important that software deployment be done in a robust way.
In support of this, dripline systems are typically designed using stateless microservice design concepts.
Here "process" is in the computing sense, i.e. an applications running on some server.

A microservice means that each program has a narrow scope of responsibility, and provides an interface to that scope.
Any problems that arise in one system should have a limited impact to only that system, and process lifecycles should be independent whenever possible.

Here, "stateless" means that if the program crashes or is killed, and then restarts, operation continues as expected.
If another service cares about the state of a system, it should confirm that that state exists each time that it cares.
If a process sets a state elsewhere and expects that state to exist for an extended period, it should confirm the state regularly and is responsible for detecting/responding to a state change.

Execution Environment
---------------------

Driplineorg provides software for executing a controls system, which can be executed in whatever way works best for a particular use case.
This could include user or system location installation, in or out of a python virtualenvironment or chroot, or even in or outside of a container.
Similarly, the process execution could be done in an interactive shell, as a background process, as a daemon process, or in a container (again, with many options for management).

In most dripline applications, software is deployed in docker containers (this is also the environment where we develop and test the software); you are encouraged to review the official documentation for docker (specifically, the Dockerfile and the docker command line tool).
Further, we typically deploy containers in one of two ways:
1. A docker-compose orchestration is convenient when working with a single host and a single user.
   This is a great way to work when doing development and prototyping, and when systems do not need to run for extended periods of time.
2. On production systems, we deploy using kubernetes.
   This requires an additional step of provisioning a kubernetes cluster, but has the advantage that it leverages the entire ecosystem of cloud-based computing developers and technologies (providing process monitoring and restart, node health monitoring, upgrade and rollbacks, node migration, etc.).
