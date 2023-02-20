Project Task Kanban Sequence Fixed
==================================

.. contents:: Table of Contents

Context
-------
The module ``project_task_kanban_sequence_fixed`` will block the drag and drop on the ``stage`` column in kanban view of project task.

This is to prevent all user to accidentally change the sequence of stage.

Usage
-----
Make sure that project is installed. So I have the main project menu.

.. image:: static/description/opening_project_menu.png

After that, I go to project then click on one record. It will show a list of task linked to this project in a kanban view.

.. image:: static/description/opening_project.png

In the kanban view, the pointer will change to ``not allowed`` style when attempting to drag and drop the column.

.. image:: static/description/pointer_preventing_moving_column_1.png

Same thing if attempting to drag and drop a folded column.

.. image:: static/description/pointer_preventing_moving_column_2.png

A pop-up will be show if I am always trying to drag and drop the column.

.. image:: static/description/pop_up_drag_and_drop_not_allowed.png


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
