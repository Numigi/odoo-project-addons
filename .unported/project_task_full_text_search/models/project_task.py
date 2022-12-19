# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from unidecode import unidecode

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from .ir_config_parameter import FULL_TEXT_SEARCH_PARAM_KEY

_logger = logging.getLogger(__name__)

FULL_TEXT_SEARCH_INDEX_NAME = 'project_task_full_text_search_idx'


class ProjectTaskWithFullTextSearch(models.Model):
    """Add full test search to tasks."""

    _inherit = 'project.task'

    full_text_search = fields.Text(
        'Full Text',
        compute=lambda self: None,
        search='_search_full_text_content',
    )

    full_text_content = fields.Text(
        'Indexed Content',
        compute='_compute_full_text_content',
        store=True,
    )

    @api.depends('name', 'description')
    def _compute_full_text_content(self):
        for task in self:
            text = ' '.join((task.name, task.description or ''))
            text_with_no_accent = unidecode(text).lower()
            task.full_text_content = text_with_no_accent

    def _search_full_text_content(self, operator, value):
        if operator != '=':
            raise ValidationError(_(
                'The operator {operator} is not supported for full text search on tasks. '
                'You may use the equal operator instead.'
            ).format(operator=operator))
        ids = self._find_tasks_from_full_text_content(value) if value else []
        return [('id', 'in', ids)]

    def _find_tasks_from_full_text_content(self, searched_text):
        """Find tasks from the given searched text.

        :param searched_text: the text to search in task contents.
        """
        lang = self._get_full_text_content_language() or 'pg_catalog.english'
        words_to_search = unidecode(searched_text).lower().split(' ')
        self.env.cr.execute(
            """
            SELECT id FROM project_task
            WHERE to_tsvector(%(lang)s, full_text_content) @@ plainto_tsquery(%(lang)s, %(words)s);
            """, {
                'lang': lang,
                'words': ' & '.join(words_to_search),
            })

        return [r[0] for r in self.env.cr.fetchall()]

    def _get_full_text_content_language(self):
        """Get the language used for full text search on tasks.

        sudo() is required because the variable is required for searching content.
        """
        return self.env['ir.config_parameter'].sudo().get_param(FULL_TEXT_SEARCH_PARAM_KEY)


class ProjectTaskWithFullTextSearchIndex(models.Model):
    """Add a full text search index tasks.

    The index is optional for searching content from tasks.
    It only increases the spead of the full text search.
    """

    _inherit = 'project.task'

    def _setup_content_index(self):
        """Setup a gin index on task content for the given language.

        :param pg_language_name: the name of the postgresql dictionnary to
            use for the the gin index.
        """
        _logger.info('Droping the full text search index on project_task if it exists.')
        query = "DROP INDEX IF EXISTS {index_name}".format(index_name=FULL_TEXT_SEARCH_INDEX_NAME)
        self.env.cr.execute(query)

        lang = self._get_full_text_content_language()

        if lang:
            _logger.info(
                'Creating the full text search index on project_task '
                'with stemmings for the language {lang}.'.format(lang=lang))
            query = """
                CREATE INDEX {index_name} ON project_task
                USING gin (to_tsvector(%(lang)s, full_text_content));
            """.format(index_name=FULL_TEXT_SEARCH_INDEX_NAME)
            self.env.cr.execute(query, {'lang': lang})
        else:
            _logger.info(
                'The system parameter {param_key} is not defined. '
                'The full text search index will not be created on project_task.'
                .format(param_key=FULL_TEXT_SEARCH_PARAM_KEY))
