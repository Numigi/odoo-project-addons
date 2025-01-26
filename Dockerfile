FROM quay.io/numigi/odoo-public:16.latest
LABEL maintainer="contact@numigi.com"

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY project_default_task_stage /mnt/extra-addons/project_default_task_stage
COPY project_group_create mnt/extra-addons/project_group_create
COPY project_milestone_enhanced /mnt/extra-addons/project_milestone_enhanced
COPY project_milestone_estimated_hours /mnt/extra-addons/project_milestone_estimated_hours
COPY project_milestone_spent_hours /mnt/extra-addons/project_milestone_spent_hours
COPY project_milestone_time_kpi /mnt/extra-addons/project_milestone_time_kpi
COPY project_no_quick_create /mnt/extra-addons/project_no_quick_create
COPY project_parent_enhanced mnt/extra-addons/project_parent_enhanced
COPY project_portal_parent_task mnt/extra-addons/project_portal_parent_task 
COPY project_portal_hide_timesheets mnt/extra-addons/project_portal_hide_timesheets
COPY project_progress_variance /mnt/extra-addons/project_progress_variance
COPY project_projected_hours mnt/extra-addons/project_projected_hours 
COPY project_remaining_hours_update /mnt/extra-addons/project_remaining_hours_update
COPY project_stage_allow_timesheet mnt/extra-addons/project_stage_allow_timesheet
COPY project_stage_no_quick_create mnt/extra-addons/project_stage_no_quick_create
COPY project_task_date_planned /mnt/extra-addons/project_task_date_planned
COPY project_task_deadline_from_project /mnt/extra-addons/project_task_deadline_from_project
COPY project_task_description_template /mnt/extra-addons/project_task_description_template
COPY project_task_draggable_column_disable /mnt/extra-addons/project_task_draggable_column_disable
COPY project_task_editable_list_view /mnt/extra-addons/project_task_editable_list_view
COPY project_task_full_text_search /mnt/extra-addons/project_task_full_text_search
COPY project_task_id_in_display_name /mnt/extra-addons/project_task_id_in_display_name
COPY project_task_milestone_mandatory /mnt/extra-addons/project_task_milestone_mandatory
COPY project_task_reference /mnt/extra-addons/project_task_reference
COPY project_task_resource_type /mnt/extra-addons/project_task_resource_type
COPY project_task_stage_external_mail /mnt/extra-addons/project_task_stage_external_mail
COPY project_task_search_parent_subtask /mnt/extra-addons/project_task_search_parent_subtask
COPY project_time_range /mnt/extra-addons/project_time_range
COPY project_track_end_date /mnt/extra-addons/project_track_end_date
COPY project_type_advanced /mnt/extra-addons/project_type_advanced

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
