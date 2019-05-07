/*
    © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).

    This code fixes a bug that happens when clicking on TAB
    after filling the field initial_qty on a project.task.material line.

    The function dom.getSelectionRange is called with an undefined argument,
    from the method ListRenderer.confirmUpdate at
    web/static/src/js/views/list/list_editable_renderer.js

    Because the next field (consumed_qty) is readonly, there is no focused element.
    Therefore, the variable focusedElement is undefined.

    This bug could be fixed in the core of Odoo.
    However, Odoo does not prioritize bugs which can not be reproduced in a vanilla
    environment.
*/
odoo.define("project_wip_material.fix_editable_list", function(require) {
"use strict";

var dom = require("web.dom");
var oldGetSelectionRange = dom.getSelectionRange

dom.getSelectionRange = function(node){
    return node === undefined ? {start: 0, end: 0} : oldGetSelectionRange(node)
}

});
