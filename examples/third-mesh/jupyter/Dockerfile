ARG img_repo=ghcr.io/driplineorg/dripline-python
ARG img_tag=latest

FROM ${img_repo}:${img_tag}

RUN pip3 install --upgrade pip &&\
    pip3 install \
    	'jupyterlab' &&\
    /bin/true

EXPOSE 8888

CMD jupyter lab --no-browser --allow-root --ip=0.0.0.0
