# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class EpRobot(models.Model):
    _name = 'ep.robot'  # Nome técnico usado pelo ORM e pelas views do Odoo.
    _description = 'Robô eParadise'
    _order = 'name'

    name = fields.Char(string='Nome', required=True)
    description = fields.Text(string='Descrição')
    active = fields.Boolean(string='Ativo', default=True)
    status = fields.Selection(  # Estados operacionais exibidos no painel da frota.
        [
            ('offline', 'Offline'),
            ('idle', 'Idle'),
            ('running', 'Em operação'),
            ('alert', 'Alerta'),
        ],
        string='Status',
        default='offline',
    )
    battery_level = fields.Float(string='Nível da bateria (%)')
    location = fields.Char(string='Localização atual')
    last_seen = fields.Datetime(string='Última conexão')
    ros_topic = fields.Char(string='Tópico ROS', default='/eparadise/command')  # O gateway ROS 2 encaminha este tópico à UDOO KEY Pro.

    def action_send_command(self):
        self.ensure_one()  # O botão da view deve atuar sobre um único robô.
        payload = {
            'robot_id': self.id,
            'command': 'status_request',
            'metadata': {'name': self.name},
        }
        result = self.env['ep.ros.client'].send_command(self.ros_topic, payload)  # Encaminha o comando pela ponte ROS.
        if result.get('error'):
            raise UserError(_('Erro ao enviar comando ROS: %s') % result['error'])
        return result

