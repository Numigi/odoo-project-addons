# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data
from odoo.exceptions import MissingError
from odoo.tests import common
from ..reference import TaskReference


@ddt
class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_1 = cls.env['project.task'].create({'name': 'Task 1'})
        cls.task_2 = cls.env['project.task'].create({'name': 'Task 2'})

    @data(
        'TA#{}',
        'ta#{}',
        'TA{}',
        'ta{}',
    )
    def test_extract_references_from_text(self, reference_format):
        reference = reference_format.format(self.task_1.id)
        text = "Some prefix text {} some suffix text".format(reference)
        result = self.env['project.task']._extract_references_from_text(text)
        assert len(result) == 1
        assert result[0].task_id == self.task_1.id

    def test_reference_string(self):
        expected_string = "ta#{}".format(self.task_1.id)
        text = "Some prefix text {} some suffix text".format(expected_string)
        reference = self.env['project.task']._extract_references_from_text(text)[0]
        assert reference.string == expected_string

    def test_reference_normalized_string(self):
        text = "Some prefix text {} some suffix text".format("ta#{}".format(self.task_1.id))
        reference = self.env['project.task']._extract_references_from_text(text)[0]
        assert reference.normalized_string == "TA#{}".format(self.task_1.id)

    def _make_reference_from_task_id(self, task_id):
        return TaskReference({'id': task_id}, string='TA#{}'.format(task_id), format_="TA#{id}")

    def test_find_task_from_reference(self):
        reference = self._make_reference_from_task_id(self.task_1.id)
        result = self.env['project.task']._find_from_reference(reference)
        assert result == self.task_1

    def test_if_wrong_task_id_in_reference__raise_missing_error(self):
        reference = self._make_reference_from_task_id(99999999999)
        with pytest.raises(MissingError):
            self.env['project.task']._find_from_reference(reference)

    def test_search_references_from_text(self):
        text = """TA#{} Improve the implementation

            See ta{} for more details.
        """.format(self.task_1.id, self.task_2.id)
        result = self.env['project.task']._search_references_from_text(text)
        assert len(result) == 2
        assert result[0].task == self.task_1
        assert result[1].task == self.task_2

    def test_if_task_id_wongly_named__raise_missing_error(self):
        regex_with_typo = r"TA#(?P<task_id>\d+)"  # task_id instead of id
        self.env['ir.config_parameter'].set_param(
            'project_task_reference.regex', regex_with_typo)
        format_with_typo = "TA#{task_id}"
        self.env['ir.config_parameter'].set_param(
            'project_task_reference.format', format_with_typo)

        text = "TA#{} Some text".format(self.task_1.id)

        with pytest.raises(MissingError):
            self.env['project.task']._search_references_from_text(text)
