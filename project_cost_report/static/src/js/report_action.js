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

var QWeb = core.qweb;

var ReportAction = Widget.extend(ControlPanelMixin, {
    events: {
        'click .o_project_cost_report__product_category': 'productCategoryClicked',
        'click .o_project_cost_report__time_category': 'timeCategoryClicked',
    },
    init: function(parent, action) {
        this._super.apply(this, arguments);
        this.controller_url = action.context.url;
        this.reportContext = {
            active_id: action.context.active_id || action.params.active_id,
            unfolded_categories: {
                'product': [],
                'time': [],
            },
        };
    },
    getHtml: function() {
        var defs = [];
        return this._rpc({
            model: 'project.cost.report',
            method: 'get_html',
            args: [this.reportContext],
        })
        .then((html) => {
            this.html = html;
            defs.push(this.updateControlPanel());
            return $.when.apply($, defs);
        });
    },
    willStart: function() {
        return this.getHtml();
    },
    setHtml: function() {
        this.$el.html(this.html);
    },
    start: function() {
        this.setHtml();
        return this._super();
    },
    async refresh(){
        await this.getHtml();
        this.setHtml();
    },
    updateControlPanel: function() {
        if (!this.$buttons) {
            this.$printButton = this.renderPrintButton();
        }
        var status = {
            breadcrumbs: this.getParent().get_breadcrumbs(),
            cp_content: {$buttons: this.$printButton},
        };
        return this.update_control_panel(status);
    },
    renderPrintButton: function() {
        var button = $(QWeb.render("projectCostReport.printButton", {}));
        button.bind('click', function () {
            console.log('PRINT BUTTON');
        });
        return button;
    },
    do_show: function() {
        this._super();
        this.updateControlPanel();
    },
    foldProductCategory(categoryId, categoryName){
        this.reportContext.unfolded_categories[categoryName] = (
            this.reportContext.unfolded_categories[categoryName].filter((c) => c != categoryId)
        );
        this.refresh();
    },
    unfoldProductCategory(categoryId, categoryName){
        this.reportContext.unfolded_categories[categoryName].push(categoryId);
        this.refresh();
    },
    categoryClicked: function(categoryId, categoryName){
        event.preventDefault();
        var unfoldedIds = this.reportContext.unfolded_categories[categoryName];
        var isUnfolded = unfoldedIds.indexOf(categoryId) !== -1;
        if(isUnfolded){
            this.foldProductCategory(categoryId, categoryName);
        }
        else{
            this.unfoldProductCategory(categoryId, categoryName);
        }
    },
    productCategoryClicked: function(event){
        event.preventDefault();
        var categoryId = parseInt(event.currentTarget.attributes['data-id'].nodeValue);
        this.categoryClicked(categoryId, 'product');
    },
    timeCategoryClicked: function(event){
        event.preventDefault();
        var attributeNode = event.currentTarget.attributes['data-id'];
        var categoryId = attributeNode ? parseInt(attributeNode.nodeValue) : false;
        this.categoryClicked(categoryId, 'time');
    },
});

core.action_registry.add("project_cost_report", ReportAction);
return ReportAction;

});
