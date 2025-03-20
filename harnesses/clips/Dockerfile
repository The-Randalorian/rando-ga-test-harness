FROM ubuntu:24.04
LABEL authors="The Randalorian"
ARG UID=696
ARG GID=696

COPY run-harness.py /usr/local/bin
COPY run.clp /usr/local/bin
RUN chmod 555 /usr/local/bin/run-harness.py
RUN apt-get update -q -y && \
    apt-get install -q -y python3 build-essential && \
    rm -rf /var/lib/apt/lists/*

# build from source because ubuntu doesn't have io functions enabled.
RUN mkdir /build
RUN mkdir /build/clips
COPY clips_core_source_642.tar.gz /build/clips.tar.gz
RUN tar -C /build/clips -xzvf /build/clips.tar.gz --strip-components=1  # best way to ignore version number
WORKDIR /build/clips/core
RUN make
RUN cp clips /usr/local/bin && \
    cp libclips.a /usr/local/lib && \
    cp clips.h /usr/local/include

RUN groupadd  --gid $GID glados && \
    useradd --uid $UID --gid $GID glados
WORKDIR /home/glados
USER glados
CMD /usr/local/bin/run-harness.py