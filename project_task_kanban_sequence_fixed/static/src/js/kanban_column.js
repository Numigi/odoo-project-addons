odoo.define('kanban_task_stage_lock.kanbanRenderer', function(require) {
    "use strict";
    var core = require('web.core');
    var KanbanColumn = require("web.KanbanColumn");

    var _t = core._t;

    KanbanColumn.include({
        start: function() {
            this._super.apply(this, arguments);

            var self = this;

            document.onmouseover = myMouseOverHandler;
            document.onmousedown = myMouseDownHandler;

            // pointer prevents user that drag and drop not allowed
            function myMouseOverHandler(event) {
                var el = event.target
                var condition = self.modelName === "project.task" &&
                    event.button === 0 &&
                    (el.classList.contains('o_column_unfold') ||
                        el.classList.contains('o_column_title') ||
                        event.target.classList.contains('fa-arrows-h'))
                if (condition) {
                    event.target.style.cursor = "not-allowed";
                }
            }

            // if user is trying to move column
            function myMouseDownHandler(event) {
                var el = event.target
                var condition = self.modelName === "project.task" &&
                    event.button === 0 &&
                    (el.classList.contains('o_column_unfold') ||
                        el.classList.contains('o_column_title') ||
                        event.target.classList.contains('fa-arrows-h'))

                if (condition) {
                    event.target.click(function(){return false;});
                    var documentToNull =  function(){
                        document.onmouseup = null;
                        document.mousemove = null;
                    };
                    function onMouseMove(event) {
                        document.removeEventListener('mousemove', onMouseMove);
                        documentToNull();
                        alert(_t("Oups! You can not sort columns order here in this view."));
                    }
                    document.addEventListener('mousemove', onMouseMove);
                    document.onmouseup = function() {
                        document.removeEventListener('mousemove', onMouseMove);
                        documentToNull();
                    };
                }
            }
        },
    });
});