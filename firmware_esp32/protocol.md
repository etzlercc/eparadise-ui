# Protocolo de comunicação UDOO KEY Pro ↔ gateway ROS

## Objetivo

Definir um contrato mínimo para que a UDOO KEY Pro possa receber comandos do gateway ROS e responder com telemetria e resultado operacional.

## 1. Fluxo geral

1. O gateway HTTP recebe um comando do Odoo.
2. O gateway publica a mensagem em um tópico ROS 2.
3. O nó ROS 2 encaminha a mensagem para a UDOO KEY Pro por Wi-Fi, MQTT ou outro canal definido.
4. O firmware da UDOO executa a ação e publica um retorno.
5. O gateway transforma esse retorno em payload JSON e o envia ao Odoo.

## 2. Mensagem de comando enviada pelo gateway

```json
{
  "task_id": 42,
  "robot_id": 7,
  "command": "navigate_to",
  "priority": "1",
  "params": {
    "x": 2.5,
    "y": 1.1,
    "yaw": 0.0
  }
}
```

### Campos

- `task_id`: identificador da tarefa no Odoo.
- `robot_id`: identificador do robô no Odoo.
- `command`: ação a ser executada pelo firmware.
- `priority`: prioridade do comando.
- `params`: parâmetros específicos do comando.

## 3. Resposta do firmware

```json
{
  "task_id": 42,
  "robot_id": 7,
  "status": "running",
  "progress": 35,
  "battery": 88,
  "location": {
    "x": 2.1,
    "y": 1.0
  },
  "message": "moving toward goal"
}
```

### Status esperados

- `accepted`
- `running`
- `done`
- `failed`
- `cancelled`

## 4. Comandos mínimos recomendados

- `ping`
- `status`
- `navigate_to`
- `stop`
- `reset`
- `reboot`

## 5. Regras de implementação

- O firmware nunca deve interpretar regras de negócio do Odoo.
- Cada comando deve retornar estado e telemetria.
- Falhas devem ser reportadas com `status: "failed"` e `message` explicativo.
- Em perda de comunicação, o firmware deve entrar em modo seguro.
- O RP2040 deve cuidar de GPIO e atuadores; o ESP32 deve cuidar de comunicação e sensores.

## 6. Segurança

- Autenticar o par de comunicação entre gateway e UDOO.
- Usar tokens ou chaves por robô.
- Restringir comandos por lista branca.
- Registrar logs de comando, resposta e falha.
