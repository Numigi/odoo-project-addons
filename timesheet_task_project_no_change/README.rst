Timesheet Task Project No Change
================================

Usage
-----

As a user of the **Project** module, when attempting to change the project of a task:

1. If timesheets have already been recorded on the task, a blocking message will appear:
   
   .. image:: static/description/task_timesheet_error.png
      :alt: Blocking error when task has timesheets

2. If timesheets have been recorded on a subtask, a similar blocking message will appear:
   
   .. image:: static/description/subtask_timesheet_error.png
      :alt: Blocking error when subtask has timesheets

3. In both cases, the task's project cannot be changed unless no timesheets exist for the task or its subtasks.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
