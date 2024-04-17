# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import ProjectIterationCase


class TestProjectFollowers(ProjectIterationCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_1 = cls.env["res.partner"].create(
            {"name": "John Doe", "email": "john.doe@example.com"}
        )
        cls.partner_2 = cls.env["res.partner"].create(
            {"name": "Jane Doe", "email": "jane.doe@example.com"}
        )
        cls.channel_1 = cls.env["mail.channel"].create({"name": "Some Channel"})
        cls.channel_2 = cls.env["mail.channel"].create({"name": "Some Other Channel"})
        cls.project_2.message_unsubscribe(
            cls.project_2.message_partner_ids.ids, cls.project_2.message_channel_ids.ids
        )
        cls.project_2.message_subscribe(cls.partner_1.ids, cls.channel_1.ids)

    def test_followers_propagated_on_create(self):
        iteration = self.env["project.project"].create(
            {"name": "Iteration", "parent_id": self.project_2.id}
        )

        assert iteration.message_partner_ids == self.partner_1
        assert iteration.message_channel_ids == self.channel_1

    def test_followers_replaced_on_write(self):
        self.iteration_1.message_subscribe(self.partner_2.ids, self.channel_2.ids)
        self.iteration_1.parent_id = self.project_2
        assert self.iteration_1.message_partner_ids == self.partner_1
        assert self.iteration_1.message_channel_ids == self.channel_1
