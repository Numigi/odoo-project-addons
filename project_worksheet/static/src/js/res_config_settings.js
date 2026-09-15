odoo.define('project_worksheet.settings', function (require) {
    "use strict";

    var BaseSettingRenderer = require('base.settings').Renderer;

    BaseSettingRenderer.include({
        _getAppIconUrl: function (module) {
            var iconUrl = this._super.apply(this, arguments);
            if (module === 'project_worksheet') {
                return iconUrl.replace("/static/description/icon.png", "/static/description/worksheet.png");
            }
            return iconUrl;
        }
    });
});