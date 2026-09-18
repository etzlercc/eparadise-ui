/**
 * Arquivo inicial para lógica de dashboard de robôs.
 * Aqui você pode conectar WebSockets ou MQTT para atualização ao vivo.
 */

odoo.define('eparadise_ui.robot_dashboard', function (require) {
    'use strict';

    const core = require('web.core'); // Utilizado para traduções compatíveis com o Odoo.
    const Dialog = require('web.Dialog'); // Placeholder visual até o dashboard em tempo real existir.

    const _t = core._t;

    function showPlaceholder() { // Mantém um ponto de entrada para conectar WebSockets ou MQTT depois.
        Dialog.alert(null, _t('Integração ROS em desenvolvimento. Este arquivo será usado para dashboards em tempo real.'));
    }

    return {
        showPlaceholder,
    };
});
