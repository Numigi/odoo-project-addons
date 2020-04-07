FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt

USER odoo

COPY project_chatter /mnt/extra-addons/project_chatter
COPY project_default_task_stage /mnt/extra-addons/project_default_task_stage
COPY project_form_with_dates /mnt/extra-addons/project_form_with_dates
COPY project_hide_create_sale_order /mnt/extra-addons/project_hide_create_sale_order
COPY project_iteration /mnt/extra-addons/project_iteration
COPY project_iteration_analytic_account_inheritance /mnt/extra-addons/project_iteration_analytic_account_inheritance
COPY project_iteration_parent_only /mnt/extra-addons/project_iteration_parent_only
COPY project_iteration_parent_type_required /mnt/extra-addons/project_iteration_parent_type_required
COPY project_portal_hide_timesheets /mnt/extra-addons/project_portal_hide_timesheets
COPY project_portal_parent_task /mnt/extra-addons/project_portal_parent_task
COPY project_remaining_hours_update /mnt/extra-addons/project_remaining_hours_update
COPY project_stage /mnt/extra-addons/project_stage
COPY project_stage_allow_timesheet /mnt/extra-addons/project_stage_allow_timesheet
COPY project_stage_no_quick_create /mnt/extra-addons/project_stage_no_quick_create
COPY project_task_date_planned /mnt/extra-addons/project_task_date_planned
COPY project_task_deadline_from_project /mnt/extra-addons/project_task_deadline_from_project
COPY project_task_full_text_search /mnt/extra-addons/project_task_full_text_search
COPY project_task_id_in_display_name /mnt/extra-addons/project_task_id_in_display_name
COPY project_task_link /mnt/extra-addons/project_task_link
COPY project_task_reference /mnt/extra-addons/project_task_reference
COPY project_task_resource_type /mnt/extra-addons/project_task_resource_type
COPY project_task_stage_external_mail /mnt/extra-addons/project_task_stage_external_mail
COPY project_task_subtask_same_project /mnt/extra-addons/project_task_subtask_same_project
COPY project_task_subtask_time_range /mnt/extra-addons/project_task_subtask_time_range
COPY project_task_time_range /mnt/extra-addons/project_task_time_range
COPY project_task_type /mnt/extra-addons/project_task_type
COPY project_template /mnt/extra-addons/project_template
COPY project_template_timesheet /mnt/extra-addons/project_template_timesheet
COPY project_time_management /mnt/extra-addons/project_time_management
COPY project_time_range /mnt/extra-addons/project_time_range
COPY project_type /mnt/extra-addons/project_type

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
