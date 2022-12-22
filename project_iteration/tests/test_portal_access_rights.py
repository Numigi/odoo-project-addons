# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import AccessError
from .common import ProjectIterationCase
from odoo.tests.common import users


class TestPortalAccessRights(ProjectIterationCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.portal_user = cls.env.ref('base.demo_user0')
        cls.portal_partner = cls.env.ref('base.partner_demo_portal')
        cls.iteration_1.privacy_visibility = 'portal'

    @users('portal')
    def test_ifHasAccessToIteration_thenCanReadTheIterationName(self):
        self.env['mail.followers'].sudo().create({
            'res_id': self.iteration_1.id,
            'res_model': 'project.project',
            'partner_id': self.portal_partner.id,

        })
        self.iteration_1.name_get()

    def test_ifHasNotAccessToIteration_thenCanReadTheIterationName(self):
        with pytest.raises(AccessError):
            self.iteration_1.sudo(self.portal_user).name_get()
