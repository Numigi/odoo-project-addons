/*
    © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("project_task_link.html_field", function(require) {
"use strict";

var HtmlField = require('web_editor.backend').FieldTextHtmlSimple;

var taskUrlRegex = /\/my\/task\/\d+$/;

/**
 * When clicking on the link of a task
 * (<a href="https://my.domain.com/my/task/123">TA#123</a>),
 * open the task in the backend instead of the portal.
 */
HtmlField.include({
    /**
     * Open the form view of a task given the task ID.
     */
    async _openTaskFormView(taskId){
        var action = await this._rpc({
            model: "project.task",
            method: "get_formview_action",
            args: [[taskId]],
            params: {
                context: odoo.session_info.user_context,
            },
        });
        this.trigger_up("do_action", {action});
    },
    _renderReadonly(){
        this._super.apply(this, arguments);
        var self = this;
        var taskLinks = this.$('a').filter(function() {
            return this.href && this.href.match(taskUrlRegex);
        });
        taskLinks.each(function() {
            var taskId = parseInt(this.href.match(/\d+$/));
            $(this).click((event) => {
                event.preventDefault();
                self._openTaskFormView(taskId);
            });
        });
    },
});

});
