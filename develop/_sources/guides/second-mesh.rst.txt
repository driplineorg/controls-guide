.. _second-mesh-walkthrough:

=======================
Second Mesh Walkthrough
=======================

This walkthrough is intended to be functionally identical to :ref:`first-mesh-walkthrough` except that instaed of deploying services using a single docker-compose file, they will each be deployed into a kubernetes cluster using helm charts.
If you haven't already done so, please at least go skim over the first mesh page, here we skip the explanations that are there and jump directly to deployment and the details specific to this setup.

As in the first mesh, it is important to note that there are lots of choices and possible configurations of the third-party components used here.
For the purposes of this guide, we've prioritized ease of configuration to simplify the demonstration; we do not necessarily recommend these choices for production environments (every case is different and you should think about what your requirements are).

Prerequisites
-------------

In order to follow this tutorial you will need to have several resources available:

.. glossary::

  A running kubernetes environment.
    This tutorial is being written and tested using kubernetes 1.15.5 as shipped with docker desktop CE (2.2.0.5) on MacOS. It is not expected to be very sensitive to those versions, but check the release notes if you differ widely or have issues.

  The `helm <https://helm.sh>`_ tool.
    Development and testing is being done on version 3.2.0, version 2 is not supported.

  A local clone of the `dripline-python repo <https://github.com/driplineorg/dripline-python>`_.
    We do not currently have a CI/CD pipeline established for bulding and publishing charts to a repository and so the dripline-python chart instances will be released from a local path.
    Throughout this guide, we assume that is located at ``DRIPLINE_PYTHON_ROOT``.

Deployment
----------

The complete set of configuration files used here are available in the `github repo for this documentation <https://github.com/driplineorg/controls-guide/tree/master/examples/second-mesh>`_.
There the values override files for releases of charts are named following the pattern ``RELEASE_NAME.values.yaml`` (where RELEASE_NAME is replaced in each case).

For third-party applications we'll use helm charts provided and maintained by bitnami.
This choice is somewhat arbitrary and you may reasonably choose to use some other available chart, or roll your own.
In order to use those, we first need to add the repository to the helm environment with the following command::

  helm repo add bitnami https://charts.bitnami.com/bitnami


Without further ado, let's start deploying our workloads.

RabbitMQ Broker
~~~~~~~~~~~~~~~

We again start by standing up the message broker.
We write a simple values override file to configure the user and password.

.. literalinclude:: ../../examples/second-mesh/rabbitmq.values.yaml
  :caption: rabbitmq.values.yaml
  :language: yaml
  :linenos:

Per the helm command line interface, we can then release an instance of the chart with::

  helm install rabbitmq bitnami/rabbitmq -f rabbitmq.values.yaml

This produces a release named ``rabbitmq`` and uses the default knubernetes namespace.

In order to connect to the broker, our dripline services will require the password we just configured.
We will create a kubernetes secret with that information and pass it into our services.
Here this is done without a chart, using a raw secret created from a manifest, but other charts may produce a strong password and provide access through their own secrets.
Also, the secret here also includes credentials for the postgreSQL database we're about to deploy.
The manifest is

.. literalinclude:: ../../examples/second-mesh/rabbitmq-authentications-secret.yaml
   :caption: rabbitmq-authentications-secret.yaml
   :language: yaml
   :linenos:

You can find more information in the `official documentation on secrets <https://kubernetes.io/docs/concepts/configuration/secret/>`_.
The manifest can be installed with::

  kubectl apply -f rabbitmq-authentications-secret.yaml

.. note::

  There is active development in the scarab repo (a dependency of dripline-cpp) on a feature which will enable the runtime configuration of dripline services to support templating at the time of execution.
  This will allow this omnibus secret to be eliminated in favor of secrets which are specific to (and associated with) the resources they provide access to.


The key-value store
~~~~~~~~~~~~~~~~~~~

Next we create a release of the dripline-python chart for our key-value store.
In the following values override, note that the entire configuration file content is included as a dictionary object, it will be used to populate a kubernetes configMap object by the chart.
Also note that we pass in the name of the secret created in the prior step.

.. literalinclude:: ../../examples/second-mesh/key-value-store.values.yaml
   :caption: key-value-store.values.yaml
   :language: yaml
   :linenos:

We deploy the release following the same patter, with::

   helm install key-value-store DRIPLINE_PYTHON_ROOT/chart -f key-value-store.values.yaml

A pause for demonstration
+++++++++++++++++++++++++

Let's pause our deployments for a moment to see how we may interact with the system.
If you're already comfortable with the ``helm`` and ``kubectl`` command line interfaces, feel free to jump ahead to the next section.

First, let's take a look at the releases we've created, ``helm list`` will list the releases and some basic status information::

  NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
  key-value-store default         1               2020-05-08 21:05:40.240297 -0700 PDT    deployed        dripline-python-1.2.0   v4.4.2-amd64
  rabbitmq        default         1               2020-05-08 21:04:47.707076 -0700 PDT    deployed        rabbitmq-6.25.9         3.8.3

We can also inspect the kubernetes pod bojects with ``kubectl get pods``, which produces complementary information::

  NAME                                                          READY   STATUS    RESTARTS   AGE
  key-value-store-dripline-python-deployment-78dfb7f6c5-gzl5k   1/1     Running   0          6s
  rabbitmq-0                                                    1/1     Running   0          5m23s

If you want to see the logs from a running service, use ``kubectl logs -f <pod-name>`` (you may also find the ``--tail`` flag useful for pods that have been running for a while, see the docs for more explanation and options).
You can use ``kubectl exec ...`` to launch a shell in the running container and use the dripline command line interface to interact with the service in the same way as you did in the first mesh tutorial.

Historical data storage
~~~~~~~~~~~~~~~~~~~~~~~

Moving on, we go ahead and once again add a postgres database.
The same caveats apply, the structure of this database is not very well suited to production or high-complexity data, but it will serve for our demonstration.
We again use the bitnami chart, where we use the override file to set the username and password, as well as creating our table with the same ``sql`` script from first mesth.
The override file is

.. literalinclude:: ../../examples/second-mesh/postgres.values.yaml
   :caption: postgres.values.yaml
   :language: yaml
   :linenos:

and we deploy it with the now familar command::

  helm install postgres bitnami/postgresql -f postgres.values.yaml

We also again deploy a ``sensor-logger`` dripline service to consume alert messages and populate the database.
The values file follows the same considerations as for the ``key-value-store`` service above

.. literalinclude:: ../../examples/second-mesh/sensor-logger.values.yaml
   :caption: sensor-logger.values.yaml
   :language: yaml
   :linenos:

Release it with::

   helm install key-value-store DRIPLINE_PYTHON_ROOT/chart -f key-value-store.values.yaml

Visualization
-------------

We again install grafana to use for looking at our daata.
We use a kubernetes manifest to create a secret with the datasource configuration required for connecting to our database and then pass it into the chart so that it gets provisioned automatically (see chart docs for details).

.. literalinclude:: ../../examples/second-mesh/grafana-datasource-secret.yaml
   :caption: grafana-datasource-secret.yaml
   :language: yaml
   :linenos:

is installed with::

   kubectl apply -f grafana-datasource-secret.yaml

and then the chart itself is configured with

.. literalinclude:: ../../examples/second-mesh/grafana.values.yaml
   :caption: grafana.values.yaml
   :language: yaml
   :linenos:

and released with::

   helm install grafana bitnami/grafana -f grafana.yaml

.. note::

  To access grafana on a local cluster, you can use ``kubectl port-forward <pod>`` to bind a local port to the container.
  For production clusters you will most likely want to configure an ingress controller; configuring that is well beyond the scope of this guide and highly dependent on your particular cluster's environment.
  Once that is done, it should be a simple matter of populating the chart's ``ingress`` configuration block.

Other Notes
-----------

Before concluding, we'll leave you with some patterns and notes that we've found to be useful.

* At times you may want to turn services on and off. Rather than delete and re-releasing the instance of the chart, it is often useful to scale the number of replicas between 0 and 1. This retains the details of the release and continues to list the chart when using various inspection commands.
* Similarly, because the containers are deployed as kubernetes ``Deployment`` objects, the system will monitor the number of running pods and restore them. If you want to quickly restart something, you can use ``kubectl delete pods ...`` to delete the running pod and let the controller immediately recreate it.
* If you want to use the dripline command line interface tools, you can use ``kubectl exec ..`` to start a shell in a running pod. This may be easier than installing the tools locally, especially because the authentication secret will be available. Note, however, that if the main service process ends then your shell will terminate with an undefined error behavior.
* There are many more third-party tools from the cloud ecosystem which you may find useful for monitoring the health of your controls system.

  * We've found `prometheus-operator <https://github.com/coreos/prometheus-operator>`_ (deployable from a helm chart per the README) very useful for monitoring the health of the underlying kubernetes cluster and compute hardware.
  * The `ELK stack <https://www.elastic.co/elastic-stack?ultron=[EL]-[B]-[Trials]-[AMER]-[US-W]-Exact&blade=adwords-s&Device=c&thor=elk%20stack&gclid=Cj0KCQjwhtT1BRCiARIsAGlY51K3Kdpj_ZQmcAgcHLEs0JqUGK2gCiAJ-IDzXM1SmCXGM2dNwGukzHcaAhT-EALw_wcB>`_ is a helpful way to aggreate logs from many services.

