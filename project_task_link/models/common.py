# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from lxml import etree


DEFAULT_TASK_REF_REGEX = r'[Tt][Aa]\#?\d+'
DEFAULT_TASK_REF_FORMAT = "TA#{task_id}"


def _get_task_ref_regex(env: 'Environment') -> str:
    return (
        env['ir.config_parameter'].sudo().get_param('project_task_link.task_ref_regex') or
        DEFAULT_TASK_REF_REGEX
    )


def _get_task_ref_format(env: 'Environment') -> str:
    return (
        env['ir.config_parameter'].sudo().get_param('project_task_link.task_ref_format') or
        DEFAULT_TASK_REF_FORMAT
    )


def _get_task_from_ref(env: 'Environment', task_ref: str) -> 'project.task':
    task_id = int(''.join(c for c in task_ref if c.isdigit()))
    return env['project.task'].sudo().browse(task_id)


def _get_link_from_task(env: 'Environment', task: 'project.task') -> str:
    task_ref_format = _get_task_ref_format(env)
    return "<a href=\"{url}\" target=\"_blank\">{task_ref}</a>".format(
        url=task.get_portal_access_url(),
        task_ref=task_ref_format.format(
            task_id=task.id
        ),
    )


def _convert_text_to_html_with_task_links(env: 'Environment', text: str) -> str:
    task_ref_regex = _get_task_ref_regex(env)

    for task_ref in re.findall(task_ref_regex, text):
        task = _get_task_from_ref(env, task_ref)
        task_link = _get_link_from_task(env, task)
        text = text.replace(task_ref, task_link)

    return "<span>{}</span>".format(text)


def _contains_task_reference(env: 'Environment', text: str) -> bool:
    task_ref_regex = _get_task_ref_regex(env)
    return bool(re.search(task_ref_regex, text))


def _add_task_links_to_xml_node(env: 'Environment', node: 'ElementTree'):
    if node.text and _contains_task_reference(env, node.text):
        text_html_with_links = _convert_text_to_html_with_task_links(env, node.text)
        text_tree_with_links = etree.HTML(text_html_with_links)
        node.insert(0, text_tree_with_links)
        node.text = ""

    child_nodes_with_ref = (c for c in node if c.tail and _contains_task_reference(env, c.tail))
    for child in child_nodes_with_ref:
        tail_html_with_links = _convert_text_to_html_with_task_links(env, child.tail)
        tail_tree_with_links = etree.HTML(tail_html_with_links)
        position = node.index(child) + 1
        node.insert(position, tail_tree_with_links)
        child.tail = ""


def get_html_with_task_links(env: 'Environment', html: str) -> str:
    html_tree = etree.HTML(html)
    nodes_not_inside_link = html_tree.xpath("//*[not(self::a)][not(ancestor::a)]")

    for node in nodes_not_inside_link:
        _add_task_links_to_xml_node(env, node)

    return etree.tostring(html_tree, pretty_print=True, method='HTML')
