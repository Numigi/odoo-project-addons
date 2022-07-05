/*
    © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("project_report_consumed_by_lot", function (require) {
"use strict";

var ControlPanelMixin = require("web.ControlPanelMixin");
var core = require("web.core");
var crashManager = require("web.crash_manager");
var framework = require("web.framework");
var rpc = require("web.rpc");
var session = require("web.session");
var Widget = require("web.Widget");
var AbstractAction = require("web.AbstractAction");

var QWeb = core.qweb;
var _t = core._t;

var ReportAction = AbstractAction.extend(ControlPanelMixin, {
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
    start(){
        var result = this._super();
        this.updateControlPanel();
        this.updateHtml();
        return result;
    },
    do_show(){
        this._super();
        this.updateControlPanel();
    },
    async refresh(){
        this.updateHtml();
    },
    updateControlPanel(){
        this.update_control_panel({
            breadcrumbs: this.getParent()._getBreadcrumbs(),
            cp_content: {$buttons: this.getControlPanelButtons()},
        });
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
    renderPrintButton(){
        var button = $(QWeb.render("projectReport.printButton", {}));
        button.bind("click", () => this.downloadPDF());
        return button;
    },
    async updateHtml(){
        var html = await this._rpc({
            model: "project.milestone.time.report",
            method: "get_html",
            args: [this.projectId],
            context: this.getSession().user_context,
        });
        this.$el.html(html);
    },
    downloadPDF(){
        framework.blockUI();
        session.get_file({
            url: "/web/project_milestone_time_report/" + this.projectId,
            complete: framework.unblockUI,
            error: crashManager.rpc_error.bind(crashManager),
        });
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
return {
    ReportAction,
};

});
