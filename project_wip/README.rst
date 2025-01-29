Project Work In Progress
========================
This module enables to manage ``Work In Progress`` (WIP) accounting.

.. contents:: Table of Contents

Work In Progress
----------------
``Work In Progress`` is an account of the general ledger.

It includes consumed products, direct labour costs and factory overhead costs
related to an unfinished manufacturing project.

Once a project is delivered, the costs associated to this project are transfered
to the ``Cost of Finished Goods`` (CFG) or to the ``Cost of Goods Sold`` (CGS).

Cost of Finished Goods
----------------------
``Cost of Finished Goods`` (CFG) is a step between WIP and CGS.

It represents finished products that are still in inventory.
Not all companies maintain a CFG account, depending on their business requirements.

The current module does not implement CFG.
The costs of a project are transfered directly to the CGS when the project is finished.

Configuration
-------------

As member of the group ``Invoicing/Billing Administrator`` and has technical group ``Show Full Accounting Features`` checked:

  .. image:: static/description/invoicing_access.png

  - I go to ``Invoicing/Configuration/Chart of Accounts``:

    * I create a new account for *WIP* with ``Àllow Reconciliation`` checked:

      .. image:: static/description/wip_account.png


    * I create a new account fot *CGS* with ``Àllow Reconciliation`` checked:

      .. image:: static/description/cgs_account.png

  - I go to ``Invoicing/Configuration/Journals``:

    * I create a tranfert journal from *WIP* to *CGS*, I set journal type to ``Miscellaneous`` and give the journal a short code:

      .. image:: static/description/transfert_journal.png


As member of the group ``Project/Manager``, I go to ``Project/Configuration/Project Types``:

  - I create a new type that can be applied for projects.

    .. image:: static/description/project_type.png

  - I can see a new page ``Accounting`` is added to the type form view.
  - I fill the fields ``WIP Account``, ``WIP To CGS Journal`` and ``CGS Account`` that already have been created.

    *WIP To CGS Journal* : This journal will be used when transfering WIP journal items into CGS.

    *WIP Account* : This account will be used to cumulate Work In Progress.

    *CGS Account* : This account will be used to cumulate Costs of Goods Sold.

    .. image:: static/description/project_type_accounting.png


How The Module Works
--------------------
As member of the group ``Project/Manager``, I create a project and give it a ``Type`` with configured accounts and an ``Analytic Account``:

  .. image:: static/description/project_with_type.png

As member of the group ``Invoicing/Billing Administrator`` and has technical groups ``Show Full Accounting Features`` and ``Analytic Accounting`` checked,

- I go to ``Invoicing/Accounting/Journal Entries``,

- I create 3 journal entries with ``No Analytic Lines`` checked:
  
  A mecanism is added by the module to prevent creating analytic entries for an account move.
  creating 2 analytic entries for this move would only pollute the database. One analytic entry would cancel the other.
  To use this feature, the field ``No Analytic Lines`` can be checked before posting the account move.

  * One entry for raw materials.

    .. image:: static/description/raw_material_entry.png

  * One entry for direct labour.

    .. image:: static/description/direct_labour_entry.png

  * One entry for outsourcing.

    .. image:: static/description/outsourcing_entry.png


- In the general ledger, I filter for the WIP account. The balance of the account is $ 300.00.

  .. image:: static/description/general_ledger_before_wip_to_cgs.png


- Back to the form view of my project, I click on ``Transfer WIP To CGS``.

  .. image:: static/description/project_wip_to_cgs_button.png


- A wizard is appears. It allows to select a specific accounting date for the transfer.
  By default, the current date is selected.

  .. image:: static/description/wip_to_cgs_wizard.png


- I click on ``Validate``.


- Back to the general ledger, I notice that the balance of the WIP account is null.

  .. image:: static/description/general_ledger_after_wip_to_cgs.png

  Every debit in the WIP account is reconciled with its related credit.

- In the ``Cost of Goods Sold`` account, I notice 3 journal items.

  .. image:: static/description/general_ledger_cgs_account.png


The transfers from WIP to CGS did not create extra analytic entries.


Repeating the Operation
-----------------------
The operation can be repeated multiple times. Each time, only the new WIP entries will be transfered to CGS.

If I go back to the project form and click on the button. The wizard will show $ 0.00 to transfer.

  .. image:: static/description/wip_to_cgs_wizard_2nd_time.png


Releases
--------
Since the version 1.1.0 of the module, the button to open the wizard on a project is only visible to
a new group named 'Transfer WIP to CGS'.

  .. image:: static/description/wip_to_cgs_group.png

Users do not need to be members of Project / Manager to transfer the journal entries.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
