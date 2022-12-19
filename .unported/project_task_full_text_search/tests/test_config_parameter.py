# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common
from ..models.ir_config_parameter import FULL_TEXT_SEARCH_PARAM_KEY
from ..models.project_task import FULL_TEXT_SEARCH_INDEX_NAME


class TestFullTextSearchParamKey(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._delete_parameter(cls.env)

    def setUp(self):
        super().setUp()
        self.assertFalse(self._index_exists(self.env))

    def test_add_full_text_language_parameter(self):
        self._add_parameter(self.env, 'french')
        self.assertTrue(self._index_exists(self.env))

    def test_update_full_text_language_parameter(self):
        self._add_parameter(self.env, 'french')
        self._update_parameter(self.env, 'english')
        self.assertTrue(self._index_exists(self.env))

    def test_delete_full_text_language_parameter(self):
        self._add_parameter(self.env, 'french')
        self._delete_parameter(self.env)
        self.assertFalse(self._index_exists(self.env))

    @staticmethod
    def _add_parameter(env, value):
        env['ir.config_parameter'].create({
            'key': FULL_TEXT_SEARCH_PARAM_KEY,
            'value': value,
        })

    @staticmethod
    def _update_parameter(env, value):
        param = env['ir.config_parameter'].search([
            ('key', '=', FULL_TEXT_SEARCH_PARAM_KEY)
        ])
        param.value = value

    @staticmethod
    def _delete_parameter(env):
        param = env['ir.config_parameter'].search([
            ('key', '=', FULL_TEXT_SEARCH_PARAM_KEY)
        ])
        if param:
            param.unlink()

    @staticmethod
    def _index_exists(env):
        # SQL query adapted from
        # https://stackoverflow.com/questions/2204058/list-columns-with-indexes-in-postgresql
        env.cr.execute("""
            SELECT 1
            FROM pg_class t, pg_class i, pg_index ix
            WHERE t.oid = ix.indrelid
            AND i.oid = ix.indexrelid
            AND t.relname = 'project_task'
            AND i.relname = %(index_name)s;
        """, {
            'index_name': FULL_TEXT_SEARCH_INDEX_NAME,
        })
        return len(env.cr.fetchall()) == 1
