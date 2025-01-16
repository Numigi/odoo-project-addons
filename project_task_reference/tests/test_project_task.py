# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data
from odoo.exceptions import MissingError
from odoo.tests.common import TransactionCase


@ddt
class TestProjectTask(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_1 = cls.env["project.task"].create({"name": "Task 1"})
        cls.task_2 = cls.env["project.task"].create({"name": "Task 2"})

    @data(
        "TA#{}",
        "ta#{}",
        "TA{}",
        "ta{}",
    )
    def test_extract_references_from_text(self, reference_format):
        reference = reference_format.format(self.task_1.id)
        text = f"Some prefix text {reference} some suffix text"
        result = self.env["project.task"]._extract_references_from_text(text)
        assert len(result) == 1
        assert result[0]["task_id"] == self.task_1.id

    def test_reference_string(self):
        expected_string = f"ta#{self.task_1.id}"
        text = f"Some prefix text {expected_string} some suffix text"
        reference = self.env["project.task"]._extract_references_from_text(text)[0]
        assert reference["string"] == expected_string

    def test_reference_normalized_string(self):
        text = f"Some prefix text ta#{self.task_1.id} some suffix text"
        reference = self.env["project.task"]._extract_references_from_text(text)[0]
        assert reference["normalized_string"] == f"TA#{self.task_1.id}"

    def test_find_task_from_reference(self):
        reference = {
            "string": f"TA#{self.task_1.id}",
            "normalized_string": f"TA#{self.task_1.id}",
            "task_id": self.task_1.id,
        }
        result = self.env["project.task"]._find_from_reference(reference)
        assert result == self.task_1

    def test_if_wrong_task_id_in_reference__raise_missing_error(self):
        reference = {
            "string": "TA#99999999999",
            "normalized_string": "TA#99999999999",
            "task_id": 99999999999,
        }
        with pytest.raises(MissingError):
            self.env["project.task"]._find_from_reference(reference)

    def test_search_references_from_text(self):
        text = f"""TA#{self.task_1.id} Improve the implementation

            See ta{self.task_2.id} for more details.
        """
        result = self.env["project.task"]._search_references_from_text(text)
        assert len(result) == 2
        assert result[0]["task"] == self.task_1
        assert result[1]["task"] == self.task_2

    def test_if_task_id_wrongly_named__raise_missing_error(self):
        regex_with_typo = r"TA#(?P<task_id>\d+)"  # task_id instead of id
        self.env["ir.config_parameter"].set_param(
            "project_task_reference.regex", regex_with_typo
        )
        format_with_typo = "TA#{task_id}"
        self.env["ir.config_parameter"].set_param(
            "project_task_reference.format", format_with_typo
        )

        text = f"TA#{self.task_1.id} Some text"

        with pytest.raises(MissingError):
            self.env["project.task"]._search_references_from_text(text)
