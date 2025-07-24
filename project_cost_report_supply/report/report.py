# Copyright 2019-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import babel.dates
from datetime import datetime
# from itertools import chain
from odoo import api, fields, models, _


SECTION_TITLES = {
    "supply": _("Shop Supply"),
    "products": _("Products"),
    "time": _("Time"),
    "outsourcing": _("Outsourcing"),
}


class ProjectCostReport(models.TransientModel):


    _inherit = "project.cost.report"


    def _get_sections(self, projects, report_context):
        return [
            self._get_section(projects, report_context, section)
            for section in  ("supply", "products", "time", "outsourcing")
        ]

    def _get_section(self, projects, report_context, section_name):
        return super(ProjectCostReport, self)._get_section(projects, report_context, section_name)