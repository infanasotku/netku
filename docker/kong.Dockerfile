FROM kong

USER root
RUN apt-get update && apt-get install -y gettext-base

WORKDIR /app

ADD ./gateways/kong/run.sh /etc/run.sh
ADD ./gateways/kong/kong.yml /kong/kong.yml

ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/kong/kong.yml
ENV KONG_LOG_LEVEL=notice

CMD ["/etc/run.sh"]
