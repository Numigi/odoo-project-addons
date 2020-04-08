Project Stage No Quick Create
=============================

This module prevents the quick creation of project stages.

It also add the field stage_ids on the project form.

Same Stages for All Projects
----------------------------
If you need to have the same stages for all project:

* Activate the developer mode.
* Go to /Settings/Technical/Actions/User-defined Defaults.
* Click on `Create`.
* In `Field` select `Tasks Stages (project.project)`.
* In `Default Value (JSON format)` enter `[[6, 0, [n1, n2, ..., n]]]`
  where [n1, n2, ..., n] is the list of ids of the stages.

Whenever you want to update the default stages, you may edit this default value.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
* Istvan Szalai (istvan.szalai@savoirfairelinux.com)

More information
----------------
* Meet us at https://bit.ly/numigi-com
