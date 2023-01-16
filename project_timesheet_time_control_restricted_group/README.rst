Project Timesheet Time Control Employee PIN
-------------------------------------------

Overview
--------
This module adds group to limit access to launch the timer except from Task Kanban View

The module depends of `project_timesheet_time_control <https://github.com/OCA/project/tree/12.0/project_timesheet_time_control>`_ module

Configuration
-------------

As a user who can manage user rights, I go to the form view of a user.
I see that a new group of rights `Timer: Limited access - task kanban view` is present.
I check the box and save the changes.

.. image:: static/description/group_limited_access.png


Usage
-----

As a user with group `Timer: Limited access - task kanban view`, I go to the Projects application.
I see that the timer launch button icon is only available from the `Task Kanban` view.

.. image:: static/description/task_kanban_view_start_timer.png

The timer is no longer displayed on the kanban and list views of `Projects`.

.. image:: static/description/project_kanban_view_without_timer.png

.. image:: static/description/project_list_view_without_timer.png

The timer is no longer displayed on the form and list views of `Tasks`.

.. image:: static/description/task_form_view_without_timer.png

.. image:: static/description/task_list_view_without_timer.png

The timer is no longer displayed on the list view of `Timesheets` from a task.

.. image:: static/description/timesheet_list_without_timer.png


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
