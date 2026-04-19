FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y tcpdump && \
    apt-get clean

CMD ["tcpdump"]