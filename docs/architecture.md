# Arquitetura eParadise UI

## 1. Visao geral

O eParadise UI integra o Odoo com uma camada de robótica baseada em ROS 2. O Odoo mantém o contexto empresarial e operacional; o gateway ROS 2 executa a comunicação com os robôs; e a UDOO KEY Pro realiza o controle embarcado de sensores e atuadores.

A UDOO KEY Pro não executa Ubuntu, Odoo ou ROS 2. Ela combina um ESP32-WROVER-E e um RP2040 para funções de IoT e controle de baixo nível.

## 2. Topologia do ambiente

```text
ASUS X571GT / BIGLinux
├── VS Code
├── Odoo 16 + PostgreSQL 15 (Docker)
└── VM Ubuntu 24.04
    ├── ROS 2 Jazzy
    ├── pacote eparadise_ros
    └── gateway HTTP :8080
          |
          | rede bridge: HTTP, MQTT, Wi-Fi ou serial
          v
      UDOO KEY Pro
      ├── ESP32-WROVER-E
      │   ├── Wi-Fi e Bluetooth
      │   ├── IMU MPU-6500
      │   └── microfone digital
      └── RP2040
          ├── GPIO
          ├── controle de baixo nivel
          └── comunicacao com o ESP32
```

O VS Code permanece no BIGLinux. O desenvolvimento ROS deve usar Remote - SSH para executar terminal, Python, `colcon` e ferramentas ROS dentro da VM.

## 3. Responsabilidades

### Odoo e eParadise UI

- Cadastro de robôs no modelo `ep.robot`.
- Cadastro e acompanhamento de tarefas no modelo `ep.task`.
- Controle de usuários, permissões e histórico empresarial.
- Envio de comandos ao gateway HTTP da VM.
- Recebimento futuro de telemetria e resultados de tarefas.

### VM Ubuntu e ROS 2

- Executar nós ROS 2 e o pacote `eparadise_ros`.
- Expor `POST /api/v1/commands` na porta `8080`.
- Validar comandos recebidos do Odoo.
- Converter tarefas Odoo em mensagens e tópicos ROS 2.
- Publicar telemetria e resultados de volta para o Odoo.

### UDOO KEY Pro

- Executar firmware no ESP32 e no RP2040.
- Ler IMU, microfone e sensores conectados.
- Controlar GPIO, motores e atuadores.
- Enviar telemetria para o gateway.
- Não armazenar regras empresariais nem assumir a função do servidor ROS.

## 4. Fluxo de uma tarefa

1. Um usuário cria uma tarefa em `ep.task` e seleciona um `ep.robot`.
2. A tarefa recebe estado `draft` e pode ser colocada em `queued`.
3. O botão de envio cria um payload HTTP para a VM.
4. O gateway valida o payload e publica o comando no ROS 2.
5. O nó ROS responsável encaminha o comando para a UDOO KEY Pro.
6. A UDOO executa a ação e publica progresso, estado ou erro.
7. O gateway envia o resultado ao Odoo.
8. O Odoo atualiza `ep.task` e `ep.robot`.

Estados suportados por `ep.task`:

```text
draft -> queued -> running -> done
                       |         \
                       v          failed
                    cancelled
```

## 5. Contrato HTTP do gateway

O addon Odoo usa uma chamada HTTP para não acoplar o servidor Odoo a bibliotecas específicas de WebSocket. O endpoint configurado em `EP_ROS_ENDPOINT` representa a raiz do gateway na VM.

### Envio de comando

`POST {EP_ROS_ENDPOINT}/api/v1/commands`

Exemplo de corpo:

```json
{
  "topic": "/eparadise/command",
  "msg": {
    "task_id": 42,
    "robot_id": 7,
    "command": "navigate_to",
    "priority": "1"
  }
}
```

O gateway deve responder com JSON. Uma resposta de sucesso pode conter:

```json
{
  "accepted": true,
  "task_id": 42,
  "message": "command queued"
}
```

Erros devem usar um status HTTP de falha e, quando possível, o formato:

```json
{
  "error": "robot unavailable"
}
```

`rosbridge_suite` pode ser usado para clientes WebSocket, mas não deve ser tratado como se oferecesse automaticamente o endpoint HTTP usado pelo addon.

## 6. Modelo de dados do addon

### `ep.robot`

Representa um robô ou unidade embarcada:

- `name`: identificação exibida no Odoo.
- `status`: `offline`, `idle`, `running` ou `alert`.
- `battery_level`: percentual de bateria.
- `location`: localização informada pela telemetria.
- `last_seen`: último contato conhecido.
- `ros_topic`: tópico usado pelo gateway para comandos.

### `ep.task`

Representa uma ação operacional:

- `robot_id`: robô responsável pela execução.
- `state`: ciclo de vida da tarefa.
- `priority`: normal ou alta.
- `command`: comando interpretado pelo gateway ROS 2.
- `progress`: percentual entre 0 e 100.
- `result_message`: resultado ou erro informado pelo gateway.
- `started_at` e `completed_at`: auditoria temporal.

## 7. Hardware da UDOO KEY Pro

Segundo a documentação oficial da UDOO:

- Formato aproximado de 130 x 40 x 10,9 mm.
- Alimentação de 5 V DC por USB Type-C.
- ESP32-WROVER-E com Wi-Fi, Bluetooth, 16 MB de Flash e 8 MB de PSRAM.
- RP2040 dual-core ARM Cortex-M0+ a 133 MHz, com 264 KB de SRAM e Flash QSPI de 8 MB.
- IMU MPU-6500 de seis eixos, exclusiva da versão Pro.
- Microfone digital omnidirecional SPK0838HT4H, exclusivo da versão Pro.
- Interfaces UART, I2C, SPI, GPIO e SWD.

Os pinos GP0 e GP1 participam da comunicação entre ESP32 e RP2040 e não devem ser presumidos como GPIOs livres.

## 8. Implantacao

### Requisitos

- BIGLinux no ASUS X571GT.
- Docker e Docker Compose no host.
- VM Ubuntu 24.04 em arquitetura x86_64.
- 4 vCPUs e 8 GB de RAM alocados inicialmente para a VM.
- ROS 2 Jazzy instalado na VM.
- Rede bridge ou outra configuração que permita comunicação entre host, VM e UDOO.

### Odoo no host

Crie `deployment/.env` no Desktop:

```dotenv
EP_ROS_ENDPOINT=http://IP_DA_VM:8080
```

Substitua `IP_DA_VM` pelo endereço real da VM. Depois, execute:

```bash
docker compose -f deployment/docker-compose.yml up -d
```

O parâmetro de sistema Odoo `eparadise_ui.ros_endpoint`, quando definido, tem prioridade sobre a variável de ambiente.

### ROS na VM

O gateway deve escutar em `0.0.0.0:8080`, e não somente em `127.0.0.1`, para aceitar conexões do container Odoo. A porta deve ser liberada no firewall da VM apenas para a rede confiável.

## 9. Segurança

A implementação atual é um scaffold de desenvolvimento. Antes de uso em rede não confiável, é necessário:

- autenticar o gateway HTTP;
- usar HTTPS ou uma rede privada/VPN;
- validar `robot_id`, `task_id` e comandos permitidos;
- limitar tamanho e frequência das requisições;
- registrar usuário, horário e resultado de cada comando;
- separar permissões de leitura, operação e administração;
- proteger credenciais MQTT, Odoo e dispositivos embarcados;
- impedir que comandos arbitrários sejam convertidos diretamente em execução de shell.

## 10. Estado atual e próximos passos

Implementado:

- modelos `ep.robot` e `ep.task`;
- views Odoo e permissões básicas;
- cliente HTTP configurável para o gateway da VM;
- Compose de desenvolvimento para Odoo e PostgreSQL;
- documentação da topologia BIGLinux, VM e UDOO KEY Pro.

Ainda necessário:

1. Implementar o gateway HTTP no pacote `eparadise_ros`.
2. Criar o nó ROS 2 que conversa com o ESP32/RP2040.
3. Definir o formato de telemetria e o endpoint de atualização do Odoo.
4. Adicionar autenticação e testes de integração.
5. Criar firmware ESP32/RP2040 para o hardware específico do robô.
6. Adicionar monitoramento, logs e recuperação de falhas.
