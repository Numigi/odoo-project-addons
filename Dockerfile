FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/requirements.txt .
RUN pip3 install -r requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY account_analytic_enhanced  /mnt/extra-addons/account_analytic_enhanced
COPY analytic_line_employee  /mnt/extra-addons/analytic_line_employee
COPY analytic_line_revenue  /mnt/extra-addons/analytic_line_revenue
COPY project_analytic_group  /mnt/extra-addons/project_analytic_group
COPY project_chatter  /mnt/extra-addons/project_chatter
COPY project_closed  /mnt/extra-addons/project_closed
COPY project_cost_smart_button  /mnt/extra-addons/project_cost_smart_button
COPY project_default_task_stage  /mnt/extra-addons/project_default_task_stage
COPY project_enhanced  /mnt/extra-addons/project_enhanced
COPY project_estimation  /mnt/extra-addons/project_estimation
COPY project_estimation_material  /mnt/extra-addons/project_estimation_material
COPY project_form_with_dates  /mnt/extra-addons/project_form_with_dates
COPY project_group_create  /mnt/extra-addons/project_group_create
COPY project_hide_create_sale_order  /mnt/extra-addons/project_hide_create_sale_order
COPY project_invoicing_profile  /mnt/extra-addons/project_invoicing_profile
COPY project_iteration  /mnt/extra-addons/project_iteration
COPY project_iteration_parent_only  /mnt/extra-addons/project_iteration_parent_only
COPY project_iteration_parent_type_required  /mnt/extra-addons/project_iteration_parent_type_required
COPY project_iteration_sale_inheritance  /mnt/extra-addons/project_iteration_sale_inheritance
COPY project_kanban_dates /mnt/extra-addons/project_kanban_dates
COPY project_kanban_to_form  /mnt/extra-addons/project_kanban_to_form
COPY project_lump_sum  /mnt/extra-addons/project_lump_sum
COPY portal_project_timesheet_conditional  /mnt/extra-addons/portal_project_timesheet_conditional
COPY project_material  /mnt/extra-addons/project_material
COPY project_material_direct  /mnt/extra-addons/project_material_direct
COPY project_material_progress  /mnt/extra-addons/project_material_progress
COPY project_material_quantity_filters  /mnt/extra-addons/project_material_quantity_filters
COPY project_milestone_dependency  /mnt/extra-addons/project_milestone_dependency
COPY project_milestone_enhanced  /mnt/extra-addons/project_milestone_enhanced
COPY project_milestone_estimated_hours  /mnt/extra-addons/project_milestone_estimated_hours
COPY project_milestone_remaining_hours  /mnt/extra-addons/project_milestone_remaining_hours
COPY project_milestone_responsible  /mnt/extra-addons/project_milestone_responsible
COPY project_milestone_spent_hours  /mnt/extra-addons/project_milestone_spent_hours
COPY project_milestone_start_date  /mnt/extra-addons/project_milestone_start_date
COPY project_milestone_time_report  /mnt/extra-addons/project_milestone_time_report
COPY project_milestone_type  /mnt/extra-addons/project_milestone_type
COPY project_milestone_time_kpi  /mnt/extra-addons/project_milestone_time_kpi
COPY project_milestone_time_pivot  /mnt/extra-addons/project_milestone_time_pivot
COPY project_milestone_time_progress  /mnt/extra-addons/project_milestone_time_progress
COPY project_milestone_time_progress_timeline  /mnt/extra-addons/project_milestone_time_progress_timeline
COPY project_milestone_timeline  /mnt/extra-addons/project_milestone_timeline
COPY project_milestone_timeline_color  /mnt/extra-addons/project_milestone_timeline_color
COPY project_milestone_timeline_dynamic  /mnt/extra-addons/project_milestone_timeline_dynamic
COPY project_milestone_week_duration  /mnt/extra-addons/project_milestone_week_duration
COPY project_no_quick_create  /mnt/extra-addons/project_no_quick_create
COPY project_outsourcing  /mnt/extra-addons/project_outsourcing
COPY project_outsourcing_timesheet_automation   /mnt/extra-addons/project_outsourcing_timesheet_automation
COPY project_portal_hide_timesheets  /mnt/extra-addons/project_portal_hide_timesheets
COPY project_portal_no_subtask  /mnt/extra-addons/project_portal_no_subtask
COPY project_portal_parent_task  /mnt/extra-addons/project_portal_parent_task
COPY project_remaining_hours_update  /mnt/extra-addons/project_remaining_hours_update
COPY project_milestone_role  /mnt/extra-addons/project_milestone_role
COPY project_stage  /mnt/extra-addons/project_stage
COPY project_stage_allow_timesheet  /mnt/extra-addons/project_stage_allow_timesheet
COPY project_stage_no_quick_create  /mnt/extra-addons/project_stage_no_quick_create
COPY project_task_analytic_lines  /mnt/extra-addons/project_task_analytic_lines
COPY project_task_analytic_lines_stock  /mnt/extra-addons/project_task_analytic_lines_stock
COPY project_task_customer_reference /mnt/extra-addons/project_task_customer_reference
COPY project_task_date_planned  /mnt/extra-addons/project_task_date_planned
COPY project_task_deadline_from_project  /mnt/extra-addons/project_task_deadline_from_project
COPY project_task_description_template  /mnt/extra-addons/project_task_description_template
COPY project_task_draggable_column_disable  /mnt/extra-addons/project_task_draggable_column_disable
COPY project_task_editable_list_stage  /mnt/extra-addons/project_task_editable_list_stage
COPY project_task_editable_list_view  /mnt/extra-addons/project_task_editable_list_view
COPY project_task_full_text_search  /mnt/extra-addons/project_task_full_text_search
COPY project_task_id_in_display_name  /mnt/extra-addons/project_task_id_in_display_name
COPY project_task_link  /mnt/extra-addons/project_task_link
COPY project_task_milestone_mandatory  /mnt/extra-addons/project_task_milestone_mandatory
COPY project_task_reference  /mnt/extra-addons/project_task_reference
COPY project_task_resource_type  /mnt/extra-addons/project_task_resource_type
COPY project_task_search_parent_subtask  /mnt/extra-addons/project_task_search_parent_subtask
COPY project_task_stage_external_mail  /mnt/extra-addons/project_task_stage_external_mail
COPY project_task_subtask_same_project  /mnt/extra-addons/project_task_subtask_same_project
COPY project_task_type  /mnt/extra-addons/project_task_type
COPY project_template  /mnt/extra-addons/project_template
COPY project_template_date_planned  /mnt/extra-addons/project_template_date_planned
COPY project_template_timesheet  /mnt/extra-addons/project_template_timesheet
COPY project_time_budget /mnt/extra-addons/project_time_budget
COPY project_time_range /mnt/extra-addons/project_time_range
COPY project_timesheet_analytic_update  /mnt/extra-addons/project_timesheet_analytic_update
COPY project_timesheet_time_control_employee_pin  /mnt/extra-addons/project_timesheet_time_control_employee_pin
COPY project_timesheet_time_control_project_wip_dysfunction  /mnt/extra-addons/project_timesheet_time_control_project_wip_dysfunction
COPY project_timesheet_time_control_restricted_group  /mnt/extra-addons/project_timesheet_time_control_restricted_group
COPY project_type  /mnt/extra-addons/project_type
COPY project_wip  /mnt/extra-addons/project_wip
COPY project_wip_material  /mnt/extra-addons/project_wip_material
COPY project_wip_outsourcing  /mnt/extra-addons/project_wip_outsourcing
COPY project_wip_supply_cost  /mnt/extra-addons/project_wip_supply_cost
COPY project_wip_timesheet  /mnt/extra-addons/project_wip_timesheet
COPY timesheet_task_project_no_change  /mnt/extra-addons/timesheet_task_project_no_change

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
