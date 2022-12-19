# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request
from werkzeug.datastructures import Headers


class PrintProjectCostReport(http.Controller):
    @http.route(
        "/web/project_milestone_time_report/<int:project_id>",
        type="http", auth="user"
    )
    def project_milestone_time_report_pdf(self, project_id, token):
        report = request.env["project.milestone.time.report"]
        output_pdf = report.get_pdf(project_id)
        filename = report.get_filename(project_id)
        headers = Headers()
        headers.add("Content-Disposition", "attachment", filename=filename)
        headers.add("Content-Type", "application/pdf")
        response = request.make_response(output_pdf, headers=headers)
        response.set_cookie("fileToken", token)
        return response
