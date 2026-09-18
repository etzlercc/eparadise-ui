# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EpTask(models.Model):
    _name = 'ep.task'  # Tarefa operacional gerenciada pelo Odoo e executada pelo gateway ROS.
    _description = 'Tarefa de robô eParadise'
    _order = 'priority desc, create_date desc'

    name = fields.Char(string='Tarefa', required=True)
    description = fields.Text(string='Descrição')
    robot_id = fields.Many2one(
        'ep.robot',
        string='Robô',
        required=True,
        ondelete='restrict',
    )
    state = fields.Selection(
        [
            ('draft', 'Rascunho'),
            ('queued', 'Na fila'),
            ('running', 'Em execução'),
            ('done', 'Concluída'),
            ('failed', 'Falhou'),
            ('cancelled', 'Cancelada'),
        ],
        string='Estado',
        default='draft',
        required=True,
    )
    priority = fields.Selection(
        [('0', 'Normal'), ('1', 'Alta')],
        string='Prioridade',
        default='0',
        required=True,
    )
    command = fields.Char(string='Comando ROS', required=True)
    progress = fields.Float(string='Progresso (%)', default=0.0)
    result_message = fields.Text(string='Resultado')
    started_at = fields.Datetime(string='Iniciada em', readonly=True)
    completed_at = fields.Datetime(string='Concluída em', readonly=True)

    @api.constrains('progress')
    def _check_progress(self):
        for task in self:
            if not 0 <= task.progress <= 100:
                raise ValidationError(_('O progresso deve estar entre 0 e 100%.'))

    def action_queue(self):
        for task in self:
            task.write({'state': 'queued', 'result_message': False})
        return True

    def action_send_command(self):
        self.ensure_one()  # Uma tarefa é enviada individualmente para manter o rastreamento do resultado.
        if self.state not in ('draft', 'queued'):
            raise UserError(_('Somente tarefas em rascunho ou na fila podem ser enviadas.'))

        payload = {
            'task_id': self.id,
            'robot_id': self.robot_id.id,
            'command': self.command,
            'priority': self.priority,
        }
        result = self.env['ep.ros.client'].send_command(self.robot_id.ros_topic, payload)
        if result.get('error'):
            self.write({'state': 'failed', 'result_message': result['error']})
            raise UserError(_('Erro ao enviar tarefa para o ROS: %s') % result['error'])

        self.write({
            'state': 'running',
            'started_at': fields.Datetime.now(),
            'progress': 0.0,
        })
        return result

    def action_cancel(self):
        for task in self:
            if task.state in ('done', 'failed', 'cancelled'):
                continue
            task.write({'state': 'cancelled', 'completed_at': fields.Datetime.now()})
        return True
