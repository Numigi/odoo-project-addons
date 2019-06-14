# © 2018 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Main Module',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Install all addons required for testing.',
    'depends': [
        'stock_account',  # required for testing project_wip

        'analytic_line_revenue',
        'analytic_line_views_prioritized',
        'project_accurate_time_spent',
        'project_cost_report',
        'project_cost_smart_button',
        'project_form_with_dates',
        'project_portal_parent_task',
        'project_stage_no_quick_create',
        'project_task_analytic_lines',
        'project_task_analytic_lines_stock',
        'project_stage',
        'project_task_date_planned',
        'project_task_deadline_from_project',
        'project_task_full_text_search',
        'project_task_id_in_display_name',
        'project_task_subtask_time_range',
        'project_task_subtask_same_project',
        'project_task_time_range',
        'project_time_management',
        'project_time_range',
        'project_task_type',
        'project_type',
        'project_wip',
        'project_wip_material',
        'project_wip_outsourcing',
        'project_wip_timesheet',
    ],
    'installable': True,
}
