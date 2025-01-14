FROM ubuntu:24.04
LABEL authors="The Randalorian"
WORKDIR /home/ubuntu
COPY run-harness.py /home/ubuntu/
RUN chmod 544 /home/ubuntu/run-harness.py
RUN apt-get update -q -y && \
    apt-get install -q -y python3 swi-prolog && \
    rm -rf /var/lib/apt/lists/*
CMD /home/ubuntu/run-harness.py