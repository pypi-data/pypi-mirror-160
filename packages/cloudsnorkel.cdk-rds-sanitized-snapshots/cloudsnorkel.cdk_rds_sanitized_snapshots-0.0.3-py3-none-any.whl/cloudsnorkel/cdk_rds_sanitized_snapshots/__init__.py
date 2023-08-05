'''
# CDK Construct for RDS Sanitized Snapshots

[![NPM](https://img.shields.io/npm/v/@cloudsnorkel/cdk-rds-sanitized-snapshots?label=npm&logo=npm)](https://www.npmjs.com/package/@cloudsnorkel/cdk-rds-sanitized-snapshots)
[![PyPI](https://img.shields.io/pypi/v/cloudsnorkel.cdk-rds-sanitized-snapshots?label=pypi&logo=pypi)](https://pypi.org/project/cloudsnorkel.cdk-rds-sanitized-snapshots)
[![Maven Central](https://img.shields.io/maven-central/v/com.cloudsnorkel/cdk.rds.sanitized-snapshots.svg?label=Maven%20Central&logo=java)](https://search.maven.org/search?q=g:%22com.cloudsnorkel%22%20AND%20a:%22cdk.rds.sanitized-snapshots%22)
[![Go](https://img.shields.io/github/v/tag/CloudSnorkel/cdk-rds-sanitized-snapshots?color=red&label=go&logo=go)](https://pkg.go.dev/github.com/CloudSnorkel/cdk-rds-sanitized-snapshots-go/cloudsnorkelcdkrdssanitizedsnapshots)
[![Nuget](https://img.shields.io/nuget/v/CloudSnorkel.Cdk.Rds.SanitizedSnapshots?color=red&&logo=nuget)](https://www.nuget.org/packages/CloudSnorkel.Cdk.Rds.SanitizedSnapshots/)
[![Release](https://github.com/CloudSnorkel/cdk-rds-sanitized-snapshots/actions/workflows/release.yml/badge.svg)](https://github.com/CloudSnorkel/cdk-rds-sanitized-snapshots/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/CloudSnorkel/cdk-rds-sanitized-snapshots/blob/main/LICENSE)

Periodically take snapshots of RDS databases, sanitize them, and share with selected accounts.

Use this to automate your development and/or QA database creation, instead of forcing them to use a database that was
created last year and was kind of kept in shape by random acts of kindness. Developers and QA love real data and this
lets you create non-production databases with sanitized production data. Use the sanitization step to delete passwords,
remove credit card numbers, eliminate PII, etc.

See [Constructs Hub](https://constructs.dev/packages/@cloudsnorkel/cdk-rds-sanitized-snapshots/) for installation instructions and API in all supported languages.

## Overview

![Architecture diagram](architecture.svg)

This project supplies a CDK construct that sets up a step function and a timer to execute this function. The
function will create a sanitized snapshot of a given database and share it with configured accounts. Those accounts can
then create new databases from those snapshots.

The step function does the following to create the snapshot:

1. Get a snapshot of the given database by either:

   * Finding the latest snapshot for the given database
   * Creating and waiting for a new fresh snapshot
2. Re-encrypt snapshot if KMS key is supplied
3. Create a temporary database from the snapshot
4. Wait for the database to be ready
5. Reset the master password on the temporary database to a random password
6. Wait for the password to be set
7. Use a Fargate task to connect to the temporary database and run configured SQL statements to sanitize the data
8. Take a snapshot of the temporary database
9. Optionally share the snapshot with other accounts (if you have separate accounts for developers/QA)
10. Delete temporary database and snapshot

## Usage

1. Confirm you're using CDK v2
2. Install the appropriate package

   1. [Python](https://pypi.org/project/cloudsnorkel.cdk-rds-sanitized-snapshots)

      ```
      pip install cloudsnorkel.cdk-rds-sanitized-snapshots
      ```
   2. [TypeScript or JavaScript](https://www.npmjs.com/package/@cloudsnorkel/cdk-rds-sanitized-snapshots)

      ```
      npm i @cloudsnorkel/cdk-rds-sanitized-snapshots
      ```
   3. [Java](https://search.maven.org/search?q=g:%22com.cloudsnorkel%22%20AND%20a:%22cdk.rds.sanitized-snapshots%22)

      ```xml
      <dependency>
      <groupId>com.cloudsnorkel</groupId>
      <artifactId>cdk.rds.sanitized-snapshots</artifactId>
      </dependency>
      ```
   4. [Go](https://pkg.go.dev/github.com/CloudSnorkel/cdk-rds-sanitized-snapshots-go/cloudsnorkelcdkrdssanitizedsnapshots)

      ```
      go get github.com/CloudSnorkel/cdk-rds-sanitized-snapshots-go/cloudsnorkelcdkrdssanitizedsnapshots
      ```
   5. [.NET](https://www.nuget.org/packages/CloudSnorkel.Cdk.Rds.SanitizedSnapshots/)

      ```
      dotnet add package CloudSnorkel.Cdk.Rds.SanitizedSnapshots
      ```
3. Use `RdsSanitizedSnapshotter` construct in your code (starting with default arguments is fine)

### Code Sample

```python
let vpc: ec2.Vpc;
let databaseInstance: rds.DatabaseInstance;

new RdsSanitizedSnapshotter(this, 'Snapshotter', {
  vpc: vpc,
  databaseInstance: databaseInstance,
  script: 'USE mydb; UPDATE users SET ssn = \'0000000000\'',
})
```

## Encryption

The new snapshot will be encrypted with the same key used by the original database. If the original database wasn't
encrypted, the snapshot won't be encrypted either. To add another step that changes the key, use the KMS key parameter.

See [AWS documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ShareSnapshot.html) for instructions
on giving other accounts access to the key.

## Troubleshooting

* Check the status of the state machine for the step function. Click on the failed step and check out the input, output
  and exception.

## Testing

```
npm run bundle && npm run integ:default:deploy
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_kms
import aws_cdk.aws_rds
import aws_cdk.aws_stepfunctions
import constructs


@jsii.interface(
    jsii_type="@cloudsnorkel/cdk-rds-sanitized-snapshots.IRdsSanitizedSnapshotter"
)
class IRdsSanitizedSnapshotter(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        '''(experimental) SQL script used to sanitize the database. It will be executed against the temporary database.

        You would usually want to start this with ``USE mydatabase;``.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) VPC where temporary database and sanitizing task will be created.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseCluster")
    def database_cluster(self) -> typing.Optional[aws_cdk.aws_rds.IDatabaseCluster]:
        '''(experimental) Database cluster to snapshot and sanitize.

        Only one of ``databaseCluster`` and ``databaseInstance`` can be specified.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseInstance")
    def database_instance(self) -> typing.Optional[aws_cdk.aws_rds.IDatabaseInstance]:
        '''(experimental) Database instance to snapshot and sanitize.

        Only one of ``databaseCluster`` and ``databaseInstance`` can be specified.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseKey")
    def database_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''(experimental) KMS key used to encrypt original database, if any.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of database to connect to inside the RDS cluster or instance.

        This database will be used to execute the SQL script.

        :default: 'postgres' for PostgreSQL and not set for MySQL

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbSubnets")
    def db_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''(experimental) VPC subnets to use for temporary databases.

        :default: ec2.SubnetType.PRIVATE_ISOLATED

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fargateCluster")
    def fargate_cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        '''(experimental) Cluster where sanitization task will be executed.

        :default: a new cluster running on given VPC

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sanitizeSubnets")
    def sanitize_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''(experimental) VPC subnets to use for sanitization task.

        :default: ec2.SubnetType.PRIVATE_WITH_NAT

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''(experimental) The schedule or rate (frequency) that determines when the sanitized snapshot runs automatically.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="shareAccounts")
    def share_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of accounts the sanitized snapshot should be shared with.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotHistoryLimit")
    def snapshot_history_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Limit the number of snapshot history.

        Set this to delete old snapshots and only leave a certain number of snapshots.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotKey")
    def snapshot_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''(experimental) Optional KMS key to encrypt target snapshot.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotPrefix")
    def snapshot_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for sanitized snapshot name.

        The current date and time will be added to it.

        :default: cluster identifier (which might be too long)

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tempPrefix")
    def temp_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for all temporary snapshots and databases.

        The step function execution id will be added to it.

        :default: 'sanitize'

        :stability: experimental
        '''
        ...


class _IRdsSanitizedSnapshotterProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@cloudsnorkel/cdk-rds-sanitized-snapshots.IRdsSanitizedSnapshotter"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        '''(experimental) SQL script used to sanitize the database. It will be executed against the temporary database.

        You would usually want to start this with ``USE mydatabase;``.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''(experimental) VPC where temporary database and sanitizing task will be created.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseCluster")
    def database_cluster(self) -> typing.Optional[aws_cdk.aws_rds.IDatabaseCluster]:
        '''(experimental) Database cluster to snapshot and sanitize.

        Only one of ``databaseCluster`` and ``databaseInstance`` can be specified.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_rds.IDatabaseCluster], jsii.get(self, "databaseCluster"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseInstance")
    def database_instance(self) -> typing.Optional[aws_cdk.aws_rds.IDatabaseInstance]:
        '''(experimental) Database instance to snapshot and sanitize.

        Only one of ``databaseCluster`` and ``databaseInstance`` can be specified.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_rds.IDatabaseInstance], jsii.get(self, "databaseInstance"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseKey")
    def database_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''(experimental) KMS key used to encrypt original database, if any.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], jsii.get(self, "databaseKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of database to connect to inside the RDS cluster or instance.

        This database will be used to execute the SQL script.

        :default: 'postgres' for PostgreSQL and not set for MySQL

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbSubnets")
    def db_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''(experimental) VPC subnets to use for temporary databases.

        :default: ec2.SubnetType.PRIVATE_ISOLATED

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], jsii.get(self, "dbSubnets"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fargateCluster")
    def fargate_cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        '''(experimental) Cluster where sanitization task will be executed.

        :default: a new cluster running on given VPC

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ecs.ICluster], jsii.get(self, "fargateCluster"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sanitizeSubnets")
    def sanitize_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''(experimental) VPC subnets to use for sanitization task.

        :default: ec2.SubnetType.PRIVATE_WITH_NAT

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], jsii.get(self, "sanitizeSubnets"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''(experimental) The schedule or rate (frequency) that determines when the sanitized snapshot runs automatically.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], jsii.get(self, "schedule"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="shareAccounts")
    def share_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of accounts the sanitized snapshot should be shared with.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "shareAccounts"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotHistoryLimit")
    def snapshot_history_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Limit the number of snapshot history.

        Set this to delete old snapshots and only leave a certain number of snapshots.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "snapshotHistoryLimit"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotKey")
    def snapshot_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        '''(experimental) Optional KMS key to encrypt target snapshot.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], jsii.get(self, "snapshotKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotPrefix")
    def snapshot_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for sanitized snapshot name.

        The current date and time will be added to it.

        :default: cluster identifier (which might be too long)

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotPrefix"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tempPrefix")
    def temp_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Prefix for all temporary snapshots and databases.

        The step function execution id will be added to it.

        :default: 'sanitize'

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tempPrefix"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRdsSanitizedSnapshotter).__jsii_proxy_class__ = lambda : _IRdsSanitizedSnapshotterProxy


class RdsSanitizedSnapshotter(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudsnorkel/cdk-rds-sanitized-snapshots.RdsSanitizedSnapshotter",
):
    '''(experimental) A process to create sanitized snapshots of RDS instance or cluster, optionally on a schedule.

    The process is handled by a step function.

    1. Snapshot the source database
    2. Optionally re-encrypt the snapshot with a different key in case you want to share it with an account that doesn't have access to the original key
    3. Create a temporary database
    4. Run a Fargate task to connect to the temporary database and execute an arbitrary SQL script to sanitize it
    5. Snapshot the sanitized database
    6. Clean-up temporary snapshots and databases

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        props: IRdsSanitizedSnapshotter,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="props")
    def props(self) -> IRdsSanitizedSnapshotter:
        '''
        :stability: experimental
        '''
        return typing.cast(IRdsSanitizedSnapshotter, jsii.get(self, "props"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotter")
    def snapshotter(self) -> aws_cdk.aws_stepfunctions.StateMachine:
        '''(experimental) Step function in charge of the entire process including snapshotting, sanitizing, and cleanup.

        Trigger this step function to get a new snapshot.

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_stepfunctions.StateMachine, jsii.get(self, "snapshotter"))

    @snapshotter.setter
    def snapshotter(self, value: aws_cdk.aws_stepfunctions.StateMachine) -> None:
        jsii.set(self, "snapshotter", value)


__all__ = [
    "IRdsSanitizedSnapshotter",
    "RdsSanitizedSnapshotter",
]

publication.publish()
