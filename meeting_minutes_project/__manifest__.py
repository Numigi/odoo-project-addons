# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Meeting Minutes for Project",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Project",
    "depends": ["project", "meeting_minutes"],
    "summary": "Add meeting minutes for project",
    "data": [
        "security/ir.model.access.csv",
        "data/mail_activity_type.xml",
        "views/meeting_minutes_views.xml",
        "views/discuss_point_views.xml",
        "views/project_project_views.xml",
        "views/project_task_views.xml",
        "views/means_communication_views.xml",
    ],
    "installable": True,
}
