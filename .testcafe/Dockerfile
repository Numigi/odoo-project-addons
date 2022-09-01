FROM node:17.9.0-stretch
LABEL maintainer="contact@numigi.com"

RUN npm install -g testcafe@1.19.0

RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list && \
    wget https://dl-ssl.google.com/linux/linux_signing_key.pub && \
    apt-key add linux_signing_key.pub && \
    apt-get update && \
    apt-get install -y google-chrome-stable

COPY tests /tests

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
