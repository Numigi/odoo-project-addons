# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Meeting Minutes Project Steering",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "project",
    "depends": [
        "meeting_minutes_project",
        "project_form_with_dates",
        "project_task_date_planned",
        "web_search_date_range",
        "web_widget_domain_editor_dialog",
    ],
    "summary": "Using project meeting minutes for steering project.",
    "data": [
        "security/ir.model.access.csv",
        "views/project_steering_kpi_views.xml",
        "views/meeting_minutes_views.xml",
        "reports/assets.xml",
        "reports/meeting_minutes_project_templates.xml",
    ],
    "installable": True,
}
