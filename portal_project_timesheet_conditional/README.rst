Portal Project List Hours Spent
===============================

.. contents:: Table of Contents

Overview
--------
Add column spent hours in portal projects and tasks lists conditionally.

Description
-----------

If a project has not a type or has a type with **Lump Sum** not checked, the module:
- Add column ``Total Spent Hours`` in portal list projects.
- Add column ``Spent hours`` in portal list tasks.

If a project has type with **Lump Sum** checked, the module hide ``Timesheets`` from portal task form view.

Usage
-----

- Create 2 projects, the first one has a type with Lump Sum checked and the second project has type with Lump Sum unchecked.
- Create tasks in each project and fill timesheet lines in those tasks.
- In portal projects list the Total Spent Hours will display only for the project which has type with ``Lump Sum`` unchecked.

    .. image:: ./static/description/portal_project_total_spent_hours.png

- In portal task list the Spent Hours will display only for the tasks of a project which has type with ``Lump Sum`` unchecked.

    .. image:: ./static/description/portal_tasks_spent_hours.png

- In portal task form the Timesheets will be hidden from a task of a project which has type with ``Lump Sum`` checked.


Contributors
------------

* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
