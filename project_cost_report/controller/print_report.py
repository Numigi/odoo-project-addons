# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from odoo import http
from odoo.http import request


class PrintProjectCostReport(http.Controller):

    @http.route('/web/project_cost_report/<int:project_id>', type='http', auth='user')
    def project_cost_report_pdf(self, project_id, report_context, token):
        """Print the PDF version of the cost report.

        :param int project_id: the ID of the project
        :param dict report_context: the rendering context of the report
        :param str token: the user token
        :rtype: Response
        """
        report_context = json.loads(report_context)
        output_pdf = request.env['project.cost.report'].get_pdf(report_context)
        response = request.make_response(
            output_pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'attachment; filename=project_cost_report.pdf;')
            ]
        )
        response.set_cookie('fileToken', token)
        return response
