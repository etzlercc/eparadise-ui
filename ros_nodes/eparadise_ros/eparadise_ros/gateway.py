# -*- coding: utf-8 -*-
"""Minimal HTTP gateway bridging Odoo commands to ROS 2 topics.

This module is intentionally small and explicit: it accepts a validated JSON
payload from Odoo, publishes the same payload on a ROS topic, and returns a
JSON response describing whether the command was accepted.
"""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
except ModuleNotFoundError:  # pragma: no cover - ROS 2 not installed in the local dev environment.
    rclpy = None
    Node = object
    String = None


class EparadiseGatewayNode(Node):
    """ROS 2 publisher node used by the gateway.

    The command payload is serialized as a JSON string and published to the
    target topic so the robot-side node can parse and dispatch it.
    """

    def __init__(self):
        if rclpy is None:
            raise RuntimeError('ROS 2 is not available in this environment.')
        super().__init__('eparadise_gateway')
        self._publishers = {}

    def publish(self, topic, payload):
        if topic not in self._publishers:
            self._publishers[topic] = self.create_publisher(String, topic, 10)
        msg = String()
        msg.data = json.dumps(payload, ensure_ascii=False)
        self._publishers[topic].publish(msg)
        return {'accepted': True, 'topic': topic, 'message': 'command queued'}


class EparadiseGatewayHandler(BaseHTTPRequestHandler):
    """HTTP endpoint used by the Odoo addon.

    The path is fixed to /api/v1/commands and the body must match the Odoo
    contract: {"topic": "...", "msg": {...}}.
    """

    server_version = 'eparadise_gateway/0.1.0'

    def do_POST(self):
        if self.path != '/api/v1/commands':
            self._send_json(404, {'error': 'not found'})
            return

        try:
            content_length = int(self.headers.get('Content-Length', '0'))
            raw_body = self.rfile.read(content_length)
            payload = json.loads(raw_body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            self._send_json(400, {'error': 'invalid json body'})
            return

        topic = payload.get('topic')
        msg = payload.get('msg')
        if not topic or not isinstance(msg, dict):
            self._send_json(400, {'error': 'expected {"topic": "...", "msg": {...}}'})
            return

        result = self.server.gateway.publish(topic, msg)
        self._send_json(202, result)

    def log_message(self, format, *args):
        # Keep logs concise and easy to follow in a robot deployment.
        return

    def _send_json(self, status_code, body):
        encoded = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


class GatewayServer(ThreadingHTTPServer):
    """Threaded HTTP server used to accept concurrent requests from Odoo."""

    def __init__(self, server_address, gateway):
        self.gateway = gateway
        super().__init__(server_address, EparadiseGatewayHandler)


def run(host='0.0.0.0', port=8080, dry_run=False):
    """Run the gateway.

    Set dry_run=True when the script is used for local validation without a ROS
    2 installation. The server still responds to HTTP requests, but does not
    publish to ROS topics.
    """

    if not dry_run and rclpy is None:
        raise RuntimeError('ROS 2 support is required unless dry_run=True is used.')

    gateway = None
    if not dry_run:
        rclpy.init()
        gateway = EparadiseGatewayNode()
    else:
        gateway = type('DryRunGateway', (), {'publish': lambda self, topic, payload: {'accepted': True, 'topic': topic, 'message': 'dry run accepted'}})()

    server = GatewayServer((host, port), gateway)
    try:
        print(f'Gateway listening on http://{host}:{port}/api/v1/commands')
        server.serve_forever()
    finally:
        server.server_close()
        if gateway and hasattr(gateway, 'destroy_node'):
            gateway.destroy_node()
        if rclpy is not None:
            rclpy.shutdown()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='eParadise ROS gateway')
    parser.add_argument('--host', default=os.getenv('EP_ROS_HOST', '0.0.0.0'))
    parser.add_argument('--port', type=int, default=int(os.getenv('EP_ROS_PORT', '8080')))
    parser.add_argument('--dry-run', action='store_true', help='validates HTTP flow without ROS 2')
    args = parser.parse_args()
    run(host=args.host, port=args.port, dry_run=args.dry_run)
