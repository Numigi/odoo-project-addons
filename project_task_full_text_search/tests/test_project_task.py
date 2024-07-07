# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestTaskFullTextSearch(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = cls.env["project.task"].create(
            {
                "name": "Full Text Search",
                "description": "Allow searching indexed content from tasks.",
            }
        )
        cls.task2 = cls.env["project.task"].create(
            {
                "name": "Mon titre de tâche en français",
                "description": "Allow searching unicode name from tasks.",
            }
        )
        cls.task3 = cls.env["project.task"].create(
            {
                "name": "My Task Title",
                "description": "Allow searching upper case name from tasks.",
            }
        )

    def test_search_task_using_words_from_title(self):
        tasks_found = self.env["project.task"].search(
            [
                ("full_text_search", "=", "Text Search"),
            ]
        )
        self.assertIn(self.task, tasks_found)

    def test_search_task_using_words_from_description(self):
        tasks_found = self.env["project.task"].search(
            [
                ("full_text_search", "=", "tasks searching content"),
            ]
        )
        self.assertIn(self.task, tasks_found)

    def test_search_task_using_words_with_unidecode(self):
        """Test that accents have no impact on text search."""
        tasks_found = self.env["project.task"].search(
            [
                ("full_text_search", "=", "tâche francais"),
            ]
        )
        self.assertIn(self.task2, tasks_found)

    def test_search_task_using_words_with_title_cases(self):
        """Test that accents have no impact on text search."""
        tasks_found = self.env["project.task"].search(
            [
                ("full_text_search", "=", "My task title"),
            ]
        )
        self.assertIn(self.task3, tasks_found)
