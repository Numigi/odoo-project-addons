# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import OutsourcingCase


class TestResPartner(OutsourcingCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_child_subcontracting_fields_sync(self):
        assert self.supplier_child.subcontracting_auto_time_entries is True
        assert self.supplier_child.employee_id == \
               self.env.ref("hr.employee_admin")
