# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase
from datetime import datetime
from dateutil.relativedelta import relativedelta


_intervalTypes = {
    'work_days': lambda interval: relativedelta(days=interval),
    'days': lambda interval: relativedelta(days=interval),
    'hours': lambda interval: relativedelta(hours=interval),
    'weeks': lambda interval: relativedelta(days=7*interval),
    'months': lambda interval: relativedelta(months=interval),
    'years': lambda interval: relativedelta(years=interval),
}


class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()

        self.PartnerObj = self.env['res.partner']
        self.TaskAutoCreateObj = self.env['partner.task.autocreate']
        self.partner = self.PartnerObj.create({
            'name': 'Autocreate Task Test Partner',
        })

    def test_partner_preference(self):
        partner = self.PartnerObj.create({'name': 'Test Partner Preference'})
        templateObj = self.env['project.task.template']
        taskObj = self.env['project.task']
        template = templateObj.create({
            'name': 'Test Template Preference',
        })
        self.partner_task_autocreate = self.TaskAutoCreateObj.create({
            'task_id': template.id,
            'partner_id': partner.id,
            'interval_number': 1,
            'interval_type': 'hours',
        })
        self.partner_task_autocreate.write(
            {'last_created': datetime.now() - _intervalTypes['hours'](2)}
        )
        self.partner_task_autocreate.create_tasks()
        tasks = taskObj.search(
            [('name', '=', template.name),
             ], limit=1)
        self.assertEqual(len(tasks), 1)
