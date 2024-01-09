# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Task Meeting Certificate",
    "version": "1.0.1",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Recording",
    "depends": [
        "report_aeroo",
        "meeting_minutes_project",
        "partner_firstname",
        "web_widget_digitized_signature",
    ],
    "summary": "Define meeting minutes on tasks.",
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "data/mail_template.xml",
        "views/meeting_minutes.xml",
        "views/meeting_minutes_signature.xml",
        "views/portal.xml",
    ],
    "demo": [
        "demo/meeting_minutes_report.xml",
    ],
    "installable": True,
}
