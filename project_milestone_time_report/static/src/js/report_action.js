    /*
    © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("project_milestone_time_report.project_milestone_time_report", function (require) {
    "use strict";
    
    // var ControlPanelMixin = require("web.ControlPanelMixin");
    const ControlPanel = require('web.ControlPanel');   
    var core = require("web.core");
    // var crashManager = require("web.crash_manager");
    var framework = require("web.framework");
    // var rpc = require("web.rpc");
    var session = require("web.session");
    // var Widget = require("web.Widget");
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
            console.log("dans init");
            // var index = this._getControllerStackIndex(options);
            // options.breadcrumbs = this._getBreadcrumbs(this.controllerStack.slice(0, index));
            // this.controlPanelProps = {
            //     action,
            //     breadcrumbs: options && options.breadcrumbs,
            // };
        },
        // willStart: function() {
        //     return Promise.all([this._super.apply(this, arguments), this.updateHtml()]);
        // },
    
        set_html: function() {
            var self = this;
            var def = Promise.resolve();
            // if (!this.report_widget) {
            //     this.report_widget = new ReportWidget(this, this.given_context);
            //     def = this.report_widget.appendTo(this.$('.o_content'));
            // }
            return def.then(function () {
            self.$el.html(self.html);
            });
        },
    
        start: function() {
            console.log("début start");
            var result = this._super();
            this.renderPrintButton();
            this.controlPanelProps.cp_content = { $buttons: this.$button };
            console.log("after rendering print button and control");
            // this.controlPanelProps.breadcrumbs = this.getParent()._getBreadcrumbs();         HERE TO FIXXXXXXXXXX
            // this.renderPrintButton();
            // this.update_control_panel();
            // await this._super(...arguments);
            this.updateHtml();
            console.log("after updaterhtml");
            // await this._super(...arguments);
            // this.set_html();
            return result;
        },
        do_show(){
            this._super();
            this.update_control_panel();
        },
        async refresh(){
            this.updateHtml();
        },
    
    
        // TODO !!!!!!!!!!! then activate all calling func
        update_cp: function() {
            if (!this.$button) {
                this.renderPrintButton();
            }
            this.controlPanelProps.cp_content = { $buttons: this.$button };
            return this.updateControlPanel();
        },
        update_control_panel(){
            // this.updateControlPanel({
                // breadcrumbs: this.getParent()._getBreadcrumbs(),
                // cp_content: {$buttons: this.getControlPanelButtons()},
                // cp_content: {$buttons: this.$button},
            // });
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
        // renderPrintButton(){
        //     var button = $(QWeb.render("projectReport.printButton", {}));
        //     button.bind("click", () => this.downloadPDF());
        //     return button;
        // },
        _downloadPDF: function () {
            framework.blockUI();
            session.get_file({
                url: "/web/project_milestone_time_report/" + this.projectId,
                complete: framework.unblockUI,
                error: (error) => this.call('crash_manager', 'rpc_error', error),
                // error: crashManager.rpc_error.bind(crashManager),
            });
        },
    
        renderPrintButton(){
            this.$button = $(QWeb.render("projectReport.printButton", {}));
            this.$button.bind("click", () => this._downloadPDF());
            // this.$button.bind('click', function () { 
            //     this._downloadPDF();
            //     // framework.blockUI();
            // });
            // return this.$button;
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
            // this.html = html; // with promise all
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
    