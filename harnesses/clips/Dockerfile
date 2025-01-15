FROM ubuntu:24.04
LABEL authors="The Randalorian"
ARG UID=696
ARG GID=696

COPY run-harness.py /usr/local/bin
RUN chmod 555 /usr/local/bin/run-harness.py
RUN apt-get update -q -y && \
    apt-get install -q -y python3 clips && \
    rm -rf /var/lib/apt/lists/*
RUN groupadd  --gid $GID nonroot && \
    useradd --uid $UID --gid $GID nonroot
WORKDIR /home/nonroot
USER nonroot
CMD /usr/local/bin/run-harness.py