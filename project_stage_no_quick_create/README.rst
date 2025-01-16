Project Stage No Quick Create
=============================

This module prevents the quick creation of project stages.

*Before installing the module*:

.. image:: static/description/quick_create_project_stage_enabled.png

*After installing the module*:

.. image:: static/description/quick_create_project_stage_disabled.png

It also add the field `type_ids` (Task Stages) on the project form.

.. image:: static/description/project_stages_form_view.png

It also remove the view of all project linked to the project stage, only in form view.
It is always in the tree view.

*Before installing the module*:

.. image:: static/description/projects_linked_to_project_stage_visible.png

*After installing the module*:

.. image:: static/description/projects_linked_to_project_stage_invisible.png

Same Stages for All Projects
----------------------------
If you need to have the same stages for all project:

* Activate the developer mode.
* Go to /Settings/Technical/Actions/User-defined Defaults.
* Click on `Create`.
* In `Field` select `Tasks Stages (project.project)`.
* In `Default Value (JSON format)` enter `[[6, 0, [n1, n2, ..., n]]]`
  where [n1, n2, ..., n] is the list of ids of the stages.

Example:

.. image:: static/description/user_defined_defaults_tasks_stages.png

After creating a new project with the previous configuration, the default stages will be as follows:

.. image:: static/description/user_defined_defaults_example.png

Whenever you want to update the default stages, you may edit this default value.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
* Istvan Szalai (istvan.szalai@savoirfairelinux.com)

More information
----------------
* Meet us at https://bit.ly/numigi-com
