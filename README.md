# eParadise UI (EPUI)

Addon Odoo para integração de robôs, ROS 2 e hardware embarcado.

> "A evolução da Integração de Robôs, Internet das Coisas (IoT) e Gestão Organizacional para um futuro abundante."

O **eParadise UI (EPUI)** une o Odoo, o ROS 2 e controladoras embarcadas para centralizar cadastro de robôs, execução de tarefas, telemetria e integração com processos empresariais.

O projeto mantém as regras de negócio no Odoo, a execução robótica em um gateway ROS 2 e o controle de baixo nível na UDOO KEY Pro. Essa separação permite desenvolver a interface no BIGLinux sem transformar a placa embarcada em um servidor empresarial.

Para a arquitetura completa, consulte [`docs/architecture.md`](docs/architecture.md).

---

## Arquitetura atual

A arquitetura atual separa funções por máquina. A máquina ROS concentra o desenvolvimento e o ambiente de robótica; a máquina Odoo fica responsável pelo backend empresarial. A UDOO KEY Pro atua como controladora embarcada e não como host Linux do ROS:

```text
Máquina Odoo
├── Odoo 16
├── PostgreSQL 15
├── backend empresarial
└── gestão de usuários e tarefas

Máquina ROS
├── Ubuntu 24.04
├── VS Code
├── ROS 2 Jazzy
├── gateway HTTP eparadise_ros
├── rosbridge_suite (opcional para clientes WebSocket)
└── ferramentas de simulação e depuração
        |
        | Wi-Fi, Ethernet, MQTT ou serial
        v
    UDOO KEY Pro
    ├── ESP32: conectividade, IMU e microfone
    └── RP2040: GPIO e controle de baixo nível
```

O VS Code permanece na máquina ROS e acessa o workspace do projeto em Ubuntu. O gateway HTTP deve ficar acessível na rede para a UDOO e para a máquina Odoo.

---

## Funcionalidades

* **Robôs:** cadastro de status, bateria, localização, último contato e tópico ROS.
* **Tarefas:** associação de `ep.task` a `ep.robot`, fila, prioridade, progresso, resultado e cancelamento.
* **Gateway:** envio HTTP para o gateway ROS 2 hospedado na máquina ROS.
* **Hardware:** integração prevista com ESP32 e RP2040 da UDOO KEY Pro.
* **Evolução planejada:** telemetria, alertas, autenticação, logs e integração com módulos Odoo.

## Ambiente de desenvolvimento

### Máquina Odoo

- Host para o backend empresarial.
- Sem necessidade de GPU dedicada.
- Deve rodar Odoo 16 e PostgreSQL em Docker.
- Deve se conectar ao gateway ROS na máquina ROS.

### Máquina ROS

- Host para Ubuntu 24.04, VS Code e ROS 2 Jazzy.
- Deve reunir desenvolvimento, simulação, depuração e ferramentas ROS.
- Deve ter melhor CPU/GPU para RViz e análise de robótica.
- Deve hospedar o gateway HTTP `eparadise_ros` e, opcionalmente, `rosbridge_suite`.

### Passo a passo

1. Prepare a máquina Odoo com Docker e Docker Compose.
2. Prepare a máquina ROS com Ubuntu 24.04, VS Code e ROS 2 Jazzy.
3. Instale o gateway HTTP `eparadise_ros` na máquina ROS.
4. Configure a rede para que a máquina Odoo consiga alcançar a máquina ROS, por exemplo `http://IP_DA_MAQUINA_ROS:8080`.
5. Crie `deployment/.env` na máquina Odoo com `EP_ROS_ENDPOINT=http://IP_DA_MAQUINA_ROS:8080`.
6. Inicie Odoo e PostgreSQL na máquina Odoo com `docker compose -f deployment/docker-compose.yml up -d`.
7. Para desenvolvimento ROS, abra o workspace diretamente na máquina ROS ou via Remote - SSH.

O parâmetro de sistema Odoo `eparadise_ui.ros_endpoint`, quando configurado, tem prioridade sobre `EP_ROS_ENDPOINT`.

---

## 📂 Estrutura do Repositório

```text
eparadise-ui/
│
├── docs/                         # Arquitetura, contratos e implantação
├── eparadise_ui/                 # Addon Odoo Python/XML/JavaScript
│   ├── models/                   # Robôs, tarefas e cliente do gateway ROS
│   ├── views/                    # Views de robôs e tarefas
│   └── static/src/               # Recursos JavaScript do backend Odoo
│
├── firmware_esp32/               # Códigos fonte para microcontroladores ESP32 (IoT)
├── ros_nodes/                    # Nós e pacotes ROS customizados para comunicação
├── deployment/                   # Compose e configurações do ambiente no BIGLinux
└── README.md
```

## Validação local

```bash
python3 -m py_compile eparadise_ui/models/*.py
python3 -c "import xml.etree.ElementTree as ET; ET.parse('eparadise_ui/views/robot_views.xml'); ET.parse('eparadise_ui/views/task_views.xml')"
node --check eparadise_ui/static/src/js/robot_dashboard.js
docker compose -f deployment/docker-compose.yml config
```

Esses comandos verificam sintaxe e configuração. Testes de instalação do módulo e testes de integração dependem de uma instância Odoo e de um gateway ROS 2 ativos.
