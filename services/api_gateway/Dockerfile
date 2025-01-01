FROM kong

USER root
RUN apt-get update && apt-get install -y gettext-base

WORKDIR /app

ADD install.sh /etc/install.sh
ADD kong.yml /kong/kong.yml

ARG USERS_URL
ENV USERS_URL=$USERS_URL
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/kong/kong.yml

RUN /etc/install.sh

CMD ["kong", "docker-start"]
