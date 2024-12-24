# Copyriht 2022-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Project Task Link",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "LGPL-3",
    "category": "Project",
    "summary": "Dynamically add links to tasks in the web interface.",
    "depends": [
        "project_task_reference",
        "web_editor",
    ],
    "assets": {
        "web.assets_backend": [
            "/project_task_link/static/src/js/html_field.js",
        ],
    },
    "installable": True,
}
