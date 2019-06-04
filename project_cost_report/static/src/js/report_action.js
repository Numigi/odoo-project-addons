/*
    © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define('project_cost_report.ReportAction', function (require) {
'use strict';

var core = require('web.core');
var session = require('web.session');
var Widget = require('web.Widget');
var ControlPanelMixin = require('web.ControlPanelMixin');
var session = require('web.session');
var framework = require('web.framework');
var crash_manager = require('web.crash_manager');
var rpc = require("web.rpc");

var QWeb = core.qweb;
var _t = core._t;

/**
 * Get a record ID from an event triggered.
 *
 * The record ID is expected to be stored in a data-id attribute on the event target.
 *
 * @param {jQuery.Event} - the triggered event
 * @returns {Number} - the record ID
 */
function getRecordIdFromEvent(event){
    var attributeNode = event.currentTarget.attributes['data-id'];
    return attributeNode ? parseInt(attributeNode.nodeValue) : false;
}

/**
 * Get a record name from an event triggered.
 *
 * The record name is expected to be stored in a data-name attribute on the event target.
 *
 * @param {jQuery.Event} - the triggered event
 * @returns {String} - the record name
 */
function getRecordNameFromEvent(event){
    var attributeNode = event.currentTarget.attributes['data-name'];
    return attributeNode ? attributeNode.nodeValue : false;
}

var ReportAction = Widget.extend(ControlPanelMixin, {
    events: {
        'click .o_project_cost_report__analytic_line': 'analyticLineClicked',
        'click .o_project_cost_report__product_category': 'productCategoryClicked',
        'click .o_project_cost_report__product_total': 'productTotalClicked',
        'click .o_project_cost_report__time_category': 'timeCategoryClicked',
        'click .o_project_cost_report__time_total_hours': 'hourTotalClicked',
        'click .o_project_cost_report__time_total': 'hourTotalClicked',
        'click .o_project_cost_report__outsourcing_category': 'outsourcingCategoryClicked',
        'click .o_project_cost_report__outsourcing_total': 'outsourcingTotalClicked',
    },
    init(parent, action) {
        this._super.apply(this, arguments);
        this.controllerURL = action.context.url;
        this.projectId = action.context.active_id || action.params.active_id;
        this.reportContext = {
            active_id: this.projectId,
            unfolded_categories: {
                'product': [],
                'time': [],
                'outsourcing': [],
            },
        };
        this.unfolded = false;
    },
    /**
     * Update the HTML content of the report.
     */
    async updateHtml(){
        var html = await this._rpc({
            model: 'project.cost.report',
            method: 'get_html',
            args: [this.reportContext],
        });
        this.$el.html(html);
    },
    /**
     * Render the PRINT button.
     *
     * returns {jQuery} the button node
     */
    renderPrintButton(){
        var button = $(QWeb.render("projectCostReport.printButton", {}));
        button.bind('click', () => this.downloadPDF());
        return button;
    },
    /**
     * Render the FOLD button.
     *
     * returns {jQuery} the button node
     */
    renderFoldButton(){
        var button = $(QWeb.render("projectCostReport.foldButton", {}));
        button.bind('click', () => this.fold());
        return button;
    },
    /**
     * Render the UNFOLD button.
     *
     * returns {jQuery} the button node
     */
    renderUnfoldButton(){
        var button = $(QWeb.render("projectCostReport.unfoldButton", {}));
        button.bind('click', () => this.unfold());
        return button;
    },
    /**
     * Render the buttons of the control panel.
     *
     * returns {Array<jQuery>} an array of button nodes
     */
    getControlPanelButtons(){
        if(!this.controlPanelButtons){
            this.printButton = this.renderPrintButton();
            this.foldButton = this.renderFoldButton();
            this.unfoldButton = this.renderUnfoldButton();
            this.controlPanelButtons = [this.printButton, this.foldButton, this.unfoldButton];
        }
        return this.controlPanelButtons;
    },
    /**
     * Update the control pannel of the report view.
     */
    updateControlPanel(){
        this.update_control_panel({
            breadcrumbs: this.getParent().get_breadcrumbs(),
            cp_content: {$buttons: this.getControlPanelButtons()},
        });
    },
    /**
     * Hide/show the FOLD/UNFOLD buttons given the folding state.
     *
     * The folding state is managed with the attribute `unfolded`.
     * This method must be called after setting the attribute
     * in order to update the DOM nodes.
     */
    updateFoldButtonVisibility(){
        if(this.unfolded){
            this.foldButton.show();
            this.foldButton.css('display', 'inline-block');
            this.unfoldButton.hide();
        }
        else {
            this.foldButton.hide();
            this.unfoldButton.show();
            this.unfoldButton.css('display', 'inline-block');
        }
    },
    /**
     * Start the widget.
     *
     * This is a standard method of web.Widget.
     * It is called when the widget is ready to be rendered.
     */
    start(){
        var result = this._super();
        this.updateControlPanel();
        this.updateHtml();
        this.updateFoldButtonVisibility();
        return result;
    },
    /**
     * Refresh the report.
     */
    async refresh(){
        this.updateHtml();
        this.updateFoldButtonVisibility();
    },
    /**
     * Download the PDF version of the report.
     */
    downloadPDF(){
        framework.blockUI();
        session.get_file({
            url: "/web/project_cost_report/" + this.projectId,
            data: {report_context: JSON.stringify(this.reportContext)},
            complete: framework.unblockUI,
            error: crash_manager.rpc_error.bind(crash_manager),
        });
    },
    /**
     * Fold all report categories.
     */
    fold(){
        this.reportContext.unfolded_categories = {
            'product': [],
            'time': [],
            'outsourcing': [],
        };
        this.unfolded = false;
        this.refresh();
    },
    /**
     * Unfold all report categories.
     */
    async unfold(){
        this.reportContext.unfolded_categories = await this._rpc({
            model: 'project.cost.report',
            method: 'get_foldable_categories',
            args: [this.projectId],
        });
        this.unfolded = true;
        this.refresh();
    },
    /**
     * Fold a single category.
     *
     * @param {Number} categoryId - the ID of the category.
     * @param {String} sectionName - the name of the section.
     */
    foldCategory(categoryId, sectionName){
        this.reportContext.unfolded_categories[sectionName] = (
            this.reportContext.unfolded_categories[sectionName].filter((c) => c != categoryId)
        );
        this.unfolded = false;
        this.refresh();
    },
    /**
     * Unfold a single category.
     *
     * @param {Number} categoryId - the ID of the category.
     * @param {String} sectionName - the name of the section.
     */
    unfoldCategory(categoryId, sectionName){
        this.reportContext.unfolded_categories[sectionName].push(categoryId);
        this.refresh();
    },
    /**
     * Handle a click on the label of a category.
     *
     * The category is toggled (folded or unfolded).
     *
     * @param {Number} categoryId - the ID of the category.
     * @param {String} sectionName - the name of the section.
     */
    categoryClicked(categoryId, sectionName){
        event.preventDefault();
        var unfoldedIds = this.reportContext.unfolded_categories[sectionName];
        var isUnfolded = unfoldedIds.indexOf(categoryId) !== -1;
        if(isUnfolded){
            this.foldCategory(categoryId, sectionName);
        }
        else{
            this.unfoldCategory(categoryId, sectionName);
        }
    },
    /**
     * Handle a click on an analytic line.
     *
     * The form view of the analytic is opened.
     *
     * @param {jQuery.Event} - the click event
     */
    analyticLineClicked(event){
        event.preventDefault();
        var lineId = getRecordIdFromEvent(event);
        this.do_action({
            res_model: "account.analytic.line",
            res_id: lineId,
            views: [[false, "form"]],
            type: "ir.actions.act_window",
        });
    },
    /**
     * Handle a click on the label of a product category.
     *
     * @param {jQuery.Event} - the click event
     */
    productCategoryClicked(event){
        event.preventDefault();
        var categoryId = getRecordIdFromEvent(event);
        this.categoryClicked(categoryId, 'product');
    },
    /**
     * Handle a click on the total of a product category.
     *
     * The list of analytic lines contained in the category is opened.
     *
     * @param {jQuery.Event} - the click event
     */
    productTotalClicked(event){
        event.preventDefault();
        var categoryId = getRecordIdFromEvent(event);
        var categoryName = getRecordNameFromEvent(event);
        var actionName = _t("Analytic Lines ({category})").replace("{category}", categoryName);
        this.do_action({
            name: actionName,
            res_model: "account.analytic.line",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            domain: [
                ["account_id.project_ids", "=", this.projectId],
                ["product_id.type", "in", ["consu", "product"]],
                ["product_id.categ_id", "=", categoryId],
            ],
        });
    },
    /**
     * Handle a click on the label of a time category.
     *
     * @param {jQuery.Event} - the click event
     */
    timeCategoryClicked(event){
        event.preventDefault();
        var categoryId = getRecordIdFromEvent(event);
        this.categoryClicked(categoryId, 'time');
    },
    /**
     * Handle a click on the total of a time category.
     *
     * The list of analytic lines contained in the category is opened.
     *
     * @param {jQuery.Event} - the click event
     */
    hourTotalClicked(event){
        event.preventDefault();
        var taskTypeId = getRecordIdFromEvent(event);
        var taskTypeName = getRecordNameFromEvent(event);
        var actionName = _t("Analytic Lines ({category})").replace("{category}", taskTypeName);
        this.do_action({
            name: actionName,
            res_model: "account.analytic.line",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            domain: [
                ["account_id.project_ids", "=", this.projectId],
                ["task_id.task_type_id", "=", taskTypeId],
                ["task_id", "!=", false],
            ],
        });
    },
    /**
     * Handle a click on the label of an uotsourcing category.
     *
     * @param {jQuery.Event} - the click event
     */
    outsourcingCategoryClicked(event){
        event.preventDefault();
        var categoryId = getRecordIdFromEvent(event);
        this.categoryClicked(categoryId, 'outsourcing');
    },
    /**
     * Handle a click on the total of an outsourcing category.
     *
     * The list of analytic lines contained in the category is opened.
     *
     * @param {jQuery.Event} - the click event
     */
    outsourcingTotalClicked(event){
        event.preventDefault();
        var categoryId = getRecordIdFromEvent(event);
        var categoryName = getRecordNameFromEvent(event);
        var actionName = _t("Analytic Lines ({category})").replace("{category}", categoryName);
        this.do_action({
            name: actionName,
            res_model: "account.analytic.line",
            views: [[false, "list"], [false, "form"]],
            type: "ir.actions.act_window",
            domain: [
                ["account_id.project_ids", "=", this.projectId],
                ["task_id", "=", false],
                ["product_id.type", "=", "service"],
            ],
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

core.action_registry.add("project_cost_report", ReportAction);
return ReportAction;

});
