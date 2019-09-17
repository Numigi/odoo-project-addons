# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields
from odoo.exceptions import ValidationError
from .common import TaskMaterialCase


class TestOpenPickingsFromTask(TaskMaterialCase):

    def test_if_one_picking__open_form_view(self):
        self._create_material_line()
        result = self.task.open_consumption_picking_view_from_task()
        assert 'res_id' in result

    def test_if_two_pickings__open_list_view(self):
        # Create a first picking by addind a material line.
        # Set the quantity to zero so that the picking is cancelled.
        line_1 = self._create_material_line()
        line_1.initial_qty = 0

        # Adding a new line creates a second picking.
        self._create_material_line()
        result = self.task.open_consumption_picking_view_from_task()
        assert 'domain' in result
