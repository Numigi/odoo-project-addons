Project Timesheet Time Control And Project WIP - Resolve Dysfunction
====================================================================
This module resolves the dysfunction caused when installing the modules:

- ``project_wip_timesheet``
- ``project_wip_supply_cost``
- ``project_timesheet_time_control``

When we switch to a new timer and the system modify the previous timesheet line to set the amount,
we consider that 2 extra lines are added by the Project WIP modules and those lines doesn't contain employee.

The error is reported in the context of the project 'Fix', see screenshot bellow:

.. image:: static/description/bug_project_timesheet_time_control.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
