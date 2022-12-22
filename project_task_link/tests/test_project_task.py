# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data, unpack
from odoo.tests import common
from urllib.parse import urljoin


@ddt
class TestProjectTask(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.task = cls.env['project.task'].create({'name': 'My Task'})
        cls.referenced_task = cls.env['project.task'].create({'name': 'Some Referenced Task'})
        cls.referenced_task_url = cls.referenced_task.get_portal_access_url()
        cls.task_ref = "TA#{}".format(cls.referenced_task.id)
        cls.task_link = "<a href=\"{url}\" target=\"_blank\">{task_ref}</a>".format(
            url=cls.referenced_task_url,
            task_ref=cls.task_ref,
        )

        cls.referenced_task_2 = cls.env['project.task'].create({'name': 'Some Other Task'})
        cls.referenced_task_url_2 = cls.referenced_task_2.get_portal_access_url()
        cls.task_ref_2 = "TA#{}".format(cls.referenced_task_2.id)
        cls.task_link_2 = "<a href=\"{url}\" target=\"_blank\">{task_ref}</a>".format(
            url=cls.referenced_task_url_2,
            task_ref=cls.task_ref_2,
        )

        cls.base_url = cls.env['ir.config_parameter'].get_param('web.base.url')

    def test_task_url_link(self):
        expected_url = urljoin(self.base_url, "/my/task/{}".format(self.task.id))
        assert self.task.get_portal_access_url() == expected_url

    @data(
        "Refer to {task_ref} for more information.",
        """
        Development of a coffee machine app.

        Refer to {task_ref} for more information.
        """,
        """
        <p>Development of a coffee machine app.</p>

        Refer to {task_ref} for more information.
        """,
        """
        <p>Development of a coffee machine app.</p>

        Refer to {task_ref} for more information.

        <p>Third paragraph</p>
        """,
    )
    def test_on_write__task_link_added_to_description(self, description):
        self.task.write({'description': description.format(task_ref=self.task_ref)})
        assert self.task_link in self.task.description

    def test_on_create__task_link_added_to_description(self):
        new_task = self.task.copy({'description': self.task_ref})
        assert self.task_link in new_task.description

    @data(
        "Refer to <a>{task_ref}<a> for more information.",
        "Refer to <a><button>{task_ref}</button><a> for more information.",
    )
    def test_if_task_ref_inside_link_node__no_link_node_added(self, description):
        self.task.write({'description': description.format(task_ref=self.task_ref)})
        assert self.task_link not in self.task.description

    @data(
        "{task_ref}{task_ref_2}",
        "{task_ref}<br>{task_ref_2}",
    )
    def test_two_task_refs_in_same_descriptions(self, description):
        self.task.write({
            'description': description.format(
                task_ref=self.task_ref,
                task_ref_2=self.task_ref_2,
            ),
        })
        assert self.task_link in self.task.description
        assert self.task_link_2 in self.task.description

    @data(
        "TA{}",
        "TA#{}",
        "ta{}",
        "ta#{}",
    )
    def test_task_ref_in_similar_format(self, ref_format):
        self.task.write({'description': ref_format.format(self.referenced_task.id)})
        assert self.task_link in self.task.description

    @data(
        "<p><br>{task_ref}</p>",
        "<p>{task_ref}",
    )
    def test_can_parse_broken_html(self, description):
        self.task.write({'description': description.format(task_ref=self.task_ref)})
        assert self.task_link in self.task.description

    @data(
        ("Refer to TI#{} for more detail.", r'TI#(?P<id>\d+)', 'TI#{id}'),
        ("Refer to TA{} for more detail.", r'TA(?P<id>\d+)', 'Ticket ({id})'),
        ("Refer to [st#{}] for more detail.", r'\[?[sS][tT]#?(?P<id>\d+)\]?', '[ST#{id}]'),
        ("Refer to [ST{}] for more detail.", r'\[?[sS][tT]#?(?P<id>\d+)\]?', '[ST#{id}]'),
        ("Refer to ST{} for more detail.", r'\[?[sS][tT]#?(?P<id>\d+)\]?', '[ST#{id}]'),
    )
    @unpack
    def test_links_with_custom_regex(self, description, regex, ref_format):
        self.env['ir.config_parameter'].set_param('project_task_reference.regex', regex)
        self.env['ir.config_parameter'].set_param('project_task_reference.format', ref_format)

        self.task.write({'description': description.format(self.referenced_task.id)})

        expected_link = "<a href=\"{url}\" target=\"_blank\">{task_ref}</a>".format(
            url=self.referenced_task_url,
            task_ref=ref_format.format(id=self.referenced_task.id),
        )

        assert expected_link in self.task.description
