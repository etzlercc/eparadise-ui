# eparadise-ui
Odoo ROS UI Manager Addon - Integração de robótica e gestão empresarial.

# eParadise UI (EPUI) - Odoo ROS UI Manager Addon

> "A evolução da Integração de Robôs, Internet das Coisas (IoT) e Gestão Organizacional para um futuro abundante."

O **eParadise UI (EPUI)** é um projeto pioneiro e de impacto social que une o poder de gestão do **Odoo (ERP)** com a flexibilidade do **ROS (Robot Operating System)** e o universo do hardware embarcado (**IoT/Edge Computing**). 

Nosso objetivo é criar uma interface de usuário (UI) revolucionária e centralizada para monitoramento, telemetria e controle remoto de frotas de robôs e dispositivos conectados, transformando dados técnicos em indicadores organizacionais em tempo real.

Inspirado na visão de John Adolphus Etzler (1836), este projeto busca democratizar o acesso à tecnologia avançada, permitindo a criação de comunidades autossustentáveis onde humanos, robôs e automação colaboram em perfeita harmonia.

---

## 🛠️ Arquitetura e Hardwares Suportados

O ecossistema do eParadise UI foi projetado para ser agnóstico e modular, integrando desde microrcontroladores de baixo custo até computadores de placa única (SBCs) industriais:

* 🐧 **Sistema Operacional Base:** Otimizado e homologado para rodar sobre o **Ubuntu Linux** (ambiente nativo para ROS e servidores Odoo).
* 🧠 **Edge Computing de Alto Desempenho:** Suporte a placas como **UDOO x86**, combinando o poder de processamento de arquitetura PC com sensores embarcados.
* 🤖 **SBCs e Gateways:** Integração com **Raspberry Pi** atuando como nós de computação móvel nos robôs ou hubs de automação local.
* 🔌 **Internet das Coisas (IoT) & Sensores:** Coleta de dados periféricos e acionamentos através de microcontroladores **ESP32**, comunicando via protocolos leves (como MQTT ou WebSockets) diretamente com o Odoo/ROS.

---

## 🚀 Funcionalidades Planejadas

* 📊 **Painel de Controle Centralizado:** Monitoramento do status operacional e localização de robôs e dispositivos IoT diretamente do backend do Odoo.
* 🔄 **Ponte de Comunicação Bidirecional:** Integração nativa (ex: via `rosbridge_suite`) para que comandos do Odoo alterem estados no ROS e vice-versa.
* 📉 **Telemetria de Sensores em Tempo Real:** Gráficos e dashboards atualizados com dados vindos de ESP32, Raspberry Pi e sensores industriais.
* 🔋 **Gestão de Ativos e Frotas:** Rastreamento do desgaste de hardware, nível de bateria dos robôs e agendamento de manutenções preventivas integradas ao módulo de Manutenção do Odoo.

---

## 📂 Estrutura do Repositório

```text
eparadise-ui/
│
├── eparadise_ui/                 # Addon Nativo do Odoo (Módulo Python/JS)
│   ├── models/                   # Modelagem de Robôs, Dispositivos IoT e Sensores
│   ├── views/                    # Views XML e Dashboards Web do Odoo
│   └── static/src/               # JavaScript para conexões em Tempo Real (WebSockets)
│
├── firmware_esp32/               # Códigos fonte para microcontroladores ESP32 (IoT)
├── ros_nodes/                    # Nós e pacotes ROS customizados para comunicação
├── deployment/                   # Scripts de instalação e guias para Ubuntu/Raspberry/UDOO
└── README.md
