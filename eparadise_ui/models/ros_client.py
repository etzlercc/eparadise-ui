# -*- coding: utf-8 -*-
import json
import logging
import os
import urllib.request
import urllib.error

from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EpROSClient(models.AbstractModel):
    _name = "ep.ros.client"  # Modelo abstrato centraliza a comunicação sem criar registros.
    _description = "Helper de Integração ROS"

    def _get_ros_endpoint(self):
        config = self.env['ir.config_parameter'].sudo()  # A configuração pode ser alterada sem editar o addon.
        endpoint = config.get_param('eparadise_ui.ros_endpoint') or os.getenv('EP_ROS_ENDPOINT')  # O endereço aponta para a VM, nunca para localhost do container.
        if not endpoint:
            raise UserError('Configure eparadise_ui.ros_endpoint com o endereço do rosbridge na VM ROS 2.')
        return endpoint.rstrip('/')

    def send_command(self, topic, payload):
        endpoint = '%s/api/v1/commands' % self._get_ros_endpoint()  # Gateway HTTP da VM traduz o comando para ROS 2.
        data = {'topic': topic, 'msg': payload}  # Formato esperado pelo serviço de publicação ROS.
        body = json.dumps(data).encode('utf-8')  # urllib exige o corpo da requisição em bytes.
        request = urllib.request.Request(
            endpoint,
            data=body,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:  # Evita bloquear uma requisição do Odoo indefinidamente.
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as exc:
            message = exc.read().decode('utf-8')
            _logger.exception('Erro HTTP ao enviar comando ROS: %s', message)
            return {'error': message}
        except Exception as exc:
            _logger.exception('Falha ao enviar comando ROS: %s', exc)
            return {'error': str(exc)}
