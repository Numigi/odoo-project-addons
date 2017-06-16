# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import api, models


class Project(models.Model):

    _inherit = 'project.project'

    @api.multi
    def write(self, vals):
        super(Project, self).write(vals)
        if 'active' in vals:
            self.mapped('analytic_account_id').write({
                'active': vals['active'],
            })

        return True
