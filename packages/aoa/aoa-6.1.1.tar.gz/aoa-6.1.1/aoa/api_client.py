from __future__ import absolute_import

from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

import json
import os
import yaml
import logging
import requests
from typing import List, Dict


class AoaClient(object):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.project_id = kwargs.get("project_id")
        self.aoa_url = None

        self.auth_mode = "oauth"
        self.__auth_user = None
        self.__auth_pass = None
        self.__credentials = None

        self.__auth_client_id = None
        self.__auth_client_secret = None
        self.__auth_client_token_url = None
        self.__auth_client_refresh_token = None

        self.session = requests.Session()
        self.__parse_aoa_config(**kwargs)

    def __parse_yaml(self, yaml_path: str):
        with open(yaml_path, "r") as handle:
            conf = yaml.safe_load(handle)
        self.__parse_kwargs(**conf)

    def __parse_kwargs(self, **kwargs):
        self.aoa_url = kwargs.get("aoa_url", self.aoa_url)

        self.auth_mode = kwargs.get("auth_mode", self.auth_mode)
        if self.auth_mode == "oauth":
            self.__auth_client_id = kwargs.get("auth_client_id", self.__auth_client_id)
            self.__auth_client_secret = kwargs.get("auth_client_secret", self.__auth_client_secret)
            self.__auth_client_token_url = kwargs.get("auth_client_token_url", self.__auth_client_token_url)
            self.__auth_client_refresh_token = kwargs.get("auth_client_refresh_token", self.__auth_client_refresh_token)

        elif self.auth_mode == "oauth-cc":
            self.__auth_client_id = kwargs.get("auth_client_id", self.__auth_client_id)
            self.__auth_client_secret = kwargs.get("auth_client_secret", self.__auth_client_secret)
            self.__auth_client_token_url = kwargs.get("auth_client_token_url", self.__auth_client_token_url)

        else:
            raise Exception(f"Auth mode: {self.auth_mode} not supported.")

        if "verify_connection" in kwargs:
            self.verify_aoa_connection = kwargs["verify_connection"]

    def __parse_env_variables(self):
        self.aoa_url = os.environ.get("AOA_URL", self.aoa_url)

        self.auth_mode = os.environ.get("AOA_API_AUTH_MODE", self.auth_mode)
        if self.auth_mode == "oauth":
            self.__auth_client_id = os.environ.get("AOA_API_AUTH_CLIENT_ID", self.__auth_client_id)
            self.__auth_client_secret = os.environ.get("AOA_API_AUTH_CLIENT_SECRET", self.__auth_client_secret)
            self.__auth_client_token_url = os.environ.get("AOA_API_AUTH_TOKEN_URL", self.__auth_client_token_url)
            self.__auth_client_refresh_token = os.environ.get("AOA_API_AUTH_REFRESH_TOKEN",
                                                              self.__auth_client_refresh_token)

        elif self.auth_mode == "oauth-cc":
            self.__auth_client_id = os.environ.get("AOA_API_AUTH_CLIENT_ID", self.__auth_client_id)
            self.__auth_client_secret = os.environ.get("AOA_API_AUTH_CLIENT_SECRET", self.__auth_client_secret)
            self.__auth_client_token_url = os.environ.get("AOA_API_AUTH_TOKEN_URL", self.__auth_client_token_url)

        else:
            raise Exception(f"Auth mode: {self.auth_mode} not supported.")

    def __parse_aoa_config(self, **kwargs):
        if "config_file" in kwargs:
            self.__parse_yaml(kwargs['config_file'])
        else:
            from pathlib import Path
            config_file = "{}/.aoa/config.yaml".format(Path.home())
            if os.path.isfile(config_file):
                self.__parse_yaml(config_file)

        self.__parse_env_variables()
        self.__parse_kwargs(**kwargs)

        if self.auth_mode == "oauth":
            self.__configure_oauth_refresh_token(
                self.__auth_client_id,
                self.__auth_client_secret,
                self.__auth_client_token_url,
                self.__auth_client_refresh_token)

        elif self.auth_mode == "oauth-cc":
            self.__configure_oauth_client_credentials_grant(
                self.__auth_client_id,
                self.__auth_client_secret,
                self.__auth_client_token_url)

    def __validate_url(self):
        if not self.aoa_url:
            raise ValueError("Run 'aoa configure' if you have not already (aoa url is not set)")

    def set_project_id(self, project_id: str):
        """
        set project id

        Parameters:
           project_id (str): project id(uuid)
        """
        self.project_id = project_id

    def get_current_project(self):
        """
        get project id

        Return:
           project_id (str): project id(uuid)
        """
        return self.project_id

    def select_header_accept(self, accepts: List[str]):
        """
        converts list of header into a string

        Return:
            (str): request header
        """
        if not accepts:
            return

        accepts = [x.lower() for x in accepts]
        return ', '.join(accepts)

    def get_request(self, path, header_params: Dict[str, str], query_params: Dict[str, str]):
        """
        wrapper for get request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters

        Returns:
            dict for resources, str for errors, None for 404
        Raise:
            raises HTTPError in case of error status code other than 404
        """

        self.__validate_url()

        resp = self.session.get(
            url=self.__strip_url(self.aoa_url) + path,
            headers=header_params,
            params=query_params
        )

        if resp.status_code == 404:
            return None

        return self.__validate_and_extract_body(resp)

    def post_request(self, path, header_params: Dict[str, str], query_params: Dict[str, str], body: Dict[str, str]):
        """
        wrapper for post request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        self.__validate_url()

        resp = self.session.post(
            url=self.__strip_url(self.aoa_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body)
        )

        return self.__validate_and_extract_body(resp)

    def put_request(self, path, header_params: Dict[str, str], query_params: Dict[str, str], body: Dict[str, str]):
        """
        wrapper for put request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        self.__validate_url()

        resp = self.session.put(
            url=self.__strip_url(self.aoa_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body)
        )

        return self.__validate_and_extract_body(resp)

    def delete_request(self, path, header_params: Dict[str, str], query_params: Dict[str, str], body: Dict[str, str]):
        """
        wrapper for delete request
        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body
        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        self.__validate_url()

        resp = self.session.delete(
            url=self.__strip_url(self.aoa_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body)
        )

        return self.__validate_and_extract_body(resp)

    def __validate_and_extract_body(self, resp):
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if resp.text:
                raise requests.exceptions.HTTPError(f"Error Message: {resp.text}")
            else:
                raise err

        try:
            return resp.json()
        except ValueError:
            return resp.text

    def __strip_url(self, url):
        return url.rstrip('/')

    def __configure_oauth_refresh_token(self, client_id, client_secret, token_url, refresh_token):
        self.logger.debug("Configuring oauth with refresh token")

        if client_id is None or client_secret is None or token_url is None or refresh_token is None:
            raise Exception("Missing CLI configuration.\n" +
                            "Please (re)copy the CLI configuration from " +
                            "ModelOps UI -> Session Details -> CLI Config\n")

        self.session = OAuth2Session(client_id=client_id)
        self.session.refresh_token(token_url=token_url, refresh_token=refresh_token,
                                       auth=HTTPBasicAuth(client_id, client_secret))

    def __configure_oauth_client_credentials_grant(self, client_id, client_secret, token_url):
        self.logger.debug("Configuring oauth with client credentials grant")

        if client_id is None or client_secret is None or token_url is None:
            raise Exception("AOA_API_AUTH_CLIENT_ID, AOA_API_AUTH_CLIENT_SECRET, "
                            "AOA_API_AUTH_TOKEN_URL must be defined "
                            "with AOA_API_AUTH_MODE of 'oauth-cc (client-credentials)'")

        from requests_oauthlib import OAuth2Session
        from requests.auth import HTTPBasicAuth
        from oauthlib.oauth2 import BackendApplicationClient

        self.session = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
        self.session.fetch_token(token_url=token_url,
                                 auth=HTTPBasicAuth(client_id, client_secret))
