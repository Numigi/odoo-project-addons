
from odoo.tests.common import SavepointCase
from psycopg2 import IntegrityError


class TestProjectInvoiceProfile(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProjectInvoiceProfile, cls).setUpClass()

        user_group_employee = cls.env.ref('base.group_user')
        user_group_project_user = cls.env.ref('project.group_project_user')
        user_group_project_manager = cls.env.ref('project.group_project_manager')
        user_group_project_profile = cls.env.ref('project_invoicing_profile.group_project_invoicing_profile')

        cls.profile_1 = cls.env['project.invoice.profile'].create({
            'name': 'Numigi',
            'note': 'Projet Numigi'})
        cls.profile_2 = cls.env['project.invoice.profile'].create({
            'name': 'Kolabus',
            'note': 'Projet Kolabus'})

        # Test users to use through the various tests
        Users = cls.env['res.users'].with_context({'no_reset_password': True})

        cls.user_projectuser = Users.create({
            'name': 'ProjectUser',
            'login': 'ProjectUser',
            'email': 'projectuser@example.com',
            'groups_id': [(6, 0, [user_group_employee.id, user_group_project_user.id])]
        })
        cls.user_projectmanager = Users.create({
            'name': 'ProjectManager',
            'login': 'ProjectManager',
            'email': 'projectmanager@example.com',
            'groups_id': [(6, 0, [user_group_employee.id, user_group_project_manager.id,
                                  user_group_project_profile.id])]})

        cls.project_1 = cls.env['project.project'].with_context({'mail_create_nolog': True}).create({
            'name': 'Project1',
            'invoicing_profile_id': cls.profile_1.id
            })

        cls.task_1 = cls.env['project.task'].with_context({'mail_create_nolog': True}).create({
            'name': 'Task1',
            'user_id': cls.user_projectuser.id,
            'project_id': cls.project_1.id})

    def test_delete_assigned_project_invoicing_profile(self):
        """User should never be able to delete an assigned project profil """
        with self.assertRaises(IntegrityError):
            self.profile_1.unlink()

    def test_project_invoicing_profile_on_task(self):
        assert self.task_1.invoicing_profile_id == self.project_1.invoicing_profile_id
