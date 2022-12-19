# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo.addons.project_task_reference.reference import TaskReference
from typing import List


def _find_task_references(env: 'Environment', text: str) -> List[TaskReference]:
    return env['project.task']._search_references_from_text(text)


def _convert_text_to_html_with_task_links(env: 'Environment', text: str) -> str:
    """Convert the given text into HTML containing task links.

    The &#8291; character is an invisible separator.
    It prevents a user (with large fingers) from inserting text inside an
    existing link by accident.
    """
    for reference in _find_task_references(env, text):
        link = "&#8291;<a href=\"{url}\" target=\"_blank\">{ref}</a>&#8291;".format(
            url=reference.task.get_portal_access_url(),
            ref=reference.normalized_string,
        )
        text = text.replace(reference.string, link)

    return "<span>{}</span>".format(text)


def _contains_task_reference(env: 'Environment', text: str) -> bool:
    return bool(_find_task_references(env, text))


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
