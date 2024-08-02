# Third Mesh

# Mesh Initialization

```
docker swarm init --advertise-addr [IP for primary node; 127.0.0.1 if running on a single host machine]
docker swarm join --token [token]
docker network create --attachable --driver overlay mesh
```

The `docker swarm init` command will provide the `docker swarm join` command, including unique token, that you need to use on either the manager node or any worker nodes.

# Mesh Shutdown

```
docker swarm leave
```

Run `docker swarm leave` for any nodes, manager or worker.

# Services

## Broker

First, of course, you'll need the RabbitMQ broker.  Deploy with:
```
cd [...]/third-mesh/dripline-config/compose
docker stack deploy --compose-file=dripline-config/compose/compose-broker.yaml broker
```

You can access the broker's web interface from a browser on your host machine by going to `http://localhost:15672`.

## Key-Value Store

Deploy with :
```
cd [...]/third-mesh/dripline-config/compose
docker stack deploy --compose-file=dripline-config/compose/compose-jupyter.yaml jupyter
```

Watch logs with:
```
docker service logs -n 100 -f kvs_key-value-store
```

## Jupyter

The DL-Jupyter image is not hosted anywhere yet, but the Dockerfile is supplied with the third mesh.  It's built on the dripline-python image, so it has access to the Dripline command-line tools and Python package.  Build and tag the DL-Jupyter image:
```
cd [...]/third-mesh/jupyter
docker build -t dl-jupyter .
```

Deploy with:
```
cd [...]/third-mesh/dripline-config/compose
docker stack deploy --compose-file=dripline-config/compose/compose-jupyter.yaml jupyter
```

Use the log to check that the server is running and to get the URL (with token) for access:
```
docker service logs -n 100 -f jupyter_dl-jupyter
```

Copy the URL that includes `http://127.0.0.1:8888/`.  Put that in a browser on your host, and it should take you to the JupyterLab main page.

### Terminal access

Open the terminal tab within Jupyter Lab.  Try a get command to check that you can communicate with the mesh:
```
dl-agent --auth-file=/root/authentications.json get peaches
```

### Python notebook access
