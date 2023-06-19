Project Timesheet Time Control And Project WIP Supply Cost - Resolve Dysfunction
================================================================================
This module resolves the dysfunction caused when installing the modules:

- ``project_wip_supply_cost``
- ``project_timesheet_time_control``

Bug:
----
When we switch to a new timer and the system modify the previous timesheet line to set the amount,
we consider that 2 extra lines are added by the Project WIP Supply Cost and those lines doesn't contain any employee.

The error is reported in the context of the project 'Fix', see screenshot bellow:

.. image:: static/description/bug_project_timesheet_time_control.png

Solution:
---------

Before creating a shop supply line, it is necessary to remove either the
default project or default task that is associated with the analytic line
created when clicking the "start work" button. The shop supply line should
not be linked to any task or project.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
