FROM quay.io/numigi/odoo-public:11.0
MAINTAINER numigi <contact@numigi.com>

COPY project_stage_no_quick_create /mnt/extra-addons/project_stage_no_quick_create
COPY project_task_date_planned /mnt/extra-addons/project_task_date_planned
COPY project_task_id_in_display_name /mnt/extra-addons/project_task_id_in_display_name
COPY project_task_time_range /mnt/extra-addons/project_task_time_range

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
