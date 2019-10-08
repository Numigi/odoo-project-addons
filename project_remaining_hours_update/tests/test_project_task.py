# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_a = cls.env['project.task'].create({'name': 'Task A'})
