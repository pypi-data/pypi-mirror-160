#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

""" Application Configuration """
from collections.abc import MutableMapping
import os
import sys
import yaml
from app.logz import create_logger


class Application(MutableMapping):
    """
    Regscale CLI configuration class
    """

    def __init__(self):
        """constructor"""

        template = {
            "domain": "https://mycompany.regscale.com/",
            "token": "Bearer <my JWT here>",
            "userId": "<enter id here>",
            "wizAccessToken": "<createdProgrammatically>",
            "wizClientId": "<myclientidgoeshere>",
            "wizClientSecret": "<mysecretgoeshere>",
            "wizScope": "<filled out programmatically after authenticating to Wiz>",
            "wizUrl": "<my Wiz URL goes here>",
            "wizAuthUrl": "https://auth.wiz.io/oauth/token",
            "wizExcludes": "My things to exclude here",
            "adAuthUrl": "https://login.microsoftonline.com/",
            "adGraphUrl": "https://graph.microsoft.com/.default",
            "adAccessToken": "Bearer <my token>",
            "adClientId": "<myclientidgoeshere>",
            "adSecret": "<mysecretgoeshere>",
            "adTenantId": "<mytenantidgoeshere>",
            "jiraUrl": "<myJiraUrl>",
            "jiraUserName": "<jiraUserName>",
            "jiraApiToken": "<jiraAPIToken>",
            "snowUrl": "<mySnowUrl>",
            "snowUserName": "<snowUserName>",
            "snowPassword": "<snowPassword>",
        }
        self.template = template
        self.config = self._gen_config()
        self.logger = create_logger()

    def __getitem__(self, key):
        """Get an item."""
        return self.config.__getitem__(self, key)

    def __setitem__(self, key, value):
        """Set an item."""

        value = int(value)
        if not 1 <= value <= 10:
            raise ValueError(f"{value} not in range [1,10]")
        self.config.__setitem__(self, key, value)

    def __delitem__(self, key):
        """Delete an item."""

        self.config.__delitem__(self, key)

    def __iter__(self):
        """return iterator"""
        return self.config.__iter__(self)

    def __len__(self):
        """get the length of the config."""

        return self.config.__len__(self)

    def __contains__(self, x: str):
        """Check config if it contains string."""

        return self.config.__contains__(self, x)

    def _gen_config(self) -> {}:
        config = self._get_env()
        if config is None:
            try:
                config = self._get_conf()
            except Exception:
                self.logger.error("No configuration loaded!!! Exiting..")
                sys.exit()
        else:
            # Update config file with sys env
            try:
                with open(r"init.yaml", "w", encoding='utf-8') as file:
                    yaml.dump(config, file)
            except OSError:
                self.logger.error("Could not dump config to init.yaml")
        # Return config
        return config

    def _get_env(self) -> {}:
        """return dict of regscale keys from system"""
        all_keys = self.template.keys()
        sys_keys = [key for key in os.environ if key in all_keys]
        #  Update Template
        dat = None
        try:
            dat = self.template
            for k in sys_keys:
                dat[k] = os.environ[k]
        except Exception as ex:
            self.logger.error("Key Error!!: %s", ex)
        return dat

    def _get_conf(self) -> {}:
        """Get configuration from init.yaml if exists"""
        config = None
        fname = "init.yaml"
        # load the config from YAML
        try:
            with open(fname, encoding="utf-8") as stream:
                config = yaml.safe_load(stream)
        except OSError:
            self.logger.error("Could not open/read file: %s", fname)
        return config
