# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from lxml import etree
from odoo import api, models
from urllib.parse import urljoin


TA_REF_REGEX = r'[Tt][Aa]\#?\d+'


def _get_task_from_ref(env: 'Environment', task_ref: str) -> 'project.task':
    task_id = int(''.join(c for c in task_ref if c.isdigit()))
    return env['project.task'].sudo().browse(task_id)


def _get_link_from_task(task: 'project.task') -> str:
    return "<a href=\"{url}\" target=\"_blank\">{task_ref}</a>".format(
        url=task.get_portal_access_url(),
        task_ref="TA#{}".format(task.id),
    )


def _convert_text_to_html_with_task_links(env: 'Environment', text: str) -> str:
    for task_ref in re.findall(TA_REF_REGEX, text):
        print(task_ref)
        task = _get_task_from_ref(env, task_ref)
        task_link = _get_link_from_task(task)
        text = text.replace(task_ref, task_link)
    return "<span>{}</span>".format(text)


def _contains_task_reference(text: str) -> bool:
    return bool(re.search(TA_REF_REGEX, text))


def _add_task_links_to_xml_node(env: 'Environment', node: 'ElementTree'):
    if node.text and _contains_task_reference(node.text):
        text_html_with_links = _convert_text_to_html_with_task_links(env, node.text)
        text_tree_with_links = etree.fromstring(text_html_with_links)
        node.insert(0, text_tree_with_links)
        node.text = ""

    child_nodes_with_ref = (c for c in node if c.tail and _contains_task_reference(c.tail))
    for child in child_nodes_with_ref:
        tail_html_with_links = _convert_text_to_html_with_task_links(env, child.tail)
        tail_tree_with_links = etree.fromstring(tail_html_with_links)
        position = node.index(child) + 1
        node.insert(position, tail_tree_with_links)
        child.tail = ""


def _get_html_with_task_links(env: 'Environment', html: str) -> str:
    html_tree = etree.fromstring("<div>{}</div>".format(html))
    nodes_not_inside_link = html_tree.xpath("//*[not(self::a)][not(ancestor::a)]")

    for node in nodes_not_inside_link:
        _add_task_links_to_xml_node(env, node)

    return etree.tostring(html_tree)


class Task(models.Model):

    _inherit = 'project.task'

    def get_portal_access_url(self):
        base_url = self.get_base_url()
        return urljoin(base_url, self.access_url)

    def _add_task_links_to_description(self):
        for task in self.with_context(no_project_task_link=True):
            task.description = _get_html_with_task_links(self.env, task.description)

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if vals.get('description') and not self._context.get('no_project_task_link'):
            self._add_task_links_to_description()
        return res

    @api.model
    def create(self, vals):
        task = super().create(vals)
        if task.description:
            task._add_task_links_to_description()
        return task
