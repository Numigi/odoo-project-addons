# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import models, _
from odoo.exceptions import MissingError
from ..reference import TaskReference

DEFAULT_TASK_REF_REGEX = r'[tT][aA]#?(?P<id>\d+)'
DEFAULT_TASK_REF_FORMAT = "TA#{id}"


def _get_task_ref_regex(env: 'Environment') -> str:
    return (
        env["ir.config_parameter"].sudo().get_param("project_task_reference.regex")
        or DEFAULT_TASK_REF_REGEX
    )


def _get_task_ref_normalized_format(env: 'Environment') -> str:
    return (
        env["ir.config_parameter"].sudo().get_param("project_task_reference.format")
        or DEFAULT_TASK_REF_FORMAT
    )


class Task(models.Model):

    _inherit = 'project.task'

    def _extract_references_from_text(self, text):
        """Extract data about references contained in the given text.

        :param text: the text to parse for references
        :ptype text: str
        :return: a list of task references.
        """
        regex = _get_task_ref_regex(self.env)
        normalized_format = _get_task_ref_normalized_format(self.env)
        return [
            TaskReference(values=i.groupdict(), string=i.group(), format_=normalized_format)
            for i in re.finditer(regex, text)
        ]

    def _find_from_reference(self, reference):
        """Find a task from the given reference.

        :param reference: the task reference for which to find a task.
        :return: a project.task record if any found, otherwise None
        """
        if not reference.task_id:
            return None

        task = self.browse(reference.task_id)

        if not task.exists():
            raise MissingError(_(
                'The task referenced by {ref} does not exist. '
                'No task found for the database ID {id}.'
            ).format(ref=reference, id=reference.task_id))

        return task

    def _search_references_from_text(self, text):
        references = self._extract_references_from_text(text)

        for ref in references:
            ref.task = self._find_from_reference(ref)
            if not ref.task:
                raise MissingError(_(
                    'Could not find a task based on the reference {ref}.'
                ).format(ref=ref))

        return references
