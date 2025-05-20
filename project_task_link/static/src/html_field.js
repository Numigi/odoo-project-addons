/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Component, useEnv } from '@odoo/owl';
import { patch } from '@web/core/utils/patch';
import { loadJS } from '@web/core/assets';
import { _lt } from '@web/core/l10n/translation';
import { useService } from '@web/core/utils/hooks';

// Regex to match portal task URLs ending with /my/task/123
const taskUrlRegex = /\/my\/task\/(\d+)$/;

/**
 * Patch the HtmlField widget rendering in readonly mode
 */
patch(registry.category('fields'), 'project_task_link.html_field', (HtmlField) => {
    class HtmlFieldOWL extends HtmlField {
        setup() {
            super.setup();
            this.orm = useService('orm');
            this.actionService = useService('action');
        }

        // override method to attach click handlers
        _render() {
            super._render();
            this.el.querySelectorAll('a').forEach(anchor => {
                const match = anchor.href.match(taskUrlRegex);
                if (match) {
                    const taskId = parseInt(match[1], 10);
                    anchor.addEventListener('click', (ev) => this._onTaskClick(ev, taskId));
                }
            });
        }

        async _onTaskClick(event, taskId) {
            event.preventDefault();
            const action = await this.orm.call('project.task', 'get_formview_action', [[taskId]], {context: this.env.user_context});
            this.actionService.doAction(action, { on_close_reload: true });
        }
    }

    return HtmlFieldOWL;
});