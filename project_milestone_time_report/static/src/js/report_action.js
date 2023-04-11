    /*
    © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("project_milestone_time_report.project_milestone_time_report", function (require) {
    "use strict";
    
    const ControlPanel = require('web.ControlPanel');   
    var core = require("web.core");
    var framework = require("web.framework");
    var session = require("web.session");;
    var AbstractAction = require("web.AbstractAction");
    
    var QWeb = core.qweb;
    var _t = core._t;
    
    var ReportAction = AbstractAction.extend({
        hasControlPanel: true,
        loadControlPanel: false,
        events: {
            "click .o_project_report__estimated_hours": "estimatedHoursClicked",
            "click .o_project_report__consumed_hours": "consumedHoursClicked",
            "click .o_project_report__total_estimated_hours": "totalEstimatedHoursClicked",
            "click .o_project_report__total_consumed_hours": "totalComsumedHoursClicked",
        },
        init(parent, action) {
            this._super.apply(this, arguments);
            this.controllerURL = action.context.url;
            this.projectId = action.context.active_id;
        },
        set_html: function() {
            var self = this;
            var def = Promise.resolve();
            return def.then(function () {
            self.$el.html(self.html);
            });
        },
        start: function() {
            var result = this._super();
            this.renderPrintButton();
            this.controlPanelProps.cp_content = { $buttons: this.$button };
            this.updateHtml();
            return result;
        },
        do_show(){
            this._super();
            this.update_control_panel();
        },
        async refresh(){
            this.updateHtml();
        },
        update_cp: function() {
            if (!this.$button) {
                this.renderPrintButton();
            }
            this.controlPanelProps.cp_content = { $buttons: this.$button };
            return this.updateControlPanel();
        },
        update_control_panel(){
            this.controlPanelProps.cp_content = { $buttons: this.$button };
            this.controlPanelProps.breadcrumbs = this.getParent()._getBreadcrumbs();
            return this.updateControlPanel();
        },
    
        getControlPanelButtons(){
            if(!this.controlPanelButtons){
                this.printButton = this.renderPrintButton();
                this.controlPanelButtons = [
                    this.printButton,
                ];
            }
            return this.controlPanelButtons;
        },
        _downloadPDF: function () {
            framework.blockUI();
            session.get_file({
                url: "/web/project_milestone_time_report/" + this.projectId,
                complete: framework.unblockUI,
                error: (error) => this.call('crash_manager', 'rpc_error', error),
            });
        },
    
        renderPrintButton(){
            this.$button = $(QWeb.render("projectReport.printButton", {}));
            this.$button.bind("click", () => this._downloadPDF());
        },
        async updateHtml(){
            var html  = await this._rpc({
                model: "project.milestone.time.report",
                method: "get_html",
                args: [this.projectId],
                context: this.getSession().user_context,
            });
            this.$('.o_content').html(html);
            this.update_cp();
        },
    
        totalComsumedHoursClicked(event){
            this.drilldownAmount(this.projectId, "total_consumed_hours_clicked")
        },
        consumedHoursClicked(event){
            const projectId = getProjectId(event)
            this.drilldownAmount(projectId, "consumed_hours_clicked")
        },
        estimatedHoursClicked(event){
            const projectId = getProjectId(event)
            this.drilldownAmount(projectId, "estimated_hours_clicked")
        },
        totalEstimatedHoursClicked(event){
            this.drilldownAmount(this.projectId, "total_estimated_hours_clicked")
        },
        async drilldownAmount(projectId, method){
            event.preventDefault();
            const action = await this._rpc({
                model: "project.milestone.time.report",
                method: method,
                args: [projectId],
                context: this.getSession().user_context,
            })
            this.do_action(action);
        },
    });
    
    function getProjectId(event){
        var attributeNode = event.currentTarget.attributes["project-id"];
        return attributeNode ? parseInt(attributeNode.nodeValue) : false;
    }
    
    core.action_registry.add("project_milestone_time_report", ReportAction);
    return ReportAction;
    
    });
    