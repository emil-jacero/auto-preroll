FROM ubuntu:20.04

# ARGS invalidates cache, if any
ARG NAME
ARG VCS_URL
ARG VCS_SOURCE
ARG VCS_REF
ARG BUILD_DATE

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.name="${NAME}"
LABEL org.label-schema.vcs-url="${VCS_URL}"
LABEL org.label-schema.vcs-source="${VCS_SOURCE}"
LABEL org.label-schema.vcs-ref="${VCS_REF}"
LABEL org.label-schema.build-date="${BUILD_DATE}"

# Run in single layer to keep size down
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates vim openssh-client git python3 python3-pip cifs-utils tzdata
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils

# Installing python modules
ADD requirements.txt /
RUN pip3 install -r requirements.txt
RUN echo ls -la

ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD src /app

WORKDIR /app
ENTRYPOINT /app/entry.sh
