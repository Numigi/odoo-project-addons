/**
 * Tests for the module project_template.
 *
 * This module contains a javascript file that allows to declare a task/project field
 * as invisible if the record is a template.
 */

import { Selector } from 'testcafe'
import { login, openAllTaskKanban, openAnyKabanRecord, clickEditButton } from './common'

fixture `Test the project_template module`
    .page `odoo:8069/web`;

function openExtraInfoTab(t){
    var tab = Selector("a[role='tab']").withText("Extra Info")
    return t.click(tab);
}

function checkIsTemplate(t){
    return t.click(".o_field_boolean[name='is_template']");
}

/**
 * This test opens the form view of any task and checks the is_template box.
 * After the box is checked, the field user_id is expected to be invisible.
 */
test('If after is_template checked, field user_id is hidden', async (t) => {
    await login(t, 'admin', 'admin')
    await openAllTaskKanban(t)
    await openAnyKabanRecord(t)
    await clickEditButton(t)
    await openExtraInfoTab(t)

    var invisibleUserField = Selector(".o_field_widget[name='user_id'].o_invisible_modifier");
    await t.expect(invisibleUserField.exists).notOk();

    await checkIsTemplate(t)

    await t.expect(invisibleUserField.exists).ok();
});
