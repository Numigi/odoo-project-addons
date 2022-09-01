
import { Selector } from "testcafe"

function login(t, login, password){
    var loginInput = Selector("#login")
    var passwordInput = Selector("#password")
    return t
        .typeText(loginInput, login)
        .typeText(passwordInput, password)
        .click("button[type='submit']")
}

function openProjectApp(t){
    return t
        .click(".o_menu_apps > li > a")
        .click("a[data-menu-xmlid='project.menu_main_pm']")
}

function openAllTaskKanban(t){
    return openProjectApp(t)
        .click("a[data-menu-xmlid='project_task_editable_list_view.search_menu']")
        .click("a[data-menu-xmlid='project.menu_project_management']")
}

function openAnyKabanRecord(t){
    return t.click(".o_kanban_record")
}

function clickEditButton(t){
    return t.click(".o_form_button_edit")
}

export {
    login,
	openProjectApp,
	openAllTaskKanban,
	openAnyKabanRecord,
	clickEditButton,
}
