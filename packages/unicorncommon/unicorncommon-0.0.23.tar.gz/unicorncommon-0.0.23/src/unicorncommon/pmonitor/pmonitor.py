#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import argparse

from pyappkit import run_daemon, DaemonRunStatus


def main(args_alt=None):
    if args_alt is None:
        parser = argparse.ArgumentParser(description='Node Process Manager for Unicorn Cluster Manager')
        parser.add_argument("--node-id",  type=str, required=True, help="node id")
        parser.add_argument("--data-dir", type=str, required=True, help="data directory", default=".")
        parser.add_argument("--pid-filename", type=str, required=False, help="pid filename", default="pmonitor.pid")
        parser.add_argument("--stdout", type=str, required=False, help="filename that stores stdout", default="pmonitor-out.txt")
        parser.add_argument("--stderr", type=str, required=False, help="filename that stores stderr", default="pmonitor-err.txt")
        parser.add_argument("--cfg-dir", type=str, required=False, help="config directory", default=".")
        parser.add_argument("--log-dir", type=str, required=False, help="logging directory", default=".")
        args = parser.parse_args()

        node_id         = args.node_id
        data_dir        = args.data_dir
        pid_filename    = args.pid_filename
        stdout          = args.stdout
        stderr          = args.stderr
        cfg_dir         = args.cfg_dir
        log_dir         = args.log_dir
    else:
        node_id         = args_alt['node_id']
        data_dir        = args_alt['data_dir']
        pid_filename    = args_alt['pid_filename']
        stdout          = args_alt['stdout']
        stderr          = args_alt['stderr']
        cfg_dir         = args_alt['cfg_dir']
        log_dir         = args_alt['log_dir']


    LOG_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "fileHandler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "filename": os.path.join(log_dir, "pmonitor.log"),
                "interval": 1,
                "when": "midnight"
            },
        },
        "loggers": {
            "": {
                "handlers": ["fileHandler"],
                "level":    "DEBUG",
                "propagate": True
            },
            "oci": {
                "handlers": ["fileHandler"],
                "level":    "WARNING",
                "propagate": False
            }
        },
        "root": {
            "handlers": ["fileHandler"],
            "level": "DEBUG",
        },
    }


    status, extra = run_daemon(
        pid_filename=pid_filename,
        stdout_filename=stdout,
        stderr_filename=stderr,
        daemon_entry="unicorncommon.pmonitor.pmonitor_impl:main",
        logging_config=LOG_CONFIG,
        daemon_args={
            "node_id": node_id,
            "cfg_dir": cfg_dir,
            "data_dir": data_dir,
        }
    )
    if status == DaemonRunStatus.LAUNCHED:
        print(f"pmonitor launched, pid = {extra}")
    else:
        print(f"Unable to launch pmonitor status={status}, extra={extra}")

if __name__ == '__main__':
    main()
