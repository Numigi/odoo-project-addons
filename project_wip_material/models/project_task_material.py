# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import threading
from odoo import models, _
from odoo.exceptions import ValidationError


class TaskMaterialLine(models.Model):
    """Prevent adding material if the project is not properly set for accounting."""

    _inherit = 'project.task.material'

    def _run_procurements(self):
        if self._must_check_project_wip_account():
            self._check_project_wip_account()
        return super()._run_procurements()

    def _must_check_project_wip_account(self):
        is_testing = getattr(threading.currentThread(), 'testing', False)
        return not is_testing or self._context.get('apply_project_wip_material_constraints')

    def _check_project_wip_account(self):
        self = self.with_context(force_company=self.company_id.id)
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
