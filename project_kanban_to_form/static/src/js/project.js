/*
    © 2017 Savoir-faire Linux <https://savoirfairelinux.com>
    © 2022 - today Numigi <https://numigi.com>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define('project_kanban_to_form', function (require) {
'use strict';

require('project.update_kanban');
var KanbanRecord = require('web.KanbanRecord');

KanbanRecord.include({
    _openRecord() {
        if (this.modelName === 'project.project') {
            this._openProjectForm()
        } else {
            this._super.apply(this, arguments);
        }
    },
    /**
     * This method was copied from the method _openRecord of web.KanbanRecord
     */
    _openProjectForm() {
        if (this.$el.hasClass('o_currently_dragged')) {
            return;
        }
        var editMode = this.$el.hasClass('oe_kanban_global_click_edit');
        this.trigger_up('open_record', {
            id: this.db_id,
            mode: editMode ? 'edit' : 'readonly',
        });
    }
});
});
