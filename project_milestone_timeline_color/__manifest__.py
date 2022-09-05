# © 2022 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Milestone Timeline Color",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Display milestones in the color assigned to the milestone type",
    "depends": [
        "project_milestone_type",
        "project_milestone_timeline",
        "web_widget_color",
    ],
    "data": [
        "views/project_milestone_type.xml",
        "views/project_milestone.xml",
    ],
    "installable": True,
}
