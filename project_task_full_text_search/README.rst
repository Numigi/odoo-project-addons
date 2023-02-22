Project Task Full Text Search
=============================
This module allows to search a task by its title and description.

When searching a task, a full text search is ran in postgresql.

The order of the searched words has no impact on the result.
The returned tasks are tasks for which the title / description contain every given words
(or similar words).

Usage
-----
* Go to Projects / Tasks
* In the search bar, type something and click on ``Search Full Text for: ...``.

Accents and Upper Cases
-----------------------
The content of a task is indexed without accents and in lower cases.

When searching using the full text search, accents are removed from the searched text
and upper cases are replaced with lower cases.

stemmings
---------
The content search uses stemmings to find similar text.

stemmings are rules applied by postgresql to match text in queries.
These rules depend on the language of the text searched.

Natively, postgresql supports the following languages:

* danish
* dutch
* english
* finnish
* french
* german
* hungarian
* italian
* norwegian
* portuguese
* romanian
* russian
* spanish
* swedish
* turkish

A list of available language can be found using the following SQL query:

`SELECT * FROM pg_catalog.pg_ts_dict;`

Configuration
-------------
By default, the text search language is set to english.

In order to set the search language to a given value (french for example):

* Go to: Settings / Technical / Parameters / System Parameters.
* Create a new entry.
* Set key to `postgresql_full_text_search_language`.
* Set value to `french` (or your prefered language).
* Save the new entry.

That's it, your task are now indexed under the new language.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
