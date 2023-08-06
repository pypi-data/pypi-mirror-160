"""
Type annotations for mgn service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_mgn.client import mgnClient
    from mypy_boto3_mgn.paginator import (
        DescribeJobLogItemsPaginator,
        DescribeJobsPaginator,
        DescribeLaunchConfigurationTemplatesPaginator,
        DescribeReplicationConfigurationTemplatesPaginator,
        DescribeSourceServersPaginator,
        DescribeVcenterClientsPaginator,
    )

    session = Session()
    client: mgnClient = session.client("mgn")

    describe_job_log_items_paginator: DescribeJobLogItemsPaginator = client.get_paginator("describe_job_log_items")
    describe_jobs_paginator: DescribeJobsPaginator = client.get_paginator("describe_jobs")
    describe_launch_configuration_templates_paginator: DescribeLaunchConfigurationTemplatesPaginator = client.get_paginator("describe_launch_configuration_templates")
    describe_replication_configuration_templates_paginator: DescribeReplicationConfigurationTemplatesPaginator = client.get_paginator("describe_replication_configuration_templates")
    describe_source_servers_paginator: DescribeSourceServersPaginator = client.get_paginator("describe_source_servers")
    describe_vcenter_clients_paginator: DescribeVcenterClientsPaginator = client.get_paginator("describe_vcenter_clients")
    ```
"""
from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestFiltersTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeLaunchConfigurationTemplatesResponseTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestFiltersTypeDef,
    DescribeSourceServersResponseTypeDef,
    DescribeVcenterClientsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "DescribeJobLogItemsPaginator",
    "DescribeJobsPaginator",
    "DescribeLaunchConfigurationTemplatesPaginator",
    "DescribeReplicationConfigurationTemplatesPaginator",
    "DescribeSourceServersPaginator",
    "DescribeVcenterClientsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeJobLogItemsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeJobLogItems)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejoblogitemspaginator)
    """

    def paginate(
        self, *, jobID: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeJobLogItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeJobLogItems.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejoblogitemspaginator)
        """


class DescribeJobsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejobspaginator)
    """

    def paginate(
        self,
        *,
        filters: DescribeJobsRequestFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describejobspaginator)
        """


class DescribeLaunchConfigurationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeLaunchConfigurationTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
    """

    def paginate(
        self,
        *,
        launchConfigurationTemplateIDs: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeLaunchConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeLaunchConfigurationTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describelaunchconfigurationtemplatespaginator)
        """


class DescribeReplicationConfigurationTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeReplicationConfigurationTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
    """

    def paginate(
        self,
        *,
        replicationConfigurationTemplateIDs: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeReplicationConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeReplicationConfigurationTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describereplicationconfigurationtemplatespaginator)
        """


class DescribeSourceServersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeSourceServers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describesourceserverspaginator)
    """

    def paginate(
        self,
        *,
        filters: DescribeSourceServersRequestFiltersTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeSourceServersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeSourceServers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describesourceserverspaginator)
        """


class DescribeVcenterClientsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeVcenterClients)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describevcenterclientspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[DescribeVcenterClientsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#mgn.Paginator.DescribeVcenterClients.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_mgn/paginators/#describevcenterclientspaginator)
        """
