#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

import datetime
import requests
import yaml
import click
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import date
import os.path
from app.logz import create_logger

logger = create_logger()

# Create group to handle Qiz.io integration
@click.group()
def wiz():
    """Integrates continuous monitoring data from Wiz.io"""
    pass


# authenticate to get token
@wiz.command()
def authenticate():
    """Login with service account to retrieve a 24 hour access token that updates YAML file"""
    print("Authenticating - Loading configuration from init.yaml file")

    # load the config from YAML
    with open("init.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    # get secrets
    if "wizClientId" in config:
        clientId = config["wizClientId"]
    else:
        logger.error("No Wiz Client ID provided in the init.yaml file.")
        quit()
    if "wizClientSecret" in config:
        client_secret = config["wizClientSecret"]
    else:
        logger.error("No Wiz Client Secret provided in the init.yaml file.")
        quit()
    if "wizAuthUrl" in config:
        wiz_auth_url = config["wizAuthUrl"]
    else:
        logger.error("No Wiz Authentication URL provided in the init.yaml file.")
        quit()

    # get access token
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = (
        "grant_type=client_credentials&client_id="
        + clientId
        + "&client_secret="
        + client_secret
        + "&audience=beyond-api"
    )

    # login and get token
    print("Attempting to retrieve OAuth token from Wiz.io")
    try:
        response = requests.request("POST", wiz_auth_url, headers=headers, data=payload)
        authResponse = response.json()
    except:
        logger.error(
            "ERROR: Unable to authenticate to Wiz.io with the credentials and endpoint provided."
        )
        quit()

    # assign values
    if "access_token" in authResponse:
        config["wizAccessToken"] = authResponse["access_token"]
    else:
        logger.error("Wiz did not return an access token.")
        quit()
    if "scope" in authResponse:
        config["wizScope"] = authResponse["scope"]
    else:
        logger.error("Wiz did not return any valid scopes associated with this token.")
        quit()
    logger.info("SUCCESS: Wiz.io access token successfully retrieved.")

    # write our the result to YAML
    # write the changes back to file
    try:
        with open(r"init.yaml", "w") as file:
            documents = yaml.dump(config, file)
        print(
            "Access token written to init.yaml call to support future API calls.  Token is good for 24 hours."
        )
    except:
        logger.error("Error opening init.yaml (permissions) or file does not exist.")


# Process inventory list from Wiz
@wiz.command()
def inventory():
    """Process inventory list from Wiz"""
    print("Inventory - COMING SOON")


# Process issues from Wiz
@wiz.command()
@click.option(
    "--issue_level",
    prompt="Enter the Level of Issues to Process",
    help="RegScale will process all issues this level or higher.  Options include: LOW, MEDIUM, HIGH, CRITICAL.",
)
@click.option(
    "--regscale_id",
    prompt="Enter the RegScale Record ID",
    help="RegScale will create and update issues as children of this record.",
)
@click.option(
    "--regscale_module",
    prompt="Enter the RegScale Module name",
    help="Enter the RegScale module.  Options include: projects, policies, supplychain, securityplans, components.",
)
def issues(issue_level, regscale_id, regscale_module):
    """Process issues from Wiz"""
    # check issue level parameter
    if (
        str(issue_level).upper() != "LOW"
        and str(issue_level).upper() != "MEDIUM"
        and str(issue_level).upper() != "HIGH"
        and str(issue_level).upper() != "CRITICAL"
    ):
        logger.error(
            "You must select one of the following issue levels: LOW, MEDIUM, HIGH, CRITICAL"
        )
        quit()

    # load the config from YAML
    with open("init.yaml", "r") as stream:
        config = yaml.safe_load(stream)

    # get secrets
    url = config["wizUrl"]
    token = config["wizAccessToken"]
    strUser = config["userId"]

    # set headers
    url_issues = (
        config["domain"]
        + "/api/issues/getAllByParent/"
        + str(regscale_id)
        + "/"
        + str(regscale_module).lower()
    )
    headersGet = {"Accept": "application/json", "Authorization": config["token"]}

    # get the existing issues for the parent record that are already in RegScale
    print("Fetching full issue list from RegScale")
    issueResponse = requests.request("GET", url_issues, headers=headersGet)
    # check for null/not found response
    if issueResponse.status_code == 204:
        logger.warning("No existing issues for this RegScale record.")
        issuesData = []
    else:
        try:
            issuesData = issueResponse.json()
        except:
            logger.error("ERROR: Unable to fetch issues from RegScale")
            quit()

    # make directory if it doesn't exist
    if os.path.exists("./artifacts") == False:
        os.mkdir("./artifacts")
        logger.warning(
            "Artifacts directory does not exist.  Creating new directory for artifact processing."
        )
    else:
        logger.info(
            "Artifacts directory exists.  This directly will store output files from all processing."
        )

    # write out issues data to file
    if len(issuesData) > 0:
        with open("artifacts/existingRecordIssues.json", "w") as outfile:
            outfile.write(json.dumps(issuesData, indent=4))
        print(
            "Writing out RegScale issue list for Record #"
            + str(regscale_id)
            + " to the artifacts folder (see existingRecordIssues.json)"
        )
    logger.info(
        str(len(issuesData))
        + " existing issues retrieved for processing from RegScale."
    )

    # The GraphQL query that defines which data you wish to fetch.
    query = gql(
        """
    query IssuesTable($filterBy: IssueFilters, $first: Int, $after: String, $orderBy: IssueOrder) {
        issues(filterBy: $filterBy, first: $first, after: $after, orderBy: $orderBy) {
        nodes {
            ...IssueDetails
        }
        pageInfo {
            hasNextPage
            endCursor
        }
        totalCount
        informationalSeverityCount
        lowSeverityCount
        mediumSeverityCount
        highSeverityCount
        criticalSeverityCount
        uniqueEntityCount
        }
    }
        
        fragment IssueDetails on Issue {
        id
        control {
        id
        name
        query
        securitySubCategories {
          id
          externalId
          title
          description
          category {
            id
            externalId
            name
            framework {
              id
              name
            }
          }
        }
        }
        createdAt
        updatedAt
        projects {
        id
        name
        businessUnit
        riskProfile {
            businessImpact
        }
        }
        status
        severity
        entity {
        id
        name
        type
        }
        entitySnapshot {
        id
        type
        name
        }
        note
        serviceTicket {
        externalId
        name
        url
        }
    }
    """
    )

    # The variables sent along with the above query
    variables = {
        "first": 25,
        "filterBy": {"status": ["OPEN", "IN_PROGRESS"]},
        "orderBy": {"field": "SEVERITY", "direction": "DESC"},
    }

    # fetch the list of issues
    transport = AIOHTTPTransport(url=url, headers={"Authorization": "Bearer " + token})
    client = Client(
        transport=transport, fetch_schema_from_transport=True, execute_timeout=55
    )

    # loop through until all records have been fetched
    intFetch = 1
    issues = {}
    while intFetch > 0:
        # Fetch the query!
        try:
            wizIssues = client.execute(query, variable_values=variables)
        except:
            # error - unable to retrieve Wiz issues
            logger.info(
                "Error - unable to fetch Wiz issues.  Ensure access token is valid and correct Wiz API endpoint was provided."
            )
            quit()
        if intFetch == 1:
            # initialize the object
            issues = wizIssues
        else:
            # append any new records
            for n in wizIssues["issues"]["nodes"]:
                issues["issues"]["nodes"].append(n)

        # get page info
        pageInfo = wizIssues["issues"]["pageInfo"]

        # Check if there are additional results
        if pageInfo["hasNextPage"]:
            # Update variables to fetch the next batch of items
            variables["after"] = pageInfo["endCursor"]
            # update loop cursor
            intFetch += 1
        else:
            # No additional results. End the loop/
            intFetch = 0

    # output the results of the Wiz issues
    with open("artifacts/wizIssues.json", "w") as outfile:
        outfile.write(json.dumps(issues, indent=4))
    logger.info(
        str(len(issues["issues"]["nodes"]))
        + " issues retrieved for processing from Wiz.io."
    )

    # create arrays for processing
    regScaleClose = []
    regScaleUpdate = []
    regScaleNew = []

    # loop through the Wiz issues
    for iss in issues["issues"]["nodes"]:
        # default to Not Found
        bFound = False

        # see if this issue already exists in RegScale
        for exists in issuesData:
            if "wizId" in exists:
                if exists["wizId"] == iss["id"]:
                    bFound = True
                    # capture the existing record
                    issFound = exists

        # pre-process metadata
        strTitle = iss["entity"]["name"] + " - " + iss["control"]["name"]
        strDescription = "<strong>Wiz Control ID: </strong>" + iss["control"]["id"]
        strDescription += "<br/><strong>Asset Type: </strong>" + iss["entity"]["type"]
        strDescription += "<br/><strong>Severity: </strong>" + iss["severity"]
        strDescription += "<br/><strong>Date First Seen: </strong>" + str(
            iss["createdAt"]
        )
        strDescription += "<br/><strong>Date Last Seen: </strong>" + str(
            iss["updatedAt"]
        )

        # process subcategories for security frameworks
        categories = iss["control"]["securitySubCategories"]
        strTable = "<table><tr><td>Control ID</td><td>Category/Family</td><td>Framework</td><td>Description</td></tr>"
        for cat in categories:
            strTable += "<tr>"
            strTable += "<td>" + str(cat["externalId"]) + "</td>"
            strTable += "<td>" + str(cat["category"]["name"]) + "</td>"
            strTable += "<td>" + str(cat["category"]["framework"]["name"]) + "</td>"
            strTable += "<td>" + str(cat["description"]) + "</td>"
            strTable += "</tr>"
        strTable += "</table>"

        # get today's date as a baseline
        todayDate = date.today().strftime("%m/%d/%y")

        # handle status and due date
        if iss["severity"] == "LOW":
            strSeverity = "III - Low - Other Weakness"
            dueDate = datetime.datetime.strptime(
                todayDate, "%m/%d/%y"
            ) + datetime.timedelta(days=365)
        elif iss["severity"] == "MEDIUM" or iss["severity"] == "HIGH":
            strSeverity = "II - Moderate - Reportable Condition"
            dueDate = datetime.datetime.strptime(
                todayDate, "%m/%d/%y"
            ) + datetime.timedelta(days=90)
        elif iss["severity"] == "CRITICAL":
            strSeverity = "I - High - Significant Deficiency"
            dueDate = datetime.datetime.strptime(
                todayDate, "%m/%d/%y"
            ) + datetime.timedelta(days=30)
        else:
            logger.error("Unknown Wiz severity level: " + iss["severity"])

        # handle parent assignments for deep linking
        if regscale_module == "securityplans":
            intSecurityPlanId = regscale_id
        else:
            intSecurityPlanId = 0
        if regscale_module == "projects":
            intProjectId = regscale_id
        else:
            intProjectId = 0
        if regscale_module == "supplychain":
            intSupplyChainId = regscale_id
        else:
            intSupplyChainId = 0
        if regscale_module == "components":
            intComponentId = regscale_id
        else:
            intComponentId = 0

        # process based on whether found or not
        if bFound == True:
            # update existing record
            print(
                "RegScale Issue #"
                + str(issFound["id"])
                + " already exists for "
                + str(issFound["wizId"])
                + ".  Queuing for update."
            )
            # update the description
            issFound["description"] = strDescription + "<br/><br/>" + strTable
            # add to the update array
            regScaleUpdate.append(issFound)
        else:
            # process new record
            issNew = {
                "id": 0,
                "uuid": iss["entity"]["id"],
                "title": strTitle,
                "dateCreated": iss["createdAt"],
                "description": strDescription,
                "severityLevel": strSeverity + "<br/><br/>" + strTable,
                "issueOwnerId": strUser,
                "costEstimate": 0,
                "levelOfEffort": 0,
                "dueDate": str(dueDate),
                "identification": "Security Control Assessment",
                "status": "Open",
                "dateCompleted": None,
                "facilityId": None,
                "orgId": None,
                "controlId": 0,
                "assessmentId": 0,
                "requirementId": 0,
                "securityPlanId": intSecurityPlanId,
                "projectId": intProjectId,
                "supplyChainId": intSupplyChainId,
                "policyId": 0,
                "componentId": intComponentId,
                "incidentId": 0,
                "jiraId": "",
                "serviceNowId": "",
                "wizId": iss["id"],
                "prismaId": "",
                "parentId": regscale_id,
                "parentModule": regscale_module,
                "createdById": strUser,
                "lastUpdatedById": strUser,
                "dateLastUpdated": iss["updatedAt"],
            }
            # add the issue to the processing array
            regScaleNew.append(issNew)

    # see if any issues are open in RegScale that have been closed in Wiz (in RegScale but not in Wiz)
    for iss in issuesData:
        # only process open issues
        if iss["status"] == "Open":
            # default to close unless found
            bClose = True
            # loop through each Wiz issue and look for a match
            for wizIss in issues["issues"]["nodes"]:
                if iss["wizId"] == wizIss["id"]:
                    # still open in Wiz
                    bClose = False
            # if not found, close it
            if bClose == True:
                # set closed status
                iss["Status"] = "Closed"
                iss["DateCompleted"] = datetime.date.today().strftime("%m/%d/%Y")
                # queue to close
                regScaleClose.append(iss)

    # output the result to logs
    with open("artifacts/regScaleUpdateIssues.json", "w") as outfile:
        outfile.write(json.dumps(regScaleUpdate, indent=4))
    logger.warning(
        str(len(regScaleUpdate))
        + " Wiz issues were previously seen and have been updated."
    )

    # output the result to logs
    with open("artifacts/regScaleNewIssues.json", "w") as outfile:
        outfile.write(json.dumps(regScaleNew, indent=4))
    logger.error(
        str(len(regScaleNew))
        + " new Wiz issues have been processed and are ready for upload."
    )

    # output the result to logs
    with open("artifacts/regScaleCloseIssues.json", "w") as outfile:
        outfile.write(json.dumps(regScaleClose, indent=4))
    logger.info(
        str(len(regScaleClose))
        + " Wiz issues have been closed and are ready for closure in RegScale."
    )

    # Warn that processing is beginning
    logger.warning("PRE-PROCESSING COMPLETE: Batch updates beginning.....")

    # update each existing Wiz issue in RegScale
    url_update_issue = config["domain"] + "/api/issues/"
    postHeader = {"Authorization": config["token"]}
    for proc in regScaleUpdate:
        try:
            issueUpload = requests.request(
                "PUT",
                (url_update_issue + str(proc["id"])),
                headers=postHeader,
                json=proc,
            )
            issueUploadResponse = issueUpload.json()
            # output the result
            logger.info(
                "Success: Issue update for RegScale # "
                + str(issueUploadResponse["id"])
                + " loaded for Wiz ID #."
                + str(issueUploadResponse["wizId"])
            )
        except:
            logger.error("ERROR: Unable to update " + str(proc["id"]))

    # load each new Wiz issue into RegScale
    url_create_issue = config["domain"] + "/api/issues"
    for proc in regScaleNew:
        try:
            issueUpload = requests.request(
                "POST", url_create_issue, headers=postHeader, json=proc
            )
            issueUploadResponse = issueUpload.json()
            # output the result
            logger.info(
                "Success: New RegScale Issue # "
                + str(issueUploadResponse["id"])
                + " loaded for Wiz ID #."
                + str(issueUploadResponse["wizId"])
            )
        except:
            logger.error("ERROR: Unable to create " + str(proc))

    # close issues that have been remediated in RegScale
    url_close_issue = config["domain"] + "/api/issues/"
    for proc in regScaleClose:
        try:
            issueUpload = requests.request(
                "PUT",
                (url_close_issue + str(proc["id"])),
                headers=postHeader,
                json=proc,
            )
            issueUploadResponse = issueUpload.json()
            # output the result
            logger.info(
                "Success: Closed RegScale Issue # "
                + str(issueUploadResponse["id"])
                + "; Wiz ID #."
                + str(issueUploadResponse["wizId"])
            )
        except:
            logger.error("ERROR: Unable to close Issue # " + str(proc["id"]))


# Process threats from Wiz
@wiz.command()
def threats():
    """Process threats from Wiz"""
    print("Threats - COMING SOON")


# Process vulnerabilities from Wiz
@wiz.command()
def vulnerabilities():
    """Process vulnerabilities from Wiz"""
    print("Vulnerabilities - COMING SOON")
