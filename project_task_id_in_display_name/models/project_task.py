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


class ProjectTaskWithIdSearchable(models.Model):
    """Add a field to allow searching a task by its ID.

    Odoo does not allow to properly search an integer value from a search bar.

    This results in an exceptions because Odoo sends the searched value
    right to the database without checking if the given string only contains digits.

    This is why we copy the id value into a varchar column.
    """

    _inherit = 'project.task'

    id_string = fields.Char('ID (String)', readonly=True)

    @api.model
    def create(self, vals):
        task = super().create(vals)
        task.id_string = str(task.id)
        return task
