# Copyright 2019-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import babel.dates
from datetime import datetime
# from itertools import chain
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round
# from typing import Callable, Mapping
from .util import (
    adjust_analytic_line_amount_sign,
    get_waiting_for_invoice_total,
    group_analytic_lines,
    purchase_line_is_waiting_invoice,
)
from .report_category import CostReportCategory


SECTION_TITLES = {
    "supply": _("Shop Supply"),
    "products": _("Products"),
    "time": _("Time"),
    "outsourcing": _("Outsourcing"),
}


class ProjectCostReport(models.TransientModel):


    _name = "project.cost.report"
    _description = "Project Cost Report"


    def _get_sections(self, projects, report_context):
        return [
            self._get_section(projects, report_context, section)
            for section in  ("supply", "products", "time", "outsourcing")
        ]