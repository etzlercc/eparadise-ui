# -*- coding: utf-8 -*-
{
    "name": "eParadise UI",
    "version": "1.0.0",
    "summary": "Addon Odoo para integração ROS e monitoramento de robôs.",
    "description": "Integra o Odoo no BIGLinux com um gateway ROS 2 Jazzy executado em VM Ubuntu e controladoras UDOO KEY Pro.",
    "category": "Operations/IoT",
    "author": "eParadise",
    "website": "https://github.com/eparadise/eparadise-ui",
    "license": "LGPL-3",
    "depends": ["base", "web"],  # Fornece ORM, permissões e componentes do backend web.
    "data": [  # Arquivos carregados durante a instalação/atualização do módulo.
        "security/ir.model.access.csv",
        "views/robot_views.xml",
        "views/task_views.xml",
    ],
    "assets": {  # Registra o JavaScript no bundle do backend do Odoo.
        "web.assets_backend": [
            "eparadise_ui/static/src/js/robot_dashboard.js",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
