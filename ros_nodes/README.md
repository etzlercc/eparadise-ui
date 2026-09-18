# ros_nodes

Pacotes ROS 2 e nós customizados para integração com o addon Odoo `eparadise_ui`. Este código será executado na VM Ubuntu, não no BIGLinux host e não diretamente na UDOO KEY Pro.

## Objetivo

- Receber no gateway HTTP as tarefas publicadas pelo Odoo na VM Ubuntu.
- Traduzir comandos de `ep.task` para tópicos ROS 2 e protocolos da UDOO KEY Pro.
- Publicar telemetria da UDOO para o Odoo via API, MQTT ou rosbridge.

## Contrato do gateway

O gateway deve escutar em `0.0.0.0:8080` e expor `POST /api/v1/commands`. O corpo recebido pelo Odoo contém `topic` e `msg`; dentro de `msg` ficam `task_id`, `robot_id`, `command` e `priority`.

O gateway deve validar o robô e o comando, publicar a mensagem em ROS 2 e retornar JSON com aceite ou erro. A atualização de progresso deve usar um canal autenticado de retorno para o Odoo.

## Próximos passos

1. Na VM Ubuntu, crie um pacote com `ros2 pkg create eparadise_ros --build-type ament_python`.
2. Implemente o endpoint `POST /api/v1/commands` na porta `8080`.
3. Converta `task_id`, `robot_id`, `command` e `priority` em mensagens ROS 2.
4. Publique status, bateria, localização e resultado para atualizar `ep.robot` e `ep.task`.
5. Use `rosbridge_suite` opcionalmente para clientes WebSocket, sem tratá-lo como endpoint HTTP.

## Execução na VM

O workspace ROS deve ficar no disco da VM para evitar lentidão e incompatibilidades de permissões em pastas compartilhadas. O VS Code no BIGLinux pode acessá-lo pela extensão Remote - SSH.
