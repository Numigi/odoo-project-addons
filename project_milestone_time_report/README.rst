Project Milestone Time Report
=============================

.. contents:: Table of Contents

Summary
-------
Add a dynamic milestone time report on projects.

Usage
-----
Go to the form view of a project.

A new smart button ``Milestone Time Report``.

    .. image:: project_milestone_time_report/static/description/milestone_time_report.png
        :width: 100%
        :align: center
        :height: 600px
        :alt: milestone_time_report

Click on the button. The report is displayed.

    .. image:: project_milestone_time_report/static/description/report.png
        :width: 100%
        :align: center
        :height: 300px
        :alt: Report

Estimated Hours
----------------
When clicking on an amount of estimated hours, the list of milestones composing this amount is displayed.

    .. image:: project_milestone_time_report/static/description/milestone_time_click.png
        :width: 100%
        :align: center
        :height: 300px
        :alt: milestone_time_click

    .. image:: project_milestone_time_report/static/description/milestone_list.png
        :width: 100%
        :align: center
        :height: 300px
        :alt: milestone_list

Consumed Hours
--------------
When clicking on an amount of consumed hours, the list of analytic lines composing this amount is displayed.

    .. image:: project_milestone_time_report/static/description/report_consumed_hours.png
        :width: 100%
        :align: center
        :height: 300px
        :alt: report_consumed_hours

    .. image:: project_milestone_time_report/static/description/analytic_line_list.png
        :width: 100%
        :align: center
        :height: 300px
        :alt: analytic_line_list

Lump Sum Projects
-----------------
When a sub-project is a lump sum, it is excluded from the report.

    .. image:: project_milestone_time_report/static/description/analytic_line_list_no_lump_sum.png
        :width: 100%
        :align: center
        :height: 300px
        :alt: analytic_line_list_no_lump_sum

See module `project_lump_sum <https://github.com/Numigi/odoo-project-addons/tree/12.0/project_lump_sum>`_ for more details.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
