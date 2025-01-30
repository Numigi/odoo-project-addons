Project Parent Enhanced
=======================

This module enhances the functionality of parent-child relationships between projects and tasks in Odoo. 
It builds upon the features of the `project_parent` module from OCA.
Adding new constraints, methods, and views to better manage project hierarchies.

Dependencies
------------
This module depends on the following OCA module:
- `project_parent`: https://github.com/OCA/project/tree/16.0/project_parent

Features
--------

**Enhanced Constraints**
   - Prevent a project from being its own parent.
   - Ensure that a child project cannot have further child projects.

**Follower Propagation**
   - Automatically propagate followers from a parent project to its child projects.

**Tasks Group by Parent Projects**
   - Add a new group option to group tasks by their parent projects.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/static/description/task_group_by_parent.png

** Search and Filter Project by Parent Projects**

   - Add a new search filter to search projects by their parent projects.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/static/description/search_project_by_parent.png

   - The filter by parent project is also available

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/static/description/filter_project_by_parent_project.png

**View Adjustments**
   - Replace project names with their `display_name` to show the hierarchy in views.

In the Kanban view:

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/static/description/iteration_name_kanban_view.png

In the List view:

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/static/description/iteration_name_list_view.png

   - Add a filter on the `parent_id` field in the project form view to display only parent projects.

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/static/description/project_list.png

.. image:: https://raw.githubusercontent.com/Numigi/odoo-project-addons/16.0/project_parent_enhanced/static/description/project_view_form.png

Contributors
------------
- Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More Information
----------------
For more details, visit:
- https://github.com/OCA/project/tree/16.0/project_parent
