import logging
logger = logging.getLogger(__name__)

import os
import importlib
from datetime import datetime
import time
from typing import Dict, Callable
import socket
import yaml

from .executor import Executor
from unicorncommon.dbagent_client import DBAgentException, DBAgentClient

def get_yaml_config(cfg_dir, filename):
    full_path = os.path.join(cfg_dir, filename)
    with open(full_path, "r") as f:
        return yaml.safe_load(f)

def get_dbagent_client(cfg_dir):
    dbagent_client_cfg = get_yaml_config(cfg_dir, "dbagent_client.yaml")

    classname   = dbagent_client_cfg['classname']
    module      = importlib.import_module('.'.join(classname.split(".")[:-1]))
    klass       = getattr(module, classname.split('.')[-1])

    dbagent_client_cfg.pop("classname")
    dbagent_client = klass(**dbagent_client_cfg)
    return dbagent_client

def get_pmonitor_server(cfg_dir):
    pmonitor_server_cfg = get_yaml_config(cfg_dir, "pmonitor_server.yaml")

    classname   = pmonitor_server_cfg['classname']
    module      = importlib.import_module('.'.join(classname.split(".")[:-1]))
    klass       = getattr(module, classname.split('.')[-1])

    pmonitor_server_cfg.pop("classname")
    pmonitor_server = klass(**pmonitor_server_cfg)
    return pmonitor_server

def main(daemon_args: Dict, quit_requested: Callable[[], bool]) -> None:
    logger.info("main: enter")

    cfg_dir     = daemon_args['cfg_dir']
    node_id     = daemon_args['node_id']
    data_dir    = daemon_args['data_dir']
    logger.info(f"cfg_dir  = {cfg_dir}")
    logger.info(f"node_id  = {node_id}")
    logger.info(f"data_dir = {data_dir}")

    dbagent_client = DBAgentClient(get_dbagent_client(cfg_dir))
    pmonitor_server = get_pmonitor_server(cfg_dir)
    # hack, not all server_endpoint has "ip" field
    ip = get_yaml_config(cfg_dir, "pmonitor_server.yaml")["server_endpoint"].get("ip")
    logger.info(f"ip={ip}")

    agent_classname, agent_endpoint = pmonitor_server.get_client()
    try:
        dbagent_client.set_node_up(node_id, agent_classname=agent_classname, agent_endpoint=agent_endpoint, ip=ip)
        logger.info(f"main: node {node_id} is registered")
    except DBAgentException as e:
        logger.warn(f"main: unable to register node, node_id={node_id}, error: {str(e)}")

    # now enter the main loop
    executor = Executor(
        dbagent_client=dbagent_client,
        base_data_dir=data_dir,
        node_id=node_id,
        cfg_dir=cfg_dir
    )
    pmonitor_server.start_server(executor, quit_requested)

    try:
        dbagent_client.set_node_down(node_id)
        logger.info(f"main: node {node_id} is deregistered")
    except DBAgentException as e:
        logger.warn(f"main: unable to deregister node, node_id={node_id}, error: {str(e)}")

    logger.info("pmonitor shutdown gracefully")
    logger.info("main: exit")
