# © 2024 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestPickingType(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.picking_type = cls.env['stock.picking.type'].create({
            'name': 'Direct Consumption',
            'code': 'consumption',
            'is_direct_consumption': True,
            'sequence_code': 'DCO',
        })

    def test_if_not_consumption__can_not_be_direct_consumption(self):
        with pytest.raises(ValidationError):
            self.picking_type.code = 'incoming'
