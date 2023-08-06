#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import yaml
from app.application import Application
from app.logz import create_logger


logger = create_logger()
# logs in the user
def login(strUser, strPassword):
    appl = Application()
    config = appl.config
    # load the config from YAML
    # with open("init.yaml", "r") as stream:
    #     config = yaml.safe_load(stream)
    if config["domain"] is None:
        raise ValueError("ERROR: No domain set in the initilization file.")
    elif config["domain"] == "":
        raise ValueError("ERROR: The domain is blank in the initialization file.")
    else:
        # set the catalog URL for your Atlasity instance
        url_login = config["domain"] + "/api/authentication/login"
        logger.info("Logging into: " + url_login)

        # create object to authenticate
        auth = {"userName": strUser, "password": strPassword, "oldPassword": ""}

        # login and get token
        response = requests.request("POST", url_login, json=auth)
        try:
            authResponse = response.json()
            userId = authResponse["id"]
            jwt = "Bearer " + authResponse["auth_token"]
        except:
            logger.error("ERROR: Unable to login user to RegScale.")
            quit()

        # update init file from login
        config["token"] = jwt
        config["userId"] = userId

        # write the changes back to file
        with open(r"init.yaml", "w") as file:
            documents = yaml.dump(config, file)
            logger.info("Login Successful!")
            logger.info("Init.yaml file updated successfully.")

        # set variables
        logger.info("User ID: " + userId)
        logger.info("RegScale Token: " + jwt)

        return jwt
