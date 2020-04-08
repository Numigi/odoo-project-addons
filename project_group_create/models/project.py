# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import models, _
from odoo.exceptions import AccessError


class Project(models.Model):
    _inherit = "project.project"

    def check_extended_security_create(self):
        super().check_extended_security_create()
        allowed_to_create = bool(
            self.env.user.has_group('project_group_create.group_project_manager_create')
        )
        if not allowed_to_create:
            raise AccessError(_('You are not allowed to create a project.'))
