FROM ubuntu:24.04
LABEL authors="The Randalorian"
RUN apt-get update -q -y && \
    apt-get install -q -y software-properties-common && \
    apt-add-repository ppa:swi-prolog/stable && \
    apt-get update -q -y && \
    apt-get install -q -y swi-prolog && \
    rm -rf /var/lib/apt/lists/*