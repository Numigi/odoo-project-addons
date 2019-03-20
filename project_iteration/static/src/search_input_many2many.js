/*
    © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).

    This javascript module allows to display the name of the project in the search bar of tasks.

    Instead of filtering by a many2one field (project_id) like in vanilla Odoo,
    the view is filtered by a many2many field (parent_project_ids).

    This allows to display the tasks below a parent projects and its iterations.

    Without this module, the ID of the project is displayed in the search bar facet
    instead of its display name.
*/
odoo.define("web_search_input_many2many.search_view_field", function(require) {
"use strict";

var searchInputs = require("web.search_inputs");

searchInputs.Field.include({
    facet_for(value){
        var field = this.getParent().fields[this.attrs.name];
        var isMany2many = field && field.type === "many2many";
        var isIdArray = value instanceof Array && value.every(function(i){return typeof i === "number";});
        if(isMany2many && isIdArray){
            return this._getFacetForMany2manyValue(value);
        }
        else{
            return this._super.apply(this, arguments);
        }
    },
    /**
     * Get a facet for a many2many field value.
     *
     * A facet is an element contained in the search bar input.
     *
     * @param {String} value - a array of record ids.
     * @returns {$.Deferred} - a deferred which returns the facet.
     */
    _getFacetForMany2manyValue(value){
        var field = this.getParent().fields[this.attrs.name];
        var self = this;
        return this._rpc({
            model: field.relation,
            method: "name_get",
            args: value,
        }).then(function(result) {
            var label = result.map(function(el){
                return el[1];
            }).sort().join(", ");
            return {
                field: self,
                category: self.attrs.string || self.attrs.name,
                values: [{label, value}],
            };
        });
    },
});

});