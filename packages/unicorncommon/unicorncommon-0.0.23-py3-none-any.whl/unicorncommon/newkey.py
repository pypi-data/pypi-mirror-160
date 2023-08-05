#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import argparse

import zmq
import zmq.auth

def main():
    parser = argparse.ArgumentParser(description='Generate ZeroMQ Certificate')
    parser.add_argument("--node-id",  type=str, required=True, help="node id")
    parser.add_argument("--dir",  type=str, required=False, help="path to store certs")
    args = parser.parse_args()

    if args.dir is None:
        cert_path = "."
    else:
        cert_path = args.dir

    if not os.path.isdir(cert_path):
        print(f"{cert_path} is not a directory!")
        sys.exit(1)

    server_public_file, server_secret_file = zmq.auth.create_certificates(
        cert_path, args.node_id
    )
    print(f"{server_public_file} generated.")
    print(f"{server_secret_file} generated.")


if __name__ == '__main__':
    main()
