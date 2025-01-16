Project Task Reference
======================
This is a technical module. It has no functional use on its own.

It allows to extract a reference to a task from a string and provides tools to normalize and locate tasks based on these references.

.. contents:: Table of Contents

Basic Usage
-----------
The module adds a method ``_search_references_from_text`` in the ``project.task`` model.

This method allows you to extract and validate references to tasks from a given text input.

.. code-block:: python

    some_text = "ta#123 Some commit message"
    reference = env['project.task']._search_references_from_text(some_text)[0]
    assert reference[task] == env['project.task'].browse(123)
    assert reference[string] == "ta#123"
    assert reference[normalized_string] == "TA#123"


The method identifies references anywhere within the given text.
It is flexible and tolerant of minor variations, such as case differences or missing # symbols.

Supported Reference Variations:
- ta#123
- TA123
- Ta#123

By default, these references correspond to tasks with the ID 123 in the database.

Advanced Configuration
----------------------

The reference parsing and normalization behavior can be customized using system parameters:

* 1- Regex for Parsing References: ``project_task_reference.regex``

- Default: [tT][aA]#?(?P<id>\d+)

- Example: Matching TA#123 or ta123.

* 2- Format for Normalizing References: ``project_task_reference.format``

- Default: TA#{id}

- Example: Converts any recognized format into TA#123.

Customization Example
---------------------

If your references should follow the format [ST#123], update the system parameters as follows:

``project_task_reference.regex``: \[?[sS][tT]#?(?P<id>\d+)\]?

``project_task_reference.format``: [ST#{id}]

This configuration would allow parsing strings like [St#123] and normalize them to the format [ST#123].

The regex must contain a parameter ``(?P<id>\d+)`` (the database ID of the task).

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
