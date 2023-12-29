Project Task Meeting Certificate
================================

.. contents:: Table of Contents

Context
-------
The module ``meeting_minutes_certificate`` defines the meeting minutes on tasks.

Overview
--------
This module adds a new tab ``Training Certificate`` on meeting minutes.

.. image:: static/description/meeting_minutes_form.png

This tab allows to manage signatures of the training certificate for each attendee.

Aeroo Report
~~~~~~~~~~~~
In this tab, I must select the Aeroo template that will be used to render the certificate.

.. image:: static/description/aeroo_report_template.png

This field can be set automatically using a default value.

Attendees
~~~~~~~~~
When adding or removing an attendee, the list of signatures is updated accordingly.

.. image:: static/description/attendees_changed.png

By default, when the meeting minutes is created, the list of signatures is already prefilled.

Trainer
~~~~~~~
The user assigned to the task is automatically defined as trainer.

.. image:: static/description/task_assigned_to.png

The column ``Type`` allows to distinguish between the trainer and the participants.

.. image:: static/description/trainer_signature.png

Also, the trainer is automatically defined as follower on the meeting minutes
(even if someone else initialized the meeting minutes).

.. image:: static/description/meeting_minutes_follower.png

Signature Request
~~~~~~~~~~~~~~~~~
A button allows to send the signature requests.

.. image:: static/description/signature_request_button.png

When clicking on the button, one email is sent to each attendee.

It is possible to resend the request to a single attendee.

.. image:: static/description/signature_request_resend_button.png

I can view the communication with a given attendee by clicking on the ``info`` icon.

.. image:: static/description/signature_info_icon.png

.. image:: static/description/signature_form_view.png

Portal
~~~~~~
In the email sent to the attendee, when clicking on the ``Sign`` button, the portal view
of the document to sign is opened.

The URL of the page contains the task ID and an access token.

.. image:: static/description/portal_form.png

Using this access token, the page can be opened without signin in.

When the user is logged in, a new menu item allows to access his training certificates.

.. image:: static/description/portal_menu.png

.. image:: static/description/portal_certificate_list.png

Signing The Certificate
~~~~~~~~~~~~~~~~~~~~~~~
From the page of the document to sign, I click on ``Sign``.

.. image:: static/description/sign_button.png

I fill my signature, then I click on ``Accept & Sign``.

.. image:: static/description/sign_modal.png

The document is updated with my signature.

.. image:: static/description/portal_form_signed.png

Signed Certificate
~~~~~~~~~~~~~~~~~~
When the certificate is signed by all attendees, an email containing the certificate is automatically
sent to each attendee individually.

.. image:: static/description/certificate_signed_email.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
