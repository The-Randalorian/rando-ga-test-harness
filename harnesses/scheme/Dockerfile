FROM ubuntu:24.04
LABEL authors="The Randalorian"
RUN apt-get update -q -y && \
    apt-get install -q -y mit-scheme && \
    rm -rf /var/lib/apt/lists/*