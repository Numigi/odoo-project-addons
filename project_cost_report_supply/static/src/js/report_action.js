/*
    © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("project_cost_report_supply.ReportAction", function (require) {
"use strict";

var core = require("web.core");
var _t = core._t;

var project_cost_report = require("project_cost_report");
var ReportAction = project_cost_report.ReportAction;
var getRecordIdFromEvent = project_cost_report.getRecordIdFromEvent;
var getRecordNameFromEvent = project_cost_report.getRecordNameFromEvent;

ReportAction.include({
    events: _.extend({}, ReportAction.prototype.events, {
        "click .o_project_cost_report__shop_supply_category": "shopSupplyCategoryClicked",
        "click .o_project_cost_report__shop_supply_total": "shopSupplyTotalClicked",
    }),
    getCategoryNames(){
        var names = this._super.apply(this, arguments);
        names.push("shop_supply");
        return names;
    },
    /**
     * Handle a click on the label of an shop supply category.
     *
     * @param {jQuery.Event} - the click event
     */
    shopSupplyCategoryClicked(event){
        event.preventDefault();
        var categoryId = getRecordIdFromEvent(event);
        this.categoryClicked(categoryId, "shop_supply");
    },
    /**
     * Handle a click on the total of an shop supply category.
     *
     * The list of analytic lines contained in the category is opened.
     *
     * @param {jQuery.Event} - the click event
     */
    shopSupplyTotalClicked(event){
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
                ["is_shop_supply", "=", true],
            ],
        });
    },
    getProductCategoryDomain(){
        var domain = this._super.apply(this, arguments);
        domain.unshift(["is_shop_supply", "=", false]);
        domain.unshift("&");
        return domain;
    },
    getTimeCategoryDomain(){
        var domain = this._super.apply(this, arguments);
        domain.unshift(["is_shop_supply", "=", false]);
        domain.unshift("&");
        return domain;
    },
    getOutsourcingCategoryDomain(){
        var domain = this._super.apply(this, arguments);
        domain.unshift(["is_shop_supply", "=", false]);
        domain.unshift("&");
        return domain;
    },
});

});
