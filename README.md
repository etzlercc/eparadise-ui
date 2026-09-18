# eParadise UI (EPUI)

Addon Odoo para integração de robôs, ROS 2 e hardware embarcado.

> "A evolução da Integração de Robôs, Internet das Coisas (IoT) e Gestão Organizacional para um futuro abundante."

O **eParadise UI (EPUI)** une o Odoo, o ROS 2 e controladoras embarcadas para centralizar cadastro de robôs, execução de tarefas, telemetria e integração com processos empresariais.

O projeto mantém as regras de negócio no Odoo, a execução robótica em um gateway ROS 2 e o controle de baixo nível na UDOO KEY Pro. Essa separação permite desenvolver a interface no BIGLinux sem transformar a placa embarcada em um servidor empresarial.

Para a arquitetura completa, consulte [`docs/architecture.md`](docs/architecture.md).

---

## Arquitetura atual

O ambiente de desenvolvimento usa o BIGLinux como sistema hospedeiro. O VS Code e o Odoo ficam no Desktop, enquanto uma VM Ubuntu 24.04 executa o ROS 2 Jazzy. A UDOO KEY Pro atua como controladora embarcada, e não como host Linux do ROS:

```text
BIGLinux no ASUS X571GT
├── VS Code e Odoo/PostgreSQL
└── VM Ubuntu 24.04
	├── ROS 2 Jazzy
	├── gateway HTTP eparadise_ros
	└── rosbridge_suite (opcional para clientes WebSocket)
			|
			| Wi-Fi, Ethernet, MQTT ou serial
			v
		UDOO KEY Pro
		├── ESP32: conectividade, IMU e microfone
		└── RP2040: GPIO e controle de baixo nível
```

O VS Code permanece no BIGLinux e acessa o workspace ROS pela extensão Remote - SSH. O modo bridge da VM é recomendado para que o gateway HTTP tenha um IP alcançável pela UDOO e pelo Odoo.

---

## Funcionalidades

* **Robôs:** cadastro de status, bateria, localização, último contato e tópico ROS.
* **Tarefas:** associação de `ep.task` a `ep.robot`, fila, prioridade, progresso, resultado e cancelamento.
* **Gateway:** envio HTTP para o gateway ROS 2 hospedado na VM Ubuntu.
* **Hardware:** integração prevista com ESP32 e RP2040 da UDOO KEY Pro.
* **Evolução planejada:** telemetria, alertas, autenticação, logs e integração com módulos Odoo.

## Ambiente de desenvolvimento

1. Execute BIGLinux no ASUS X571GT como host.
2. Reserve 4 vCPUs e 8 GB de RAM para uma VM Ubuntu 24.04.
3. Instale ROS 2 Jazzy e o gateway HTTP `eparadise_ros` na VM.
4. Use rede bridge e descubra o IP da VM, por exemplo `192.168.1.50`.
5. Crie `deployment/.env` com `EP_ROS_ENDPOINT=http://192.168.1.50:8080`.
6. Inicie Odoo e PostgreSQL com `docker compose -f deployment/docker-compose.yml up -d`.
7. Para desenvolvimento ROS, abra o workspace da VM no VS Code pela extensão Remote - SSH.

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
