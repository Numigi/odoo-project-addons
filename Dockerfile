FROM quay.io/numigi/odoo-public:11.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt

USER odoo

COPY project_accurate_time_spent /mnt/extra-addons/project_accurate_time_spent
COPY project_form_with_dates /mnt/extra-addons/project_form_with_dates
COPY project_portal_parent_task /mnt/extra-addons/project_portal_parent_task
COPY project_stage_no_quick_create /mnt/extra-addons/project_stage_no_quick_create
COPY project_stage /mnt/extra-addons/project_stage
COPY project_task_date_planned /mnt/extra-addons/project_task_date_planned
COPY project_task_deadline_from_project /mnt/extra-addons/project_task_deadline_from_project
COPY project_task_full_text_search /mnt/extra-addons/project_task_full_text_search
COPY project_task_id_in_display_name /mnt/extra-addons/project_task_id_in_display_name
COPY project_task_subtask_time_range /mnt/extra-addons/project_task_subtask_time_range
COPY project_task_subtask_same_project /mnt/extra-addons/project_task_subtask_same_project
COPY project_task_time_range /mnt/extra-addons/project_task_time_range
COPY project_time_management /mnt/extra-addons/project_time_management
COPY project_time_range /mnt/extra-addons/project_time_range
COPY project_task_type /mnt/extra-addons/project_task_type
COPY project_type /mnt/extra-addons/project_type
COPY project_wip /mnt/extra-addons/project_wip
COPY project_wip_material /mnt/extra-addons/project_wip_material

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
