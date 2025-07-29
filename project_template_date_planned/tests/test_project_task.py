# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests import common


class TestTask(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env["project.task"].create(
            {"name": "Template Task A", "is_template": True}
        )

    def test_date_planned_emptied(self):
        self.template.date_planned = datetime.now().date()
        self.template.refresh()
        assert not self.template.date_planned
