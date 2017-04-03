/*
    © 2017 Savoir-faire Linux <https://savoirfairelinux.com>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define('project_invoicing.hr_timesheet', function (require) {
"use strict";

require('hr_timesheet_sheet.sheet');

var core = require('web.core');
var form_common = require('web.form_common');
var weekly_timesheet = core.form_custom_registry.get('weekly_timesheet');

weekly_timesheet.include({

    update_sheets: function() {
        if(this.querying) {
            return;
        }
        this.updating = true;

        var commands = [form_common.commands.delete_all()];
        _.each(this.get("sheets"), function (_data) {
            var data = _.clone(_data);
            if(data.id) {
                commands.push(form_common.commands.link_to(data.id));
                commands.push(form_common.commands.update(data.id, data));
            } else {
                // Only the following line was added to the original method.
                data.is_timesheet = true;
                commands.push(form_common.commands.create(data));
            }
        });

        var self = this;
        this.field_manager.set_values({'timesheet_ids': commands}).done(function() {
            self.updating = false;
        });
    },
});

});
