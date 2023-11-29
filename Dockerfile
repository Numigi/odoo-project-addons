FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"

COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

COPY \
    account_analytic_enhanced \
    analytic_line_employee \
    analytic_line_revenue \
    portal_project_list_hours_spent \
    portal_project_timesheet_conditional \
    project_analytic_group \
    project_chatter \
    project_closed \
    project_cost_report \
    project_cost_smart_button \
    project_default_task_stage \
    project_enhanced \
    project_estimation \
    project_estimation_material \
    project_form_with_dates \
    project_group_create \
    project_hide_create_sale_order \
    project_invoicing_profile \
    project_iteration \
    project_iteration_parent_only \
    project_iteration_parent_type_required \
    project_iteration_sale_inheritance \
    project_kanban_dates \
    project_kanban_to_form \
    project_lump_sum \
    project_material \
    project_material_closed \
    project_material_direct \
    project_material_progress \
    project_material_quantity_filters \
    project_milestone_dependency \
    project_milestone_enhanced \
    project_milestone_estimated_hours \
    project_milestone_remaining_hours \
    project_milestone_responsible \
    project_milestone_role \
    project_milestone_spent_hours \
    project_milestone_start_date \
    project_milestone_time_kpi \
    project_milestone_time_pivot \
    project_milestone_time_progress \
    project_milestone_time_progress_timeline \
    project_milestone_time_report \
    project_milestone_time_report_advanced \
    project_milestone_timeline \
    project_milestone_timeline_color \
    project_milestone_timeline_dynamic \
    project_milestone_type \
    project_milestone_week_duration \
    project_no_quick_create \
    project_outsourcing \
    project_outsourcing_timesheet_automation \
    project_portal_hide_timesheets \
    project_portal_no_subtask \
    project_portal_parent_task \
    project_progress_variance \
    project_projected_hours \
    project_remaining_hours_update \
    project_stage \
    project_stage_allow_timesheet \
    project_stage_no_quick_create \
    project_task_analytic_lines \
    project_task_analytic_lines_stock \
    project_task_customer_reference \
    project_task_date_planned \
    project_task_deadline_from_project \
    project_task_description_template \
    project_task_draggable_column_disable \
    project_task_editable_list_stage \
    project_task_editable_list_view \
    project_task_full_text_search \
    project_task_id_in_display_name \
    project_task_kanban_view_partner \
    project_task_link \
    project_task_milestone_mandatory \
    project_task_reference \
    project_task_resource_type \
    project_task_search_parent_subtask \
    project_task_stage_external_mail \
    project_task_subtask_same_project \
    project_task_type \
    project_template \
    project_template_date_planned \
    project_template_timesheet \
    project_time_budget \
    project_time_range \
    project_timesheet_analytic_update \
    project_timesheet_time_control_employee_pin \
    project_timesheet_time_control_project_wip_dysfunction \
    project_timesheet_time_control_restricted_group \
    project_track_end_date \
    project_type \
    project_wip \
    project_wip_material \
    project_wip_outsourcing \
    project_wip_supply_cost \
    project_wip_timesheet \
    timesheet_task_project_no_change \
    /mnt/extra-addons/

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
