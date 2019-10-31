/*
    © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("project_template.hidden_fields", function(require) {
"use strict";

var Domain = require("web.Domain");

/**
 * Define whether a node is a date field.
 *
 * All date fields should be invisible on templates.
 *
 * The reason for this special case is to prevent requiring multiple binding modules.
 * 
 * -> project.project.date: added by module `project_form_with_dates`
 * -> project.project.date_end: added by module `project_form_with_dates`
 * -> project.task.date_start: added by `https://github.com/OCA/project/tree/12.0/project_timeline`
 * -> project.task.date_end: added by `https://github.com/OCA/project/tree/12.0/project_timeline`
 * -> project.task.date_planned: added by `project_task_date_planned`
 */
function isDateField(node){
    return node.tag === "field" && (node.attrs.name || "").startsWith("date")
}

function isNodeInvisibleOnTemplate(node){
    if(!node.attrs){
        return false;
    }
    var invisibleAttribute = node.attrs.invisible_on_template;
    return isDateField(node) || (
        invisibleAttribute && Boolean(eval(node.attrs.invisible_on_template))
    );
}

function updateProjectInvisibleModifiers(node){
    if(isNodeInvisibleOnTemplate(node)){
        node.attrs.modifiers.project_template_invisible = "[('is_template', '=', True)]";
    }
    (node.children || []).forEach((c) => updateProjectInvisibleModifiers(c));
}

require("web.FormRenderer").include({
    /**
     * Add a shortcut for the `project_template_invisible` modifier.
     *
     * The shortcut is to use the attribute `invisible_on_template`
     * instead of attrs="{'project_template_invisible': [('is_template', '=', True)]}".
     *
     * <field name="my_field" invisible_on_template="1"/>
     *
     * This improves the readability and prevents having to rewrite the whole attrs
     * for each node.
     */
    init() {
        this._super.apply(this, arguments);
        updateProjectInvisibleModifiers(this.arch);
    },
});

require("web.BasicModel").include({
    /**
     * Apply the `project_template_invisible` modifier.
     *
     * This modifier is used to make an xml node (i.e. a field node) invisible if the task/project is a template.
     * It forces the modifier `invisible` to True.
     *
     * If the modifier `invisible` is already evaluated to True, `project_template_invisible`
     * is not evaluated.
     *
     * The reverse logic is applied for the `required` modifier.
     * If the field is invisible for templates, then it should not be mandatory for templates.
     */
    _evalModifiers(element, modifiers) {
        var result = this._super.apply(this, arguments);

        if (modifiers.project_template_invisible) {
            var evalContext = this._getEvalContext(element);
            var modifier = modifiers.project_template_invisible;
            var modifierValue = new Domain(modifier, evalContext).compute(evalContext);

            result.invisible = result.invisible ? true : modifierValue;
            result.required = result.required ? (!modifierValue) : false;
        }

        return result;
    }
});

});
