# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class ProjectTaskWithCode(models.Model):

    _inherit = 'project.task'

    @api.multi
    def name_get(self):
        return [(t.id, t._get_complete_name()) for t in self]

    def _get_complete_name(self):
        """Get the complete name of the task.

        :return: a string containing the id and the name of the task.
        """
        return '[{id}] {name}'.format(id=self.id, name=self.name)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Search tasks using the code before searching for a name."""
        args = args or []
        tasks = self.browse()

        if name and name.isdigit():
            tasks = self.search([('id', '=', int(name))] + args, limit=limit)

        if not tasks:
            tasks = self.search([('name', operator, name)] + args, limit=limit)

        return tasks.name_get()
