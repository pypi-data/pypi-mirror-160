# -*- coding: utf-8 -*-

"""
This module allow you to use AWS Lambda to process the CodeBuild
notification event. You can configure CodeBuild notification rule and send
those events to SNS topic, then use AWS Lambda to subscribe the SNS topic.

It enables you to react to build job run "start, failed, succeeded".
For example, you can send message to slack, send email when failed, etc ...
"""

from typing import Tuple
import dataclasses
from datetime import datetime
from .compat import need_cached_property

if need_cached_property:  # pragma: no cover
    from cached_property import cached_property
else:  # pragma: no cover
    from functools import cached_property


class CodeBuildEventTypeEnum:
    state_in_progress = "state_in_progress"
    state_failed = "state_failed"
    state_succeeded = "state_succeeded"
    unknown = "unknown"


@dataclasses.dataclass
class CodeBuildEvent:
    """
    Data container class to represent a CodeBuild event.

    - snake case attributes are json data key value pair
    - camel case properties are human friendly derived value
    """
    detail_type: str = ""
    build_id: str = ""
    build_status: str = ""
    completed_phase: str = ""
    completed_phase_context: str = ""
    completed_phase_duration_seconds: str = ""
    completed_phase_end: str = ""
    completed_phase_start: str = ""
    completed_phase_status: str = ""
    current_phase: str = ""
    current_phase_context: str = ""
    project_name: str = ""
    version: str = ""
    source_location: str = ""
    source_version: str = ""
    build_start_time: str = ""
    build_number: str = ""

    @classmethod
    def from_event(cls, event: dict) -> "CodeBuildEvent":
        # the raw event use "-" in it's naming convention
        kwargs = {k.replace("-", "_"): v for k, v in event["detail"].items()}
        more_info = kwargs.pop("additional_information")
        kwargs["source_location"] = more_info["source"]["location"]
        kwargs["source_version"] = more_info["source-version"]
        kwargs["build_number"] = str(int(more_info.get("build-number", 0)))
        kwargs["build_start_time"] = more_info["build-start-time"]
        kwargs["detail_type"] = event["detailType"]
        return cls(**kwargs)

    def to_env_var(self, prefix="") -> dict:
        return {(prefix + k).upper(): v for k, v in dataclasses.asdict(self).items()}

    @classmethod
    def from_env_var(cls, env_var: dict, prefix="") -> "CodeBuildEvent":
        field_set = {field.name for field in dataclasses.fields(cls)}
        kwargs = dict()
        for field_name in field_set:
            key = (prefix + field_name).upper()
            if key in env_var:
                kwargs[field_name] = env_var[key]
        return cls(**kwargs)

    @cached_property
    def parsed_build_id(self) -> Tuple[str, str, str, str, str]:
        first, second = self.build_id.split("/")
        first_parts, second_parts = first.split(":"), second.split(":")
        aws_account_id = first_parts[4]
        aws_region = first_parts[3]
        build_project = second_parts[0]
        build_uuid = second_parts[1]
        build_full_id = second
        return (aws_account_id, aws_region, build_full_id, build_project, build_uuid)

    @cached_property
    def awsAccountId(self) -> str:
        """
        AWS Account ID where this job runs.
        """
        return self.parsed_build_id[0]

    @cached_property
    def awsRegion(self) -> str:
        """
        AWS Region where this job runs.
        """
        return self.parsed_build_id[1]

    @cached_property
    def buildUUID(self) -> str:
        """
        Full job id, it is the project name + uuid.
        """
        return self.parsed_build_id[2]

    @cached_property
    def buildProject(self) -> str:
        """
        AWS CodeBuild Project name of this job run.
        """
        return self.parsed_build_id[3]

    @cached_property
    def buildId(self) -> str:
        """
        The UUID4 part of of this job run.
        """
        return self.parsed_build_id[4]

    @cached_property
    def buildRunConsoleUrl(self) -> str:
        """
        AWS Console Url of this job run details.
        """
        return f"https://{self.awsRegion}.console.aws.amazon.com/codesuite/codebuild/{self.awsAccountId}/projects/{self.buildProject}/build/{self.buildUUID}/?region={self.awsRegion}"

    @cached_property
    def buildNumber(self) -> int:
        """
        Digits job run id.
        """
        return int(self.build_number)

    @cached_property
    def buildStartTime(self) -> datetime:
        """
        Job run start time in datetime.
        """
        return datetime.strptime(self.build_start_time, "%b %d, %Y %I:%M:%S %p")

    @cached_property
    def event_type(self) -> str:
        if self.detail_type == "CodeBuild Build State Change":
            if self.build_status == "IN_PROGRESS":
                return CodeBuildEventTypeEnum.state_in_progress
            elif self.build_status == "FAILED":
                return CodeBuildEventTypeEnum.state_failed
            elif self.build_status == "SUCCEEDED":
                return CodeBuildEventTypeEnum.state_succeeded
            else:  # pragma: no cover
                return CodeBuildEventTypeEnum.unknown
        elif self.detail_type == "CodeBuild Build Phase Change":  # pragma: no cover
            return CodeBuildEventTypeEnum.unknown
        else:  # pragma: no cover
            return CodeBuildEventTypeEnum.unknown

    @cached_property
    def is_state_in_progress(self) -> bool:
        """
        Is it a job start event?
        """
        return self.event_type == CodeBuildEventTypeEnum.state_in_progress

    @cached_property
    def is_state_failed(self) -> bool:
        """
        Is it a job failed event?
        """
        return self.event_type == CodeBuildEventTypeEnum.state_failed

    @cached_property
    def is_state_succeeded(self) -> bool:
        """
        Is it a job succeeeded event?
        """
        return self.event_type == CodeBuildEventTypeEnum.state_succeeded
