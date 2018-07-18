Project Accurate Time Spent
===========================
In Odoo, the time spent on a task is complex to understand and explain to people.

Before installing the module, the behavior is the following:

* Hours Spent (effective_hours): The time spent on the task
* Sub-tasks Hours (children_hours):
    * The total time spent on archived sub-tasks
    * Plus: the time spent on sub-tasks that are not archived for which the estimated time is exceeded.
    * Plus: the estimated time on sub-tasks that are not archived for which the estimated time is not exceeded.
* Total Hours (total_hours_spent): Hours Spent + Sub-tasks Hours
* Remaining Hours (remaining_hours): Initially Planned Hours - Total Hours

After installing the module, the behavior is the following:

* Hours Spent (effective_hours): The time spent on the task
* Sub-tasks Hours (children_hours): The time spent on sub-tasks
* Total Hours (total_hours_spent): Hours Spent + Sub-tasks Hours
* Remaining Hours (remaining_hours): Initially Planned Hours - Total Hours

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
