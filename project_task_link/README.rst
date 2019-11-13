Project Task Link
=================
This module allows to insert dynamic links in the description of tasks.

.. contents:: Table of Contents

Overview
--------
As member of the group ``Project / User``, I go the form view of a task.

.. image:: static/description/task_form.png

In the description, I need to reference the task ID=18.
Therefore, I write ``TA#18`` in the description.

.. image:: static/description/task_form_edit_mode.png

When I save, I notice that a link was inserted dynamically.

.. image:: static/description/task_form_saved.png

If I click on the link, the referenced task is open.

.. image:: static/description/linked_task_form.png

Portal
~~~~~~
As user of the portal, I go to the form view of the task.

.. image:: static/description/portal_task_with_link.png

When I click on a dynamic link, the referenced task is open in a new window.

.. image:: static/description/portal_linked_task.png

Advanced Setup
--------------
By default, the system uses the following regex to detect where to insert dynamic links:

..

    [Tt][Aa]\#?(?P<id>\d+)

This means that inserting either ``TA#123``, ``ta#123``, ``TA123`` or ``ta123``
will generate a link that point to the task with ID=123.

To customize the format of references, please refer to the module `project_task_reference <https://github.com/Numigi/odoo-project-addons/tree/12.0/project_task_reference>`_.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
