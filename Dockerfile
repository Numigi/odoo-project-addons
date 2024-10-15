FROM quay.io/numigi/odoo-public:12.43
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
        # Required for aeroo reports
        libreoffice \
        libreoffice-writer \
        default-jre \
        libreoffice-java-common \
        openjdk-11-jre \
        pdftk \
    && rm -rf /var/lib/apt/lists/*

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"

COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY . /mnt/extra-addons/

USER root

# Cleaning extra-addons after massive copy
RUN [ "/bin/bash", "-c", "\
    find /mnt/extra-addons/ -maxdepth 1 -type f -delete && \
    find /mnt/extra-addons/ -maxdepth 1 -type d -iname '.*' -print0 | xargs -I {} -0 rm -rvf '{}'\
    " ]

USER odoo

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
