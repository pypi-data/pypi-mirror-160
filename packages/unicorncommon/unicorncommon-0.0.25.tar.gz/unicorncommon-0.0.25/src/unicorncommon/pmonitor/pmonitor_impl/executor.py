import logging
logger = logging.getLogger(__name__)

import os
import subprocess
import signal
from datetime import datetime, timedelta
from shlex import split, quote

from jsonschema.exceptions import ValidationError

from unicorncommon.server_status import SERVER_STATUS
from .api_input import validate_model
from unicorncommon.dbagent_client import DBAgentException


class Executor:
    def __init__(self, *, dbagent_client, base_data_dir, node_id, cfg_dir):
        self.base_data_dir  = base_data_dir
        self.node_id        = node_id
        self.dbagent_client = dbagent_client
        self.cfg_dir        = cfg_dir

        self.runs_dir = os.path.join(self.base_data_dir, "runs")

    def on_idle(self):
        pass

    def handle_request_run_application(self, request):
        log_prefix = "handle_request_run_application"
        # request example
        # {
        #     "action": "run-application",
        #     "id": 123,
        #     "args": ["foo", "bar"],
        #     "input": "ls -al\nclear\n"
        # }
        try:
            validate_model('run_application_input', request)
        except ValidationError as e:
            logger.exception(f"{log_prefix}: validation error, schema: run_application_input, error: {str(e)}")
            return {
                "status": SERVER_STATUS.INVALID_REQUEST_SCHEMA.value,
                "message": str(e)
            }

        application_id = request["id"]
        args = request.get('args', [])
        input = request.get('input')
        run = None
        launched = False
        try:
            try:
                run = self.dbagent_client.create_run(
                    application_id = application_id,
                    node_id = self.node_id,
                    args = args,
                    input = input,
                )
            except DBAgentException as e:
                logger.exception(f"{log_prefix}: failed to create run, error: {str(e)}")
                return {"status": e.resp["status"]}
            log_prefix = f"{log_prefix}(Run({run['id']})"
            logger.info(f"{log_prefix}: run created!")

            run_dir = os.path.join(self.runs_dir, str(run['id']))
            try:
                os.makedirs(run_dir)
                logger.info(f"{log_prefix}: run home directory {run_dir} created!")
            except OSError as e:
                logger.exception(f"{log_prefix}: failed to create run home directory {run_dir}, error: {str(e)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_ERROR.value,
                }

            try:
                cmd = f"pwrapper -r {run['id']} --data-dir {self.base_data_dir} --cfg-dir {self.cfg_dir}"
                logger.info(f"{log_prefix}: launch wrapper via command: \"{cmd}\"")
                r = subprocess.Popen(cmd, shell = True)
                launched = True
                logger.info(f"{log_prefix}: wrapper launched, pid={r.pid}")
            except OSError as e:
                logger.exception(f"{log_prefix}: failed to launch wrapper, error: {str(e)}")
                return {
                    "status": SERVER_STATUS.LAUNCH_PROCESS_FAILED.value,
                    "message": str(e)
                }

            # successfully launched
            return {
                "status": SERVER_STATUS.OK.value,
                "run_id": run['id']
            }
        finally:
            if not launched:
                log_prefix = f"{log_prefix}(cleanup)"
                if run is not None:
                    try:
                        self.dbagent_client.delete_run(run['id'])
                        logger.warn(f"{log_prefix}: run({run['id']}) is deleted!")
                    except DBAgentException as e:
                        logger.exception(f"{log_prefix}: failed to delete run({run['id']}), error: {str(e)}")


    # execute an application using task
    def handle_request_run_task(self, request):
        log_prefix = "handle_request_run_task"
        # request example
        # {
        #     "action": "run-task",
        #     "id": 123,
        # }
        try:
            validate_model('run_task_input', request)
        except ValidationError as e:
            logger.exception(f"{log_prefix}: validation error, schema: run_task_input, error: {str(e)}")
            return {
                "status": SERVER_STATUS.INVALID_REQUEST_SCHEMA.value,
                "message": str(e)
            }

        task_id = request["id"]
        try:
            task = self.dbagent_client.get_task(task_id)
        except DBAgentException as e:
            logger.exception(f"{log_prefix}: failed to get task({task_id}), error: {str(e)}")
            return {"status": e.resp['status']}

        application = task["application"]
        run = None
        active_run_set = False
        launched = False
        try:
            try:
                run = self.dbagent_client.create_run(
                    application_id = application['id'],
                    node_id = self.node_id,
                    args = task['args'],
                    input= task['input'],
                    task_id = task['id'],
                )
            except DBAgentException as e:
                logger.exception(f"{log_prefix}: failed to create run, error: {str(e)}")
                return {"status": e.resp['status']}
            log_prefix = f"{log_prefix}(Run({run['id']})"
            logger.info(f"{log_prefix}: run created!")

            if task['is_singleton']:
                try:
                    self.dbagent_client.set_active_run(task['id'], run_id = run['id'])
                    active_run_set = True
                except DBAgentException as e:
                    logger.exception(f"{log_prefix}: failed to acquire task lock, error: {str(e)}")
                    return {"status": e.resp['status']}
                logger.info(f"{log_prefix}: task({task['id']}) lock acquired")

            run_dir = os.path.join(self.runs_dir, str(run['id']))
            try:
                os.makedirs(run_dir)
                logger.info(f"{log_prefix}: run home directory {run_dir} created!")
            except OSError as e:
                logger.exception(f"{log_prefix}: failed to create run home directory {run_dir}, error: {str(e)}")
                return {
                    "status": SERVER_STATUS.INTERNAL_ERROR.value,
                }

            try:
                if task['is_singleton']:
                    cmd = f"pwrapper -r {run['id']} -t {task['id']} --is-singleton --data-dir {self.base_data_dir} --cfg-dir {self.cfg_dir}"
                else:
                    cmd = f"pwrapper -r {run['id']} -t {task['id']} --data-dir {self.base_data_dir} --cfg-dir {self.cfg_dir}"
                logger.info(f"{log_prefix}: launch wrapper via command: \"{cmd}\"")
                r = subprocess.Popen(cmd, shell = True)
                launched = True
                logger.info(f"{log_prefix}: wrapper launched, pid={r.pid}")
            except OSError as e:
                logger.exception(f"{log_prefix}: failed to launch wrapper, error: {str(e)}")
                return {
                    "status": SERVER_STATUS.LAUNCH_PROCESS_FAILED.value,
                    "message": str(e)
                }

            # successfully launched
            return {
                "status": SERVER_STATUS.OK.value,
                "run_id": run['id']
            }
        finally:
            if not launched:
                log_prefix = f"{log_prefix}(cleanup)"
                if active_run_set:
                    try:
                        self.dbagent_client.unset_active_run(task['id'])
                        logger.warn(f"{log_prefix}: task lock released")
                    except DBAgentException as e:
                        logger.exception(f"{log_prefix}: failed to relase task lock, error: {str(e)}")
                if run is not None:
                    try:
                        self.dbagent_client.delete_run(run['id'])
                        logger.warn(f"{log_prefix}: run({run['id']}) is deleted!")
                    except DBAgentException as e:
                        logger.exception(f"{log_prefix}: failed to delete run({run['id']}), error: {str(e)}")


    def handle_request_stop_run(self, request):
        log_prefix = "handle_request_stop_run"
        # request example
        # {
        #     "action": "stop-run",
        #     "id": 123,
        # }
        try:
            validate_model('stop_run_input', request)
        except ValidationError as e:
            logger.exception(f"{log_prefix}: validation error, schema: stop_run_input, error: {str(e)}")
            return {
                "status": SERVER_STATUS.INVALID_REQUEST_SCHEMA.value,
                "message": str(e)
            }

        id = request["id"]
        try:
            run = self.dbagent_client.get_run(id)
        except DBAgentException as e:
            logger.exception(f"{log_prefix}: failed to get run, run_id={id}, error: {str(e)}")
            return {"status": e.resp['status']}
        log_prefix = f"{log_prefix}(Run({run['id']})"

        if run["is_finished"]:
            logger.warn(f"{log_prefix}: run is already stopped")
            return {
                "status": SERVER_STATUS.RUN_ALREADY_STOPPED.value,
            }

        if run["pid"] is None:
            logger.error(f"{log_prefix}: missing pid")
            return {
                "status": SERVER_STATUS.INTERNAL_ERROR.value,
            }

        try:
            logger.info(f"{log_prefix}: send SIGTERM to pid({run['pid']})")
            os.kill(run["pid"], signal.SIGTERM)
        except OSError as e:
            logger.exception(f"{log_prefix}: failed to send SIGTERM to process(pid={run['pid']}), error: {str(e)}")
            return {
                "status": SERVER_STATUS.STOP_PROCESS_FAILED.value,
                "message": str(e)
            }

        return {
            "status": SERVER_STATUS.OK.value,
        }


    def handle_request(self, request):
        logger.info(f"request: {request}")
        action = request.get('action')
        if action == "ping":
            response = {
                "status": SERVER_STATUS.OK.value,
                "payload": "pong"
            }
        elif action == "run-application":
            response = self.handle_request_run_application(request)
        elif action == "run-task":
            response = self.handle_request_run_task(request)
        elif action == "stop-run":
            response = self.handle_request_stop_run(request)
        else:
            response = {"status": SERVER_STATUS.INVALID_ACTION.value}
        return response
