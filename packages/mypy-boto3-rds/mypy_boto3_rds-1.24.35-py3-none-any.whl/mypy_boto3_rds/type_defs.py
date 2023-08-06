"""
Type annotations for rds service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rds/type_defs/)

Usage::

    ```python
    from mypy_boto3_rds.type_defs import AccountQuotaTypeDef

    data: AccountQuotaTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ActivityStreamModeType,
    ActivityStreamStatusType,
    ApplyMethodType,
    AutomationModeType,
    CustomEngineVersionStatusType,
    DBProxyEndpointStatusType,
    DBProxyEndpointTargetRoleType,
    DBProxyStatusType,
    EngineFamilyType,
    FailoverStatusType,
    IAMAuthModeType,
    ReplicaModeType,
    SourceTypeType,
    TargetHealthReasonType,
    TargetRoleType,
    TargetStateType,
    TargetTypeType,
    WriteForwardingStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AccountQuotaTypeDef",
    "ResponseMetadataTypeDef",
    "AddRoleToDBClusterMessageRequestTypeDef",
    "AddRoleToDBInstanceMessageRequestTypeDef",
    "AddSourceIdentifierToSubscriptionMessageRequestTypeDef",
    "EventSubscriptionTypeDef",
    "TagTypeDef",
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    "AuthorizeDBSecurityGroupIngressMessageRequestTypeDef",
    "AvailabilityZoneTypeDef",
    "AvailableProcessorFeatureTypeDef",
    "BacktrackDBClusterMessageRequestTypeDef",
    "CancelExportTaskMessageRequestTypeDef",
    "CertificateTypeDef",
    "CharacterSetTypeDef",
    "ClientGenerateDbAuthTokenRequestTypeDef",
    "CloudwatchLogsExportConfigurationTypeDef",
    "PendingCloudwatchLogsExportsTypeDef",
    "ConnectionPoolConfigurationInfoTypeDef",
    "ConnectionPoolConfigurationTypeDef",
    "DBClusterParameterGroupTypeDef",
    "DBParameterGroupTypeDef",
    "ScalingConfigurationTypeDef",
    "ServerlessV2ScalingConfigurationTypeDef",
    "ProcessorFeatureTypeDef",
    "DBProxyEndpointTypeDef",
    "UserAuthConfigTypeDef",
    "CreateGlobalClusterMessageRequestTypeDef",
    "DBClusterBacktrackTypeDef",
    "DBClusterEndpointTypeDef",
    "DBClusterMemberTypeDef",
    "DBClusterOptionGroupStatusTypeDef",
    "ParameterTypeDef",
    "DBClusterRoleTypeDef",
    "DBClusterSnapshotAttributeTypeDef",
    "DomainMembershipTypeDef",
    "ScalingConfigurationInfoTypeDef",
    "ServerlessV2ScalingConfigurationInfoTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "TimezoneTypeDef",
    "UpgradeTargetTypeDef",
    "DBInstanceAutomatedBackupsReplicationTypeDef",
    "RestoreWindowTypeDef",
    "DBInstanceRoleTypeDef",
    "DBInstanceStatusInfoTypeDef",
    "DBParameterGroupStatusTypeDef",
    "DBSecurityGroupMembershipTypeDef",
    "EndpointTypeDef",
    "OptionGroupMembershipTypeDef",
    "TargetHealthTypeDef",
    "UserAuthConfigInfoTypeDef",
    "EC2SecurityGroupTypeDef",
    "IPRangeTypeDef",
    "DBSnapshotAttributeTypeDef",
    "DeleteCustomDBEngineVersionMessageRequestTypeDef",
    "DeleteDBClusterEndpointMessageRequestTypeDef",
    "DeleteDBClusterMessageRequestTypeDef",
    "DeleteDBClusterParameterGroupMessageRequestTypeDef",
    "DeleteDBClusterSnapshotMessageRequestTypeDef",
    "DeleteDBInstanceAutomatedBackupMessageRequestTypeDef",
    "DeleteDBInstanceMessageRequestTypeDef",
    "DeleteDBParameterGroupMessageRequestTypeDef",
    "DeleteDBProxyEndpointRequestRequestTypeDef",
    "DeleteDBProxyRequestRequestTypeDef",
    "DeleteDBSecurityGroupMessageRequestTypeDef",
    "DeleteDBSnapshotMessageRequestTypeDef",
    "DeleteDBSubnetGroupMessageRequestTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "DeleteGlobalClusterMessageRequestTypeDef",
    "DeleteOptionGroupMessageRequestTypeDef",
    "DeregisterDBProxyTargetsRequestRequestTypeDef",
    "FilterTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDBClusterSnapshotAttributesMessageRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeDBLogFilesDetailsTypeDef",
    "DescribeDBSnapshotAttributesMessageRequestTypeDef",
    "DescribeValidDBInstanceModificationsMessageRequestTypeDef",
    "DoubleRangeTypeDef",
    "DownloadDBLogFilePortionMessageRequestTypeDef",
    "EventCategoriesMapTypeDef",
    "EventTypeDef",
    "ExportTaskTypeDef",
    "FailoverDBClusterMessageRequestTypeDef",
    "FailoverGlobalClusterMessageRequestTypeDef",
    "FailoverStateTypeDef",
    "GlobalClusterMemberTypeDef",
    "MinimumEngineVersionPerAllowedValueTypeDef",
    "ModifyCertificatesMessageRequestTypeDef",
    "ModifyCurrentDBClusterCapacityMessageRequestTypeDef",
    "ModifyCustomDBEngineVersionMessageRequestTypeDef",
    "ModifyDBClusterEndpointMessageRequestTypeDef",
    "ModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    "ModifyDBProxyEndpointRequestRequestTypeDef",
    "ModifyDBSnapshotAttributeMessageRequestTypeDef",
    "ModifyDBSnapshotMessageRequestTypeDef",
    "ModifyDBSubnetGroupMessageRequestTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "ModifyGlobalClusterMessageRequestTypeDef",
    "OptionSettingTypeDef",
    "OptionVersionTypeDef",
    "OutpostTypeDef",
    "PendingMaintenanceActionTypeDef",
    "PromoteReadReplicaDBClusterMessageRequestTypeDef",
    "PromoteReadReplicaMessageRequestTypeDef",
    "RangeTypeDef",
    "RebootDBClusterMessageRequestTypeDef",
    "RebootDBInstanceMessageRequestTypeDef",
    "RecurringChargeTypeDef",
    "RegisterDBProxyTargetsRequestRequestTypeDef",
    "RemoveFromGlobalClusterMessageRequestTypeDef",
    "RemoveRoleFromDBClusterMessageRequestTypeDef",
    "RemoveRoleFromDBInstanceMessageRequestTypeDef",
    "RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "RevokeDBSecurityGroupIngressMessageRequestTypeDef",
    "SourceRegionTypeDef",
    "StartActivityStreamRequestRequestTypeDef",
    "StartDBClusterMessageRequestTypeDef",
    "StartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef",
    "StartDBInstanceMessageRequestTypeDef",
    "StartExportTaskMessageRequestTypeDef",
    "StopActivityStreamRequestRequestTypeDef",
    "StopDBClusterMessageRequestTypeDef",
    "StopDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef",
    "StopDBInstanceMessageRequestTypeDef",
    "AccountAttributesMessageTypeDef",
    "DBClusterBacktrackResponseMetadataTypeDef",
    "DBClusterCapacityInfoTypeDef",
    "DBClusterEndpointResponseMetadataTypeDef",
    "DBClusterParameterGroupNameMessageTypeDef",
    "DBParameterGroupNameMessageTypeDef",
    "DownloadDBLogFilePortionDetailsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportTaskResponseMetadataTypeDef",
    "StartActivityStreamResponseTypeDef",
    "StopActivityStreamResponseTypeDef",
    "AddSourceIdentifierToSubscriptionResultTypeDef",
    "CreateEventSubscriptionResultTypeDef",
    "DeleteEventSubscriptionResultTypeDef",
    "EventSubscriptionsMessageTypeDef",
    "ModifyEventSubscriptionResultTypeDef",
    "RemoveSourceIdentifierFromSubscriptionResultTypeDef",
    "AddTagsToResourceMessageRequestTypeDef",
    "CopyDBClusterParameterGroupMessageRequestTypeDef",
    "CopyDBClusterSnapshotMessageRequestTypeDef",
    "CopyDBParameterGroupMessageRequestTypeDef",
    "CopyDBSnapshotMessageRequestTypeDef",
    "CopyOptionGroupMessageRequestTypeDef",
    "CreateCustomDBEngineVersionMessageRequestTypeDef",
    "CreateDBClusterEndpointMessageRequestTypeDef",
    "CreateDBClusterParameterGroupMessageRequestTypeDef",
    "CreateDBClusterSnapshotMessageRequestTypeDef",
    "CreateDBParameterGroupMessageRequestTypeDef",
    "CreateDBProxyEndpointRequestRequestTypeDef",
    "CreateDBSecurityGroupMessageRequestTypeDef",
    "CreateDBSnapshotMessageRequestTypeDef",
    "CreateDBSubnetGroupMessageRequestTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "CreateOptionGroupMessageRequestTypeDef",
    "DBClusterSnapshotTypeDef",
    "PurchaseReservedDBInstancesOfferingMessageRequestTypeDef",
    "TagListMessageTypeDef",
    "OrderableDBInstanceOptionTypeDef",
    "CertificateMessageTypeDef",
    "ModifyCertificatesResultTypeDef",
    "ClusterPendingModifiedValuesTypeDef",
    "DBProxyTargetGroupTypeDef",
    "ModifyDBProxyTargetGroupRequestRequestTypeDef",
    "CopyDBClusterParameterGroupResultTypeDef",
    "CreateDBClusterParameterGroupResultTypeDef",
    "DBClusterParameterGroupsMessageTypeDef",
    "CopyDBParameterGroupResultTypeDef",
    "CreateDBParameterGroupResultTypeDef",
    "DBParameterGroupsMessageTypeDef",
    "CreateDBClusterMessageRequestTypeDef",
    "ModifyDBClusterMessageRequestTypeDef",
    "RestoreDBClusterFromS3MessageRequestTypeDef",
    "RestoreDBClusterFromSnapshotMessageRequestTypeDef",
    "RestoreDBClusterToPointInTimeMessageRequestTypeDef",
    "CreateDBInstanceMessageRequestTypeDef",
    "CreateDBInstanceReadReplicaMessageRequestTypeDef",
    "DBSnapshotTypeDef",
    "ModifyDBInstanceMessageRequestTypeDef",
    "PendingModifiedValuesTypeDef",
    "RestoreDBInstanceFromDBSnapshotMessageRequestTypeDef",
    "RestoreDBInstanceFromS3MessageRequestTypeDef",
    "RestoreDBInstanceToPointInTimeMessageRequestTypeDef",
    "CreateDBProxyEndpointResponseTypeDef",
    "DeleteDBProxyEndpointResponseTypeDef",
    "DescribeDBProxyEndpointsResponseTypeDef",
    "ModifyDBProxyEndpointResponseTypeDef",
    "CreateDBProxyRequestRequestTypeDef",
    "ModifyDBProxyRequestRequestTypeDef",
    "DBClusterBacktrackMessageTypeDef",
    "DBClusterEndpointMessageTypeDef",
    "DBClusterParameterGroupDetailsTypeDef",
    "DBParameterGroupDetailsTypeDef",
    "EngineDefaultsTypeDef",
    "ModifyDBClusterParameterGroupMessageRequestTypeDef",
    "ModifyDBParameterGroupMessageRequestTypeDef",
    "ResetDBClusterParameterGroupMessageRequestTypeDef",
    "ResetDBParameterGroupMessageRequestTypeDef",
    "DBClusterSnapshotAttributesResultTypeDef",
    "DBEngineVersionResponseMetadataTypeDef",
    "DBEngineVersionTypeDef",
    "DBInstanceAutomatedBackupTypeDef",
    "DBProxyTargetTypeDef",
    "DBProxyTypeDef",
    "DBSecurityGroupTypeDef",
    "DBSnapshotAttributesResultTypeDef",
    "DescribeCertificatesMessageRequestTypeDef",
    "DescribeDBClusterBacktracksMessageRequestTypeDef",
    "DescribeDBClusterEndpointsMessageRequestTypeDef",
    "DescribeDBClusterParameterGroupsMessageRequestTypeDef",
    "DescribeDBClusterParametersMessageRequestTypeDef",
    "DescribeDBClusterSnapshotsMessageRequestTypeDef",
    "DescribeDBClustersMessageRequestTypeDef",
    "DescribeDBEngineVersionsMessageRequestTypeDef",
    "DescribeDBInstanceAutomatedBackupsMessageRequestTypeDef",
    "DescribeDBInstancesMessageRequestTypeDef",
    "DescribeDBLogFilesMessageRequestTypeDef",
    "DescribeDBParameterGroupsMessageRequestTypeDef",
    "DescribeDBParametersMessageRequestTypeDef",
    "DescribeDBProxiesRequestRequestTypeDef",
    "DescribeDBProxyEndpointsRequestRequestTypeDef",
    "DescribeDBProxyTargetGroupsRequestRequestTypeDef",
    "DescribeDBProxyTargetsRequestRequestTypeDef",
    "DescribeDBSecurityGroupsMessageRequestTypeDef",
    "DescribeDBSnapshotsMessageRequestTypeDef",
    "DescribeDBSubnetGroupsMessageRequestTypeDef",
    "DescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    "DescribeEngineDefaultParametersMessageRequestTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeExportTasksMessageRequestTypeDef",
    "DescribeGlobalClustersMessageRequestTypeDef",
    "DescribeOptionGroupOptionsMessageRequestTypeDef",
    "DescribeOptionGroupsMessageRequestTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    "DescribeReservedDBInstancesMessageRequestTypeDef",
    "DescribeReservedDBInstancesOfferingsMessageRequestTypeDef",
    "DescribeSourceRegionsMessageRequestTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    "DescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef",
    "DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef",
    "DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef",
    "DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    "DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef",
    "DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef",
    "DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef",
    "DescribeDBInstanceAutomatedBackupsMessageDescribeDBInstanceAutomatedBackupsPaginateTypeDef",
    "DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef",
    "DescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef",
    "DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef",
    "DescribeDBParametersMessageDescribeDBParametersPaginateTypeDef",
    "DescribeDBProxiesRequestDescribeDBProxiesPaginateTypeDef",
    "DescribeDBProxyEndpointsRequestDescribeDBProxyEndpointsPaginateTypeDef",
    "DescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef",
    "DescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef",
    "DescribeDBSecurityGroupsMessageDescribeDBSecurityGroupsPaginateTypeDef",
    "DescribeDBSnapshotsMessageDescribeDBSnapshotsPaginateTypeDef",
    "DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef",
    "DescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef",
    "DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef",
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    "DescribeExportTasksMessageDescribeExportTasksPaginateTypeDef",
    "DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef",
    "DescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef",
    "DescribeOptionGroupsMessageDescribeOptionGroupsPaginateTypeDef",
    "DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    "DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef",
    "DescribeReservedDBInstancesMessageDescribeReservedDBInstancesPaginateTypeDef",
    "DescribeReservedDBInstancesOfferingsMessageDescribeReservedDBInstancesOfferingsPaginateTypeDef",
    "DescribeSourceRegionsMessageDescribeSourceRegionsPaginateTypeDef",
    "DownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef",
    "DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef",
    "DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef",
    "DescribeDBClustersMessageDBClusterAvailableWaitTypeDef",
    "DescribeDBClustersMessageDBClusterDeletedWaitTypeDef",
    "DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef",
    "DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef",
    "DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef",
    "DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef",
    "DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef",
    "DescribeDBLogFilesResponseTypeDef",
    "EventCategoriesMessageTypeDef",
    "EventsMessageTypeDef",
    "ExportTasksMessageTypeDef",
    "GlobalClusterTypeDef",
    "OptionGroupOptionSettingTypeDef",
    "OptionConfigurationTypeDef",
    "OptionTypeDef",
    "SubnetTypeDef",
    "ResourcePendingMaintenanceActionsTypeDef",
    "ValidStorageOptionsTypeDef",
    "ReservedDBInstanceTypeDef",
    "ReservedDBInstancesOfferingTypeDef",
    "SourceRegionMessageTypeDef",
    "CopyDBClusterSnapshotResultTypeDef",
    "CreateDBClusterSnapshotResultTypeDef",
    "DBClusterSnapshotMessageTypeDef",
    "DeleteDBClusterSnapshotResultTypeDef",
    "OrderableDBInstanceOptionsMessageTypeDef",
    "DBClusterTypeDef",
    "DescribeDBProxyTargetGroupsResponseTypeDef",
    "ModifyDBProxyTargetGroupResponseTypeDef",
    "CopyDBSnapshotResultTypeDef",
    "CreateDBSnapshotResultTypeDef",
    "DBSnapshotMessageTypeDef",
    "DeleteDBSnapshotResultTypeDef",
    "ModifyDBSnapshotResultTypeDef",
    "DescribeEngineDefaultClusterParametersResultTypeDef",
    "DescribeEngineDefaultParametersResultTypeDef",
    "DescribeDBClusterSnapshotAttributesResultTypeDef",
    "ModifyDBClusterSnapshotAttributeResultTypeDef",
    "DBEngineVersionMessageTypeDef",
    "DBInstanceAutomatedBackupMessageTypeDef",
    "DeleteDBInstanceAutomatedBackupResultTypeDef",
    "StartDBInstanceAutomatedBackupsReplicationResultTypeDef",
    "StopDBInstanceAutomatedBackupsReplicationResultTypeDef",
    "DescribeDBProxyTargetsResponseTypeDef",
    "RegisterDBProxyTargetsResponseTypeDef",
    "CreateDBProxyResponseTypeDef",
    "DeleteDBProxyResponseTypeDef",
    "DescribeDBProxiesResponseTypeDef",
    "ModifyDBProxyResponseTypeDef",
    "AuthorizeDBSecurityGroupIngressResultTypeDef",
    "CreateDBSecurityGroupResultTypeDef",
    "DBSecurityGroupMessageTypeDef",
    "RevokeDBSecurityGroupIngressResultTypeDef",
    "DescribeDBSnapshotAttributesResultTypeDef",
    "ModifyDBSnapshotAttributeResultTypeDef",
    "CreateGlobalClusterResultTypeDef",
    "DeleteGlobalClusterResultTypeDef",
    "FailoverGlobalClusterResultTypeDef",
    "GlobalClustersMessageTypeDef",
    "ModifyGlobalClusterResultTypeDef",
    "RemoveFromGlobalClusterResultTypeDef",
    "OptionGroupOptionTypeDef",
    "ModifyOptionGroupMessageRequestTypeDef",
    "OptionGroupTypeDef",
    "DBSubnetGroupTypeDef",
    "ApplyPendingMaintenanceActionResultTypeDef",
    "PendingMaintenanceActionsMessageTypeDef",
    "ValidDBInstanceModificationsMessageTypeDef",
    "PurchaseReservedDBInstancesOfferingResultTypeDef",
    "ReservedDBInstanceMessageTypeDef",
    "ReservedDBInstancesOfferingMessageTypeDef",
    "CreateDBClusterResultTypeDef",
    "DBClusterMessageTypeDef",
    "DeleteDBClusterResultTypeDef",
    "FailoverDBClusterResultTypeDef",
    "ModifyDBClusterResultTypeDef",
    "PromoteReadReplicaDBClusterResultTypeDef",
    "RebootDBClusterResultTypeDef",
    "RestoreDBClusterFromS3ResultTypeDef",
    "RestoreDBClusterFromSnapshotResultTypeDef",
    "RestoreDBClusterToPointInTimeResultTypeDef",
    "StartDBClusterResultTypeDef",
    "StopDBClusterResultTypeDef",
    "OptionGroupOptionsMessageTypeDef",
    "CopyOptionGroupResultTypeDef",
    "CreateOptionGroupResultTypeDef",
    "ModifyOptionGroupResultTypeDef",
    "OptionGroupsTypeDef",
    "CreateDBSubnetGroupResultTypeDef",
    "DBInstanceTypeDef",
    "DBSubnetGroupMessageTypeDef",
    "ModifyDBSubnetGroupResultTypeDef",
    "DescribeValidDBInstanceModificationsResultTypeDef",
    "CreateDBInstanceReadReplicaResultTypeDef",
    "CreateDBInstanceResultTypeDef",
    "DBInstanceMessageTypeDef",
    "DeleteDBInstanceResultTypeDef",
    "ModifyDBInstanceResultTypeDef",
    "PromoteReadReplicaResultTypeDef",
    "RebootDBInstanceResultTypeDef",
    "RestoreDBInstanceFromDBSnapshotResultTypeDef",
    "RestoreDBInstanceFromS3ResultTypeDef",
    "RestoreDBInstanceToPointInTimeResultTypeDef",
    "StartDBInstanceResultTypeDef",
    "StopDBInstanceResultTypeDef",
)

AccountQuotaTypeDef = TypedDict(
    "AccountQuotaTypeDef",
    {
        "AccountQuotaName": str,
        "Used": int,
        "Max": int,
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

_RequiredAddRoleToDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredAddRoleToDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "RoleArn": str,
    },
)
_OptionalAddRoleToDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalAddRoleToDBClusterMessageRequestTypeDef",
    {
        "FeatureName": str,
    },
    total=False,
)


class AddRoleToDBClusterMessageRequestTypeDef(
    _RequiredAddRoleToDBClusterMessageRequestTypeDef,
    _OptionalAddRoleToDBClusterMessageRequestTypeDef,
):
    pass


AddRoleToDBInstanceMessageRequestTypeDef = TypedDict(
    "AddRoleToDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "RoleArn": str,
        "FeatureName": str,
    },
)

AddSourceIdentifierToSubscriptionMessageRequestTypeDef = TypedDict(
    "AddSourceIdentifierToSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SourceIdentifier": str,
    },
)

EventSubscriptionTypeDef = TypedDict(
    "EventSubscriptionTypeDef",
    {
        "CustomerAwsId": str,
        "CustSubscriptionId": str,
        "SnsTopicArn": str,
        "Status": str,
        "SubscriptionCreationTime": str,
        "SourceType": str,
        "SourceIdsList": List[str],
        "EventCategoriesList": List[str],
        "Enabled": bool,
        "EventSubscriptionArn": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
    total=False,
)

ApplyPendingMaintenanceActionMessageRequestTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "ApplyAction": str,
        "OptInType": str,
    },
)

_RequiredAuthorizeDBSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_RequiredAuthorizeDBSecurityGroupIngressMessageRequestTypeDef",
    {
        "DBSecurityGroupName": str,
    },
)
_OptionalAuthorizeDBSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_OptionalAuthorizeDBSecurityGroupIngressMessageRequestTypeDef",
    {
        "CIDRIP": str,
        "EC2SecurityGroupName": str,
        "EC2SecurityGroupId": str,
        "EC2SecurityGroupOwnerId": str,
    },
    total=False,
)


class AuthorizeDBSecurityGroupIngressMessageRequestTypeDef(
    _RequiredAuthorizeDBSecurityGroupIngressMessageRequestTypeDef,
    _OptionalAuthorizeDBSecurityGroupIngressMessageRequestTypeDef,
):
    pass


AvailabilityZoneTypeDef = TypedDict(
    "AvailabilityZoneTypeDef",
    {
        "Name": str,
    },
    total=False,
)

AvailableProcessorFeatureTypeDef = TypedDict(
    "AvailableProcessorFeatureTypeDef",
    {
        "Name": str,
        "DefaultValue": str,
        "AllowedValues": str,
    },
    total=False,
)

_RequiredBacktrackDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredBacktrackDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "BacktrackTo": Union[datetime, str],
    },
)
_OptionalBacktrackDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalBacktrackDBClusterMessageRequestTypeDef",
    {
        "Force": bool,
        "UseEarliestTimeOnPointInTimeUnavailable": bool,
    },
    total=False,
)


class BacktrackDBClusterMessageRequestTypeDef(
    _RequiredBacktrackDBClusterMessageRequestTypeDef,
    _OptionalBacktrackDBClusterMessageRequestTypeDef,
):
    pass


CancelExportTaskMessageRequestTypeDef = TypedDict(
    "CancelExportTaskMessageRequestTypeDef",
    {
        "ExportTaskIdentifier": str,
    },
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "CertificateIdentifier": str,
        "CertificateType": str,
        "Thumbprint": str,
        "ValidFrom": datetime,
        "ValidTill": datetime,
        "CertificateArn": str,
        "CustomerOverride": bool,
        "CustomerOverrideValidTill": datetime,
    },
    total=False,
)

CharacterSetTypeDef = TypedDict(
    "CharacterSetTypeDef",
    {
        "CharacterSetName": str,
        "CharacterSetDescription": str,
    },
    total=False,
)

_RequiredClientGenerateDbAuthTokenRequestTypeDef = TypedDict(
    "_RequiredClientGenerateDbAuthTokenRequestTypeDef",
    {
        "DBHostname": str,
        "Port": int,
        "DBUsername": str,
    },
)
_OptionalClientGenerateDbAuthTokenRequestTypeDef = TypedDict(
    "_OptionalClientGenerateDbAuthTokenRequestTypeDef",
    {
        "Region": str,
    },
    total=False,
)


class ClientGenerateDbAuthTokenRequestTypeDef(
    _RequiredClientGenerateDbAuthTokenRequestTypeDef,
    _OptionalClientGenerateDbAuthTokenRequestTypeDef,
):
    pass


CloudwatchLogsExportConfigurationTypeDef = TypedDict(
    "CloudwatchLogsExportConfigurationTypeDef",
    {
        "EnableLogTypes": Sequence[str],
        "DisableLogTypes": Sequence[str],
    },
    total=False,
)

PendingCloudwatchLogsExportsTypeDef = TypedDict(
    "PendingCloudwatchLogsExportsTypeDef",
    {
        "LogTypesToEnable": List[str],
        "LogTypesToDisable": List[str],
    },
    total=False,
)

ConnectionPoolConfigurationInfoTypeDef = TypedDict(
    "ConnectionPoolConfigurationInfoTypeDef",
    {
        "MaxConnectionsPercent": int,
        "MaxIdleConnectionsPercent": int,
        "ConnectionBorrowTimeout": int,
        "SessionPinningFilters": List[str],
        "InitQuery": str,
    },
    total=False,
)

ConnectionPoolConfigurationTypeDef = TypedDict(
    "ConnectionPoolConfigurationTypeDef",
    {
        "MaxConnectionsPercent": int,
        "MaxIdleConnectionsPercent": int,
        "ConnectionBorrowTimeout": int,
        "SessionPinningFilters": Sequence[str],
        "InitQuery": str,
    },
    total=False,
)

DBClusterParameterGroupTypeDef = TypedDict(
    "DBClusterParameterGroupTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
        "DBClusterParameterGroupArn": str,
    },
    total=False,
)

DBParameterGroupTypeDef = TypedDict(
    "DBParameterGroupTypeDef",
    {
        "DBParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
        "DBParameterGroupArn": str,
    },
    total=False,
)

ScalingConfigurationTypeDef = TypedDict(
    "ScalingConfigurationTypeDef",
    {
        "MinCapacity": int,
        "MaxCapacity": int,
        "AutoPause": bool,
        "SecondsUntilAutoPause": int,
        "TimeoutAction": str,
        "SecondsBeforeTimeout": int,
    },
    total=False,
)

ServerlessV2ScalingConfigurationTypeDef = TypedDict(
    "ServerlessV2ScalingConfigurationTypeDef",
    {
        "MinCapacity": float,
        "MaxCapacity": float,
    },
    total=False,
)

ProcessorFeatureTypeDef = TypedDict(
    "ProcessorFeatureTypeDef",
    {
        "Name": str,
        "Value": str,
    },
    total=False,
)

DBProxyEndpointTypeDef = TypedDict(
    "DBProxyEndpointTypeDef",
    {
        "DBProxyEndpointName": str,
        "DBProxyEndpointArn": str,
        "DBProxyName": str,
        "Status": DBProxyEndpointStatusType,
        "VpcId": str,
        "VpcSecurityGroupIds": List[str],
        "VpcSubnetIds": List[str],
        "Endpoint": str,
        "CreatedDate": datetime,
        "TargetRole": DBProxyEndpointTargetRoleType,
        "IsDefault": bool,
    },
    total=False,
)

UserAuthConfigTypeDef = TypedDict(
    "UserAuthConfigTypeDef",
    {
        "Description": str,
        "UserName": str,
        "AuthScheme": Literal["SECRETS"],
        "SecretArn": str,
        "IAMAuth": IAMAuthModeType,
    },
    total=False,
)

CreateGlobalClusterMessageRequestTypeDef = TypedDict(
    "CreateGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "SourceDBClusterIdentifier": str,
        "Engine": str,
        "EngineVersion": str,
        "DeletionProtection": bool,
        "DatabaseName": str,
        "StorageEncrypted": bool,
    },
    total=False,
)

DBClusterBacktrackTypeDef = TypedDict(
    "DBClusterBacktrackTypeDef",
    {
        "DBClusterIdentifier": str,
        "BacktrackIdentifier": str,
        "BacktrackTo": datetime,
        "BacktrackedFrom": datetime,
        "BacktrackRequestCreationTime": datetime,
        "Status": str,
    },
    total=False,
)

DBClusterEndpointTypeDef = TypedDict(
    "DBClusterEndpointTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
        "DBClusterIdentifier": str,
        "DBClusterEndpointResourceIdentifier": str,
        "Endpoint": str,
        "Status": str,
        "EndpointType": str,
        "CustomEndpointType": str,
        "StaticMembers": List[str],
        "ExcludedMembers": List[str],
        "DBClusterEndpointArn": str,
    },
    total=False,
)

DBClusterMemberTypeDef = TypedDict(
    "DBClusterMemberTypeDef",
    {
        "DBInstanceIdentifier": str,
        "IsClusterWriter": bool,
        "DBClusterParameterGroupStatus": str,
        "PromotionTier": int,
    },
    total=False,
)

DBClusterOptionGroupStatusTypeDef = TypedDict(
    "DBClusterOptionGroupStatusTypeDef",
    {
        "DBClusterOptionGroupName": str,
        "Status": str,
    },
    total=False,
)

ParameterTypeDef = TypedDict(
    "ParameterTypeDef",
    {
        "ParameterName": str,
        "ParameterValue": str,
        "Description": str,
        "Source": str,
        "ApplyType": str,
        "DataType": str,
        "AllowedValues": str,
        "IsModifiable": bool,
        "MinimumEngineVersion": str,
        "ApplyMethod": ApplyMethodType,
        "SupportedEngineModes": List[str],
    },
    total=False,
)

DBClusterRoleTypeDef = TypedDict(
    "DBClusterRoleTypeDef",
    {
        "RoleArn": str,
        "Status": str,
        "FeatureName": str,
    },
    total=False,
)

DBClusterSnapshotAttributeTypeDef = TypedDict(
    "DBClusterSnapshotAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValues": List[str],
    },
    total=False,
)

DomainMembershipTypeDef = TypedDict(
    "DomainMembershipTypeDef",
    {
        "Domain": str,
        "Status": str,
        "FQDN": str,
        "IAMRoleName": str,
    },
    total=False,
)

ScalingConfigurationInfoTypeDef = TypedDict(
    "ScalingConfigurationInfoTypeDef",
    {
        "MinCapacity": int,
        "MaxCapacity": int,
        "AutoPause": bool,
        "SecondsUntilAutoPause": int,
        "TimeoutAction": str,
        "SecondsBeforeTimeout": int,
    },
    total=False,
)

ServerlessV2ScalingConfigurationInfoTypeDef = TypedDict(
    "ServerlessV2ScalingConfigurationInfoTypeDef",
    {
        "MinCapacity": float,
        "MaxCapacity": float,
    },
    total=False,
)

VpcSecurityGroupMembershipTypeDef = TypedDict(
    "VpcSecurityGroupMembershipTypeDef",
    {
        "VpcSecurityGroupId": str,
        "Status": str,
    },
    total=False,
)

TimezoneTypeDef = TypedDict(
    "TimezoneTypeDef",
    {
        "TimezoneName": str,
    },
    total=False,
)

UpgradeTargetTypeDef = TypedDict(
    "UpgradeTargetTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "Description": str,
        "AutoUpgrade": bool,
        "IsMajorVersionUpgrade": bool,
        "SupportedEngineModes": List[str],
        "SupportsParallelQuery": bool,
        "SupportsGlobalDatabases": bool,
        "SupportsBabelfish": bool,
    },
    total=False,
)

DBInstanceAutomatedBackupsReplicationTypeDef = TypedDict(
    "DBInstanceAutomatedBackupsReplicationTypeDef",
    {
        "DBInstanceAutomatedBackupsArn": str,
    },
    total=False,
)

RestoreWindowTypeDef = TypedDict(
    "RestoreWindowTypeDef",
    {
        "EarliestTime": datetime,
        "LatestTime": datetime,
    },
    total=False,
)

DBInstanceRoleTypeDef = TypedDict(
    "DBInstanceRoleTypeDef",
    {
        "RoleArn": str,
        "FeatureName": str,
        "Status": str,
    },
    total=False,
)

DBInstanceStatusInfoTypeDef = TypedDict(
    "DBInstanceStatusInfoTypeDef",
    {
        "StatusType": str,
        "Normal": bool,
        "Status": str,
        "Message": str,
    },
    total=False,
)

DBParameterGroupStatusTypeDef = TypedDict(
    "DBParameterGroupStatusTypeDef",
    {
        "DBParameterGroupName": str,
        "ParameterApplyStatus": str,
    },
    total=False,
)

DBSecurityGroupMembershipTypeDef = TypedDict(
    "DBSecurityGroupMembershipTypeDef",
    {
        "DBSecurityGroupName": str,
        "Status": str,
    },
    total=False,
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "Port": int,
        "HostedZoneId": str,
    },
    total=False,
)

OptionGroupMembershipTypeDef = TypedDict(
    "OptionGroupMembershipTypeDef",
    {
        "OptionGroupName": str,
        "Status": str,
    },
    total=False,
)

TargetHealthTypeDef = TypedDict(
    "TargetHealthTypeDef",
    {
        "State": TargetStateType,
        "Reason": TargetHealthReasonType,
        "Description": str,
    },
    total=False,
)

UserAuthConfigInfoTypeDef = TypedDict(
    "UserAuthConfigInfoTypeDef",
    {
        "Description": str,
        "UserName": str,
        "AuthScheme": Literal["SECRETS"],
        "SecretArn": str,
        "IAMAuth": IAMAuthModeType,
    },
    total=False,
)

EC2SecurityGroupTypeDef = TypedDict(
    "EC2SecurityGroupTypeDef",
    {
        "Status": str,
        "EC2SecurityGroupName": str,
        "EC2SecurityGroupId": str,
        "EC2SecurityGroupOwnerId": str,
    },
    total=False,
)

IPRangeTypeDef = TypedDict(
    "IPRangeTypeDef",
    {
        "Status": str,
        "CIDRIP": str,
    },
    total=False,
)

DBSnapshotAttributeTypeDef = TypedDict(
    "DBSnapshotAttributeTypeDef",
    {
        "AttributeName": str,
        "AttributeValues": List[str],
    },
    total=False,
)

DeleteCustomDBEngineVersionMessageRequestTypeDef = TypedDict(
    "DeleteCustomDBEngineVersionMessageRequestTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
    },
)

DeleteDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterEndpointMessageRequestTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
    },
)

_RequiredDeleteDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredDeleteDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalDeleteDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalDeleteDBClusterMessageRequestTypeDef",
    {
        "SkipFinalSnapshot": bool,
        "FinalDBSnapshotIdentifier": str,
    },
    total=False,
)


class DeleteDBClusterMessageRequestTypeDef(
    _RequiredDeleteDBClusterMessageRequestTypeDef, _OptionalDeleteDBClusterMessageRequestTypeDef
):
    pass


DeleteDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)

DeleteDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "DeleteDBClusterSnapshotMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
    },
)

DeleteDBInstanceAutomatedBackupMessageRequestTypeDef = TypedDict(
    "DeleteDBInstanceAutomatedBackupMessageRequestTypeDef",
    {
        "DbiResourceId": str,
        "DBInstanceAutomatedBackupsArn": str,
    },
    total=False,
)

_RequiredDeleteDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredDeleteDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalDeleteDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalDeleteDBInstanceMessageRequestTypeDef",
    {
        "SkipFinalSnapshot": bool,
        "FinalDBSnapshotIdentifier": str,
        "DeleteAutomatedBackups": bool,
    },
    total=False,
)


class DeleteDBInstanceMessageRequestTypeDef(
    _RequiredDeleteDBInstanceMessageRequestTypeDef, _OptionalDeleteDBInstanceMessageRequestTypeDef
):
    pass


DeleteDBParameterGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
    },
)

DeleteDBProxyEndpointRequestRequestTypeDef = TypedDict(
    "DeleteDBProxyEndpointRequestRequestTypeDef",
    {
        "DBProxyEndpointName": str,
    },
)

DeleteDBProxyRequestRequestTypeDef = TypedDict(
    "DeleteDBProxyRequestRequestTypeDef",
    {
        "DBProxyName": str,
    },
)

DeleteDBSecurityGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBSecurityGroupMessageRequestTypeDef",
    {
        "DBSecurityGroupName": str,
    },
)

DeleteDBSnapshotMessageRequestTypeDef = TypedDict(
    "DeleteDBSnapshotMessageRequestTypeDef",
    {
        "DBSnapshotIdentifier": str,
    },
)

DeleteDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "DeleteDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
    },
)

DeleteEventSubscriptionMessageRequestTypeDef = TypedDict(
    "DeleteEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)

DeleteGlobalClusterMessageRequestTypeDef = TypedDict(
    "DeleteGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
    },
)

DeleteOptionGroupMessageRequestTypeDef = TypedDict(
    "DeleteOptionGroupMessageRequestTypeDef",
    {
        "OptionGroupName": str,
    },
)

_RequiredDeregisterDBProxyTargetsRequestRequestTypeDef = TypedDict(
    "_RequiredDeregisterDBProxyTargetsRequestRequestTypeDef",
    {
        "DBProxyName": str,
    },
)
_OptionalDeregisterDBProxyTargetsRequestRequestTypeDef = TypedDict(
    "_OptionalDeregisterDBProxyTargetsRequestRequestTypeDef",
    {
        "TargetGroupName": str,
        "DBInstanceIdentifiers": Sequence[str],
        "DBClusterIdentifiers": Sequence[str],
    },
    total=False,
)


class DeregisterDBProxyTargetsRequestRequestTypeDef(
    _RequiredDeregisterDBProxyTargetsRequestRequestTypeDef,
    _OptionalDeregisterDBProxyTargetsRequestRequestTypeDef,
):
    pass


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": str,
        "Values": Sequence[str],
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

DescribeDBClusterSnapshotAttributesMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterSnapshotAttributesMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

DescribeDBLogFilesDetailsTypeDef = TypedDict(
    "DescribeDBLogFilesDetailsTypeDef",
    {
        "LogFileName": str,
        "LastWritten": int,
        "Size": int,
    },
    total=False,
)

DescribeDBSnapshotAttributesMessageRequestTypeDef = TypedDict(
    "DescribeDBSnapshotAttributesMessageRequestTypeDef",
    {
        "DBSnapshotIdentifier": str,
    },
)

DescribeValidDBInstanceModificationsMessageRequestTypeDef = TypedDict(
    "DescribeValidDBInstanceModificationsMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)

DoubleRangeTypeDef = TypedDict(
    "DoubleRangeTypeDef",
    {
        "From": float,
        "To": float,
    },
    total=False,
)

_RequiredDownloadDBLogFilePortionMessageRequestTypeDef = TypedDict(
    "_RequiredDownloadDBLogFilePortionMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "LogFileName": str,
    },
)
_OptionalDownloadDBLogFilePortionMessageRequestTypeDef = TypedDict(
    "_OptionalDownloadDBLogFilePortionMessageRequestTypeDef",
    {
        "Marker": str,
        "NumberOfLines": int,
    },
    total=False,
)


class DownloadDBLogFilePortionMessageRequestTypeDef(
    _RequiredDownloadDBLogFilePortionMessageRequestTypeDef,
    _OptionalDownloadDBLogFilePortionMessageRequestTypeDef,
):
    pass


EventCategoriesMapTypeDef = TypedDict(
    "EventCategoriesMapTypeDef",
    {
        "SourceType": str,
        "EventCategories": List[str],
    },
    total=False,
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "Message": str,
        "EventCategories": List[str],
        "Date": datetime,
        "SourceArn": str,
    },
    total=False,
)

ExportTaskTypeDef = TypedDict(
    "ExportTaskTypeDef",
    {
        "ExportTaskIdentifier": str,
        "SourceArn": str,
        "ExportOnly": List[str],
        "SnapshotTime": datetime,
        "TaskStartTime": datetime,
        "TaskEndTime": datetime,
        "S3Bucket": str,
        "S3Prefix": str,
        "IamRoleArn": str,
        "KmsKeyId": str,
        "Status": str,
        "PercentProgress": int,
        "TotalExtractedDataInGB": int,
        "FailureCause": str,
        "WarningMessage": str,
    },
    total=False,
)

_RequiredFailoverDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredFailoverDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalFailoverDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalFailoverDBClusterMessageRequestTypeDef",
    {
        "TargetDBInstanceIdentifier": str,
    },
    total=False,
)


class FailoverDBClusterMessageRequestTypeDef(
    _RequiredFailoverDBClusterMessageRequestTypeDef, _OptionalFailoverDBClusterMessageRequestTypeDef
):
    pass


FailoverGlobalClusterMessageRequestTypeDef = TypedDict(
    "FailoverGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "TargetDbClusterIdentifier": str,
    },
)

FailoverStateTypeDef = TypedDict(
    "FailoverStateTypeDef",
    {
        "Status": FailoverStatusType,
        "FromDbClusterArn": str,
        "ToDbClusterArn": str,
    },
    total=False,
)

GlobalClusterMemberTypeDef = TypedDict(
    "GlobalClusterMemberTypeDef",
    {
        "DBClusterArn": str,
        "Readers": List[str],
        "IsWriter": bool,
        "GlobalWriteForwardingStatus": WriteForwardingStatusType,
    },
    total=False,
)

MinimumEngineVersionPerAllowedValueTypeDef = TypedDict(
    "MinimumEngineVersionPerAllowedValueTypeDef",
    {
        "AllowedValue": str,
        "MinimumEngineVersion": str,
    },
    total=False,
)

ModifyCertificatesMessageRequestTypeDef = TypedDict(
    "ModifyCertificatesMessageRequestTypeDef",
    {
        "CertificateIdentifier": str,
        "RemoveCustomerOverride": bool,
    },
    total=False,
)

_RequiredModifyCurrentDBClusterCapacityMessageRequestTypeDef = TypedDict(
    "_RequiredModifyCurrentDBClusterCapacityMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalModifyCurrentDBClusterCapacityMessageRequestTypeDef = TypedDict(
    "_OptionalModifyCurrentDBClusterCapacityMessageRequestTypeDef",
    {
        "Capacity": int,
        "SecondsBeforeTimeout": int,
        "TimeoutAction": str,
    },
    total=False,
)


class ModifyCurrentDBClusterCapacityMessageRequestTypeDef(
    _RequiredModifyCurrentDBClusterCapacityMessageRequestTypeDef,
    _OptionalModifyCurrentDBClusterCapacityMessageRequestTypeDef,
):
    pass


_RequiredModifyCustomDBEngineVersionMessageRequestTypeDef = TypedDict(
    "_RequiredModifyCustomDBEngineVersionMessageRequestTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
    },
)
_OptionalModifyCustomDBEngineVersionMessageRequestTypeDef = TypedDict(
    "_OptionalModifyCustomDBEngineVersionMessageRequestTypeDef",
    {
        "Description": str,
        "Status": CustomEngineVersionStatusType,
    },
    total=False,
)


class ModifyCustomDBEngineVersionMessageRequestTypeDef(
    _RequiredModifyCustomDBEngineVersionMessageRequestTypeDef,
    _OptionalModifyCustomDBEngineVersionMessageRequestTypeDef,
):
    pass


_RequiredModifyDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterEndpointMessageRequestTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
    },
)
_OptionalModifyDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterEndpointMessageRequestTypeDef",
    {
        "EndpointType": str,
        "StaticMembers": Sequence[str],
        "ExcludedMembers": Sequence[str],
    },
    total=False,
)


class ModifyDBClusterEndpointMessageRequestTypeDef(
    _RequiredModifyDBClusterEndpointMessageRequestTypeDef,
    _OptionalModifyDBClusterEndpointMessageRequestTypeDef,
):
    pass


_RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "AttributeName": str,
    },
)
_OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef",
    {
        "ValuesToAdd": Sequence[str],
        "ValuesToRemove": Sequence[str],
    },
    total=False,
)


class ModifyDBClusterSnapshotAttributeMessageRequestTypeDef(
    _RequiredModifyDBClusterSnapshotAttributeMessageRequestTypeDef,
    _OptionalModifyDBClusterSnapshotAttributeMessageRequestTypeDef,
):
    pass


_RequiredModifyDBProxyEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredModifyDBProxyEndpointRequestRequestTypeDef",
    {
        "DBProxyEndpointName": str,
    },
)
_OptionalModifyDBProxyEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalModifyDBProxyEndpointRequestRequestTypeDef",
    {
        "NewDBProxyEndpointName": str,
        "VpcSecurityGroupIds": Sequence[str],
    },
    total=False,
)


class ModifyDBProxyEndpointRequestRequestTypeDef(
    _RequiredModifyDBProxyEndpointRequestRequestTypeDef,
    _OptionalModifyDBProxyEndpointRequestRequestTypeDef,
):
    pass


_RequiredModifyDBSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBSnapshotAttributeMessageRequestTypeDef",
    {
        "DBSnapshotIdentifier": str,
        "AttributeName": str,
    },
)
_OptionalModifyDBSnapshotAttributeMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBSnapshotAttributeMessageRequestTypeDef",
    {
        "ValuesToAdd": Sequence[str],
        "ValuesToRemove": Sequence[str],
    },
    total=False,
)


class ModifyDBSnapshotAttributeMessageRequestTypeDef(
    _RequiredModifyDBSnapshotAttributeMessageRequestTypeDef,
    _OptionalModifyDBSnapshotAttributeMessageRequestTypeDef,
):
    pass


_RequiredModifyDBSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBSnapshotMessageRequestTypeDef",
    {
        "DBSnapshotIdentifier": str,
    },
)
_OptionalModifyDBSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBSnapshotMessageRequestTypeDef",
    {
        "EngineVersion": str,
        "OptionGroupName": str,
    },
    total=False,
)


class ModifyDBSnapshotMessageRequestTypeDef(
    _RequiredModifyDBSnapshotMessageRequestTypeDef, _OptionalModifyDBSnapshotMessageRequestTypeDef
):
    pass


_RequiredModifyDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalModifyDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupDescription": str,
    },
    total=False,
)


class ModifyDBSubnetGroupMessageRequestTypeDef(
    _RequiredModifyDBSubnetGroupMessageRequestTypeDef,
    _OptionalModifyDBSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
    },
)
_OptionalModifyEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalModifyEventSubscriptionMessageRequestTypeDef",
    {
        "SnsTopicArn": str,
        "SourceType": str,
        "EventCategories": Sequence[str],
        "Enabled": bool,
    },
    total=False,
)


class ModifyEventSubscriptionMessageRequestTypeDef(
    _RequiredModifyEventSubscriptionMessageRequestTypeDef,
    _OptionalModifyEventSubscriptionMessageRequestTypeDef,
):
    pass


ModifyGlobalClusterMessageRequestTypeDef = TypedDict(
    "ModifyGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "NewGlobalClusterIdentifier": str,
        "DeletionProtection": bool,
        "EngineVersion": str,
        "AllowMajorVersionUpgrade": bool,
    },
    total=False,
)

OptionSettingTypeDef = TypedDict(
    "OptionSettingTypeDef",
    {
        "Name": str,
        "Value": str,
        "DefaultValue": str,
        "Description": str,
        "ApplyType": str,
        "DataType": str,
        "AllowedValues": str,
        "IsModifiable": bool,
        "IsCollection": bool,
    },
    total=False,
)

OptionVersionTypeDef = TypedDict(
    "OptionVersionTypeDef",
    {
        "Version": str,
        "IsDefault": bool,
    },
    total=False,
)

OutpostTypeDef = TypedDict(
    "OutpostTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

PendingMaintenanceActionTypeDef = TypedDict(
    "PendingMaintenanceActionTypeDef",
    {
        "Action": str,
        "AutoAppliedAfterDate": datetime,
        "ForcedApplyDate": datetime,
        "OptInStatus": str,
        "CurrentApplyDate": datetime,
        "Description": str,
    },
    total=False,
)

PromoteReadReplicaDBClusterMessageRequestTypeDef = TypedDict(
    "PromoteReadReplicaDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

_RequiredPromoteReadReplicaMessageRequestTypeDef = TypedDict(
    "_RequiredPromoteReadReplicaMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalPromoteReadReplicaMessageRequestTypeDef = TypedDict(
    "_OptionalPromoteReadReplicaMessageRequestTypeDef",
    {
        "BackupRetentionPeriod": int,
        "PreferredBackupWindow": str,
    },
    total=False,
)


class PromoteReadReplicaMessageRequestTypeDef(
    _RequiredPromoteReadReplicaMessageRequestTypeDef,
    _OptionalPromoteReadReplicaMessageRequestTypeDef,
):
    pass


RangeTypeDef = TypedDict(
    "RangeTypeDef",
    {
        "From": int,
        "To": int,
        "Step": int,
    },
    total=False,
)

RebootDBClusterMessageRequestTypeDef = TypedDict(
    "RebootDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

_RequiredRebootDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredRebootDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalRebootDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalRebootDBInstanceMessageRequestTypeDef",
    {
        "ForceFailover": bool,
    },
    total=False,
)


class RebootDBInstanceMessageRequestTypeDef(
    _RequiredRebootDBInstanceMessageRequestTypeDef, _OptionalRebootDBInstanceMessageRequestTypeDef
):
    pass


RecurringChargeTypeDef = TypedDict(
    "RecurringChargeTypeDef",
    {
        "RecurringChargeAmount": float,
        "RecurringChargeFrequency": str,
    },
    total=False,
)

_RequiredRegisterDBProxyTargetsRequestRequestTypeDef = TypedDict(
    "_RequiredRegisterDBProxyTargetsRequestRequestTypeDef",
    {
        "DBProxyName": str,
    },
)
_OptionalRegisterDBProxyTargetsRequestRequestTypeDef = TypedDict(
    "_OptionalRegisterDBProxyTargetsRequestRequestTypeDef",
    {
        "TargetGroupName": str,
        "DBInstanceIdentifiers": Sequence[str],
        "DBClusterIdentifiers": Sequence[str],
    },
    total=False,
)


class RegisterDBProxyTargetsRequestRequestTypeDef(
    _RequiredRegisterDBProxyTargetsRequestRequestTypeDef,
    _OptionalRegisterDBProxyTargetsRequestRequestTypeDef,
):
    pass


RemoveFromGlobalClusterMessageRequestTypeDef = TypedDict(
    "RemoveFromGlobalClusterMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "DbClusterIdentifier": str,
    },
    total=False,
)

_RequiredRemoveRoleFromDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredRemoveRoleFromDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "RoleArn": str,
    },
)
_OptionalRemoveRoleFromDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalRemoveRoleFromDBClusterMessageRequestTypeDef",
    {
        "FeatureName": str,
    },
    total=False,
)


class RemoveRoleFromDBClusterMessageRequestTypeDef(
    _RequiredRemoveRoleFromDBClusterMessageRequestTypeDef,
    _OptionalRemoveRoleFromDBClusterMessageRequestTypeDef,
):
    pass


RemoveRoleFromDBInstanceMessageRequestTypeDef = TypedDict(
    "RemoveRoleFromDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "RoleArn": str,
        "FeatureName": str,
    },
)

RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef = TypedDict(
    "RemoveSourceIdentifierFromSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SourceIdentifier": str,
    },
)

RemoveTagsFromResourceMessageRequestTypeDef = TypedDict(
    "RemoveTagsFromResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredRevokeDBSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_RequiredRevokeDBSecurityGroupIngressMessageRequestTypeDef",
    {
        "DBSecurityGroupName": str,
    },
)
_OptionalRevokeDBSecurityGroupIngressMessageRequestTypeDef = TypedDict(
    "_OptionalRevokeDBSecurityGroupIngressMessageRequestTypeDef",
    {
        "CIDRIP": str,
        "EC2SecurityGroupName": str,
        "EC2SecurityGroupId": str,
        "EC2SecurityGroupOwnerId": str,
    },
    total=False,
)


class RevokeDBSecurityGroupIngressMessageRequestTypeDef(
    _RequiredRevokeDBSecurityGroupIngressMessageRequestTypeDef,
    _OptionalRevokeDBSecurityGroupIngressMessageRequestTypeDef,
):
    pass


SourceRegionTypeDef = TypedDict(
    "SourceRegionTypeDef",
    {
        "RegionName": str,
        "Endpoint": str,
        "Status": str,
        "SupportsDBInstanceAutomatedBackupsReplication": bool,
    },
    total=False,
)

_RequiredStartActivityStreamRequestRequestTypeDef = TypedDict(
    "_RequiredStartActivityStreamRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Mode": ActivityStreamModeType,
        "KmsKeyId": str,
    },
)
_OptionalStartActivityStreamRequestRequestTypeDef = TypedDict(
    "_OptionalStartActivityStreamRequestRequestTypeDef",
    {
        "ApplyImmediately": bool,
        "EngineNativeAuditFieldsIncluded": bool,
    },
    total=False,
)


class StartActivityStreamRequestRequestTypeDef(
    _RequiredStartActivityStreamRequestRequestTypeDef,
    _OptionalStartActivityStreamRequestRequestTypeDef,
):
    pass


StartDBClusterMessageRequestTypeDef = TypedDict(
    "StartDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

_RequiredStartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef = TypedDict(
    "_RequiredStartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef",
    {
        "SourceDBInstanceArn": str,
    },
)
_OptionalStartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef = TypedDict(
    "_OptionalStartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef",
    {
        "BackupRetentionPeriod": int,
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "SourceRegion": str,
    },
    total=False,
)


class StartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef(
    _RequiredStartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef,
    _OptionalStartDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef,
):
    pass


StartDBInstanceMessageRequestTypeDef = TypedDict(
    "StartDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)

_RequiredStartExportTaskMessageRequestTypeDef = TypedDict(
    "_RequiredStartExportTaskMessageRequestTypeDef",
    {
        "ExportTaskIdentifier": str,
        "SourceArn": str,
        "S3BucketName": str,
        "IamRoleArn": str,
        "KmsKeyId": str,
    },
)
_OptionalStartExportTaskMessageRequestTypeDef = TypedDict(
    "_OptionalStartExportTaskMessageRequestTypeDef",
    {
        "S3Prefix": str,
        "ExportOnly": Sequence[str],
    },
    total=False,
)


class StartExportTaskMessageRequestTypeDef(
    _RequiredStartExportTaskMessageRequestTypeDef, _OptionalStartExportTaskMessageRequestTypeDef
):
    pass


_RequiredStopActivityStreamRequestRequestTypeDef = TypedDict(
    "_RequiredStopActivityStreamRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalStopActivityStreamRequestRequestTypeDef = TypedDict(
    "_OptionalStopActivityStreamRequestRequestTypeDef",
    {
        "ApplyImmediately": bool,
    },
    total=False,
)


class StopActivityStreamRequestRequestTypeDef(
    _RequiredStopActivityStreamRequestRequestTypeDef,
    _OptionalStopActivityStreamRequestRequestTypeDef,
):
    pass


StopDBClusterMessageRequestTypeDef = TypedDict(
    "StopDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)

StopDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef = TypedDict(
    "StopDBInstanceAutomatedBackupsReplicationMessageRequestTypeDef",
    {
        "SourceDBInstanceArn": str,
    },
)

_RequiredStopDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredStopDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalStopDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalStopDBInstanceMessageRequestTypeDef",
    {
        "DBSnapshotIdentifier": str,
    },
    total=False,
)


class StopDBInstanceMessageRequestTypeDef(
    _RequiredStopDBInstanceMessageRequestTypeDef, _OptionalStopDBInstanceMessageRequestTypeDef
):
    pass


AccountAttributesMessageTypeDef = TypedDict(
    "AccountAttributesMessageTypeDef",
    {
        "AccountQuotas": List[AccountQuotaTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterBacktrackResponseMetadataTypeDef = TypedDict(
    "DBClusterBacktrackResponseMetadataTypeDef",
    {
        "DBClusterIdentifier": str,
        "BacktrackIdentifier": str,
        "BacktrackTo": datetime,
        "BacktrackedFrom": datetime,
        "BacktrackRequestCreationTime": datetime,
        "Status": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterCapacityInfoTypeDef = TypedDict(
    "DBClusterCapacityInfoTypeDef",
    {
        "DBClusterIdentifier": str,
        "PendingCapacity": int,
        "CurrentCapacity": int,
        "SecondsBeforeTimeout": int,
        "TimeoutAction": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterEndpointResponseMetadataTypeDef = TypedDict(
    "DBClusterEndpointResponseMetadataTypeDef",
    {
        "DBClusterEndpointIdentifier": str,
        "DBClusterIdentifier": str,
        "DBClusterEndpointResourceIdentifier": str,
        "Endpoint": str,
        "Status": str,
        "EndpointType": str,
        "CustomEndpointType": str,
        "StaticMembers": List[str],
        "ExcludedMembers": List[str],
        "DBClusterEndpointArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupNameMessageTypeDef = TypedDict(
    "DBClusterParameterGroupNameMessageTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBParameterGroupNameMessageTypeDef = TypedDict(
    "DBParameterGroupNameMessageTypeDef",
    {
        "DBParameterGroupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DownloadDBLogFilePortionDetailsTypeDef = TypedDict(
    "DownloadDBLogFilePortionDetailsTypeDef",
    {
        "LogFileData": str,
        "Marker": str,
        "AdditionalDataPending": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportTaskResponseMetadataTypeDef = TypedDict(
    "ExportTaskResponseMetadataTypeDef",
    {
        "ExportTaskIdentifier": str,
        "SourceArn": str,
        "ExportOnly": List[str],
        "SnapshotTime": datetime,
        "TaskStartTime": datetime,
        "TaskEndTime": datetime,
        "S3Bucket": str,
        "S3Prefix": str,
        "IamRoleArn": str,
        "KmsKeyId": str,
        "Status": str,
        "PercentProgress": int,
        "TotalExtractedDataInGB": int,
        "FailureCause": str,
        "WarningMessage": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartActivityStreamResponseTypeDef = TypedDict(
    "StartActivityStreamResponseTypeDef",
    {
        "KmsKeyId": str,
        "KinesisStreamName": str,
        "Status": ActivityStreamStatusType,
        "Mode": ActivityStreamModeType,
        "ApplyImmediately": bool,
        "EngineNativeAuditFieldsIncluded": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopActivityStreamResponseTypeDef = TypedDict(
    "StopActivityStreamResponseTypeDef",
    {
        "KmsKeyId": str,
        "KinesisStreamName": str,
        "Status": ActivityStreamStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddSourceIdentifierToSubscriptionResultTypeDef = TypedDict(
    "AddSourceIdentifierToSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEventSubscriptionResultTypeDef = TypedDict(
    "CreateEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEventSubscriptionResultTypeDef = TypedDict(
    "DeleteEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventSubscriptionsMessageTypeDef = TypedDict(
    "EventSubscriptionsMessageTypeDef",
    {
        "Marker": str,
        "EventSubscriptionsList": List[EventSubscriptionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyEventSubscriptionResultTypeDef = TypedDict(
    "ModifyEventSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveSourceIdentifierFromSubscriptionResultTypeDef = TypedDict(
    "RemoveSourceIdentifierFromSubscriptionResultTypeDef",
    {
        "EventSubscription": EventSubscriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AddTagsToResourceMessageRequestTypeDef = TypedDict(
    "AddTagsToResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
        "Tags": Sequence[TagTypeDef],
    },
)

_RequiredCopyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "SourceDBClusterParameterGroupIdentifier": str,
        "TargetDBClusterParameterGroupIdentifier": str,
        "TargetDBClusterParameterGroupDescription": str,
    },
)
_OptionalCopyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredCopyDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalCopyDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCopyDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBClusterSnapshotMessageRequestTypeDef",
    {
        "SourceDBClusterSnapshotIdentifier": str,
        "TargetDBClusterSnapshotIdentifier": str,
    },
)
_OptionalCopyDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBClusterSnapshotMessageRequestTypeDef",
    {
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "CopyTags": bool,
        "Tags": Sequence[TagTypeDef],
        "SourceRegion": str,
    },
    total=False,
)


class CopyDBClusterSnapshotMessageRequestTypeDef(
    _RequiredCopyDBClusterSnapshotMessageRequestTypeDef,
    _OptionalCopyDBClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredCopyDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBParameterGroupMessageRequestTypeDef",
    {
        "SourceDBParameterGroupIdentifier": str,
        "TargetDBParameterGroupIdentifier": str,
        "TargetDBParameterGroupDescription": str,
    },
)
_OptionalCopyDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyDBParameterGroupMessageRequestTypeDef(
    _RequiredCopyDBParameterGroupMessageRequestTypeDef,
    _OptionalCopyDBParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCopyDBSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCopyDBSnapshotMessageRequestTypeDef",
    {
        "SourceDBSnapshotIdentifier": str,
        "TargetDBSnapshotIdentifier": str,
    },
)
_OptionalCopyDBSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCopyDBSnapshotMessageRequestTypeDef",
    {
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
        "CopyTags": bool,
        "PreSignedUrl": str,
        "OptionGroupName": str,
        "TargetCustomAvailabilityZone": str,
        "SourceRegion": str,
    },
    total=False,
)


class CopyDBSnapshotMessageRequestTypeDef(
    _RequiredCopyDBSnapshotMessageRequestTypeDef, _OptionalCopyDBSnapshotMessageRequestTypeDef
):
    pass


_RequiredCopyOptionGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCopyOptionGroupMessageRequestTypeDef",
    {
        "SourceOptionGroupIdentifier": str,
        "TargetOptionGroupIdentifier": str,
        "TargetOptionGroupDescription": str,
    },
)
_OptionalCopyOptionGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCopyOptionGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CopyOptionGroupMessageRequestTypeDef(
    _RequiredCopyOptionGroupMessageRequestTypeDef, _OptionalCopyOptionGroupMessageRequestTypeDef
):
    pass


_RequiredCreateCustomDBEngineVersionMessageRequestTypeDef = TypedDict(
    "_RequiredCreateCustomDBEngineVersionMessageRequestTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DatabaseInstallationFilesS3BucketName": str,
        "KMSKeyId": str,
        "Manifest": str,
    },
)
_OptionalCreateCustomDBEngineVersionMessageRequestTypeDef = TypedDict(
    "_OptionalCreateCustomDBEngineVersionMessageRequestTypeDef",
    {
        "DatabaseInstallationFilesS3Prefix": str,
        "Description": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateCustomDBEngineVersionMessageRequestTypeDef(
    _RequiredCreateCustomDBEngineVersionMessageRequestTypeDef,
    _OptionalCreateCustomDBEngineVersionMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterEndpointMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterEndpointIdentifier": str,
        "EndpointType": str,
    },
)
_OptionalCreateDBClusterEndpointMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterEndpointMessageRequestTypeDef",
    {
        "StaticMembers": Sequence[str],
        "ExcludedMembers": Sequence[str],
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterEndpointMessageRequestTypeDef(
    _RequiredCreateDBClusterEndpointMessageRequestTypeDef,
    _OptionalCreateDBClusterEndpointMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
    },
)
_OptionalCreateDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredCreateDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalCreateDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterSnapshotMessageRequestTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "DBClusterIdentifier": str,
    },
)
_OptionalCreateDBClusterSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterSnapshotMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBClusterSnapshotMessageRequestTypeDef(
    _RequiredCreateDBClusterSnapshotMessageRequestTypeDef,
    _OptionalCreateDBClusterSnapshotMessageRequestTypeDef,
):
    pass


_RequiredCreateDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
        "DBParameterGroupFamily": str,
        "Description": str,
    },
)
_OptionalCreateDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBParameterGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBParameterGroupMessageRequestTypeDef(
    _RequiredCreateDBParameterGroupMessageRequestTypeDef,
    _OptionalCreateDBParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateDBProxyEndpointRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDBProxyEndpointRequestRequestTypeDef",
    {
        "DBProxyName": str,
        "DBProxyEndpointName": str,
        "VpcSubnetIds": Sequence[str],
    },
)
_OptionalCreateDBProxyEndpointRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDBProxyEndpointRequestRequestTypeDef",
    {
        "VpcSecurityGroupIds": Sequence[str],
        "TargetRole": DBProxyEndpointTargetRoleType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBProxyEndpointRequestRequestTypeDef(
    _RequiredCreateDBProxyEndpointRequestRequestTypeDef,
    _OptionalCreateDBProxyEndpointRequestRequestTypeDef,
):
    pass


_RequiredCreateDBSecurityGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBSecurityGroupMessageRequestTypeDef",
    {
        "DBSecurityGroupName": str,
        "DBSecurityGroupDescription": str,
    },
)
_OptionalCreateDBSecurityGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBSecurityGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBSecurityGroupMessageRequestTypeDef(
    _RequiredCreateDBSecurityGroupMessageRequestTypeDef,
    _OptionalCreateDBSecurityGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateDBSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBSnapshotMessageRequestTypeDef",
    {
        "DBSnapshotIdentifier": str,
        "DBInstanceIdentifier": str,
    },
)
_OptionalCreateDBSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBSnapshotMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBSnapshotMessageRequestTypeDef(
    _RequiredCreateDBSnapshotMessageRequestTypeDef, _OptionalCreateDBSnapshotMessageRequestTypeDef
):
    pass


_RequiredCreateDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBSubnetGroupMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "DBSubnetGroupDescription": str,
        "SubnetIds": Sequence[str],
    },
)
_OptionalCreateDBSubnetGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBSubnetGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBSubnetGroupMessageRequestTypeDef(
    _RequiredCreateDBSubnetGroupMessageRequestTypeDef,
    _OptionalCreateDBSubnetGroupMessageRequestTypeDef,
):
    pass


_RequiredCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_RequiredCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "SnsTopicArn": str,
    },
)
_OptionalCreateEventSubscriptionMessageRequestTypeDef = TypedDict(
    "_OptionalCreateEventSubscriptionMessageRequestTypeDef",
    {
        "SourceType": str,
        "EventCategories": Sequence[str],
        "SourceIds": Sequence[str],
        "Enabled": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateEventSubscriptionMessageRequestTypeDef(
    _RequiredCreateEventSubscriptionMessageRequestTypeDef,
    _OptionalCreateEventSubscriptionMessageRequestTypeDef,
):
    pass


_RequiredCreateOptionGroupMessageRequestTypeDef = TypedDict(
    "_RequiredCreateOptionGroupMessageRequestTypeDef",
    {
        "OptionGroupName": str,
        "EngineName": str,
        "MajorEngineVersion": str,
        "OptionGroupDescription": str,
    },
)
_OptionalCreateOptionGroupMessageRequestTypeDef = TypedDict(
    "_OptionalCreateOptionGroupMessageRequestTypeDef",
    {
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateOptionGroupMessageRequestTypeDef(
    _RequiredCreateOptionGroupMessageRequestTypeDef, _OptionalCreateOptionGroupMessageRequestTypeDef
):
    pass


DBClusterSnapshotTypeDef = TypedDict(
    "DBClusterSnapshotTypeDef",
    {
        "AvailabilityZones": List[str],
        "DBClusterSnapshotIdentifier": str,
        "DBClusterIdentifier": str,
        "SnapshotCreateTime": datetime,
        "Engine": str,
        "EngineMode": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "VpcId": str,
        "ClusterCreateTime": datetime,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "PercentProgress": int,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DBClusterSnapshotArn": str,
        "SourceDBClusterSnapshotArn": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "TagList": List[TagTypeDef],
    },
    total=False,
)

_RequiredPurchaseReservedDBInstancesOfferingMessageRequestTypeDef = TypedDict(
    "_RequiredPurchaseReservedDBInstancesOfferingMessageRequestTypeDef",
    {
        "ReservedDBInstancesOfferingId": str,
    },
)
_OptionalPurchaseReservedDBInstancesOfferingMessageRequestTypeDef = TypedDict(
    "_OptionalPurchaseReservedDBInstancesOfferingMessageRequestTypeDef",
    {
        "ReservedDBInstanceId": str,
        "DBInstanceCount": int,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class PurchaseReservedDBInstancesOfferingMessageRequestTypeDef(
    _RequiredPurchaseReservedDBInstancesOfferingMessageRequestTypeDef,
    _OptionalPurchaseReservedDBInstancesOfferingMessageRequestTypeDef,
):
    pass


TagListMessageTypeDef = TypedDict(
    "TagListMessageTypeDef",
    {
        "TagList": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OrderableDBInstanceOptionTypeDef = TypedDict(
    "OrderableDBInstanceOptionTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "AvailabilityZoneGroup": str,
        "AvailabilityZones": List[AvailabilityZoneTypeDef],
        "MultiAZCapable": bool,
        "ReadReplicaCapable": bool,
        "Vpc": bool,
        "SupportsStorageEncryption": bool,
        "StorageType": str,
        "SupportsIops": bool,
        "SupportsEnhancedMonitoring": bool,
        "SupportsIAMDatabaseAuthentication": bool,
        "SupportsPerformanceInsights": bool,
        "MinStorageSize": int,
        "MaxStorageSize": int,
        "MinIopsPerDbInstance": int,
        "MaxIopsPerDbInstance": int,
        "MinIopsPerGib": float,
        "MaxIopsPerGib": float,
        "AvailableProcessorFeatures": List[AvailableProcessorFeatureTypeDef],
        "SupportedEngineModes": List[str],
        "SupportsStorageAutoscaling": bool,
        "SupportsKerberosAuthentication": bool,
        "OutpostCapable": bool,
        "SupportedActivityStreamModes": List[str],
        "SupportsGlobalDatabases": bool,
        "SupportsClusters": bool,
        "SupportedNetworkTypes": List[str],
    },
    total=False,
)

CertificateMessageTypeDef = TypedDict(
    "CertificateMessageTypeDef",
    {
        "Certificates": List[CertificateTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyCertificatesResultTypeDef = TypedDict(
    "ModifyCertificatesResultTypeDef",
    {
        "Certificate": CertificateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterPendingModifiedValuesTypeDef = TypedDict(
    "ClusterPendingModifiedValuesTypeDef",
    {
        "PendingCloudwatchLogsExports": PendingCloudwatchLogsExportsTypeDef,
        "DBClusterIdentifier": str,
        "MasterUserPassword": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "EngineVersion": str,
    },
    total=False,
)

DBProxyTargetGroupTypeDef = TypedDict(
    "DBProxyTargetGroupTypeDef",
    {
        "DBProxyName": str,
        "TargetGroupName": str,
        "TargetGroupArn": str,
        "IsDefault": bool,
        "Status": str,
        "ConnectionPoolConfig": ConnectionPoolConfigurationInfoTypeDef,
        "CreatedDate": datetime,
        "UpdatedDate": datetime,
    },
    total=False,
)

_RequiredModifyDBProxyTargetGroupRequestRequestTypeDef = TypedDict(
    "_RequiredModifyDBProxyTargetGroupRequestRequestTypeDef",
    {
        "TargetGroupName": str,
        "DBProxyName": str,
    },
)
_OptionalModifyDBProxyTargetGroupRequestRequestTypeDef = TypedDict(
    "_OptionalModifyDBProxyTargetGroupRequestRequestTypeDef",
    {
        "ConnectionPoolConfig": ConnectionPoolConfigurationTypeDef,
        "NewName": str,
    },
    total=False,
)


class ModifyDBProxyTargetGroupRequestRequestTypeDef(
    _RequiredModifyDBProxyTargetGroupRequestRequestTypeDef,
    _OptionalModifyDBProxyTargetGroupRequestRequestTypeDef,
):
    pass


CopyDBClusterParameterGroupResultTypeDef = TypedDict(
    "CopyDBClusterParameterGroupResultTypeDef",
    {
        "DBClusterParameterGroup": DBClusterParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterParameterGroupResultTypeDef = TypedDict(
    "CreateDBClusterParameterGroupResultTypeDef",
    {
        "DBClusterParameterGroup": DBClusterParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupsMessageTypeDef = TypedDict(
    "DBClusterParameterGroupsMessageTypeDef",
    {
        "Marker": str,
        "DBClusterParameterGroups": List[DBClusterParameterGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyDBParameterGroupResultTypeDef = TypedDict(
    "CopyDBParameterGroupResultTypeDef",
    {
        "DBParameterGroup": DBParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBParameterGroupResultTypeDef = TypedDict(
    "CreateDBParameterGroupResultTypeDef",
    {
        "DBParameterGroup": DBParameterGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBParameterGroupsMessageTypeDef = TypedDict(
    "DBParameterGroupsMessageTypeDef",
    {
        "Marker": str,
        "DBParameterGroups": List[DBParameterGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "Engine": str,
    },
)
_OptionalCreateDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBClusterMessageRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "BackupRetentionPeriod": int,
        "CharacterSetName": str,
        "DatabaseName": str,
        "DBClusterParameterGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "DBSubnetGroupName": str,
        "EngineVersion": str,
        "Port": int,
        "MasterUsername": str,
        "MasterUserPassword": str,
        "OptionGroupName": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReplicationSourceIdentifier": str,
        "Tags": Sequence[TagTypeDef],
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "EnableIAMDatabaseAuthentication": bool,
        "BacktrackWindow": int,
        "EnableCloudwatchLogsExports": Sequence[str],
        "EngineMode": str,
        "ScalingConfiguration": ScalingConfigurationTypeDef,
        "DeletionProtection": bool,
        "GlobalClusterIdentifier": str,
        "EnableHttpEndpoint": bool,
        "CopyTagsToSnapshot": bool,
        "Domain": str,
        "DomainIAMRoleName": str,
        "EnableGlobalWriteForwarding": bool,
        "DBClusterInstanceClass": str,
        "AllocatedStorage": int,
        "StorageType": str,
        "Iops": int,
        "PubliclyAccessible": bool,
        "AutoMinorVersionUpgrade": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "ServerlessV2ScalingConfiguration": ServerlessV2ScalingConfigurationTypeDef,
        "SourceRegion": str,
    },
    total=False,
)


class CreateDBClusterMessageRequestTypeDef(
    _RequiredCreateDBClusterMessageRequestTypeDef, _OptionalCreateDBClusterMessageRequestTypeDef
):
    pass


_RequiredModifyDBClusterMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBClusterMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalModifyDBClusterMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBClusterMessageRequestTypeDef",
    {
        "NewDBClusterIdentifier": str,
        "ApplyImmediately": bool,
        "BackupRetentionPeriod": int,
        "DBClusterParameterGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Port": int,
        "MasterUserPassword": str,
        "OptionGroupName": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "EnableIAMDatabaseAuthentication": bool,
        "BacktrackWindow": int,
        "CloudwatchLogsExportConfiguration": CloudwatchLogsExportConfigurationTypeDef,
        "EngineVersion": str,
        "AllowMajorVersionUpgrade": bool,
        "DBInstanceParameterGroupName": str,
        "Domain": str,
        "DomainIAMRoleName": str,
        "ScalingConfiguration": ScalingConfigurationTypeDef,
        "DeletionProtection": bool,
        "EnableHttpEndpoint": bool,
        "CopyTagsToSnapshot": bool,
        "EnableGlobalWriteForwarding": bool,
        "DBClusterInstanceClass": str,
        "AllocatedStorage": int,
        "StorageType": str,
        "Iops": int,
        "AutoMinorVersionUpgrade": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "ServerlessV2ScalingConfiguration": ServerlessV2ScalingConfigurationTypeDef,
    },
    total=False,
)


class ModifyDBClusterMessageRequestTypeDef(
    _RequiredModifyDBClusterMessageRequestTypeDef, _OptionalModifyDBClusterMessageRequestTypeDef
):
    pass


_RequiredRestoreDBClusterFromS3MessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBClusterFromS3MessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "Engine": str,
        "MasterUsername": str,
        "MasterUserPassword": str,
        "SourceEngine": str,
        "SourceEngineVersion": str,
        "S3BucketName": str,
        "S3IngestionRoleArn": str,
    },
)
_OptionalRestoreDBClusterFromS3MessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBClusterFromS3MessageRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "BackupRetentionPeriod": int,
        "CharacterSetName": str,
        "DatabaseName": str,
        "DBClusterParameterGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "DBSubnetGroupName": str,
        "EngineVersion": str,
        "Port": int,
        "OptionGroupName": str,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "Tags": Sequence[TagTypeDef],
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "EnableIAMDatabaseAuthentication": bool,
        "S3Prefix": str,
        "BacktrackWindow": int,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DeletionProtection": bool,
        "CopyTagsToSnapshot": bool,
        "Domain": str,
        "DomainIAMRoleName": str,
        "ServerlessV2ScalingConfiguration": ServerlessV2ScalingConfigurationTypeDef,
    },
    total=False,
)


class RestoreDBClusterFromS3MessageRequestTypeDef(
    _RequiredRestoreDBClusterFromS3MessageRequestTypeDef,
    _OptionalRestoreDBClusterFromS3MessageRequestTypeDef,
):
    pass


_RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "SnapshotIdentifier": str,
        "Engine": str,
    },
)
_OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef",
    {
        "AvailabilityZones": Sequence[str],
        "EngineVersion": str,
        "Port": int,
        "DBSubnetGroupName": str,
        "DatabaseName": str,
        "OptionGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "EnableIAMDatabaseAuthentication": bool,
        "BacktrackWindow": int,
        "EnableCloudwatchLogsExports": Sequence[str],
        "EngineMode": str,
        "ScalingConfiguration": ScalingConfigurationTypeDef,
        "DBClusterParameterGroupName": str,
        "DeletionProtection": bool,
        "CopyTagsToSnapshot": bool,
        "Domain": str,
        "DomainIAMRoleName": str,
        "DBClusterInstanceClass": str,
        "StorageType": str,
        "Iops": int,
        "PubliclyAccessible": bool,
        "ServerlessV2ScalingConfiguration": ServerlessV2ScalingConfigurationTypeDef,
    },
    total=False,
)


class RestoreDBClusterFromSnapshotMessageRequestTypeDef(
    _RequiredRestoreDBClusterFromSnapshotMessageRequestTypeDef,
    _OptionalRestoreDBClusterFromSnapshotMessageRequestTypeDef,
):
    pass


_RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "SourceDBClusterIdentifier": str,
    },
)
_OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef",
    {
        "RestoreType": str,
        "RestoreToTime": Union[datetime, str],
        "UseLatestRestorableTime": bool,
        "Port": int,
        "DBSubnetGroupName": str,
        "OptionGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Tags": Sequence[TagTypeDef],
        "KmsKeyId": str,
        "EnableIAMDatabaseAuthentication": bool,
        "BacktrackWindow": int,
        "EnableCloudwatchLogsExports": Sequence[str],
        "DBClusterParameterGroupName": str,
        "DeletionProtection": bool,
        "CopyTagsToSnapshot": bool,
        "Domain": str,
        "DomainIAMRoleName": str,
        "ScalingConfiguration": ScalingConfigurationTypeDef,
        "EngineMode": str,
        "DBClusterInstanceClass": str,
        "StorageType": str,
        "PubliclyAccessible": bool,
        "Iops": int,
        "ServerlessV2ScalingConfiguration": ServerlessV2ScalingConfigurationTypeDef,
    },
    total=False,
)


class RestoreDBClusterToPointInTimeMessageRequestTypeDef(
    _RequiredRestoreDBClusterToPointInTimeMessageRequestTypeDef,
    _OptionalRestoreDBClusterToPointInTimeMessageRequestTypeDef,
):
    pass


_RequiredCreateDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "Engine": str,
    },
)
_OptionalCreateDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBInstanceMessageRequestTypeDef",
    {
        "DBName": str,
        "AllocatedStorage": int,
        "MasterUsername": str,
        "MasterUserPassword": str,
        "DBSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "AvailabilityZone": str,
        "DBSubnetGroupName": str,
        "PreferredMaintenanceWindow": str,
        "DBParameterGroupName": str,
        "BackupRetentionPeriod": int,
        "PreferredBackupWindow": str,
        "Port": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupName": str,
        "CharacterSetName": str,
        "NcharCharacterSetName": str,
        "PubliclyAccessible": bool,
        "Tags": Sequence[TagTypeDef],
        "DBClusterIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "TdeCredentialPassword": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "Domain": str,
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "DomainIAMRoleName": str,
        "PromotionTier": int,
        "Timezone": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "EnableCloudwatchLogsExports": Sequence[str],
        "ProcessorFeatures": Sequence[ProcessorFeatureTypeDef],
        "DeletionProtection": bool,
        "MaxAllocatedStorage": int,
        "EnableCustomerOwnedIp": bool,
        "CustomIamInstanceProfile": str,
        "BackupTarget": str,
        "NetworkType": str,
    },
    total=False,
)


class CreateDBInstanceMessageRequestTypeDef(
    _RequiredCreateDBInstanceMessageRequestTypeDef, _OptionalCreateDBInstanceMessageRequestTypeDef
):
    pass


_RequiredCreateDBInstanceReadReplicaMessageRequestTypeDef = TypedDict(
    "_RequiredCreateDBInstanceReadReplicaMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "SourceDBInstanceIdentifier": str,
    },
)
_OptionalCreateDBInstanceReadReplicaMessageRequestTypeDef = TypedDict(
    "_OptionalCreateDBInstanceReadReplicaMessageRequestTypeDef",
    {
        "DBInstanceClass": str,
        "AvailabilityZone": str,
        "Port": int,
        "MultiAZ": bool,
        "AutoMinorVersionUpgrade": bool,
        "Iops": int,
        "OptionGroupName": str,
        "DBParameterGroupName": str,
        "PubliclyAccessible": bool,
        "Tags": Sequence[TagTypeDef],
        "DBSubnetGroupName": str,
        "VpcSecurityGroupIds": Sequence[str],
        "StorageType": str,
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "KmsKeyId": str,
        "PreSignedUrl": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "EnableCloudwatchLogsExports": Sequence[str],
        "ProcessorFeatures": Sequence[ProcessorFeatureTypeDef],
        "UseDefaultProcessorFeatures": bool,
        "DeletionProtection": bool,
        "Domain": str,
        "DomainIAMRoleName": str,
        "ReplicaMode": ReplicaModeType,
        "MaxAllocatedStorage": int,
        "CustomIamInstanceProfile": str,
        "NetworkType": str,
        "SourceRegion": str,
    },
    total=False,
)


class CreateDBInstanceReadReplicaMessageRequestTypeDef(
    _RequiredCreateDBInstanceReadReplicaMessageRequestTypeDef,
    _OptionalCreateDBInstanceReadReplicaMessageRequestTypeDef,
):
    pass


DBSnapshotTypeDef = TypedDict(
    "DBSnapshotTypeDef",
    {
        "DBSnapshotIdentifier": str,
        "DBInstanceIdentifier": str,
        "SnapshotCreateTime": datetime,
        "Engine": str,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "InstanceCreateTime": datetime,
        "MasterUsername": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "SnapshotType": str,
        "Iops": int,
        "OptionGroupName": str,
        "PercentProgress": int,
        "SourceRegion": str,
        "SourceDBSnapshotIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "Encrypted": bool,
        "KmsKeyId": str,
        "DBSnapshotArn": str,
        "Timezone": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "ProcessorFeatures": List[ProcessorFeatureTypeDef],
        "DbiResourceId": str,
        "TagList": List[TagTypeDef],
        "OriginalSnapshotCreateTime": datetime,
        "SnapshotTarget": str,
    },
    total=False,
)

_RequiredModifyDBInstanceMessageRequestTypeDef = TypedDict(
    "_RequiredModifyDBInstanceMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalModifyDBInstanceMessageRequestTypeDef = TypedDict(
    "_OptionalModifyDBInstanceMessageRequestTypeDef",
    {
        "AllocatedStorage": int,
        "DBInstanceClass": str,
        "DBSubnetGroupName": str,
        "DBSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "ApplyImmediately": bool,
        "MasterUserPassword": str,
        "DBParameterGroupName": str,
        "BackupRetentionPeriod": int,
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AllowMajorVersionUpgrade": bool,
        "AutoMinorVersionUpgrade": bool,
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupName": str,
        "NewDBInstanceIdentifier": str,
        "StorageType": str,
        "TdeCredentialArn": str,
        "TdeCredentialPassword": str,
        "CACertificateIdentifier": str,
        "Domain": str,
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "DBPortNumber": int,
        "PubliclyAccessible": bool,
        "MonitoringRoleArn": str,
        "DomainIAMRoleName": str,
        "PromotionTier": int,
        "EnableIAMDatabaseAuthentication": bool,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "CloudwatchLogsExportConfiguration": CloudwatchLogsExportConfigurationTypeDef,
        "ProcessorFeatures": Sequence[ProcessorFeatureTypeDef],
        "UseDefaultProcessorFeatures": bool,
        "DeletionProtection": bool,
        "MaxAllocatedStorage": int,
        "CertificateRotationRestart": bool,
        "ReplicaMode": ReplicaModeType,
        "EnableCustomerOwnedIp": bool,
        "AwsBackupRecoveryPointArn": str,
        "AutomationMode": AutomationModeType,
        "ResumeFullAutomationModeMinutes": int,
        "NetworkType": str,
    },
    total=False,
)


class ModifyDBInstanceMessageRequestTypeDef(
    _RequiredModifyDBInstanceMessageRequestTypeDef, _OptionalModifyDBInstanceMessageRequestTypeDef
):
    pass


PendingModifiedValuesTypeDef = TypedDict(
    "PendingModifiedValuesTypeDef",
    {
        "DBInstanceClass": str,
        "AllocatedStorage": int,
        "MasterUserPassword": str,
        "Port": int,
        "BackupRetentionPeriod": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "LicenseModel": str,
        "Iops": int,
        "DBInstanceIdentifier": str,
        "StorageType": str,
        "CACertificateIdentifier": str,
        "DBSubnetGroupName": str,
        "PendingCloudwatchLogsExports": PendingCloudwatchLogsExportsTypeDef,
        "ProcessorFeatures": List[ProcessorFeatureTypeDef],
        "IAMDatabaseAuthenticationEnabled": bool,
        "AutomationMode": AutomationModeType,
        "ResumeFullAutomationModeTime": datetime,
    },
    total=False,
)

_RequiredRestoreDBInstanceFromDBSnapshotMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBInstanceFromDBSnapshotMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBSnapshotIdentifier": str,
    },
)
_OptionalRestoreDBInstanceFromDBSnapshotMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBInstanceFromDBSnapshotMessageRequestTypeDef",
    {
        "DBInstanceClass": str,
        "Port": int,
        "AvailabilityZone": str,
        "DBSubnetGroupName": str,
        "MultiAZ": bool,
        "PubliclyAccessible": bool,
        "AutoMinorVersionUpgrade": bool,
        "LicenseModel": str,
        "DBName": str,
        "Engine": str,
        "Iops": int,
        "OptionGroupName": str,
        "Tags": Sequence[TagTypeDef],
        "StorageType": str,
        "TdeCredentialArn": str,
        "TdeCredentialPassword": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Domain": str,
        "CopyTagsToSnapshot": bool,
        "DomainIAMRoleName": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnableCloudwatchLogsExports": Sequence[str],
        "ProcessorFeatures": Sequence[ProcessorFeatureTypeDef],
        "UseDefaultProcessorFeatures": bool,
        "DBParameterGroupName": str,
        "DeletionProtection": bool,
        "EnableCustomerOwnedIp": bool,
        "CustomIamInstanceProfile": str,
        "BackupTarget": str,
        "NetworkType": str,
    },
    total=False,
)


class RestoreDBInstanceFromDBSnapshotMessageRequestTypeDef(
    _RequiredRestoreDBInstanceFromDBSnapshotMessageRequestTypeDef,
    _OptionalRestoreDBInstanceFromDBSnapshotMessageRequestTypeDef,
):
    pass


_RequiredRestoreDBInstanceFromS3MessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBInstanceFromS3MessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "Engine": str,
        "SourceEngine": str,
        "SourceEngineVersion": str,
        "S3BucketName": str,
        "S3IngestionRoleArn": str,
    },
)
_OptionalRestoreDBInstanceFromS3MessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBInstanceFromS3MessageRequestTypeDef",
    {
        "DBName": str,
        "AllocatedStorage": int,
        "MasterUsername": str,
        "MasterUserPassword": str,
        "DBSecurityGroups": Sequence[str],
        "VpcSecurityGroupIds": Sequence[str],
        "AvailabilityZone": str,
        "DBSubnetGroupName": str,
        "PreferredMaintenanceWindow": str,
        "DBParameterGroupName": str,
        "BackupRetentionPeriod": int,
        "PreferredBackupWindow": str,
        "Port": int,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupName": str,
        "PubliclyAccessible": bool,
        "Tags": Sequence[TagTypeDef],
        "StorageType": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "EnableIAMDatabaseAuthentication": bool,
        "S3Prefix": str,
        "EnablePerformanceInsights": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "EnableCloudwatchLogsExports": Sequence[str],
        "ProcessorFeatures": Sequence[ProcessorFeatureTypeDef],
        "UseDefaultProcessorFeatures": bool,
        "DeletionProtection": bool,
        "MaxAllocatedStorage": int,
        "NetworkType": str,
    },
    total=False,
)


class RestoreDBInstanceFromS3MessageRequestTypeDef(
    _RequiredRestoreDBInstanceFromS3MessageRequestTypeDef,
    _OptionalRestoreDBInstanceFromS3MessageRequestTypeDef,
):
    pass


_RequiredRestoreDBInstanceToPointInTimeMessageRequestTypeDef = TypedDict(
    "_RequiredRestoreDBInstanceToPointInTimeMessageRequestTypeDef",
    {
        "TargetDBInstanceIdentifier": str,
    },
)
_OptionalRestoreDBInstanceToPointInTimeMessageRequestTypeDef = TypedDict(
    "_OptionalRestoreDBInstanceToPointInTimeMessageRequestTypeDef",
    {
        "SourceDBInstanceIdentifier": str,
        "RestoreTime": Union[datetime, str],
        "UseLatestRestorableTime": bool,
        "DBInstanceClass": str,
        "Port": int,
        "AvailabilityZone": str,
        "DBSubnetGroupName": str,
        "MultiAZ": bool,
        "PubliclyAccessible": bool,
        "AutoMinorVersionUpgrade": bool,
        "LicenseModel": str,
        "DBName": str,
        "Engine": str,
        "Iops": int,
        "OptionGroupName": str,
        "CopyTagsToSnapshot": bool,
        "Tags": Sequence[TagTypeDef],
        "StorageType": str,
        "TdeCredentialArn": str,
        "TdeCredentialPassword": str,
        "VpcSecurityGroupIds": Sequence[str],
        "Domain": str,
        "DomainIAMRoleName": str,
        "EnableIAMDatabaseAuthentication": bool,
        "EnableCloudwatchLogsExports": Sequence[str],
        "ProcessorFeatures": Sequence[ProcessorFeatureTypeDef],
        "UseDefaultProcessorFeatures": bool,
        "DBParameterGroupName": str,
        "DeletionProtection": bool,
        "SourceDbiResourceId": str,
        "MaxAllocatedStorage": int,
        "SourceDBInstanceAutomatedBackupsArn": str,
        "EnableCustomerOwnedIp": bool,
        "CustomIamInstanceProfile": str,
        "BackupTarget": str,
        "NetworkType": str,
    },
    total=False,
)


class RestoreDBInstanceToPointInTimeMessageRequestTypeDef(
    _RequiredRestoreDBInstanceToPointInTimeMessageRequestTypeDef,
    _OptionalRestoreDBInstanceToPointInTimeMessageRequestTypeDef,
):
    pass


CreateDBProxyEndpointResponseTypeDef = TypedDict(
    "CreateDBProxyEndpointResponseTypeDef",
    {
        "DBProxyEndpoint": DBProxyEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBProxyEndpointResponseTypeDef = TypedDict(
    "DeleteDBProxyEndpointResponseTypeDef",
    {
        "DBProxyEndpoint": DBProxyEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDBProxyEndpointsResponseTypeDef = TypedDict(
    "DescribeDBProxyEndpointsResponseTypeDef",
    {
        "DBProxyEndpoints": List[DBProxyEndpointTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBProxyEndpointResponseTypeDef = TypedDict(
    "ModifyDBProxyEndpointResponseTypeDef",
    {
        "DBProxyEndpoint": DBProxyEndpointTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDBProxyRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDBProxyRequestRequestTypeDef",
    {
        "DBProxyName": str,
        "EngineFamily": EngineFamilyType,
        "Auth": Sequence[UserAuthConfigTypeDef],
        "RoleArn": str,
        "VpcSubnetIds": Sequence[str],
    },
)
_OptionalCreateDBProxyRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDBProxyRequestRequestTypeDef",
    {
        "VpcSecurityGroupIds": Sequence[str],
        "RequireTLS": bool,
        "IdleClientTimeout": int,
        "DebugLogging": bool,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateDBProxyRequestRequestTypeDef(
    _RequiredCreateDBProxyRequestRequestTypeDef, _OptionalCreateDBProxyRequestRequestTypeDef
):
    pass


_RequiredModifyDBProxyRequestRequestTypeDef = TypedDict(
    "_RequiredModifyDBProxyRequestRequestTypeDef",
    {
        "DBProxyName": str,
    },
)
_OptionalModifyDBProxyRequestRequestTypeDef = TypedDict(
    "_OptionalModifyDBProxyRequestRequestTypeDef",
    {
        "NewDBProxyName": str,
        "Auth": Sequence[UserAuthConfigTypeDef],
        "RequireTLS": bool,
        "IdleClientTimeout": int,
        "DebugLogging": bool,
        "RoleArn": str,
        "SecurityGroups": Sequence[str],
    },
    total=False,
)


class ModifyDBProxyRequestRequestTypeDef(
    _RequiredModifyDBProxyRequestRequestTypeDef, _OptionalModifyDBProxyRequestRequestTypeDef
):
    pass


DBClusterBacktrackMessageTypeDef = TypedDict(
    "DBClusterBacktrackMessageTypeDef",
    {
        "Marker": str,
        "DBClusterBacktracks": List[DBClusterBacktrackTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterEndpointMessageTypeDef = TypedDict(
    "DBClusterEndpointMessageTypeDef",
    {
        "Marker": str,
        "DBClusterEndpoints": List[DBClusterEndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterParameterGroupDetailsTypeDef = TypedDict(
    "DBClusterParameterGroupDetailsTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBParameterGroupDetailsTypeDef = TypedDict(
    "DBParameterGroupDetailsTypeDef",
    {
        "Parameters": List[ParameterTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EngineDefaultsTypeDef = TypedDict(
    "EngineDefaultsTypeDef",
    {
        "DBParameterGroupFamily": str,
        "Marker": str,
        "Parameters": List[ParameterTypeDef],
    },
    total=False,
)

ModifyDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "ModifyDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Parameters": Sequence[ParameterTypeDef],
    },
)

ModifyDBParameterGroupMessageRequestTypeDef = TypedDict(
    "ModifyDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
        "Parameters": Sequence[ParameterTypeDef],
    },
)

_RequiredResetDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredResetDBClusterParameterGroupMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalResetDBClusterParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalResetDBClusterParameterGroupMessageRequestTypeDef",
    {
        "ResetAllParameters": bool,
        "Parameters": Sequence[ParameterTypeDef],
    },
    total=False,
)


class ResetDBClusterParameterGroupMessageRequestTypeDef(
    _RequiredResetDBClusterParameterGroupMessageRequestTypeDef,
    _OptionalResetDBClusterParameterGroupMessageRequestTypeDef,
):
    pass


_RequiredResetDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_RequiredResetDBParameterGroupMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
    },
)
_OptionalResetDBParameterGroupMessageRequestTypeDef = TypedDict(
    "_OptionalResetDBParameterGroupMessageRequestTypeDef",
    {
        "ResetAllParameters": bool,
        "Parameters": Sequence[ParameterTypeDef],
    },
    total=False,
)


class ResetDBParameterGroupMessageRequestTypeDef(
    _RequiredResetDBParameterGroupMessageRequestTypeDef,
    _OptionalResetDBParameterGroupMessageRequestTypeDef,
):
    pass


DBClusterSnapshotAttributesResultTypeDef = TypedDict(
    "DBClusterSnapshotAttributesResultTypeDef",
    {
        "DBClusterSnapshotIdentifier": str,
        "DBClusterSnapshotAttributes": List[DBClusterSnapshotAttributeTypeDef],
    },
    total=False,
)

DBEngineVersionResponseMetadataTypeDef = TypedDict(
    "DBEngineVersionResponseMetadataTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "DBEngineDescription": str,
        "DBEngineVersionDescription": str,
        "DefaultCharacterSet": CharacterSetTypeDef,
        "SupportedCharacterSets": List[CharacterSetTypeDef],
        "SupportedNcharCharacterSets": List[CharacterSetTypeDef],
        "ValidUpgradeTarget": List[UpgradeTargetTypeDef],
        "SupportedTimezones": List[TimezoneTypeDef],
        "ExportableLogTypes": List[str],
        "SupportsLogExportsToCloudwatchLogs": bool,
        "SupportsReadReplica": bool,
        "SupportedEngineModes": List[str],
        "SupportedFeatureNames": List[str],
        "Status": str,
        "SupportsParallelQuery": bool,
        "SupportsGlobalDatabases": bool,
        "MajorEngineVersion": str,
        "DatabaseInstallationFilesS3BucketName": str,
        "DatabaseInstallationFilesS3Prefix": str,
        "DBEngineVersionArn": str,
        "KMSKeyId": str,
        "CreateTime": datetime,
        "TagList": List[TagTypeDef],
        "SupportsBabelfish": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBEngineVersionTypeDef = TypedDict(
    "DBEngineVersionTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "DBEngineDescription": str,
        "DBEngineVersionDescription": str,
        "DefaultCharacterSet": CharacterSetTypeDef,
        "SupportedCharacterSets": List[CharacterSetTypeDef],
        "SupportedNcharCharacterSets": List[CharacterSetTypeDef],
        "ValidUpgradeTarget": List[UpgradeTargetTypeDef],
        "SupportedTimezones": List[TimezoneTypeDef],
        "ExportableLogTypes": List[str],
        "SupportsLogExportsToCloudwatchLogs": bool,
        "SupportsReadReplica": bool,
        "SupportedEngineModes": List[str],
        "SupportedFeatureNames": List[str],
        "Status": str,
        "SupportsParallelQuery": bool,
        "SupportsGlobalDatabases": bool,
        "MajorEngineVersion": str,
        "DatabaseInstallationFilesS3BucketName": str,
        "DatabaseInstallationFilesS3Prefix": str,
        "DBEngineVersionArn": str,
        "KMSKeyId": str,
        "CreateTime": datetime,
        "TagList": List[TagTypeDef],
        "SupportsBabelfish": bool,
    },
    total=False,
)

DBInstanceAutomatedBackupTypeDef = TypedDict(
    "DBInstanceAutomatedBackupTypeDef",
    {
        "DBInstanceArn": str,
        "DbiResourceId": str,
        "Region": str,
        "DBInstanceIdentifier": str,
        "RestoreWindow": RestoreWindowTypeDef,
        "AllocatedStorage": int,
        "Status": str,
        "Port": int,
        "AvailabilityZone": str,
        "VpcId": str,
        "InstanceCreateTime": datetime,
        "MasterUsername": str,
        "Engine": str,
        "EngineVersion": str,
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupName": str,
        "TdeCredentialArn": str,
        "Encrypted": bool,
        "StorageType": str,
        "KmsKeyId": str,
        "Timezone": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "BackupRetentionPeriod": int,
        "DBInstanceAutomatedBackupsArn": str,
        "DBInstanceAutomatedBackupsReplications": List[
            DBInstanceAutomatedBackupsReplicationTypeDef
        ],
        "BackupTarget": str,
    },
    total=False,
)

DBProxyTargetTypeDef = TypedDict(
    "DBProxyTargetTypeDef",
    {
        "TargetArn": str,
        "Endpoint": str,
        "TrackedClusterId": str,
        "RdsResourceId": str,
        "Port": int,
        "Type": TargetTypeType,
        "Role": TargetRoleType,
        "TargetHealth": TargetHealthTypeDef,
    },
    total=False,
)

DBProxyTypeDef = TypedDict(
    "DBProxyTypeDef",
    {
        "DBProxyName": str,
        "DBProxyArn": str,
        "Status": DBProxyStatusType,
        "EngineFamily": str,
        "VpcId": str,
        "VpcSecurityGroupIds": List[str],
        "VpcSubnetIds": List[str],
        "Auth": List[UserAuthConfigInfoTypeDef],
        "RoleArn": str,
        "Endpoint": str,
        "RequireTLS": bool,
        "IdleClientTimeout": int,
        "DebugLogging": bool,
        "CreatedDate": datetime,
        "UpdatedDate": datetime,
    },
    total=False,
)

DBSecurityGroupTypeDef = TypedDict(
    "DBSecurityGroupTypeDef",
    {
        "OwnerId": str,
        "DBSecurityGroupName": str,
        "DBSecurityGroupDescription": str,
        "VpcId": str,
        "EC2SecurityGroups": List[EC2SecurityGroupTypeDef],
        "IPRanges": List[IPRangeTypeDef],
        "DBSecurityGroupArn": str,
    },
    total=False,
)

DBSnapshotAttributesResultTypeDef = TypedDict(
    "DBSnapshotAttributesResultTypeDef",
    {
        "DBSnapshotIdentifier": str,
        "DBSnapshotAttributes": List[DBSnapshotAttributeTypeDef],
    },
    total=False,
)

DescribeCertificatesMessageRequestTypeDef = TypedDict(
    "DescribeCertificatesMessageRequestTypeDef",
    {
        "CertificateIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDBClusterBacktracksMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDBClusterBacktracksMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalDescribeDBClusterBacktracksMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDBClusterBacktracksMessageRequestTypeDef",
    {
        "BacktrackIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDBClusterBacktracksMessageRequestTypeDef(
    _RequiredDescribeDBClusterBacktracksMessageRequestTypeDef,
    _OptionalDescribeDBClusterBacktracksMessageRequestTypeDef,
):
    pass


DescribeDBClusterEndpointsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterEndpointsMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterEndpointIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBClusterParameterGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterParameterGroupsMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDBClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDBClusterParametersMessageRequestTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalDescribeDBClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDBClusterParametersMessageRequestTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDBClusterParametersMessageRequestTypeDef(
    _RequiredDescribeDBClusterParametersMessageRequestTypeDef,
    _OptionalDescribeDBClusterParametersMessageRequestTypeDef,
):
    pass


DescribeDBClusterSnapshotsMessageRequestTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
    },
    total=False,
)

DescribeDBClustersMessageRequestTypeDef = TypedDict(
    "DescribeDBClustersMessageRequestTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
    },
    total=False,
)

DescribeDBEngineVersionsMessageRequestTypeDef = TypedDict(
    "DescribeDBEngineVersionsMessageRequestTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "DefaultOnly": bool,
        "ListSupportedCharacterSets": bool,
        "ListSupportedTimezones": bool,
        "IncludeAll": bool,
    },
    total=False,
)

DescribeDBInstanceAutomatedBackupsMessageRequestTypeDef = TypedDict(
    "DescribeDBInstanceAutomatedBackupsMessageRequestTypeDef",
    {
        "DbiResourceId": str,
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "DBInstanceAutomatedBackupsArn": str,
    },
    total=False,
)

DescribeDBInstancesMessageRequestTypeDef = TypedDict(
    "DescribeDBInstancesMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDBLogFilesMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDBLogFilesMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalDescribeDBLogFilesMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDBLogFilesMessageRequestTypeDef",
    {
        "FilenameContains": str,
        "FileLastWritten": int,
        "FileSize": int,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDBLogFilesMessageRequestTypeDef(
    _RequiredDescribeDBLogFilesMessageRequestTypeDef,
    _OptionalDescribeDBLogFilesMessageRequestTypeDef,
):
    pass


DescribeDBParameterGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBParameterGroupsMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeDBParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeDBParametersMessageRequestTypeDef",
    {
        "DBParameterGroupName": str,
    },
)
_OptionalDescribeDBParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeDBParametersMessageRequestTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeDBParametersMessageRequestTypeDef(
    _RequiredDescribeDBParametersMessageRequestTypeDef,
    _OptionalDescribeDBParametersMessageRequestTypeDef,
):
    pass


DescribeDBProxiesRequestRequestTypeDef = TypedDict(
    "DescribeDBProxiesRequestRequestTypeDef",
    {
        "DBProxyName": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribeDBProxyEndpointsRequestRequestTypeDef = TypedDict(
    "DescribeDBProxyEndpointsRequestRequestTypeDef",
    {
        "DBProxyName": str,
        "DBProxyEndpointName": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

_RequiredDescribeDBProxyTargetGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDBProxyTargetGroupsRequestRequestTypeDef",
    {
        "DBProxyName": str,
    },
)
_OptionalDescribeDBProxyTargetGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDBProxyTargetGroupsRequestRequestTypeDef",
    {
        "TargetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)


class DescribeDBProxyTargetGroupsRequestRequestTypeDef(
    _RequiredDescribeDBProxyTargetGroupsRequestRequestTypeDef,
    _OptionalDescribeDBProxyTargetGroupsRequestRequestTypeDef,
):
    pass


_RequiredDescribeDBProxyTargetsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeDBProxyTargetsRequestRequestTypeDef",
    {
        "DBProxyName": str,
    },
)
_OptionalDescribeDBProxyTargetsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeDBProxyTargetsRequestRequestTypeDef",
    {
        "TargetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)


class DescribeDBProxyTargetsRequestRequestTypeDef(
    _RequiredDescribeDBProxyTargetsRequestRequestTypeDef,
    _OptionalDescribeDBProxyTargetsRequestRequestTypeDef,
):
    pass


DescribeDBSecurityGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBSecurityGroupsMessageRequestTypeDef",
    {
        "DBSecurityGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeDBSnapshotsMessageRequestTypeDef = TypedDict(
    "DescribeDBSnapshotsMessageRequestTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
        "DbiResourceId": str,
    },
    total=False,
)

DescribeDBSubnetGroupsMessageRequestTypeDef = TypedDict(
    "DescribeDBSubnetGroupsMessageRequestTypeDef",
    {
        "DBSubnetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeEngineDefaultClusterParametersMessageRequestTypeDef(
    _RequiredDescribeEngineDefaultClusterParametersMessageRequestTypeDef,
    _OptionalDescribeEngineDefaultClusterParametersMessageRequestTypeDef,
):
    pass


_RequiredDescribeEngineDefaultParametersMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultParametersMessageRequestTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultParametersMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultParametersMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeEngineDefaultParametersMessageRequestTypeDef(
    _RequiredDescribeEngineDefaultParametersMessageRequestTypeDef,
    _OptionalDescribeEngineDefaultParametersMessageRequestTypeDef,
):
    pass


DescribeEventCategoriesMessageRequestTypeDef = TypedDict(
    "DescribeEventCategoriesMessageRequestTypeDef",
    {
        "SourceType": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

DescribeEventSubscriptionsMessageRequestTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeEventsMessageRequestTypeDef = TypedDict(
    "DescribeEventsMessageRequestTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeExportTasksMessageRequestTypeDef = TypedDict(
    "DescribeExportTasksMessageRequestTypeDef",
    {
        "ExportTaskIdentifier": str,
        "SourceArn": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribeGlobalClustersMessageRequestTypeDef = TypedDict(
    "DescribeGlobalClustersMessageRequestTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

_RequiredDescribeOptionGroupOptionsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeOptionGroupOptionsMessageRequestTypeDef",
    {
        "EngineName": str,
    },
)
_OptionalDescribeOptionGroupOptionsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeOptionGroupOptionsMessageRequestTypeDef",
    {
        "MajorEngineVersion": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeOptionGroupOptionsMessageRequestTypeDef(
    _RequiredDescribeOptionGroupOptionsMessageRequestTypeDef,
    _OptionalDescribeOptionGroupOptionsMessageRequestTypeDef,
):
    pass


DescribeOptionGroupsMessageRequestTypeDef = TypedDict(
    "DescribeOptionGroupsMessageRequestTypeDef",
    {
        "OptionGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
        "EngineName": str,
        "MajorEngineVersion": str,
    },
    total=False,
)

_RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef = TypedDict(
    "_RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    {
        "Engine": str,
    },
)
_OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef = TypedDict(
    "_OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef",
    {
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "AvailabilityZoneGroup": str,
        "Vpc": bool,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)


class DescribeOrderableDBInstanceOptionsMessageRequestTypeDef(
    _RequiredDescribeOrderableDBInstanceOptionsMessageRequestTypeDef,
    _OptionalDescribeOrderableDBInstanceOptionsMessageRequestTypeDef,
):
    pass


DescribePendingMaintenanceActionsMessageRequestTypeDef = TypedDict(
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    {
        "ResourceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "Marker": str,
        "MaxRecords": int,
    },
    total=False,
)

DescribeReservedDBInstancesMessageRequestTypeDef = TypedDict(
    "DescribeReservedDBInstancesMessageRequestTypeDef",
    {
        "ReservedDBInstanceId": str,
        "ReservedDBInstancesOfferingId": str,
        "DBInstanceClass": str,
        "Duration": str,
        "ProductDescription": str,
        "OfferingType": str,
        "MultiAZ": bool,
        "LeaseId": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeReservedDBInstancesOfferingsMessageRequestTypeDef = TypedDict(
    "DescribeReservedDBInstancesOfferingsMessageRequestTypeDef",
    {
        "ReservedDBInstancesOfferingId": str,
        "DBInstanceClass": str,
        "Duration": str,
        "ProductDescription": str,
        "OfferingType": str,
        "MultiAZ": bool,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
    },
    total=False,
)

DescribeSourceRegionsMessageRequestTypeDef = TypedDict(
    "DescribeSourceRegionsMessageRequestTypeDef",
    {
        "RegionName": str,
        "MaxRecords": int,
        "Marker": str,
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)

_RequiredListTagsForResourceMessageRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceMessageRequestTypeDef",
    {
        "ResourceName": str,
    },
)
_OptionalListTagsForResourceMessageRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceMessageRequestTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
    },
    total=False,
)


class ListTagsForResourceMessageRequestTypeDef(
    _RequiredListTagsForResourceMessageRequestTypeDef,
    _OptionalListTagsForResourceMessageRequestTypeDef,
):
    pass


DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef = TypedDict(
    "DescribeCertificatesMessageDescribeCertificatesPaginateTypeDef",
    {
        "CertificateIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
    },
)
_OptionalDescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef",
    {
        "BacktrackIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef(
    _RequiredDescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef,
    _OptionalDescribeDBClusterBacktracksMessageDescribeDBClusterBacktracksPaginateTypeDef,
):
    pass


DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef = TypedDict(
    "DescribeDBClusterEndpointsMessageDescribeDBClusterEndpointsPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterEndpointIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef = TypedDict(
    "DescribeDBClusterParameterGroupsMessageDescribeDBClusterParameterGroupsPaginateTypeDef",
    {
        "DBClusterParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    {
        "DBClusterParameterGroupName": str,
    },
)
_OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef(
    _RequiredDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
    _OptionalDescribeDBClusterParametersMessageDescribeDBClusterParametersPaginateTypeDef,
):
    pass


DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageDescribeDBClusterSnapshotsPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "IncludeShared": bool,
        "IncludePublic": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef = TypedDict(
    "DescribeDBClustersMessageDescribeDBClustersPaginateTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "IncludeShared": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef = TypedDict(
    "DescribeDBEngineVersionsMessageDescribeDBEngineVersionsPaginateTypeDef",
    {
        "Engine": str,
        "EngineVersion": str,
        "DBParameterGroupFamily": str,
        "Filters": Sequence[FilterTypeDef],
        "DefaultOnly": bool,
        "ListSupportedCharacterSets": bool,
        "ListSupportedTimezones": bool,
        "IncludeAll": bool,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBInstanceAutomatedBackupsMessageDescribeDBInstanceAutomatedBackupsPaginateTypeDef = TypedDict(
    "DescribeDBInstanceAutomatedBackupsMessageDescribeDBInstanceAutomatedBackupsPaginateTypeDef",
    {
        "DbiResourceId": str,
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "DBInstanceAutomatedBackupsArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef = TypedDict(
    "DescribeDBInstancesMessageDescribeDBInstancesPaginateTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef",
    {
        "DBInstanceIdentifier": str,
    },
)
_OptionalDescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef",
    {
        "FilenameContains": str,
        "FileLastWritten": int,
        "FileSize": int,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef(
    _RequiredDescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef,
    _OptionalDescribeDBLogFilesMessageDescribeDBLogFilesPaginateTypeDef,
):
    pass


DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef = TypedDict(
    "DescribeDBParameterGroupsMessageDescribeDBParameterGroupsPaginateTypeDef",
    {
        "DBParameterGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef",
    {
        "DBParameterGroupName": str,
    },
)
_OptionalDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef",
    {
        "Source": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBParametersMessageDescribeDBParametersPaginateTypeDef(
    _RequiredDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef,
    _OptionalDescribeDBParametersMessageDescribeDBParametersPaginateTypeDef,
):
    pass


DescribeDBProxiesRequestDescribeDBProxiesPaginateTypeDef = TypedDict(
    "DescribeDBProxiesRequestDescribeDBProxiesPaginateTypeDef",
    {
        "DBProxyName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBProxyEndpointsRequestDescribeDBProxyEndpointsPaginateTypeDef = TypedDict(
    "DescribeDBProxyEndpointsRequestDescribeDBProxyEndpointsPaginateTypeDef",
    {
        "DBProxyName": str,
        "DBProxyEndpointName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef",
    {
        "DBProxyName": str,
    },
)
_OptionalDescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef",
    {
        "TargetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef(
    _RequiredDescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef,
    _OptionalDescribeDBProxyTargetGroupsRequestDescribeDBProxyTargetGroupsPaginateTypeDef,
):
    pass


_RequiredDescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef = TypedDict(
    "_RequiredDescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef",
    {
        "DBProxyName": str,
    },
)
_OptionalDescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef = TypedDict(
    "_OptionalDescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef",
    {
        "TargetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef(
    _RequiredDescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef,
    _OptionalDescribeDBProxyTargetsRequestDescribeDBProxyTargetsPaginateTypeDef,
):
    pass


DescribeDBSecurityGroupsMessageDescribeDBSecurityGroupsPaginateTypeDef = TypedDict(
    "DescribeDBSecurityGroupsMessageDescribeDBSecurityGroupsPaginateTypeDef",
    {
        "DBSecurityGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBSnapshotsMessageDescribeDBSnapshotsPaginateTypeDef = TypedDict(
    "DescribeDBSnapshotsMessageDescribeDBSnapshotsPaginateTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "IncludeShared": bool,
        "IncludePublic": bool,
        "DbiResourceId": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef = TypedDict(
    "DescribeDBSubnetGroupsMessageDescribeDBSubnetGroupsPaginateTypeDef",
    {
        "DBSubnetGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef(
    _RequiredDescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef,
    _OptionalDescribeEngineDefaultClusterParametersMessageDescribeEngineDefaultClusterParametersPaginateTypeDef,
):
    pass


_RequiredDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef = TypedDict(
    "_RequiredDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef",
    {
        "DBParameterGroupFamily": str,
    },
)
_OptionalDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef = TypedDict(
    "_OptionalDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef",
    {
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef(
    _RequiredDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef,
    _OptionalDescribeEngineDefaultParametersMessageDescribeEngineDefaultParametersPaginateTypeDef,
):
    pass


DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef = TypedDict(
    "DescribeEventSubscriptionsMessageDescribeEventSubscriptionsPaginateTypeDef",
    {
        "SubscriptionName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeEventsMessageDescribeEventsPaginateTypeDef = TypedDict(
    "DescribeEventsMessageDescribeEventsPaginateTypeDef",
    {
        "SourceIdentifier": str,
        "SourceType": SourceTypeType,
        "StartTime": Union[datetime, str],
        "EndTime": Union[datetime, str],
        "Duration": int,
        "EventCategories": Sequence[str],
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeExportTasksMessageDescribeExportTasksPaginateTypeDef = TypedDict(
    "DescribeExportTasksMessageDescribeExportTasksPaginateTypeDef",
    {
        "ExportTaskIdentifier": str,
        "SourceArn": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef = TypedDict(
    "DescribeGlobalClustersMessageDescribeGlobalClustersPaginateTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef",
    {
        "EngineName": str,
    },
)
_OptionalDescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef",
    {
        "MajorEngineVersion": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef(
    _RequiredDescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef,
    _OptionalDescribeOptionGroupOptionsMessageDescribeOptionGroupOptionsPaginateTypeDef,
):
    pass


DescribeOptionGroupsMessageDescribeOptionGroupsPaginateTypeDef = TypedDict(
    "DescribeOptionGroupsMessageDescribeOptionGroupsPaginateTypeDef",
    {
        "OptionGroupName": str,
        "Filters": Sequence[FilterTypeDef],
        "EngineName": str,
        "MajorEngineVersion": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    {
        "Engine": str,
    },
)
_OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef",
    {
        "EngineVersion": str,
        "DBInstanceClass": str,
        "LicenseModel": str,
        "AvailabilityZoneGroup": str,
        "Vpc": bool,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef(
    _RequiredDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
    _OptionalDescribeOrderableDBInstanceOptionsMessageDescribeOrderableDBInstanceOptionsPaginateTypeDef,
):
    pass


DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef = (
    TypedDict(
        "DescribePendingMaintenanceActionsMessageDescribePendingMaintenanceActionsPaginateTypeDef",
        {
            "ResourceIdentifier": str,
            "Filters": Sequence[FilterTypeDef],
            "PaginationConfig": PaginatorConfigTypeDef,
        },
        total=False,
    )
)

DescribeReservedDBInstancesMessageDescribeReservedDBInstancesPaginateTypeDef = TypedDict(
    "DescribeReservedDBInstancesMessageDescribeReservedDBInstancesPaginateTypeDef",
    {
        "ReservedDBInstanceId": str,
        "ReservedDBInstancesOfferingId": str,
        "DBInstanceClass": str,
        "Duration": str,
        "ProductDescription": str,
        "OfferingType": str,
        "MultiAZ": bool,
        "LeaseId": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeReservedDBInstancesOfferingsMessageDescribeReservedDBInstancesOfferingsPaginateTypeDef = TypedDict(
    "DescribeReservedDBInstancesOfferingsMessageDescribeReservedDBInstancesOfferingsPaginateTypeDef",
    {
        "ReservedDBInstancesOfferingId": str,
        "DBInstanceClass": str,
        "Duration": str,
        "ProductDescription": str,
        "OfferingType": str,
        "MultiAZ": bool,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

DescribeSourceRegionsMessageDescribeSourceRegionsPaginateTypeDef = TypedDict(
    "DescribeSourceRegionsMessageDescribeSourceRegionsPaginateTypeDef",
    {
        "RegionName": str,
        "Filters": Sequence[FilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef = TypedDict(
    "_RequiredDownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef",
    {
        "DBInstanceIdentifier": str,
        "LogFileName": str,
    },
)
_OptionalDownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef = TypedDict(
    "_OptionalDownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef(
    _RequiredDownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef,
    _OptionalDownloadDBLogFilePortionMessageDownloadDBLogFilePortionPaginateTypeDef,
):
    pass


DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageDBClusterSnapshotAvailableWaitTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef = TypedDict(
    "DescribeDBClusterSnapshotsMessageDBClusterSnapshotDeletedWaitTypeDef",
    {
        "DBClusterIdentifier": str,
        "DBClusterSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBClustersMessageDBClusterAvailableWaitTypeDef = TypedDict(
    "DescribeDBClustersMessageDBClusterAvailableWaitTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBClustersMessageDBClusterDeletedWaitTypeDef = TypedDict(
    "DescribeDBClustersMessageDBClusterDeletedWaitTypeDef",
    {
        "DBClusterIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef = TypedDict(
    "DescribeDBInstancesMessageDBInstanceAvailableWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef = TypedDict(
    "DescribeDBInstancesMessageDBInstanceDeletedWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef = TypedDict(
    "DescribeDBSnapshotsMessageDBSnapshotAvailableWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
        "DbiResourceId": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef = TypedDict(
    "DescribeDBSnapshotsMessageDBSnapshotCompletedWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
        "DbiResourceId": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef = TypedDict(
    "DescribeDBSnapshotsMessageDBSnapshotDeletedWaitTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBSnapshotIdentifier": str,
        "SnapshotType": str,
        "Filters": Sequence[FilterTypeDef],
        "MaxRecords": int,
        "Marker": str,
        "IncludeShared": bool,
        "IncludePublic": bool,
        "DbiResourceId": str,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)

DescribeDBLogFilesResponseTypeDef = TypedDict(
    "DescribeDBLogFilesResponseTypeDef",
    {
        "DescribeDBLogFiles": List[DescribeDBLogFilesDetailsTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventCategoriesMessageTypeDef = TypedDict(
    "EventCategoriesMessageTypeDef",
    {
        "EventCategoriesMapList": List[EventCategoriesMapTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventsMessageTypeDef = TypedDict(
    "EventsMessageTypeDef",
    {
        "Marker": str,
        "Events": List[EventTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportTasksMessageTypeDef = TypedDict(
    "ExportTasksMessageTypeDef",
    {
        "Marker": str,
        "ExportTasks": List[ExportTaskTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GlobalClusterTypeDef = TypedDict(
    "GlobalClusterTypeDef",
    {
        "GlobalClusterIdentifier": str,
        "GlobalClusterResourceId": str,
        "GlobalClusterArn": str,
        "Status": str,
        "Engine": str,
        "EngineVersion": str,
        "DatabaseName": str,
        "StorageEncrypted": bool,
        "DeletionProtection": bool,
        "GlobalClusterMembers": List[GlobalClusterMemberTypeDef],
        "FailoverState": FailoverStateTypeDef,
    },
    total=False,
)

OptionGroupOptionSettingTypeDef = TypedDict(
    "OptionGroupOptionSettingTypeDef",
    {
        "SettingName": str,
        "SettingDescription": str,
        "DefaultValue": str,
        "ApplyType": str,
        "AllowedValues": str,
        "IsModifiable": bool,
        "IsRequired": bool,
        "MinimumEngineVersionPerAllowedValue": List[MinimumEngineVersionPerAllowedValueTypeDef],
    },
    total=False,
)

_RequiredOptionConfigurationTypeDef = TypedDict(
    "_RequiredOptionConfigurationTypeDef",
    {
        "OptionName": str,
    },
)
_OptionalOptionConfigurationTypeDef = TypedDict(
    "_OptionalOptionConfigurationTypeDef",
    {
        "Port": int,
        "OptionVersion": str,
        "DBSecurityGroupMemberships": Sequence[str],
        "VpcSecurityGroupMemberships": Sequence[str],
        "OptionSettings": Sequence[OptionSettingTypeDef],
    },
    total=False,
)


class OptionConfigurationTypeDef(
    _RequiredOptionConfigurationTypeDef, _OptionalOptionConfigurationTypeDef
):
    pass


OptionTypeDef = TypedDict(
    "OptionTypeDef",
    {
        "OptionName": str,
        "OptionDescription": str,
        "Persistent": bool,
        "Permanent": bool,
        "Port": int,
        "OptionVersion": str,
        "OptionSettings": List[OptionSettingTypeDef],
        "DBSecurityGroupMemberships": List[DBSecurityGroupMembershipTypeDef],
        "VpcSecurityGroupMemberships": List[VpcSecurityGroupMembershipTypeDef],
    },
    total=False,
)

SubnetTypeDef = TypedDict(
    "SubnetTypeDef",
    {
        "SubnetIdentifier": str,
        "SubnetAvailabilityZone": AvailabilityZoneTypeDef,
        "SubnetOutpost": OutpostTypeDef,
        "SubnetStatus": str,
    },
    total=False,
)

ResourcePendingMaintenanceActionsTypeDef = TypedDict(
    "ResourcePendingMaintenanceActionsTypeDef",
    {
        "ResourceIdentifier": str,
        "PendingMaintenanceActionDetails": List[PendingMaintenanceActionTypeDef],
    },
    total=False,
)

ValidStorageOptionsTypeDef = TypedDict(
    "ValidStorageOptionsTypeDef",
    {
        "StorageType": str,
        "StorageSize": List[RangeTypeDef],
        "ProvisionedIops": List[RangeTypeDef],
        "IopsToStorageRatio": List[DoubleRangeTypeDef],
        "SupportsStorageAutoscaling": bool,
    },
    total=False,
)

ReservedDBInstanceTypeDef = TypedDict(
    "ReservedDBInstanceTypeDef",
    {
        "ReservedDBInstanceId": str,
        "ReservedDBInstancesOfferingId": str,
        "DBInstanceClass": str,
        "StartTime": datetime,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "CurrencyCode": str,
        "DBInstanceCount": int,
        "ProductDescription": str,
        "OfferingType": str,
        "MultiAZ": bool,
        "State": str,
        "RecurringCharges": List[RecurringChargeTypeDef],
        "ReservedDBInstanceArn": str,
        "LeaseId": str,
    },
    total=False,
)

ReservedDBInstancesOfferingTypeDef = TypedDict(
    "ReservedDBInstancesOfferingTypeDef",
    {
        "ReservedDBInstancesOfferingId": str,
        "DBInstanceClass": str,
        "Duration": int,
        "FixedPrice": float,
        "UsagePrice": float,
        "CurrencyCode": str,
        "ProductDescription": str,
        "OfferingType": str,
        "MultiAZ": bool,
        "RecurringCharges": List[RecurringChargeTypeDef],
    },
    total=False,
)

SourceRegionMessageTypeDef = TypedDict(
    "SourceRegionMessageTypeDef",
    {
        "Marker": str,
        "SourceRegions": List[SourceRegionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyDBClusterSnapshotResultTypeDef = TypedDict(
    "CopyDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterSnapshotResultTypeDef = TypedDict(
    "CreateDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterSnapshotMessageTypeDef = TypedDict(
    "DBClusterSnapshotMessageTypeDef",
    {
        "Marker": str,
        "DBClusterSnapshots": List[DBClusterSnapshotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBClusterSnapshotResultTypeDef = TypedDict(
    "DeleteDBClusterSnapshotResultTypeDef",
    {
        "DBClusterSnapshot": DBClusterSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OrderableDBInstanceOptionsMessageTypeDef = TypedDict(
    "OrderableDBInstanceOptionsMessageTypeDef",
    {
        "OrderableDBInstanceOptions": List[OrderableDBInstanceOptionTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterTypeDef = TypedDict(
    "DBClusterTypeDef",
    {
        "AllocatedStorage": int,
        "AvailabilityZones": List[str],
        "BackupRetentionPeriod": int,
        "CharacterSetName": str,
        "DatabaseName": str,
        "DBClusterIdentifier": str,
        "DBClusterParameterGroup": str,
        "DBSubnetGroup": str,
        "Status": str,
        "AutomaticRestartTime": datetime,
        "PercentProgress": str,
        "EarliestRestorableTime": datetime,
        "Endpoint": str,
        "ReaderEndpoint": str,
        "CustomEndpoints": List[str],
        "MultiAZ": bool,
        "Engine": str,
        "EngineVersion": str,
        "LatestRestorableTime": datetime,
        "Port": int,
        "MasterUsername": str,
        "DBClusterOptionGroupMemberships": List[DBClusterOptionGroupStatusTypeDef],
        "PreferredBackupWindow": str,
        "PreferredMaintenanceWindow": str,
        "ReplicationSourceIdentifier": str,
        "ReadReplicaIdentifiers": List[str],
        "DBClusterMembers": List[DBClusterMemberTypeDef],
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "HostedZoneId": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbClusterResourceId": str,
        "DBClusterArn": str,
        "AssociatedRoles": List[DBClusterRoleTypeDef],
        "IAMDatabaseAuthenticationEnabled": bool,
        "CloneGroupId": str,
        "ClusterCreateTime": datetime,
        "EarliestBacktrackTime": datetime,
        "BacktrackWindow": int,
        "BacktrackConsumedChangeRecords": int,
        "EnabledCloudwatchLogsExports": List[str],
        "Capacity": int,
        "EngineMode": str,
        "ScalingConfigurationInfo": ScalingConfigurationInfoTypeDef,
        "DeletionProtection": bool,
        "HttpEndpointEnabled": bool,
        "ActivityStreamMode": ActivityStreamModeType,
        "ActivityStreamStatus": ActivityStreamStatusType,
        "ActivityStreamKmsKeyId": str,
        "ActivityStreamKinesisStreamName": str,
        "CopyTagsToSnapshot": bool,
        "CrossAccountClone": bool,
        "DomainMemberships": List[DomainMembershipTypeDef],
        "TagList": List[TagTypeDef],
        "GlobalWriteForwardingStatus": WriteForwardingStatusType,
        "GlobalWriteForwardingRequested": bool,
        "PendingModifiedValues": ClusterPendingModifiedValuesTypeDef,
        "DBClusterInstanceClass": str,
        "StorageType": str,
        "Iops": int,
        "PubliclyAccessible": bool,
        "AutoMinorVersionUpgrade": bool,
        "MonitoringInterval": int,
        "MonitoringRoleArn": str,
        "PerformanceInsightsEnabled": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "ServerlessV2ScalingConfiguration": ServerlessV2ScalingConfigurationInfoTypeDef,
    },
    total=False,
)

DescribeDBProxyTargetGroupsResponseTypeDef = TypedDict(
    "DescribeDBProxyTargetGroupsResponseTypeDef",
    {
        "TargetGroups": List[DBProxyTargetGroupTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBProxyTargetGroupResponseTypeDef = TypedDict(
    "ModifyDBProxyTargetGroupResponseTypeDef",
    {
        "DBProxyTargetGroup": DBProxyTargetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyDBSnapshotResultTypeDef = TypedDict(
    "CopyDBSnapshotResultTypeDef",
    {
        "DBSnapshot": DBSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBSnapshotResultTypeDef = TypedDict(
    "CreateDBSnapshotResultTypeDef",
    {
        "DBSnapshot": DBSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBSnapshotMessageTypeDef = TypedDict(
    "DBSnapshotMessageTypeDef",
    {
        "Marker": str,
        "DBSnapshots": List[DBSnapshotTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBSnapshotResultTypeDef = TypedDict(
    "DeleteDBSnapshotResultTypeDef",
    {
        "DBSnapshot": DBSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBSnapshotResultTypeDef = TypedDict(
    "ModifyDBSnapshotResultTypeDef",
    {
        "DBSnapshot": DBSnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEngineDefaultClusterParametersResultTypeDef = TypedDict(
    "DescribeEngineDefaultClusterParametersResultTypeDef",
    {
        "EngineDefaults": EngineDefaultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEngineDefaultParametersResultTypeDef = TypedDict(
    "DescribeEngineDefaultParametersResultTypeDef",
    {
        "EngineDefaults": EngineDefaultsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDBClusterSnapshotAttributesResultTypeDef = TypedDict(
    "DescribeDBClusterSnapshotAttributesResultTypeDef",
    {
        "DBClusterSnapshotAttributesResult": DBClusterSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBClusterSnapshotAttributeResultTypeDef = TypedDict(
    "ModifyDBClusterSnapshotAttributeResultTypeDef",
    {
        "DBClusterSnapshotAttributesResult": DBClusterSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBEngineVersionMessageTypeDef = TypedDict(
    "DBEngineVersionMessageTypeDef",
    {
        "Marker": str,
        "DBEngineVersions": List[DBEngineVersionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBInstanceAutomatedBackupMessageTypeDef = TypedDict(
    "DBInstanceAutomatedBackupMessageTypeDef",
    {
        "Marker": str,
        "DBInstanceAutomatedBackups": List[DBInstanceAutomatedBackupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBInstanceAutomatedBackupResultTypeDef = TypedDict(
    "DeleteDBInstanceAutomatedBackupResultTypeDef",
    {
        "DBInstanceAutomatedBackup": DBInstanceAutomatedBackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDBInstanceAutomatedBackupsReplicationResultTypeDef = TypedDict(
    "StartDBInstanceAutomatedBackupsReplicationResultTypeDef",
    {
        "DBInstanceAutomatedBackup": DBInstanceAutomatedBackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDBInstanceAutomatedBackupsReplicationResultTypeDef = TypedDict(
    "StopDBInstanceAutomatedBackupsReplicationResultTypeDef",
    {
        "DBInstanceAutomatedBackup": DBInstanceAutomatedBackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDBProxyTargetsResponseTypeDef = TypedDict(
    "DescribeDBProxyTargetsResponseTypeDef",
    {
        "Targets": List[DBProxyTargetTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterDBProxyTargetsResponseTypeDef = TypedDict(
    "RegisterDBProxyTargetsResponseTypeDef",
    {
        "DBProxyTargets": List[DBProxyTargetTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBProxyResponseTypeDef = TypedDict(
    "CreateDBProxyResponseTypeDef",
    {
        "DBProxy": DBProxyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBProxyResponseTypeDef = TypedDict(
    "DeleteDBProxyResponseTypeDef",
    {
        "DBProxy": DBProxyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDBProxiesResponseTypeDef = TypedDict(
    "DescribeDBProxiesResponseTypeDef",
    {
        "DBProxies": List[DBProxyTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBProxyResponseTypeDef = TypedDict(
    "ModifyDBProxyResponseTypeDef",
    {
        "DBProxy": DBProxyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AuthorizeDBSecurityGroupIngressResultTypeDef = TypedDict(
    "AuthorizeDBSecurityGroupIngressResultTypeDef",
    {
        "DBSecurityGroup": DBSecurityGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBSecurityGroupResultTypeDef = TypedDict(
    "CreateDBSecurityGroupResultTypeDef",
    {
        "DBSecurityGroup": DBSecurityGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBSecurityGroupMessageTypeDef = TypedDict(
    "DBSecurityGroupMessageTypeDef",
    {
        "Marker": str,
        "DBSecurityGroups": List[DBSecurityGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RevokeDBSecurityGroupIngressResultTypeDef = TypedDict(
    "RevokeDBSecurityGroupIngressResultTypeDef",
    {
        "DBSecurityGroup": DBSecurityGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDBSnapshotAttributesResultTypeDef = TypedDict(
    "DescribeDBSnapshotAttributesResultTypeDef",
    {
        "DBSnapshotAttributesResult": DBSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBSnapshotAttributeResultTypeDef = TypedDict(
    "ModifyDBSnapshotAttributeResultTypeDef",
    {
        "DBSnapshotAttributesResult": DBSnapshotAttributesResultTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGlobalClusterResultTypeDef = TypedDict(
    "CreateGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteGlobalClusterResultTypeDef = TypedDict(
    "DeleteGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FailoverGlobalClusterResultTypeDef = TypedDict(
    "FailoverGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GlobalClustersMessageTypeDef = TypedDict(
    "GlobalClustersMessageTypeDef",
    {
        "Marker": str,
        "GlobalClusters": List[GlobalClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyGlobalClusterResultTypeDef = TypedDict(
    "ModifyGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RemoveFromGlobalClusterResultTypeDef = TypedDict(
    "RemoveFromGlobalClusterResultTypeDef",
    {
        "GlobalCluster": GlobalClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OptionGroupOptionTypeDef = TypedDict(
    "OptionGroupOptionTypeDef",
    {
        "Name": str,
        "Description": str,
        "EngineName": str,
        "MajorEngineVersion": str,
        "MinimumRequiredMinorEngineVersion": str,
        "PortRequired": bool,
        "DefaultPort": int,
        "OptionsDependedOn": List[str],
        "OptionsConflictsWith": List[str],
        "Persistent": bool,
        "Permanent": bool,
        "RequiresAutoMinorEngineVersionUpgrade": bool,
        "VpcOnly": bool,
        "SupportsOptionVersionDowngrade": bool,
        "OptionGroupOptionSettings": List[OptionGroupOptionSettingTypeDef],
        "OptionGroupOptionVersions": List[OptionVersionTypeDef],
    },
    total=False,
)

_RequiredModifyOptionGroupMessageRequestTypeDef = TypedDict(
    "_RequiredModifyOptionGroupMessageRequestTypeDef",
    {
        "OptionGroupName": str,
    },
)
_OptionalModifyOptionGroupMessageRequestTypeDef = TypedDict(
    "_OptionalModifyOptionGroupMessageRequestTypeDef",
    {
        "OptionsToInclude": Sequence[OptionConfigurationTypeDef],
        "OptionsToRemove": Sequence[str],
        "ApplyImmediately": bool,
    },
    total=False,
)


class ModifyOptionGroupMessageRequestTypeDef(
    _RequiredModifyOptionGroupMessageRequestTypeDef, _OptionalModifyOptionGroupMessageRequestTypeDef
):
    pass


OptionGroupTypeDef = TypedDict(
    "OptionGroupTypeDef",
    {
        "OptionGroupName": str,
        "OptionGroupDescription": str,
        "EngineName": str,
        "MajorEngineVersion": str,
        "Options": List[OptionTypeDef],
        "AllowsVpcAndNonVpcInstanceMemberships": bool,
        "VpcId": str,
        "OptionGroupArn": str,
    },
    total=False,
)

DBSubnetGroupTypeDef = TypedDict(
    "DBSubnetGroupTypeDef",
    {
        "DBSubnetGroupName": str,
        "DBSubnetGroupDescription": str,
        "VpcId": str,
        "SubnetGroupStatus": str,
        "Subnets": List[SubnetTypeDef],
        "DBSubnetGroupArn": str,
        "SupportedNetworkTypes": List[str],
    },
    total=False,
)

ApplyPendingMaintenanceActionResultTypeDef = TypedDict(
    "ApplyPendingMaintenanceActionResultTypeDef",
    {
        "ResourcePendingMaintenanceActions": ResourcePendingMaintenanceActionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PendingMaintenanceActionsMessageTypeDef = TypedDict(
    "PendingMaintenanceActionsMessageTypeDef",
    {
        "PendingMaintenanceActions": List[ResourcePendingMaintenanceActionsTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ValidDBInstanceModificationsMessageTypeDef = TypedDict(
    "ValidDBInstanceModificationsMessageTypeDef",
    {
        "Storage": List[ValidStorageOptionsTypeDef],
        "ValidProcessorFeatures": List[AvailableProcessorFeatureTypeDef],
    },
    total=False,
)

PurchaseReservedDBInstancesOfferingResultTypeDef = TypedDict(
    "PurchaseReservedDBInstancesOfferingResultTypeDef",
    {
        "ReservedDBInstance": ReservedDBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReservedDBInstanceMessageTypeDef = TypedDict(
    "ReservedDBInstanceMessageTypeDef",
    {
        "Marker": str,
        "ReservedDBInstances": List[ReservedDBInstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReservedDBInstancesOfferingMessageTypeDef = TypedDict(
    "ReservedDBInstancesOfferingMessageTypeDef",
    {
        "Marker": str,
        "ReservedDBInstancesOfferings": List[ReservedDBInstancesOfferingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBClusterResultTypeDef = TypedDict(
    "CreateDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBClusterMessageTypeDef = TypedDict(
    "DBClusterMessageTypeDef",
    {
        "Marker": str,
        "DBClusters": List[DBClusterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBClusterResultTypeDef = TypedDict(
    "DeleteDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FailoverDBClusterResultTypeDef = TypedDict(
    "FailoverDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBClusterResultTypeDef = TypedDict(
    "ModifyDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PromoteReadReplicaDBClusterResultTypeDef = TypedDict(
    "PromoteReadReplicaDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootDBClusterResultTypeDef = TypedDict(
    "RebootDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBClusterFromS3ResultTypeDef = TypedDict(
    "RestoreDBClusterFromS3ResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBClusterFromSnapshotResultTypeDef = TypedDict(
    "RestoreDBClusterFromSnapshotResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBClusterToPointInTimeResultTypeDef = TypedDict(
    "RestoreDBClusterToPointInTimeResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDBClusterResultTypeDef = TypedDict(
    "StartDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDBClusterResultTypeDef = TypedDict(
    "StopDBClusterResultTypeDef",
    {
        "DBCluster": DBClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OptionGroupOptionsMessageTypeDef = TypedDict(
    "OptionGroupOptionsMessageTypeDef",
    {
        "OptionGroupOptions": List[OptionGroupOptionTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyOptionGroupResultTypeDef = TypedDict(
    "CopyOptionGroupResultTypeDef",
    {
        "OptionGroup": OptionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOptionGroupResultTypeDef = TypedDict(
    "CreateOptionGroupResultTypeDef",
    {
        "OptionGroup": OptionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyOptionGroupResultTypeDef = TypedDict(
    "ModifyOptionGroupResultTypeDef",
    {
        "OptionGroup": OptionGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

OptionGroupsTypeDef = TypedDict(
    "OptionGroupsTypeDef",
    {
        "OptionGroupsList": List[OptionGroupTypeDef],
        "Marker": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBSubnetGroupResultTypeDef = TypedDict(
    "CreateDBSubnetGroupResultTypeDef",
    {
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBInstanceTypeDef = TypedDict(
    "DBInstanceTypeDef",
    {
        "DBInstanceIdentifier": str,
        "DBInstanceClass": str,
        "Engine": str,
        "DBInstanceStatus": str,
        "AutomaticRestartTime": datetime,
        "MasterUsername": str,
        "DBName": str,
        "Endpoint": EndpointTypeDef,
        "AllocatedStorage": int,
        "InstanceCreateTime": datetime,
        "PreferredBackupWindow": str,
        "BackupRetentionPeriod": int,
        "DBSecurityGroups": List[DBSecurityGroupMembershipTypeDef],
        "VpcSecurityGroups": List[VpcSecurityGroupMembershipTypeDef],
        "DBParameterGroups": List[DBParameterGroupStatusTypeDef],
        "AvailabilityZone": str,
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "PreferredMaintenanceWindow": str,
        "PendingModifiedValues": PendingModifiedValuesTypeDef,
        "LatestRestorableTime": datetime,
        "MultiAZ": bool,
        "EngineVersion": str,
        "AutoMinorVersionUpgrade": bool,
        "ReadReplicaSourceDBInstanceIdentifier": str,
        "ReadReplicaDBInstanceIdentifiers": List[str],
        "ReadReplicaDBClusterIdentifiers": List[str],
        "ReplicaMode": ReplicaModeType,
        "LicenseModel": str,
        "Iops": int,
        "OptionGroupMemberships": List[OptionGroupMembershipTypeDef],
        "CharacterSetName": str,
        "NcharCharacterSetName": str,
        "SecondaryAvailabilityZone": str,
        "PubliclyAccessible": bool,
        "StatusInfos": List[DBInstanceStatusInfoTypeDef],
        "StorageType": str,
        "TdeCredentialArn": str,
        "DbInstancePort": int,
        "DBClusterIdentifier": str,
        "StorageEncrypted": bool,
        "KmsKeyId": str,
        "DbiResourceId": str,
        "CACertificateIdentifier": str,
        "DomainMemberships": List[DomainMembershipTypeDef],
        "CopyTagsToSnapshot": bool,
        "MonitoringInterval": int,
        "EnhancedMonitoringResourceArn": str,
        "MonitoringRoleArn": str,
        "PromotionTier": int,
        "DBInstanceArn": str,
        "Timezone": str,
        "IAMDatabaseAuthenticationEnabled": bool,
        "PerformanceInsightsEnabled": bool,
        "PerformanceInsightsKMSKeyId": str,
        "PerformanceInsightsRetentionPeriod": int,
        "EnabledCloudwatchLogsExports": List[str],
        "ProcessorFeatures": List[ProcessorFeatureTypeDef],
        "DeletionProtection": bool,
        "AssociatedRoles": List[DBInstanceRoleTypeDef],
        "ListenerEndpoint": EndpointTypeDef,
        "MaxAllocatedStorage": int,
        "TagList": List[TagTypeDef],
        "DBInstanceAutomatedBackupsReplications": List[
            DBInstanceAutomatedBackupsReplicationTypeDef
        ],
        "CustomerOwnedIpEnabled": bool,
        "AwsBackupRecoveryPointArn": str,
        "ActivityStreamStatus": ActivityStreamStatusType,
        "ActivityStreamKmsKeyId": str,
        "ActivityStreamKinesisStreamName": str,
        "ActivityStreamMode": ActivityStreamModeType,
        "ActivityStreamEngineNativeAuditFieldsIncluded": bool,
        "AutomationMode": AutomationModeType,
        "ResumeFullAutomationModeTime": datetime,
        "CustomIamInstanceProfile": str,
        "BackupTarget": str,
        "NetworkType": str,
    },
    total=False,
)

DBSubnetGroupMessageTypeDef = TypedDict(
    "DBSubnetGroupMessageTypeDef",
    {
        "Marker": str,
        "DBSubnetGroups": List[DBSubnetGroupTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBSubnetGroupResultTypeDef = TypedDict(
    "ModifyDBSubnetGroupResultTypeDef",
    {
        "DBSubnetGroup": DBSubnetGroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeValidDBInstanceModificationsResultTypeDef = TypedDict(
    "DescribeValidDBInstanceModificationsResultTypeDef",
    {
        "ValidDBInstanceModificationsMessage": ValidDBInstanceModificationsMessageTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBInstanceReadReplicaResultTypeDef = TypedDict(
    "CreateDBInstanceReadReplicaResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDBInstanceResultTypeDef = TypedDict(
    "CreateDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DBInstanceMessageTypeDef = TypedDict(
    "DBInstanceMessageTypeDef",
    {
        "Marker": str,
        "DBInstances": List[DBInstanceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDBInstanceResultTypeDef = TypedDict(
    "DeleteDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ModifyDBInstanceResultTypeDef = TypedDict(
    "ModifyDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PromoteReadReplicaResultTypeDef = TypedDict(
    "PromoteReadReplicaResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootDBInstanceResultTypeDef = TypedDict(
    "RebootDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBInstanceFromDBSnapshotResultTypeDef = TypedDict(
    "RestoreDBInstanceFromDBSnapshotResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBInstanceFromS3ResultTypeDef = TypedDict(
    "RestoreDBInstanceFromS3ResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreDBInstanceToPointInTimeResultTypeDef = TypedDict(
    "RestoreDBInstanceToPointInTimeResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDBInstanceResultTypeDef = TypedDict(
    "StartDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopDBInstanceResultTypeDef = TypedDict(
    "StopDBInstanceResultTypeDef",
    {
        "DBInstance": DBInstanceTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
