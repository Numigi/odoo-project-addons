=======================================
Project Milestone Progress Notification
=======================================
This module allows you to send email notifications to the project manager when a project milestone percent is reached.

Usage
-----
To use this module, you need to:
* Go to `Project > Configuration > Settings` and enable the option "Milestone progression notification" (by default enabled) in `Notifications` section.
* By default, a mail template is created with the subject "Milestone Progress Notification" and set by default. You can customize it as needed.
* Set the rate limit of milestone to notify the project manager when the progression is reached.

.. image:: static/description/milestone_notification_configuration.png

When the milestone progress reaches the rate limit, an email is sent to the project manager.

.. image:: static/description/milestone_progression.png

.. image:: static/description/mail_notification.png

Use cases
---------
1. Initial rate for notification configured is 60%.
I have a project with a milestone. The milestone have 2 tasks.
The milestone progress is 50%.
I do some changes on tasks to increase the progress.
Now, milestone progress reaches 67%, a notification email is sent.

Il all task was completed, the milestone progress should be 100%, and no additional email is sent.

I can have the progress to 0%, with a specific reason.
But if the milestone progress is back to 67% or greater by completing tasks, another notification email is sent.


2. If I change the notification rate to 33%. And progress change to 33.33%, triggering another notification email.
But after that I change the notification rate to 90%, and the milestone progress is 100%, this should trigger a final notification email.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
