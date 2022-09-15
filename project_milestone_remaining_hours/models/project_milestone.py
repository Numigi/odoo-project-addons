# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, models, fields


class ProjectMilestone(models.Model):

    _inherit = "project.milestone"

    remaining_hours = fields.Float(compute='_compute_remaining_hours', string="Remaining Hours")


    @api.depends("estimated_hours", "total_hours")
    def _compute_remaining_hours(self):
        for rec in self:
            rec.remaining_hours = rec.estimated_hours - rec.total_hours

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        res = super(ProjectMilestone, self).read_group(domain, fields, groupby, offset=offset, limit=limit,
                                                       orderby=orderby, lazy=lazy)
        if 'remaining_hours' in fields:
            for line in res:
                if '__domain' in line:
                    lines = self.search(line['__domain'])
                    remaining_hours = 0.0
                    for record in lines:
                        remaining_hours += record.remaining_hours
                    line['remaining_hours'] = remaining_hours
        return res
