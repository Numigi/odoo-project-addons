odoo.define("project_cost_report.report_action", function (require) {
    "use strict";

    const core = require("web.core");
    const framework = require("web.framework");
    const session = require("web.session");
    const AbstractAction = require("web.AbstractAction");
    const QWeb = core.qweb;

    const ReportAction = AbstractAction.extend({
        hasControlPanel: true,
        events: {
            "click .o_project_cost_report__analytic_line": "onAnalyticLineClick",
            "click .o_project_cost_report__category": "onCategoryClick",
            "click .o_project_cost_report__category_cost": "onCategoryCostClick",
            "click .o_project_cost_report__category_revenue": "onCategoryRevenueClick",
            "click .o_project_cost_report__category_profit": "onCategoryProfitClick",
            "click .o_project_cost_report__purchase_order_name": "onPurchaseOrderClick",
        },

        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.controllerURL = action.context.url;
            this.projectId = action.context.active_id || action.params.active_id;
            this.reportContext = {
                active_id: this.projectId,
                unfolded_categories: [],
                show_summary: true,
            };
            this.isUnfolded = false;
        },

        start: function () {
            const result = this._super();
            this.refreshContent();
            this.setupButtons();
            this.updateFoldButtonState();
            this.updateSummaryButtonState();
            return result;
        },

        getHtml: async function () {
            return await this._rpc({
                model: "project.cost.report",
                method: "get_html",
                args: [this.reportContext],
                context: this.getSession().user_context,
            });
        },

        updateFoldButtonState: function () {
            const $foldButton = this.$(".cost_report_fold");
            const $unfoldButton = this.$(".cost_report_unfold");

            if (this.isUnfolded) {
                $foldButton.css("display", "inline-block").show();
                $unfoldButton.hide();
            } else {
                $foldButton.hide();
                $unfoldButton.css("display", "inline-block").show();
            }
        },

        updateSummaryButtonState: function () {
            const $showSummaryButton = this.$(".cost_report_show");
            const $hideSummaryButton = this.$(".cost_report_hide");

            if (this.reportContext.show_summary) {
                $showSummaryButton.hide();
                $hideSummaryButton.css("display", "inline-block").show();
            } else {
                $showSummaryButton.css("display", "inline-block").show();
                $hideSummaryButton.hide();
            }
        },

        setupButtons: function () {
            this.$buttons = $(QWeb.render("projectCostReport.buttons", this));
            this.$buttons.filter(".cost_report_print").on("click", this.onDownloadPDF.bind(this));
            this.$buttons.filter(".cost_report_unfold").on("click", this.onUnfold.bind(this));
            this.$buttons.filter(".cost_report_fold").on("click", this.onFold.bind(this));
            this.$buttons.filter(".cost_report_show").on("click", this.onShowSummary.bind(this));
            this.$buttons.filter(".cost_report_hide").on("click", this.onHideSummary.bind(this));

            this.controlPanelProps.cp_content = {
                $buttons: this.$buttons,
            };
        },

        refreshContent: async function () {
            const content = await this.getHtml();
            this.$(".o_content").html(content);
        },

        refreshView: function () {
            this.refreshContent();
            this.setupButtons();
            this.updateFoldButtonState();
            this.updateSummaryButtonState();
        },

        onDownloadPDF: function () {
            framework.blockUI();
            session.get_file({
                url: `/web/project_cost_report/${this.projectId}`,
                data: { report_context: JSON.stringify(this.reportContext) },
                complete: framework.unblockUI,
            });
        },

        onFold: function () {
            this.reportContext.unfolded_categories = [];
            this.isUnfolded = false;
            this.refreshView();
        },

        onUnfold: async function () {
            const allCategories = await this._rpc({
                model: "project.cost.category",
                method: "search",
                args: [[]],
            });
            this.reportContext.unfolded_categories = allCategories;
            this.isUnfolded = true;
            this.refreshView();
        },

        onShowSummary: function () {
            this.reportContext.show_summary = true;
            this.refreshView();
        },

        onHideSummary: function () {
            this.reportContext.show_summary = false;
            this.refreshView();
        },

        onCategoryClick: function (event) {
            event.preventDefault();
            const categoryId = this.getEventAttribute(event, "category-id");
            if (this.isCategoryFolded(categoryId)) {
                this.unfoldCategory(categoryId);
            } else {
                this.foldCategory(categoryId);
            }
        },

        isCategoryFolded: function (categoryId) {
            return !this.reportContext.unfolded_categories.includes(categoryId);
        },

        foldCategory: function (categoryId) {
            this.reportContext.unfolded_categories = this.reportContext.unfolded_categories.filter((id) => id !== categoryId);
            this.isUnfolded = false;
            this.refreshView();
        },

        unfoldCategory: function (categoryId) {
            this.reportContext.unfolded_categories.push(categoryId);
            this.refreshView();
        },

        onAnalyticLineClick: function (event) {
            const analyticLineId = this.getEventAttribute(event, "analytic-line-id");
            this.triggerDrilldown("analytic_line_clicked", [analyticLineId]);
        },

        onCategoryCostClick: function (event) {
            this.triggerCategoryDrilldown(event, "category_cost_clicked");
        },

        onCategoryRevenueClick: function (event) {
            this.triggerCategoryDrilldown(event, "category_revenue_clicked");
        },

        onCategoryProfitClick: function (event) {
            this.triggerCategoryDrilldown(event, "category_profit_clicked");
        },

        triggerCategoryDrilldown: function (event, method) {
            const sectionName = this.getEventAttribute(event, "section");
            const categoryId = this.getEventAttribute(event, "category-id");
            this.triggerDrilldown(method, [this.reportContext, sectionName, categoryId]);
        },

        triggerDrilldown: async function (method, args) {
            event.preventDefault();
            const action = await this._rpc({
                model: "project.cost.report",
                method: method,
                args: args,
                context: this.getSession().user_context,
            });
            this.do_action(action);
        },

        onPurchaseOrderClick: function (event) {
            event.preventDefault();
            const orderId = this.getEventAttribute(event, "purchase-order-id");
            this.do_action({
                res_model: "purchase.order",
                views: [[false, "form"]],
                type: "ir.actions.act_window",
                res_id: orderId,
            });
        },

        getEventAttribute: function (event, attribute) {
            const attributeNode = event.currentTarget.attributes[attribute];
            return attributeNode ? parseInt(attributeNode.nodeValue) : null;
        },
    });

    core.action_registry.add("project_cost_report", ReportAction);
    return ReportAction;
});
