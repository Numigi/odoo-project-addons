# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import models, _, fields
from odoo.exceptions import MissingError

DEFAULT_TASK_REF_REGEX = r"[tT][aA]#?(?P<id>\d+)"
DEFAULT_TASK_REF_FORMAT = "TA#{id}"


class Task(models.Model):
    _inherit = "project.task"

    def _get_task_ref_regex(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("project_task_reference.regex", DEFAULT_TASK_REF_REGEX)
        )

    def _get_task_ref_normalized_format(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("project_task_reference.format", DEFAULT_TASK_REF_FORMAT)
        )

    def _extract_references_from_text(self, text):
        """Extract data about references contained in the given text.

        :param text: the text to parse for references
        :ptype text: str
        :return: a list of dictionaries containing task references.
        """
        regex = self._get_task_ref_regex()
        normalized_format = self._get_task_ref_normalized_format()
        return [
            {
                "string": match.group(),
                "normalized_string": normalized_format.format(**match.groupdict()),
                "values": match.groupdict(),
                "task_id": (
                    int(match.group("id")) if "id" in match.groupdict() else None
                ),
            }
            for match in re.finditer(regex, text)
        ]

    def _find_from_reference(self, reference):
        """Find a task from the given reference.

        :param reference: the task reference dictionary for which to find a task.
        :return: a project.task record if any found, otherwise None
        """
        task_id = reference.get("task_id")
        if not task_id:
            return None

        task = self.browse(task_id)

        if not task.exists():
            raise MissingError(
                _(
                    f"The task referenced by {reference['string']} does not exist. "
                    f"No task found for the database ID {task_id}."
                )
            )

        return task

    def _search_references_from_text(self, text):
        references = self._extract_references_from_text(text)
        for ref in references:
            ref["task"] = self._find_from_reference(ref)
            if not ref["task"]:
                raise MissingError(
                    _(f"Could not find a task based on the reference {ref['string']}.")
                )

        return references
