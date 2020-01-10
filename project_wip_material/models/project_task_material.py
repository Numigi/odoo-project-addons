# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import ValidationError


class TaskMaterialLine(models.Model):
    """Prevent adding material the project is not properly set for accounting."""

    _inherit = 'project.task.material'

    def _run_procurements(self):
        self._check_project_has_wip_account()
        return super()._run_procurements()

    def _check_project_has_wip_account(self):
        project = self.task_id.project_id
        if not project.project_type_id:
            raise ValidationError(_(
                'Material can not be added to the task because '
                'the project {} has no project type.'
            ).format(project.display_name))

        if not project.project_type_id.wip_account_id:
            raise ValidationError(_(
                'Material can not be added to the task because '
                'the project type {} has no WIP account.'
            ).format(project.project_type_id.display_name))
