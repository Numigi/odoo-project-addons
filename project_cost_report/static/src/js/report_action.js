/*
    © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("project_cost_report", function (require) {
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
        "click .o_project_cost_report__analytic_line": "analyticLineClicked",
        "click .o_project_cost_report__category": "categoryClicked",
        "click .o_project_cost_report__category_cost": "categoryCostClicked",
        "click .o_project_cost_report__category_revenue": "categoryRevenueClicked",
        "click .o_project_cost_report__category_profit": "categoryProfitClicked",
        "click .o_project_cost_report__purchase_order_name": "purchaseOrderNameClicked",
    },
    init(parent, action) {
        this._super.apply(this, arguments);
        this.controllerURL = action.context.url;
        this.projectId = action.context.active_id || action.params.active_id;
        this.reportContext = {
            active_id: this.projectId,
            unfolded_categories: [],
            show_summary: true,
        };
        this.unfolded = false;
    },

    async updateHtml(){
        var html = await this._rpc({
            model: "project.cost.report",
            method: "get_html",
            args: [this.reportContext],
            context: this.getSession().user_context,
        });
        this.$el.html(html);
    },
    renderPrintButton(){
        var button = $(QWeb.render("projectCostReport.printButton", {}));
        button.bind("click", () => this.downloadPDF());
        return button;
    },
    renderFoldButton(){
        var button = $(QWeb.render("projectCostReport.foldButton", {}));
        button.bind("click", () => this.fold());
        return button;
    },
    renderUnfoldButton(){
        var button = $(QWeb.render("projectCostReport.unfoldButton", {}));
        button.bind("click", () => this.unfold());
        return button;
    },
    renderShowSummaryButton(){
        var button = $(QWeb.render("projectCostReport.showSummaryButton", {}));
        button.bind("click", () => this.showSummary());
        return button;
    },
    renderHideSummaryButton(){
        var button = $(QWeb.render("projectCostReport.hideSummaryButton", {}));
        button.bind("click", () => this.hideSummary());
        return button;
    },
    getControlPanelButtons(){
        if(!this.controlPanelButtons){
            this.printButton = this.renderPrintButton();
            this.foldButton = this.renderFoldButton();
            this.unfoldButton = this.renderUnfoldButton();
            this.showSummaryButton = this.renderShowSummaryButton();
            this.hideSummaryButton = this.renderHideSummaryButton();
            this.controlPanelButtons = [
                this.printButton,
                this.foldButton,
                this.unfoldButton,
                this.showSummaryButton,
                this.hideSummaryButton,
            ];
        }
        return this.controlPanelButtons;
    },
    updateControlPanel(){
        this.update_control_panel({
            breadcrumbs: this.getParent()._getBreadcrumbs(),
            cp_content: {$buttons: this.getControlPanelButtons()},
        });
    },
    updateFoldButtonVisibility(){
        if(this.unfolded){
            this.foldButton.show();
            this.foldButton.css("display", "inline-block");
            this.unfoldButton.hide();
        }
        else {
            this.foldButton.hide();
            this.unfoldButton.show();
            this.unfoldButton.css("display", "inline-block");
        }
    },
    updateSummaryButtonVisibility(){
        if(this.reportContext.show_summary){
            this.showSummaryButton.hide();
            this.hideSummaryButton.show();
            this.hideSummaryButton.css("display", "inline-block");
        }
        else {
            this.showSummaryButton.show();
            this.showSummaryButton.css("display", "inline-block");
            this.hideSummaryButton.hide();
        }
    },
    start(){
        var result = this._super();
        this.updateControlPanel();
        this.updateHtml();
        this.updateFoldButtonVisibility();
        this.updateSummaryButtonVisibility();
        return result;
    },
    async refresh(){
        this.updateHtml();
        this.updateFoldButtonVisibility();
        this.updateSummaryButtonVisibility();
    },
    downloadPDF(){
        framework.blockUI();
        session.get_file({
            url: "/web/project_cost_report/" + this.projectId,
            data: {report_context: JSON.stringify(this.reportContext)},
            complete: framework.unblockUI,
            error: crashManager.rpc_error.bind(crashManager),
        });
    },
    fold(){
        this.reportContext.unfolded_categories = [];
        this.unfolded = false;
        this.refresh();
    },
    async unfold(){
        const allCategories = await this._rpc({
            model: "project.cost.category",
            method: "search",
            args: [[]],
        });
        this.reportContext.unfolded_categories = allCategories
        this.unfolded = true;
        this.refresh();
    },
    showSummary(){
        this.reportContext.show_summary = true;
        this.refresh();
    },
    hideSummary(){
        this.reportContext.show_summary = false;
        this.refresh();
    },
    categoryClicked(event){
        event.preventDefault();
        const categoryId = getCategoryId(event)
        if(this.isCategoryFolded(categoryId)){
            this.unfoldCategory(categoryId);
        }
        else{
            this.foldCategory(categoryId);
        }
    },
    isCategoryFolded(categoryId) {
        return this.reportContext.unfolded_categories.indexOf(categoryId) === -1;
    },
    foldCategory(categoryId){
        const categories = this.reportContext.unfolded_categories
        this.reportContext.unfolded_categories = categories.filter((c) => c !== categoryId)
        this.unfolded = false;
        this.refresh();
    },
    unfoldCategory(categoryId){
        this.reportContext.unfolded_categories.push(categoryId);
        this.refresh();
    },
    analyticLineClicked(event){
        const analyticLineId = getAnalyticLineId(event)
        this.drilldownAmount("analytic_line_clicked", [analyticLineId])
    },
    categoryCostClicked(event){
        const sectionName = getSectionName(event)
        const categoryId = getCategoryId(event)
        this.drilldownAmount("category_cost_clicked", [this.reportContext, sectionName, categoryId])
    },
    categoryRevenueClicked(event){
        const sectionName = getSectionName(event)
        const categoryId = getCategoryId(event)
        this.drilldownAmount("category_revenue_clicked", [this.reportContext, sectionName, categoryId])
    },
    categoryProfitClicked(event){
        const sectionName = getSectionName(event)
        const categoryId = getCategoryId(event)
        this.drilldownAmount("category_profit_clicked", [this.reportContext, sectionName, categoryId])
    },
    async drilldownAmount(method, args){
        event.preventDefault();
        const action = await this._rpc({
            model: "project.cost.report",
            method: method,
            args: args,
            context: this.getSession().user_context,
        })
        this.do_action(action);
    },
    purchaseOrderNameClicked(event){
        event.preventDefault();
        var orderId = getPurchaseOrderId(event);
        this.do_action({
            res_model: "purchase.order",
            views: [[false, "form"]],
            type: "ir.actions.act_window",
            res_id: orderId,
        });
    },
    /**
     * Show the widget.
     *
     * This is a standard method of web.Widget.
     * It is called when the report is reopened after a click on the breadcrumb.
     */
    do_show(){
        this._super();
        this.updateControlPanel();
    },
});

function getSectionName(event){
    return getAttribute(event, "section")
}

function getCategoryId(event){
    return parseInt(getAttribute(event, "category-id"))
}

function getAnalyticLineId(event){
    return parseInt(getAttribute(event, "analytic-line-id"))
}

function getPurchaseOrderId(event){
    return parseInt(getAttribute(event, "purchase-order-id"))
}

function getAttribute(event, key) {
    var attributeNode = event.currentTarget.attributes[key];
    return attributeNode ? attributeNode.nodeValue : null;
}

core.action_registry.add("project_cost_report", ReportAction);
return {
    ReportAction,
};

});
