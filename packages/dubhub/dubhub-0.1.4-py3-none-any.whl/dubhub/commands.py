import json
import logging
import os

import requests
import re

from .version import VERSION

logger = logging.getLogger(__name__)

class Commands:
    def __init__(self, server):
        self.SERVER = server

    def start_clone(self, dub_uuid, org_token, output):
        try:
            CI_PIPELINE_ID = os.environ.get("CI_PIPELINE_ID", "GITHUB_RUN_ID")
            CI_COMMIT_REF_NAME = os.environ.get("CI_COMMIT_REF_NAME", "GITHUB_HEAD_REF")
            CI_COMMIT_SHA = os.environ.get("CI_COMMIT_SHA", "GITHUB_SHA")
            CI_MERGE_REQUEST_IID = os.environ.get("CI_MERGE_REQUEST_IID", "github")
            CI_DEFAULT_BRANCH = os.environ.get("CI_DEFAULT_BRANCH", "GITHUB_BASE_REF")
            if type(CI_MERGE_REQUEST_IID) != "str":
                CI_MERGE_REQUEST_IID = CI_MERGE_REQUEST_IID
            response = requests.post(
                f"{self.SERVER}/api/clone/start",
                json={
                    "dubUuid": dub_uuid,
                    "orgToken": org_token,
                    "CI_PIPELINE_ID": CI_PIPELINE_ID,
                    "CI_COMMIT_REF_NAME": CI_COMMIT_REF_NAME,
                    "CI_COMMIT_SHA": CI_COMMIT_SHA,
                    "CI_MERGE_REQUEST_IID": CI_MERGE_REQUEST_IID,
                    "CI_DEFAULT_BRANCH": CI_DEFAULT_BRANCH,
                    "VERSION": VERSION
                },
            )
        except Exception as e:
            logger.error("Error with sending post request:" + str(e))
            # load and dump json so its formatted properly; also helps validate
            # that the json returned is proper
        try:
            connection_string = json.loads(json.dumps(json.loads(response.content)))['conn_string']
            with open("start_clone_output.json", "w") as outfile:
                json.dump(json.dumps(json.loads(response.content)), outfile)
            if output == "json":
                host_start_index = connection_string.find("@") + 1
                host_end_index = connection_string.rfind(":")
                json_output = {
                    "host": connection_string[host_start_index: host_end_index],
                    "port": re.findall("\d+(?=\D*$)", connection_string)[-1],
                    "username": "postgres",
                    "password": "",
                    "database": "postgres",
                    "clone_uuid": json.loads(json.dumps(json.loads(response.content)))['cloneUuid'],
                    "dub_uuid": dub_uuid
                    }
                print(json_output)
        except Exception as e:
            logger.error("Error converting response object to JSON file:" + str(e))

    def stop_clone(self, clone_uuid, org_token):
        try:
            response = requests.post(
                f"{self.SERVER}/api/clone/stop",
                json={
                    "cloneUuid": clone_uuid,
                    "orgToken": org_token,
                    "VERSION": VERSION
                },
            )
            # logger.info(json.loads(json.dumps(json.loads(response.content))))
            print(json.loads(json.dumps(json.loads(response.content))))
        except Exception as e:
            logger.error("Error with sending post request:" + str(e))

    def analyse_clone(self, cloneUuid, org_token, token):
        try:
            CI_API_V4_URL = os.environ.get("CI_API_V4_URL", None)
            CI_PROJECT_ID = os.environ.get("CI_PROJECT_ID", None)
            CI_MERGE_REQUEST_IID = os.environ.get("CI_MERGE_REQUEST_IID", "github")
            if type(CI_MERGE_REQUEST_IID) != "string":
                CI_MERGE_REQUEST_IID = CI_MERGE_REQUEST_IID
            CI_DEFAULT_BRANCH = os.environ.get("CI_DEFAULT_BRANCH", "GITHUB_BASE_REF")
            GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", None)
            GITHUB_SHA = os.environ.get("GITHUB_SHA", None)
            GITHUB_REF = os.environ.get("GITHUB_REF", None)
            if GITHUB_REPOSITORY is None:
                GITHUB_OR_GITLAB = "gitlab"
            else:
                GITHUB_OR_GITLAB = "github"
        except Exception as e:
            logger.error("Error converting JSON file to JSON object:" + str(e))
        try:
            requests.post(
                f"{self.SERVER}/api/clone/analyse",
                json={
                    "cloneUuid": cloneUuid,
                    "orgToken": org_token,
                    "token": token,
                    "CI_API_V4_URL": CI_API_V4_URL,
                    "CI_PROJECT_ID": CI_PROJECT_ID,
                    "CI_MERGE_REQUEST_IID": CI_MERGE_REQUEST_IID,
                    "CI_DEFAULT_BRANCH": CI_DEFAULT_BRANCH,
                    "GITHUB_OR_GITLAB": GITHUB_OR_GITLAB,
                    "GITHUB_REPOSITORY": GITHUB_REPOSITORY,
                    "GITHUB_SHA": GITHUB_SHA,
                    "GITHUB_REF": GITHUB_REF,
                    "VERSION": VERSION
                },
            )
            # print(f"See your results here: {response}")
        except Exception as e:
            logger.error("Error with sending post request:" + str(e))
