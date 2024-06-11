# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.addons.project.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem
from odoo.tools.safe_eval import safe_eval


class CustomerPortal(CustomerPortal):
    @http.route(
        ["/my/tasks", "/my/tasks/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_tasks(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        groupby="project",
        indicator="empty",
        **kw
    ):
        super(CustomerPortal, self).portal_my_tasks(
            page=page,
            date_begin=date_begin,
            date_end=date_end,
            sortby=sortby,
            filterby=filterby,
            search=search,
            search_in=search_in,
            groupby=groupby,
            **kw
        )
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Title"), "order": "name"},
            "stage": {"label": _("Stage"), "order": "stage_id"},
            "update": {
                "label": _("Last Stage Update"),
                "order": "date_last_stage_update desc",
            },
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {
            "content": {
                "input": "content",
                "label": _('Search <span class="nolabel"> (in Content)</span>'),
            },
            "message": {"input": "message", "label": _("Search in Messages")},
            "customer": {"input": "customer", "label": _("Search in Customer")},
            "stage": {"input": "stage", "label": _("Search in Stages")},
            "all": {"input": "all", "label": _("Search in All")},
        }
        searchbar_groupby = {
            "none": {"input": "none", "label": _("None")},
            "project": {"input": "project", "label": _("Project")},
        }

        records = request.env["project.steering.kpi"].search(
            [
                ("model_id.model", "=", "project.task"),
                ("available_on_portal", "=", True),
            ]
        )

        # Indicator from project steering KPI is used to filter tasks
        searchbar_indicators = {
            str(record.id): {"label": _(record.name), "domain": record.filter_domain}
            for record in records
        }
        prepend_item = {"empty": {"label": _("None"), "domain": []}}
        searchbar_indicators = {**prepend_item, **searchbar_indicators}

        # extends filterby criteria with project the customer has access to
        projects = request.env["project.project"].search([])
        for project in projects:
            searchbar_filters.update(
                {
                    str(project.id): {
                        "label": project.name,
                        "domain": [("project_id", "=", project.id)],
                    }
                }
            )

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env["project.task"].read_group(
            [("project_id", "not in", projects.ids)], ["project_id"], ["project_id"]
        )
        for group in project_groups:
            proj_id = group["project_id"][0] if group["project_id"] else False
            proj_name = group["project_id"][1] if group["project_id"] else _("Others")
            searchbar_filters.update(
                {
                    str(proj_id): {
                        "label": proj_name,
                        "domain": [("project_id", "=", proj_id)],
                    }
                }
            )

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("project.task", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ("content", "all"):
                search_domain = OR(
                    [
                        search_domain,
                        [
                            "|",
                            ("name", "ilike", search),
                            ("description", "ilike", search),
                        ],
                    ]
                )
            if search_in in ("customer", "all"):
                search_domain = OR([search_domain, [("partner_id", "ilike", search)]])
            if search_in in ("message", "all"):
                search_domain = OR(
                    [search_domain, [("message_ids.body", "ilike", search)]]
                )
            if search_in in ("stage", "all"):
                search_domain = OR([search_domain, [("stage_id", "ilike", search)]])
            domain += search_domain

        # Filter by indicator
        if indicator != "empty":
            domain += safe_eval(searchbar_indicators[indicator]["domain"])

        # task count
        task_count = request.env["project.task"].search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tasks",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
                "indicator": indicator,
            },
            total=task_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        if groupby == "project":
            order = (
                "project_id, %s" % order
            )  # force sort on project first to group by project in view
        tasks = request.env["project.task"].search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=(page - 1) * self._items_per_page,
        )
        request.session["my_tasks_history"] = tasks.ids[:100]
        if groupby == "project":
            grouped_tasks = [
                request.env["project.task"].concat(*g)
                for k, g in groupbyelem(tasks, itemgetter("project_id"))
            ]
        else:
            grouped_tasks = [tasks]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "grouped_tasks": grouped_tasks,
                "page_name": "task",
                "archive_groups": archive_groups,
                "default_url": "/my/tasks",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "searchbar_indicators": searchbar_indicators,
                "search_in": search_in,
                "sortby": sortby,
                "groupby": groupby,
                "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
                "filterby": filterby,
                "indicator": indicator,
            }
        )
        return request.render("project.portal_my_tasks", values)

    @http.route(
        ["/my/projects", "/my/projects/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_projects(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        indicator="empty",
        **kw
    ):
        super(CustomerPortal, self).portal_my_projects(
            page=page, date_begin=date_begin, date_end=date_end, sortby=sortby, **kw
        )
        values = self._prepare_portal_layout_values()
        Project = request.env["project.project"]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }

        records = request.env["project.steering.kpi"].search(
            [
                ("model_id.model", "=", "project.project"),
                ("available_on_portal", "=", True),
            ]
        )

        # Indicator from project steering KPI is used to filter tasks
        searchbar_indicators = {
            str(record.id): {"label": _(record.name), "domain": record.filter_domain}
            for record in records
        }
        prepend_item = {"empty": {"label": _("None"), "domain": []}}
        searchbar_indicators = {**prepend_item, **searchbar_indicators}

        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("project.project", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        # Filter by indicator
        if indicator != "empty":
            domain += safe_eval(searchbar_indicators[indicator]["domain"])

        # projects count
        project_count = Project.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/projects",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "indicator": indicator,
            },
            total=project_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        projects = Project.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_projects_history"] = projects.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "projects": projects,
                "page_name": "project",
                "archive_groups": archive_groups,
                "default_url": "/my/projects",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "indicator": indicator,
                "searchbar_indicators": searchbar_indicators,
            }
        )
        return request.render("project.portal_my_projects", values)
