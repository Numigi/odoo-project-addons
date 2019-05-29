# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import ValidationError
from odoo.addons.project_outsourcing.tests.common import OutsourcingCase


class TestOutsourcingPurchaseOrder(OutsourcingCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wip_account = cls.env['account.account'].create({
            'name': 'Work In Progress',
            'code': '140102',
            'user_type_id': cls.env.ref('account.data_account_type_non_current_assets').id,
            'reconcile': True,
            'company_id': cls.env.user.company_id.id,
        })
        cls.project_type = cls.env['project.type'].create({
            'name': 'Manufacture',
            'wip_account_id': cls.wip_account.id,
        })
        cls.project.project_type_id = cls.project_type

    def test_on_purchase_confirm__if_no_project_type__error_raised(self):
        self.project.project_type_id = False
        order_sudo = self.order.sudo(self.purchase_user)
        with pytest.raises(ValidationError):
            order_sudo.button_confirm()

    def test_on_purchase_confirm__if_no_wip_account__error_raised(self):
        self.project_type.wip_account_id = False
        order_sudo = self.order.sudo(self.purchase_user)
        with pytest.raises(ValidationError):
            order_sudo.button_confirm()

    def test_on_purchase_confirm__if_project_and_wip_account__error_not_raised(self):
        self.order.sudo(self.purchase_user).button_confirm()
        assert self.order.state == 'purchase'
