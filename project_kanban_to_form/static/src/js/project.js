/*
    © 2017 Savoir-faire Linux <https://savoirfairelinux.com>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define('project_kanban_to_form', function (require) {
'use strict';

require('project.update_kanban');
var KanbanRecord = require('web_kanban.Record');

KanbanRecord.include({
    on_card_clicked: function () {
        if (this.model === 'project.project') {
            // The following lines were copied from the original method in the module web_kanban
            if (this.$el.hasClass('oe_kanban_global_click_edit') && this.$el.data('routing')) {
                framework.redirect(this.$el.data('routing') + "/" + this.id);
            } else if (this.$el.hasClass('oe_kanban_global_click_edit')) {
                this.trigger_up('kanban_record_edit', {id: this.id});
            } else {
                this.trigger_up('kanban_record_open', {id: this.id});
            }
        } else {
            this._super.apply(this, arguments);
        }
    },
});
});
