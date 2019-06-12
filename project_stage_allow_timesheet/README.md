# Project Stage Allow Timesheet

This module adds the notion of time sheet on project stages.
With this implementation, the field allow_timesheets on project is now readonly and it
is driven by the stage the project is in.

![Stage Form](static/description/project_stage_form.png?raw=true)

![Stage List](static/description/project_stage_list.png?raw=true)

Additionally, the module implements two new constraints that avoid to move time sheets in a project that does not
allow time sheets.


![Task Error](static/description/task_error.png?raw=true)
*It is now forbidden to move a task with time sheets to a project that does not allow time sheets.* 


![Timesheet Error](static/description/timesheet_error.png?raw=true)
*It is not forbidden to move a time sheet into another task if the project does not allow time sheets.*

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
