#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging.config
import logging
import os
import argparse
import json
import sys
import importlib
from shlex import split, quote
import subprocess
import signal

import yaml

from unicorncommon.server_status import SERVER_STATUS
from unicorncommon.dbagent_client import DBAgentException, DBAgentClient

def get_yaml_config(cfg_dir, filename):
    full_path = os.path.join(cfg_dir, filename)
    with open(full_path, "r") as f:
        return yaml.safe_load(f)

#############################################################
# pwrapper exit code
# 0: everything is ok
# 1: invalid arguments, unlikely, if happened, we must have a code bug in executor(inside pmonitor)
# 2: unable to get run details, process not launched.
# 3: unable to create output file for child process, process not launched.
# 4: unable to create input file for child process, process not launched.
# 5: create child process failed, process not launched.
# 6: unable to set run to started after child process is launched, we tried to kill the process.
# 7: unable to remove the task singleton lock after process is terminated
# 8: unable to set run to finished after process is terminated.
# 20: both 6 and 7
#############################################################

def cleanup(run_id, task_id, is_singleton, dbagent_client, *, logger):
    log_prefix = "cleanup"
    if task_id is None or not is_singleton:
        logger.info(f"{log_prefix}: not a task based run nor a singleton task!")
    else:
        try:
            dbagent_client.unset_active_run(task_id)
            logger.info(f"{log_prefix}: task lock released!")
        except DBAgentException as e:
            logger.exception(f"{log_prefix}: failed to release task lock, error is {str(e)}")
    try:
        dbagent_client.delete_run(run_id)
        logger.info(f"{log_prefix}: Run({run_id}) is deleted")
    except DBAgentException as e:
        logger.exception(f"{log_prefix}: failed to delete run, Run({run_id}), error is {str(e)}")

def kill_process(kill_cmd, child_process, *, logger):
    log_prefix = "kill_process"
    if kill_cmd is None:
        logger.info(f"{log_prefix}: send SIGTERM to child process")
        child_process.terminate()
    else:
        logger.info(f"{log_prefix}: execute kill command: \"{kill_cmd}\"")
        try:
            os.system(kill_cmd)
            logger.info(f"{log_prefix}: kill command executed")
        except OSError as e:
            logger.info(f"{log_prefix}: failed to execute kill command, error: {str(e)}")

APP_CTX = { }
def shutdown_handler(logger):
    log_prefix = "shutdown_handler"

    def handler(signal_umber, frame):
        _, _ = signal_umber, frame
        child_process = APP_CTX.get('child_process')
        kill_cmd = APP_CTX.get('kill_cmd')
        if not child_process:
            logger.info(f"{log_prefix}: ignored since no child process found")
            return
        kill_process(kill_cmd, child_process, logger=logger)
    return handler

def json_2_str(obj):
    return json.dumps(obj, indent=4, separators=(',', ': '))


def get_dbagent_client(cfg_dir):
    dbagent_client_cfg = get_yaml_config(cfg_dir, "dbagent_client.yaml")

    classname   = dbagent_client_cfg['classname']
    module      = importlib.import_module('.'.join(classname.split(".")[:-1]))
    klass       = getattr(module, classname.split('.')[-1])

    dbagent_client_cfg.pop("classname")
    dbagent_client = klass(**dbagent_client_cfg)
    return dbagent_client

def get_path(path):
    if path is None:
        return None
    path = path.strip()
    if len(path) == 0:
        return None
    return os.path.expandvars(path)

def generate_execute_command(application, args):
    cmd = ""

    venv_dir = get_path(application.get('venv_dir'))
    if venv_dir is not None:
        # if the application has venv_dir, we need to activate virtual environment
        cmd += f"source {os.path.join(venv_dir, 'bin', 'activate')}\n"

    entry = application['entry']
    if entry.endswith(".py"):
        cmd_line = f"python {entry}"
    else:
        cmd_line = f"{entry}"
    for arg in args:
        cmd_line += f" {quote(arg)}"
    cmd += f"{cmd_line}\n"
    return cmd


def main():
    parser = argparse.ArgumentParser(
        description='Process Wrapper for Unicorn Cluster Manager'
    )
    parser.add_argument(
        "-r", "--run-id", type=str, required=True, help="Specify the run id for the wrapper"
    )
    parser.add_argument(
        "-t", "--task-id", type=str, required=False, help="Specify the task id for the wrapper"
    )
    parser.add_argument(
        "--is-singleton", action="store_true", help="Specify if the task is a single"
    )
    parser.add_argument(
        "--data-dir", type=str, required=True, help="Specify the data directory"
    )
    parser.add_argument(
        "--cfg-dir", type=str, required=True, help="Specify the config directory"
    )
    args = parser.parse_args()

    run_id = int(args.run_id)
    if args.task_id is None:
        task_id = None
    else:
        task_id = int(args.task_id)
    run_dir = os.path.join(args.data_dir, "runs", str(run_id))
    cfg_dir = args.cfg_dir
    is_singleton = args.is_singleton

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "fileHandler": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": f"{run_dir}/pwrapper.log",
            },
        },
        "loggers": {
            "": {
                "handlers": ["fileHandler"],
                "level":    "DEBUG",
                "propagate": True
            },
        },
        "root": {
            "handlers": ["fileHandler"],
            "level": "DEBUG",
        },
    })

    logger = logging.getLogger(__name__)
    log_prefix = "main"
    logger.info(f"{log_prefix}: enter")
    logger.info(f"{log_prefix}: args={args}")
    logger.info(f"{log_prefix}: run_id={run_id}")
    logger.info(f"{log_prefix}: task_id={task_id}")
    logger.info(f"{log_prefix}: is_singleton={is_singleton}")
    logger.info(f"{log_prefix}: run_dir={run_dir}")
    logger.info(f"{log_prefix}: cfg_dir={cfg_dir}")

    if is_singleton and task_id is None:
        # There must be a bug in executor if we are here
        logger.error(f"{log_prefix}: task_id MUST be specified for singleton task")
        sys.exit(1)

    # get dbagent client
    dbagent_client = DBAgentClient(get_dbagent_client(cfg_dir), logger=logger)

    try:
        run = dbagent_client.get_run(run_id)
    except DBAgentException as e:
        logger.exception(f"{log_prefix}: failed to get run info, erro: {str(e)}")
        # we need to delete the run created by pmonitor, we have not set run to started yet
        cleanup(run_id, task_id, is_singleton, dbagent_client, logger=logger)
        logger.info(f"{log_prefix}: exit")
        sys.exit(2)

    logger.info(f"{log_prefix}: run loaded\n{json_2_str(run)}\n")
    application = run['application']
    task = run['task']
    app_args = json.loads(run['args'])
    app_input = run.get('input')
    cmd = generate_execute_command(application, app_args)
    logger.info(f"{log_prefix}: generate command: cmd=\"{cmd}\"")

    if task is None:
        kill_cmd = None
    else:
        kill_cmd = task.get("kill_cmd")
        if kill_cmd is not None and len(kill_cmd.strip()) == 0:
            kill_cmd = None
    APP_CTX['kill_cmd'] = kill_cmd
    logger.info(f"{log_prefix}: kill_cmd: \"{kill_cmd}\", stored in APP_CTX")

    # create output file
    out_f = None
    filename = os.path.join(run_dir, "out.txt")
    try:
        out_f = open(filename, "wb")
        logger.info(f"{log_prefix}: output file \"{filename}\" is generated")
    except OSError as e:
        logger.exception(f"{log_prefix}: failed to generate output file \"{filename}\", error: {str(e)}")
        cleanup(run_id, task_id, is_singleton, dbagent_client, logger=logger)
        logger.info(f"{log_prefix}: exit")
        sys.exit(3)

    # create stdin if needed
    in_f = None
    if app_input is not None:
        filename = os.path.join(run_dir, "input.txt")
        try:
            with open(filename, "wb") as tmp_f:
                tmp_f.write(app_input.encode("utf-8"))
            in_f = open(filename, "rb")
            logger.info(f"{log_prefix}: input file \"{filename}\" is generated")
        except OSError as e:
            logger.exception(f"{log_prefix}: failed to generate input file \"{filename}\", error: {str(e)}")
            cleanup(run_id, task_id, is_singleton, dbagent_client, logger=logger)
            logger.info(f"{log_prefix}: exit")
            sys.exit(4)

    home_dir = get_path(application.get("home_dir"))
    try:
        child_process = subprocess.Popen(
            cmd,
            cwd = home_dir,
            shell = True,
            stdin = subprocess.DEVNULL if in_f is None else in_f.fileno(),
            stdout = out_f,
            stderr = subprocess.STDOUT
        )
        launched = True
        logger.info(f"{log_prefix}: child process launched, pid={child_process.pid}")
    except OSError as e:
        logger.exception(f"{log_prefix}: failed to launch child process, error: {str(e)}")
        cleanup(run_id, task_id, is_singleton, dbagent_client, logger=logger)
        logger.info(f"{log_prefix}: exit")
        sys.exit(5)
    finally:
        if out_f is not None:
            try:
                out_f.close()
            except OSError as e:
                logger.exception(f"{log_prefix}: failed to close output file handle, error: {str(e)}")
        if in_f is not None:
            try:
                in_f.close()
            except OSError as e:
                logger.exception(f"{log_prefix}: failed to close input file handle, error: {str(e)}")

    try:
        dbagent_client.set_run_started(run_id)
        logger.info(f"{log_prefix}: set run({run_id}) to started!")
    except DBAgentException as e:
        logger.exception(f"{log_prefix}: failed to set run({run_id}) to started, error: {str(e)}")
        logger.info(f"{log_prefix}: terminate child process")
        kill_process(kill_cmd, child_process, logger=logger)
        logger.info(f"{log_prefix}: wait for child process to finish")
        child_process.wait()
        logger.info(f"{log_prefix}: child process finished")
        logger.info(f"{log_prefix}: exit")
        sys.exit(6)

    APP_CTX['child_process'] = child_process
    old_term_handler = signal.signal(signal.SIGTERM, shutdown_handler(logger))
    logger.info(f"{log_prefix}: wait for child process to finish")
    child_process.wait()

    # restore the old signal handler for kill since the child process is already finished
    signal.signal(signal.SIGTERM, old_term_handler)
    logger.info(f"{log_prefix}: child process finished with exit code({child_process.returncode})")

    # need to set run to stopped
    exit_code = 0
    if task is None or not task['is_singleton']:
        logger.info(f"{log_prefix}: not task related nor a singleton")
    else:
        try:
            dbagent_client.unset_active_run(task['id'])
            logger.info(f"{log_prefix}: task lock released")
        except DBAgentException as e:
            logger.exception(f"{log_prefix}: failed to release task lock, error: {str(e)}")
            exit_code = 7

    try:
        dbagent_client.set_run_finished(run_id, exit_code=child_process.returncode)
        logger.info(f"{log_prefix}: set run to finished")
    except DBAgentException as e:
        logger.exception(f"{log_prefix}: failed to set run to finished, error: {str(e)}")
        if exit_code == 0:
            exit_code = 8
        else:
            exit_code = 20

    logger.info(f"{log_prefix}: exit")
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
