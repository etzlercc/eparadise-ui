# firmware_esp32

Código e exemplos de firmware para o ESP32-WROVER-E presente na UDOO KEY Pro.

## Objetivo

- Enviar telemetria de sensores ao gateway ROS 2.
- Receber comandos remotos encaminhados pelo gateway.
- Ler a IMU MPU-6500 e o microfone digital da versão Pro.
- Comunicar por MQTT, HTTP, serial ou outro protocolo definido pelo gateway.
- Delegar ao RP2040 as rotinas de GPIO e controle de baixo nível que exigem temporização precisa.

## Limites do firmware

O firmware não deve conter regras empresariais, credenciais administrativas do Odoo ou lógica de fila de tarefas. Ele deve receber comandos validados, executar a ação local e publicar estado, telemetria e erros.

## Próximos passos

1. Criar exemplos usando ESP-IDF ou PlatformIO.
2. Definir o protocolo entre ESP32 e o gateway ROS 2.
3. Implementar conexão MQTT ou HTTP com autenticação.
4. Publicar dados de sensores e receber comandos de atuadores.
5. Documentar pinagem, alimentação, watchdog e comportamento em perda de comunicação.
