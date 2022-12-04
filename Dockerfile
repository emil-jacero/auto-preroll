FROM ubuntu:22.04

# ARGS invalidates cache, if any
ARG TITLE
ARG VCS_URL
ARG VCS_REF
ARG BUILD_DATE
ARG VERSION

LABEL org.opencontainers.image.authors="emil@jacero.se"
LABEL org.opencontainers.image.title="${TITLE}"
LABEL org.opencontainers.image.source="${VCS_URL}"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.version="${VERSION}"

# Run in single layer to keep size down
RUN apt-get update && apt-get upgrade -y &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates vim openssh-client git python3 python3-pip tzdata
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y dnsutils

# Installing python modules
ADD requirements.txt /
RUN pip3 install -r requirements.txt

ENV TZ=Europe/Stockholm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir /app
ADD auto_preroll.py /app

WORKDIR /app
ENTRYPOINT /app/auto_preroll.py