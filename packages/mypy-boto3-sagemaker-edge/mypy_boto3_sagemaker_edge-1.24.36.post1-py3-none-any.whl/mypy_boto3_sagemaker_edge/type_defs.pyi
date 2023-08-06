"""
Type annotations for sagemaker-edge service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_edge/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_edge.type_defs import ChecksumTypeDef

    data: ChecksumTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import DeploymentStatusType, FailureHandlingPolicyType, ModelStateType

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ChecksumTypeDef",
    "DeploymentModelTypeDef",
    "EdgeMetricTypeDef",
    "ResponseMetadataTypeDef",
    "GetDeploymentsRequestRequestTypeDef",
    "GetDeviceRegistrationRequestRequestTypeDef",
    "DefinitionTypeDef",
    "DeploymentResultTypeDef",
    "ModelTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDeviceRegistrationResultTypeDef",
    "EdgeDeploymentTypeDef",
    "SendHeartbeatRequestRequestTypeDef",
    "GetDeploymentsResultTypeDef",
)

ChecksumTypeDef = TypedDict(
    "ChecksumTypeDef",
    {
        "Type": Literal["SHA1"],
        "Sum": str,
    },
    total=False,
)

DeploymentModelTypeDef = TypedDict(
    "DeploymentModelTypeDef",
    {
        "ModelHandle": str,
        "ModelName": str,
        "ModelVersion": str,
        "DesiredState": ModelStateType,
        "State": ModelStateType,
        "Status": DeploymentStatusType,
        "StatusReason": str,
        "RollbackFailureReason": str,
    },
    total=False,
)

EdgeMetricTypeDef = TypedDict(
    "EdgeMetricTypeDef",
    {
        "Dimension": str,
        "MetricName": str,
        "Value": float,
        "Timestamp": Union[datetime, str],
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

GetDeploymentsRequestRequestTypeDef = TypedDict(
    "GetDeploymentsRequestRequestTypeDef",
    {
        "DeviceName": str,
        "DeviceFleetName": str,
    },
)

GetDeviceRegistrationRequestRequestTypeDef = TypedDict(
    "GetDeviceRegistrationRequestRequestTypeDef",
    {
        "DeviceName": str,
        "DeviceFleetName": str,
    },
)

DefinitionTypeDef = TypedDict(
    "DefinitionTypeDef",
    {
        "ModelHandle": str,
        "S3Url": str,
        "Checksum": ChecksumTypeDef,
        "State": ModelStateType,
    },
    total=False,
)

DeploymentResultTypeDef = TypedDict(
    "DeploymentResultTypeDef",
    {
        "DeploymentName": str,
        "DeploymentStatus": str,
        "DeploymentStatusMessage": str,
        "DeploymentStartTime": Union[datetime, str],
        "DeploymentEndTime": Union[datetime, str],
        "DeploymentModels": Sequence[DeploymentModelTypeDef],
    },
    total=False,
)

ModelTypeDef = TypedDict(
    "ModelTypeDef",
    {
        "ModelName": str,
        "ModelVersion": str,
        "LatestSampleTime": Union[datetime, str],
        "LatestInference": Union[datetime, str],
        "ModelMetrics": Sequence[EdgeMetricTypeDef],
    },
    total=False,
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDeviceRegistrationResultTypeDef = TypedDict(
    "GetDeviceRegistrationResultTypeDef",
    {
        "DeviceRegistration": str,
        "CacheTTL": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EdgeDeploymentTypeDef = TypedDict(
    "EdgeDeploymentTypeDef",
    {
        "DeploymentName": str,
        "Type": Literal["Model"],
        "FailureHandlingPolicy": FailureHandlingPolicyType,
        "Definitions": List[DefinitionTypeDef],
    },
    total=False,
)

_RequiredSendHeartbeatRequestRequestTypeDef = TypedDict(
    "_RequiredSendHeartbeatRequestRequestTypeDef",
    {
        "AgentVersion": str,
        "DeviceName": str,
        "DeviceFleetName": str,
    },
)
_OptionalSendHeartbeatRequestRequestTypeDef = TypedDict(
    "_OptionalSendHeartbeatRequestRequestTypeDef",
    {
        "AgentMetrics": Sequence[EdgeMetricTypeDef],
        "Models": Sequence[ModelTypeDef],
        "DeploymentResult": DeploymentResultTypeDef,
    },
    total=False,
)

class SendHeartbeatRequestRequestTypeDef(
    _RequiredSendHeartbeatRequestRequestTypeDef, _OptionalSendHeartbeatRequestRequestTypeDef
):
    pass

GetDeploymentsResultTypeDef = TypedDict(
    "GetDeploymentsResultTypeDef",
    {
        "Deployments": List[EdgeDeploymentTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
