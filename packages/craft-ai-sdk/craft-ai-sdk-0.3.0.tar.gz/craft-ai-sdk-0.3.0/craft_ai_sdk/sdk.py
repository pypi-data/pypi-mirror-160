import base64
import csv
import os
import json
import sys
import requests

from craft_ai_sdk.exceptions import SdkException

from .utils import (
    _datetime_to_timestamp_in_ms,
    handle_data_store_response,
    handle_http_request,
    log_action,
    log_func_result,
)


class CraftAiSdk:
    """Main class to instantiate

    Attributes:
        base_environment_url (str): Base URL to CraftAI Environment.
        base_api_url (str): Base URL to CraftAI API.
        verbose_log (bool): If True, information during method execution will be
            printed.
    """

    def __init__(self, access_token=None, environment_url=None, verbose_log=None):
        """Inits CraftAiSdk.

        Args:
            access_token (:obj:`str`, optional): CraftAI access token.
                Defaults to ``CRAFT_AI_ACCESS_TOKEN`` environment variable.
            environment_url (:obj:`str`, optional): URL to CraftAI environment.
                Defaults to ``CRAFT_AI_ENVIRONMENT_URL`` environment variable.
            verbose_log (:obj:`bool`, optional): If True, information during method
                execution will be printed. It is set to True, if the environment
                variable ``SDK_VERBOSE_LOG`` is set to ``true``; False if it is
                set to ``false``. Defaults to True in interactive mode; False otherwise.

        Raises:
            ValueError: if the ``environment_url`` is not defined
                or when the corresponding environment variable is not set.
        """
        self._session = requests.Session()

        # Set authorization token
        if access_token is None:
            access_token = os.environ.get("CRAFT_AI_ACCESS_TOKEN")
        if not access_token:
            raise ValueError(
                'Parameter "access_token" should be set, since '
                '"CRAFT_AI_ACCESS_TOKEN" environment variable is not defined.'
            )
        self._session.headers["Authorization"] = f"Bearer {access_token}"

        # Set base environment url
        if environment_url is None:
            environment_url = os.environ.get("CRAFT_AI_ENVIRONMENT_URL")
        if not environment_url:
            raise ValueError(
                'Parameter "environment_url" should be set, since '
                '"CRAFT_AI_ENVIRONMENT_URL" environment variable is not defined.'
            )
        self.base_environment_url = environment_url
        self.base_api_url = f"{environment_url}/api/v1"

        if verbose_log is None:
            env_verbose_log = os.environ.get("SDK_VERBOSE_LOG", "").lower()
            # Detect interactive mode: https://stackoverflow.com/a/64523765
            verbose_log = (
                True
                if env_verbose_log == "true"
                else False
                if env_verbose_log == "false"
                else hasattr(sys, "ps1")
            )
        self.verbose_log = verbose_log

    # _____ REQUESTS METHODS _____

    @handle_http_request
    def _get(self, url, params=None, **kwargs):
        return self._session.get(url, params=params, **kwargs)

    @handle_http_request
    def _post(self, url, data=None, params=None, files=None, **kwargs):
        return self._session.post(url, data=data, params=params, files=files, **kwargs)

    @handle_http_request
    def _delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    # _____ STEPS _____

    @log_func_result("Steps creation")
    def create_steps(self, repo, private_key, branch_name=None, step_names=None):
        """Create pipeline steps from a source code located on a remote repository.

        Args:
            repo (str): Remote repository url.
            private_key (str): Private SSH key related to the repository.
            branch_name (:obj:`str`, optional): Branch name. Defaults to None.
            step_names (:obj:`list`, optional): List of the step names (as defined
                in the ``config.yaml`` configuration file) to create. Defaults to None.

        Returns:
            :obj:`list` of :obj:`dict[str, str]`: List of steps represented as
            :obj:`dict` (with either keys ``"id"`` and ``"name"`` if the creation
            succeeded or keys ``"name"`` and ``"error"`` if the creation failed).
        """
        url = f"{self.base_api_url}/steps"

        data = {
            "repo": repo,
            "private_key": private_key,
        }
        if branch_name is not None:
            data["branch_name"] = branch_name
        if step_names is not None:
            data["step_names"] = step_names

        log_action(
            self,
            "Please wait while step(s) is/are being created. This may take a while...",
        )
        return self._post(url, json=data)

    def get_step(self, step_name):
        """Get a single step if it exists.

        Args:
            step_name (str): The name of the step to get.

        Returns:
            :obj:`dict`: The step informations (with keys ``"id"``, ``"name"``)
            or None if the step does not exists.
        """
        url = f"{self.base_api_url}/steps/{step_name}"
        try:
            return self._get(url)
        except SdkException as error:
            if error.status_code == 404:
                return None
            raise error

    def list_steps(self):
        """Get the list of all steps.

        Returns:
            :obj:`list` of :obj:`dict`: List of steps represented as :obj:`dict`
            (with keys ``"id"``, ``"name"``).
        """
        url = f"{self.base_api_url}/steps"

        return self._get(url)

    @log_func_result("Step deletion")
    def delete_one_step(self, step_name):
        """Delete one step.

        Args:
            step_name (str): Name of the step to delete
                as defined in the ``config.yaml`` configuration file.

        Returns:
            :obj:`dict[str, str]`: Deleted step represented as :obj:`dict`
            (with keys ``"id"`` and ``"name"``).
        """
        url = os.path.join(f"{self.base_api_url}/steps", step_name)
        return self._delete(url)

    # _____ PIPELINES _____

    @log_func_result("Pipeline creation")
    def create_pipeline(self, pipeline_name, step_name):
        """Create a pipeline containing a single step.

        Args:
            pipeline_name (str): Name of the pipeline to be created.
            step_name (str): Name of the step to be included in the pipeline.

        Returns:
            :obj:`dict[str, str]`: Created pipeline represented as :obj:`dict`
            (with key ``"id"``).
        """
        url = f"{self.base_api_url}/pipelines"
        body = {
            "pipeline_name": pipeline_name,
            "step_names": [step_name],
        }

        resp = self._post(url, json=body)
        return resp

    def get_pipeline(self, pipeline_name):
        """Get a single pipeline if it exists.

        Args:
            pipeline_name (str): Name of the pipeline to get.

        Returns:
            :obj:`dict`: The pipeline informations (with keys ``"id"``,
            ``"pipeline_name"``) or None if the pipeline does not
            exists.
        """
        url = f"{self.base_api_url}/pipelines/{pipeline_name}"
        try:
            return self._get(url)
        except SdkException as error:
            if error.status_code == 404:
                return None
            raise error

    @log_func_result("Pipeline deletion")
    def delete_pipeline(self, pipeline_name, force_endpoints_deletion=False):
        """Delete a pipeline identified by its name and id.

        Args:
            pipeline_name (str): Name of the pipeline.
            force_endpoints_deletion (:obj:`bool`, optional): if True the associated
                endpoints will be deleted too. Defaults to False.

        Returns:
            :obj:`dict`: The deleted pipeline and assiocated deleted endpoints.
            The returned ``dict`` contains two keys:

                * ``"pipeline"`` (:obj:`dict`): Deleted pipeline represented as
                  :obj:`dict` (with keys ``"id"`` and ``"name"``).
                * ``"endpoints"`` (:obj:`list`): List of deleted endpoints represented
                  as :obj:`dict` (with keys ``"id"``, ``"name"``, ``"body_params"``
                  and ``allow_unknown_params``).
        """
        url = f"{self.base_api_url}/pipelines"
        params = {
            "pipeline_name": pipeline_name,
            "force_endpoints_deletion": force_endpoints_deletion,
        }
        return self._delete(url, params=params)

    def get_pipeline_status(self, pipeline_name):
        """Get the status of all executions of a pipeline identified by its name.

        Args:
            pipeline_name (str): Name of the pipeline.

        Returns:
            :obj:`dict`: Information on the pipeline and its executions. The returned
            ``dict`` contains the following keys:

                * ``"id"`` (:obj:`str`): Pipeline id.
                * ``"name"`` (:obj:`str`): Pipeline name.
                * ``"created_at"`` (:obj:`str`): Pipeline date of creation.
                * ``"executions"`` (:obj:`list`): List of pipeline executions
                  represented as :obj:`dict` (with keys ``"id"``, ``"name"``,
                  ``"status"``, ``"created_at"``, ``"steps"``). The value associated
                  with the key ``"steps"`` is a :obj:`list` of the steps represented
                  as :obj:`dict` (with keys ``"name"``, ``"status"``).
        """
        url = f"{self.base_api_url}/pipelines/status"
        params = {
            "pipeline_name": pipeline_name,
        }
        return self._get(url, params=params)

    # _____ PIPELINE EXECUTIONS _____

    @log_func_result("Pipeline execution")
    def execute_pipeline(self, pipeline_name):
        """Execute a pipeline.

        Args:
            pipeline_name (str): Name of an existing pipeline.

        Returns:
            :obj:`dict[str, str]`: Created pipeline execution represented as :obj:`dict`
            (with key ``"execution_name"``).
        """
        url = f"{self.base_api_url}/pipelines"
        params = {
            "pipeline_name": pipeline_name,
        }

        resp = self._get(url, params=params)
        return resp

    def get_pipeline_execution_status(self, execution_name):
        """Get the status of one pipeline execution identified by its name.

        Args:
            execution_name (str): Name of the pipeline execution.

        Returns:
            :obj:`dict`: Information on the pipeline execution with name
            ``execution_name`` represented as dict (with keys ``"id"``, ``"name"``,
            ``"status"``, ``"created_at``, ``"steps"``, ``"pipeline"``).
            In particular the keys:

                * ``"steps"`` is a :obj:`list` of the execution steps represented
                  as :obj:`dict` (with keys ``"name"``, ``"status"``).
                * ``"pipeline"`` is the executed pipeline represented
                  as :obj:`dict` (with keys ``"id"``, ``"name"``).
        """
        url = f"{self.base_api_url}/pipelines/status/{execution_name}"

        return self._get(url)

    def get_pipeline_execution_logs(
        self, execution_name, from_datetime=None, to_datetime=None, limit=None
    ):
        """Get the logs of an executed pipeline identified by its name.

        Args:
            execution_name (str): Name of the pipeline execution.
            from_datetime (:obj:`datetime.time`, optional): Datetime from which the logs
                are collected.
            to_datetime (:obj:`datetime.time`, optional): Datetime until which the logs
                are collected.
            limit (:obj:`int`, optional): Maximum number of logs that are collected.

        Returns:
            :obj:`list`: List of collected logs.
        """
        url = f"{self.base_api_url}/pipelines/{execution_name}/logs"

        data = {}
        if from_datetime is not None:
            data["from"] = _datetime_to_timestamp_in_ms(from_datetime)
        if to_datetime is not None:
            data["to"] = _datetime_to_timestamp_in_ms(to_datetime)
        if limit is not None:
            data["limit"] = limit

        log_action(
            self,
            "Please wait while logs are being downloaded. This may take a while...",
        )
        response = self._post(url, json=data)
        if len(response) == 0:
            return []

        lines = response[0].splitlines()
        return list(csv.reader(lines))

    # _____ ENDPOINTS _____

    @log_func_result("Endpoint creation")
    def create_endpoint(
        self,
        pipeline_name,
        endpoint_name,
        endpoint_params=None,
        allow_unknown_params=None,
    ):
        """Create a custom endpoint associated to a given pipeline.

        Args:
            pipeline_name (str): Name of the pipeline.
            endpoint_name (str): Name of the endpoint.
            endpoint_params (:obj:`dict[str, dict]`, optional): structure of the
                endpoint parameters. Each item defines a parameter which name is given
                by the key and which constraints (type and requirement) are given by
                the value. An item has the form::

                    [str: parameter name] : {
                        "required": [bool],
                        "type": [str in ["string", "number", "object", "array"]],
                    }

                Defaults to None.
            allow_unknown_params (:obj:`bool`, optional): if True the custom endpoint
                allows other parameters not specified in ``endpoint_params``.
                Defaults to None.

        Returns:
            :obj:`dict[str, str]`: Created endpoint represented as :obj:`dict`
            (with key ``"id"`` and ``"name"``).
        """
        url = f"{self.base_api_url}/endpoints"

        endpoint_params = {} if endpoint_params is None else endpoint_params
        data = {
            "pipeline_name": pipeline_name,
            "name": endpoint_name,
            "allow_unknown_params": allow_unknown_params,
            "body_params": endpoint_params,
        }
        # filter optional parameters
        data = {k: v for k, v in data.items() if v is not None}

        return self._post(url, json=data)

    @log_func_result("Endpoint deletion")
    def delete_endpoint(self, endpoint_name):
        """Delete an endpoint identified by its name.

        Args:
            endpoint_name (str): Name of the endpoint.

        Returns:
            :obj:`dict`: Deleted endpoint represented as dict (with keys ``"id"``,
            ``"name"``, ``"body_params"``, ``"allow_unknown_params"``).
        """
        url = os.path.join(f"{self.base_api_url}/endpoints", endpoint_name)
        return self._delete(url)

    def list_endpoints(self):
        """Get the list of all endpoints.

        Returns:
            :obj:`list` of :obj:`dict`: List of endpoints represented as :obj:`dict`
            (with keys ``"id"``, ``"name"``, ``"body_params"``,
            ``"allow_unknown_params"`` and ``"pipeline"``).
        """
        url = f"{self.base_api_url}/endpoints"
        return self._get(url)

    def get_endpoint(self, endpoint_name):
        """Get information of an endpoint.

        Args:
            endpoint_name (str): Name of the endpoint.

        Returns:
            :obj:`dict`: Endpoint information represented as :obj:`dict` (with keys
            ``"id"``, ``"name"``, ``"body_params"``, ``"allow_unknown_params"`` and
            ``"pipeline"``).
        """
        url = os.path.join(f"{self.base_api_url}/endpoints", endpoint_name)
        return self._get(url)

    @log_func_result("Endpoint trigger")
    def trigger_endpoint(self, endpoint_name, params=None):
        """Trigger an endpoint.

        Args:
            endpoint_name (str): Name of the endpoint.
            params (:obj:`dict`, optional): Parameters to be provided to the endpoint.
                Defaults to None.

        Returns:
            :obj:`dict[str, str]`: Created pipeline execution represented as :obj:`dict`
            (with key ``"execution_name"``).
        """
        url = os.path.join(f"{self.base_environment_url}/endpoints", endpoint_name)
        return self._post(url, json=params)

    # _____ DATA STORE _____

    def data_store_list_objects(self):
        """Get the list of the objects stored in the data store.

        Returns:
            :obj:`list` of :obj:`dict`: List of objects in the data store represented
            as :obj:`dict` (with keys ``"path"``, ``"last_modified"``, and ``"size"``).
        """
        url = f"{self.base_api_url}/data-store/list"
        response = self._get(url)

        return response

    def _get_upload_presigned_url(self):
        url = f"{self.base_api_url}/data-store/upload"
        resp = self._get(url)
        presigned_url, data = resp["signed_url"], resp["fields"]

        # Extract prefix condition from the presigned url
        policy = data["policy"]
        policy_decode = json.loads(base64.b64decode(policy))
        prefix_condition = policy_decode["conditions"][0]
        prefix = prefix_condition[-1]
        return presigned_url, data, prefix

    @log_func_result("Object upload")
    def data_store_upload_object(self, filepath_or_buffer, object_path_in_datastore):
        """Upload a file as an object into the data store.

        Args:
            filepath_or_buffer (:obj:`str`, or file-like object): String, path to the
                file to be uploaded ;
                or file-like object implenting a ``read()`` method (e.g. via buildin
                ``open`` function). The file object must be opened in binary mode,
                not text mode.
            object_path_in_datastore (str): Destination of the uploaded file.
        """
        if isinstance(filepath_or_buffer, str):
            # this is a filepath: call the method again with a buffer
            with open(filepath_or_buffer, "rb") as file_buffer:
                return self.data_store_upload_object(
                    file_buffer, object_path_in_datastore
                )

        if not hasattr(filepath_or_buffer, "read"):  # not a readable buffer
            raise ValueError(
                "'filepath_or_buffer' must be either a string (filepath) or an object "
                "with a read() method (file-like object)."
            )

        file_buffer = filepath_or_buffer
        files = {"file": file_buffer}
        presigned_url, data, prefix = self._get_upload_presigned_url()
        data["key"] = os.path.join(prefix, object_path_in_datastore)

        resp = requests.post(url=presigned_url, data=data, files=files)
        handle_data_store_response(resp)

    def _get_download_presigned_url(self, object_path_in_datastore):
        url = f"{self.base_api_url}/data-store/download"
        data = {
            "path_to_object": object_path_in_datastore,
        }
        presigned_url = self._post(url, data=data)["signed_url"]
        return presigned_url

    @log_func_result("Object download")
    def data_store_download_object(self, object_path_in_datastore, filepath_or_buffer):
        """Download an object in the data store and save it into a file.

        Args:
            object_path_in_datastore (str): Location of the object to download from the
                data store.
            filepath_or_buffer (:obj:`str` or file-like object):
                String, filepath to save the file to ; or a file-like object
                implementing a ``write()`` method, (e.g. via builtin ``open`` function).

        Returns:
            str: content of the file
        """
        presigned_url = self._get_download_presigned_url(object_path_in_datastore)
        resp = requests.get(presigned_url)
        object_content = handle_data_store_response(resp)

        if isinstance(filepath_or_buffer, str):  # filepath
            with open(filepath_or_buffer, "w") as f:
                f.write(object_content)
        elif hasattr(filepath_or_buffer, "write"):  # writable buffer
            filepath_or_buffer.write(object_content)
        else:
            raise ValueError(
                "'filepath_or_buffer' must be either a string (filepath) or an object "
                "with a write() method (file-like object)."
            )

    @log_func_result("Object deletion")
    def data_store_delete_object(self, object_path_in_datastore):
        """Delete an object on the datastore.

        Args:
            object_path_in_datastore (str): Location of the object to be deleted in the
                data store.

        Returns:
            :obj:`dict`: Deleted object represented as dict (with key ``"path"``).
        """
        url = f"{self.base_api_url}/data-store/delete"
        data = {
            "path_to_object": object_path_in_datastore,
        }
        return self._delete(url, data=data)
