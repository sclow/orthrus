from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *

class ProvisioningProfileListArguments(TaskArguments):
    def __init__(self, command_line):
        super().__init__(command_line)
        self.args = {}

    async def parse_arguments(self):
        pass


class ProvisioningProfileListCommand(CommandBase):
    cmd = "provisioning_profile_list"
    needs_admin = False
    help_cmd = "provisioning_profile_list"
    description = "Retrieve a list of installed provisioning profiles."
    version = 1
    is_exit = False
    is_file_browse = False
    is_process_list = False
    is_download_file = False
    is_remove_file = False
    is_upload_file = False
    author = "@rookuu"
    argument_class = ProvisioningProfileListArguments
    attackmapping = ["T1430.001"]

    async def create_tasking(self, task: MythicTask) -> MythicTask:
        return task

    async def process_response(self, response: AgentResponse):
        pass