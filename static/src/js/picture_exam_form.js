odoo.define('aws_question.exam_question_form', function (require) {
'use strict';

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var FormRenderer = require('web.FormRenderer');
    var viewRegistry = require('web.view_registry');

    var EmployeeFormRenderer = FormRenderer.extend({
         dynamicallyLoadScript(url) {
        var script = document.createElement("script");  // create a script DOM node
         script.src = url;  // set its src to the provided URL

        document.head.appendChild(script);  // add it to the end of the head section of the page (could change 'head' to 'body' to add it to the end of the body section instead)
       },
        dynamicallyLoadCss(url) {
        var script = document.createElement("link");  // create a script DOM node
         script.href = url;  // set its src to the provided URL
         script.type = 'text/cs';  // set its src to the provided URL
         script.rel = 'stylesheet';  // set its src to the provided URL

        document.head.appendChild(script);  // add it to the end of the head section of the page (could change 'head' to 'body' to add it to the end of the body section instead)
       },

        /**
         * @override
         */
        _render: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
              self.dynamicallyLoadScript('/aws_question/static/src/js/countdown.js');
              self.dynamicallyLoadCss('/aws_question/static/src/css/countdown.css');
            });
        },

        destroy: function () {
            this.$el.find('.o_employee_chat_btn').off('click');
            return this._super();
        },

        _onOpenChat: function(ev) {
            ev.preventDefault();
            ev.stopImmediatePropagation();
            this.trigger_up('open_chat', {
                partner_id: this.state.data.user_partner_id.res_id
            });
            return true;
        },
    });

    var EmployeeFormController = FormController.extend({
        custom_events: _.extend({}, FormController.prototype.custom_events, {
            open_chat: '_onOpenChat'
        }),

        _onOpenChat: function(ev) {
            var self = this;
            var dmChat = this.call('mail_service', 'getDMChatFromPartnerID', ev.data.partner_id);
            if (dmChat) {
                dmChat.detach();
            } else {
                var def = this.call('mail_service', 'createChannel', ev.data.partner_id, 'dm_chat').then(function (dmChatId) {
                    dmChat = self.call('mail_service', 'getChannel', dmChatId);
                    dmChat.detach();
                });
                Promise.resolve(def);
            }
        },
    });

    var EmployeeFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: EmployeeFormController,
            Renderer: EmployeeFormRenderer
        }),
    });

    viewRegistry.add('aws_question_exam_question_form', EmployeeFormView);
    return EmployeeFormView;
});
