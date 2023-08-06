import uuid
from copy import deepcopy
import time
from datetime import datetime

from oci_core import get_os_client, list_objects_start_with, os_has_object, os_download_json, os_delete_object, os_upload_json

class BucketServer:
    def __init__(self, server_endpoint, server_config):
        self.server_config = deepcopy(server_config)
        self.server_endpoint = deepcopy(server_endpoint)
        # server_config:
        #     oci_config: dict or None, oci config
        # server_endpoint:
        #     bucket_name: name of the bucket
        #     namespace  : namespace
        #     server_name: the name of the server

    def get_client(self):
        return "unicorncommon.channels.bucket.BucketClient", deepcopy(self.server_endpoint)

    def start_server(self, server, quit_requested):
        oci_config      = self.server_config['oci_config']
        os_client       = get_os_client(None, oci_config)
        bucket_name     = self.server_endpoint['bucket_name']
        namespace       = self.server_endpoint['namespace']
        server_name     = self.server_endpoint['server_name']

        request_prefix  = f"{server_name}/request-"
        response_prefix = f"{server_name}/response-"
        idle_interval   = self.server_config.get('idle_interval', 1)


        while not quit_requested():
            count = 0
            for object_summary in list_objects_start_with(os_client, namespace, bucket_name, request_prefix, fields="name"):
                request_object_name = object_summary.name
                transaction_id = request_object_name[len(request_prefix):]
                response_object_name = f"{response_prefix}{transaction_id}"
                if os_has_object(os_client, namespace, bucket_name, response_object_name):
                    # skip this request since it has been answered
                    continue
                request = os_download_json(os_client, namespace, bucket_name, request_object_name)
                os_delete_object(os_client, namespace, bucket_name, request_object_name)
                count += 1
                response = server.handle_request(request)
                os_upload_json(os_client, response, namespace, bucket_name, response_object_name)
                server.on_idle()

            if count == 0:
                server.on_idle()
                if idle_interval is not None:
                    time.sleep(idle_interval)
                continue


class BucketClient:
    def __init__(self, server_endpoint, client_config):
        self.client_config = deepcopy(client_config)
        oci_config      = self.client_config['oci_config']
        self.os_client  = get_os_client(None, oci_config)
        self.server_endpoint = deepcopy(server_endpoint)

    def send(self, request):
        bucket_name     = self.server_endpoint['bucket_name']
        namespace       = self.server_endpoint['namespace']
        server_name     = self.server_endpoint['server_name']

        request_prefix  = f"{server_name}/request-"
        response_prefix = f"{server_name}/response-"
        timeout         = self.client_config.get('timeout', 300)

        start_time = datetime.utcnow()
        # get a unique transaction id
        while True:
            transaction_id          = str(uuid.uuid4())
            request_object_name     = f"{request_prefix}{transaction_id}"
            response_object_name    = f"{response_prefix}{transaction_id}"
            if not os_has_object(self.os_client, namespace, bucket_name, request_object_name) \
                    and not os_has_object(self.os_client, namespace, bucket_name, response_object_name):
                break
            if timeout is not None and (datetime.utcnow() - start_time).total_seconds() > timeout:
                raise TimeoutError()
            time.sleep(1)

        os_upload_json(self.os_client, request, namespace, bucket_name, request_object_name)
        # wait for server to acknowledge the request by deleting it
        while True:
            if not os_has_object(self.os_client, namespace, bucket_name, request_object_name):
                break
            if timeout is not None and (datetime.utcnow() - start_time).total_seconds() > timeout:
                raise TimeoutError()
            time.sleep(1)

        # wait for server to generate response object
        while True:
            if os_has_object(self.os_client, namespace, bucket_name, response_object_name):
                break
            if timeout is not None and (datetime.utcnow() - start_time).total_seconds() > timeout:
                raise TimeoutError()
            time.sleep(1)

        response = os_download_json(self.os_client, namespace, bucket_name, response_object_name)
        os_delete_object(self.os_client, namespace, bucket_name, response_object_name)
        return response
