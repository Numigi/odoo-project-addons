# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Worksheet",
    "summary": "Manage field worksheets for project interventions",
    "version": "14.0.1.0.0",
    "category": "Project Management",
    "website": "https://github.com/OCA/project",
    "author": "Numigi, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "project",
        "hr_timesheet",
        "project_stage_allow_timesheet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/project_worksheet_sequence.xml",
        "data/mail_template_data.xml",
        "wizards/project_worksheet_complement_views.xml",
        "views/project_worksheet_views.xml",
        "views/project_project_views.xml",
        "views/portal_worksheet_templates.xml",
        "views/res_config_settings_views.xml",
        "reports/project_worksheet_report.xml",
    ],
}