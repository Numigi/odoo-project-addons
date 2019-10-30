Project Template
================
This module allows to define project and task templates.

.. contents:: Table of Contents

Task Templates
--------------
A task template is a task, but with a special flag activated.

.. image:: static/description/task_template_form_checkbox.png

Warning Message
~~~~~~~~~~~~~~~
A warning message is displayed on the form view to signal that the user that
task being edited is a template.

.. image:: static/description/task_template_form_checkbox.png

Hidden Fields
~~~~~~~~~~~~~
Multiple fields are hidden in the form of view of task templates including:

* Project
* Assigned To
* Customer
* Kanban State

These fields are not relevant for a template.

Some irrelevant smart buttons are also hidden.

Search Filters
~~~~~~~~~~~~~~
By default task flagged as template do not appear in search results.

In list / kanban / pivot views, tasks templates can be shown by activating the ``Task Templates`` filter.

.. image:: static/description/task_template_filter.png

By selecting both ``Task Templates`` and ``Tasks`` filters, both templates and normal tasks are shown together.

.. image:: static/description/task_template_filter.png

Known Issues
------------
For now project templates are not implemented. This will be implemented in this module.

Integration with timesheets will also be implemented in a separate module (`project_template_timesheet`).

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
