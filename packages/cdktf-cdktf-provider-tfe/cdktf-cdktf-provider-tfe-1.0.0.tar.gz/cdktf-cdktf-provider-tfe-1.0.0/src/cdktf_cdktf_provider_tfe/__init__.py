'''
# Terraform CDK tfe Provider ~> 0.33.0

This repo builds and publishes the Terraform tfe Provider bindings for [cdktf](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-tfe](https://www.npmjs.com/package/@cdktf/provider-tfe).

`npm install @cdktf/provider-tfe`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-tfe](https://pypi.org/project/cdktf-cdktf-provider-tfe).

`pipenv install cdktf-cdktf-provider-tfe`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Tfe](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Tfe).

`dotnet add package HashiCorp.Cdktf.Providers.Tfe`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-tfe](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-tfe).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-tfe</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)

## Versioning

This project is explicitly not tracking the Terraform tfe Provider version 1:1. In fact, it always tracks `latest` of `~> 0.33.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform tfe Provider](https://github.com/terraform-providers/terraform-provider-tfe)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped. While the Terraform Engine and the Terraform tfe Provider are relatively stable, the Terraform CDK is in an early stage. Therefore, it's likely that there will be breaking changes.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
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

import cdktf
import constructs


class AgentPool(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.AgentPool",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool tfe_agent_pool}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool tfe_agent_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#name AgentPool#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#organization AgentPool#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#id AgentPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AgentPoolConfig(
            name=name,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.AgentPoolConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "id": "id",
    },
)
class AgentPoolConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#name AgentPool#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#organization AgentPool#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#id AgentPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#name AgentPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#organization AgentPool#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_pool#id AgentPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AgentToken(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.AgentToken",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/agent_token tfe_agent_token}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        agent_pool_id: builtins.str,
        description: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/agent_token tfe_agent_token} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param agent_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#agent_pool_id AgentToken#agent_pool_id}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#description AgentToken#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#id AgentToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = AgentTokenConfig(
            agent_pool_id=agent_pool_id,
            description=description,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="agentPoolIdInput")
    def agent_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentPoolIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="agentPoolId")
    def agent_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentPoolId"))

    @agent_pool_id.setter
    def agent_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "agentPoolId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.AgentTokenConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "agent_pool_id": "agentPoolId",
        "description": "description",
        "id": "id",
    },
)
class AgentTokenConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        agent_pool_id: builtins.str,
        description: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param agent_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#agent_pool_id AgentToken#agent_pool_id}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#description AgentToken#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#id AgentToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "agent_pool_id": agent_pool_id,
            "description": description,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def agent_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#agent_pool_id AgentToken#agent_pool_id}.'''
        result = self._values.get("agent_pool_id")
        assert result is not None, "Required property 'agent_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#description AgentToken#description}.'''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/agent_token#id AgentToken#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeAgentPool(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeAgentPool",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool tfe_agent_pool}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool tfe_agent_pool} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#name DataTfeAgentPool#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#organization DataTfeAgentPool#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#id DataTfeAgentPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeAgentPoolConfig(
            name=name,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeAgentPoolConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "id": "id",
    },
)
class DataTfeAgentPoolConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#name DataTfeAgentPool#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#organization DataTfeAgentPool#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#id DataTfeAgentPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#name DataTfeAgentPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#organization DataTfeAgentPool#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/agent_pool#id DataTfeAgentPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeAgentPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeIpRanges(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeIpRanges",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/ip_ranges tfe_ip_ranges}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/ip_ranges tfe_ip_ranges} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ip_ranges#id DataTfeIpRanges#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeIpRangesConfig(
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="api")
    def api(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "api"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notifications")
    def notifications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifications"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sentinel")
    def sentinel(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "sentinel"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcs")
    def vcs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "vcs"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeIpRangesConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "id": "id",
    },
)
class DataTfeIpRangesConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ip_ranges#id DataTfeIpRanges#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ip_ranges#id DataTfeIpRanges#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeIpRangesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeOauthClient(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeOauthClient",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client tfe_oauth_client}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        oauth_client_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client tfe_oauth_client} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param oauth_client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client#oauth_client_id DataTfeOauthClient#oauth_client_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client#id DataTfeOauthClient#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeOauthClientConfig(
            oauth_client_id=oauth_client_id,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiUrl")
    def api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpUrl")
    def http_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenId")
    def oauth_token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthClientIdInput")
    def oauth_client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthClientIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthClientId")
    def oauth_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthClientId"))

    @oauth_client_id.setter
    def oauth_client_id(self, value: builtins.str) -> None:
        jsii.set(self, "oauthClientId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeOauthClientConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "oauth_client_id": "oauthClientId",
        "id": "id",
    },
)
class DataTfeOauthClientConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        oauth_client_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param oauth_client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client#oauth_client_id DataTfeOauthClient#oauth_client_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client#id DataTfeOauthClient#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "oauth_client_id": oauth_client_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def oauth_client_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client#oauth_client_id DataTfeOauthClient#oauth_client_id}.'''
        result = self._values.get("oauth_client_id")
        assert result is not None, "Required property 'oauth_client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/oauth_client#id DataTfeOauthClient#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeOauthClientConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeOrganization(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeOrganization",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/organization tfe_organization}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/organization tfe_organization} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization#name DataTfeOrganization#name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization#id DataTfeOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeOrganizationConfig(
            name=name,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="collaboratorAuthPolicy")
    def collaborator_auth_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collaboratorAuthPolicy"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="costEstimationEnabled")
    def cost_estimation_enabled(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "costEstimationEnabled"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ownersTeamSamlRoleId")
    def owners_team_saml_role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownersTeamSamlRoleId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sendPassingStatusesForUntriggeredSpeculativePlans")
    def send_passing_statuses_for_untriggered_speculative_plans(
        self,
    ) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "sendPassingStatusesForUntriggeredSpeculativePlans"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="twoFactorConformant")
    def two_factor_conformant(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "twoFactorConformant"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeOrganizationConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "id": "id",
    },
)
class DataTfeOrganizationConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization#name DataTfeOrganization#name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization#id DataTfeOrganization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization#name DataTfeOrganization#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization#id DataTfeOrganization#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeOrganizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeOrganizationMembership(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeOrganizationMembership",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership tfe_organization_membership}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        email: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership tfe_organization_membership} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#email DataTfeOrganizationMembership#email}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#organization DataTfeOrganizationMembership#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#id DataTfeOrganizationMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeOrganizationMembershipConfig(
            email=email,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        jsii.set(self, "email", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeOrganizationMembershipConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "email": "email",
        "organization": "organization",
        "id": "id",
    },
)
class DataTfeOrganizationMembershipConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        email: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#email DataTfeOrganizationMembership#email}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#organization DataTfeOrganizationMembership#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#id DataTfeOrganizationMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "email": email,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#email DataTfeOrganizationMembership#email}.'''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#organization DataTfeOrganizationMembership#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_membership#id DataTfeOrganizationMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeOrganizationMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeOrganizationRunTask(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeOrganizationRunTask",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task tfe_organization_run_task}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        category: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task tfe_organization_run_task} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#name DataTfeOrganizationRunTask#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#organization DataTfeOrganizationRunTask#organization}.
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#category DataTfeOrganizationRunTask#category}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#enabled DataTfeOrganizationRunTask#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#id DataTfeOrganizationRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#url DataTfeOrganizationRunTask#url}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeOrganizationRunTaskConfig(
            name=name,
            organization=organization,
            category=category,
            enabled=enabled,
            id=id,
            url=url,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetCategory")
    def reset_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategory", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        jsii.set(self, "category", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        jsii.set(self, "url", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeOrganizationRunTaskConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "category": "category",
        "enabled": "enabled",
        "id": "id",
        "url": "url",
    },
)
class DataTfeOrganizationRunTaskConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        category: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#name DataTfeOrganizationRunTask#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#organization DataTfeOrganizationRunTask#organization}.
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#category DataTfeOrganizationRunTask#category}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#enabled DataTfeOrganizationRunTask#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#id DataTfeOrganizationRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#url DataTfeOrganizationRunTask#url}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if category is not None:
            self._values["category"] = category
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#name DataTfeOrganizationRunTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#organization DataTfeOrganizationRunTask#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def category(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#category DataTfeOrganizationRunTask#category}.'''
        result = self._values.get("category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#enabled DataTfeOrganizationRunTask#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#id DataTfeOrganizationRunTask#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organization_run_task#url DataTfeOrganizationRunTask#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeOrganizationRunTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeOrganizations(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeOrganizations",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/organizations tfe_organizations}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        admin: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/organizations tfe_organizations} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param admin: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organizations#admin DataTfeOrganizations#admin}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organizations#id DataTfeOrganizations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeOrganizationsConfig(
            admin=admin,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAdmin")
    def reset_admin(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdmin", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ids")
    def ids(self) -> cdktf.StringMap:
        return typing.cast(cdktf.StringMap, jsii.get(self, "ids"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="names")
    def names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "names"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="adminInput")
    def admin_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "adminInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="admin")
    def admin(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "admin"))

    @admin.setter
    def admin(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "admin", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeOrganizationsConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "admin": "admin",
        "id": "id",
    },
)
class DataTfeOrganizationsConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        admin: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param admin: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organizations#admin DataTfeOrganizations#admin}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organizations#id DataTfeOrganizations#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if admin is not None:
            self._values["admin"] = admin
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def admin(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organizations#admin DataTfeOrganizations#admin}.'''
        result = self._values.get("admin")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/organizations#id DataTfeOrganizations#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeOrganizationsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeOutputs(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeOutputs",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/outputs tfe_outputs}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        organization: builtins.str,
        workspace: builtins.str,
        values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/outputs tfe_outputs} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param organization: The organization to fetch the remote state from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#organization DataTfeOutputs#organization}
        :param workspace: The workspace to fetch the remote state from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#workspace DataTfeOutputs#workspace}
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#values DataTfeOutputs#values}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeOutputsConfig(
            organization=organization,
            workspace=workspace,
            values=values,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetValues")
    def reset_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValues", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "valuesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceInput")
    def workspace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="values")
    def values(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.Mapping[builtins.str, typing.Any]) -> None:
        jsii.set(self, "values", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: builtins.str) -> None:
        jsii.set(self, "workspace", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeOutputsConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "organization": "organization",
        "workspace": "workspace",
        "values": "values",
    },
)
class DataTfeOutputsConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        organization: builtins.str,
        workspace: builtins.str,
        values: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param organization: The organization to fetch the remote state from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#organization DataTfeOutputs#organization}
        :param workspace: The workspace to fetch the remote state from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#workspace DataTfeOutputs#workspace}
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#values DataTfeOutputs#values}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
            "workspace": workspace,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''The organization to fetch the remote state from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#organization DataTfeOutputs#organization}
        '''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace(self) -> builtins.str:
        '''The workspace to fetch the remote state from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#workspace DataTfeOutputs#workspace}
        '''
        result = self._values.get("workspace")
        assert result is not None, "Required property 'workspace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/outputs#values DataTfeOutputs#values}.'''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeOutputsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeSlug(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeSlug",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/slug tfe_slug}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        source_path: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/slug tfe_slug} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param source_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/slug#source_path DataTfeSlug#source_path}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/slug#id DataTfeSlug#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeSlugConfig(
            source_path=source_path,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourcePathInput")
    def source_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourcePathInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourcePath")
    def source_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourcePath"))

    @source_path.setter
    def source_path(self, value: builtins.str) -> None:
        jsii.set(self, "sourcePath", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeSlugConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "source_path": "sourcePath",
        "id": "id",
    },
)
class DataTfeSlugConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        source_path: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param source_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/slug#source_path DataTfeSlug#source_path}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/slug#id DataTfeSlug#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "source_path": source_path,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def source_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/slug#source_path DataTfeSlug#source_path}.'''
        result = self._values.get("source_path")
        assert result is not None, "Required property 'source_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/slug#id DataTfeSlug#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeSlugConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeSshKey(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeSshKey",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key tfe_ssh_key}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key tfe_ssh_key} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#name DataTfeSshKey#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#organization DataTfeSshKey#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#id DataTfeSshKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeSshKeyConfig(
            name=name,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeSshKeyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "id": "id",
    },
)
class DataTfeSshKeyConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#name DataTfeSshKey#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#organization DataTfeSshKey#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#id DataTfeSshKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#name DataTfeSshKey#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#organization DataTfeSshKey#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/ssh_key#id DataTfeSshKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeSshKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeTeam(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeTeam",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/team tfe_team}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/team tfe_team} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#name DataTfeTeam#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#organization DataTfeTeam#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#id DataTfeTeam#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeTeamConfig(
            name=name,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ssoTeamId")
    def sso_team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoTeamId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


class DataTfeTeamAccess(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeTeamAccess",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/team_access tfe_team_access}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        team_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/team_access tfe_team_access} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#team_id DataTfeTeamAccess#team_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#workspace_id DataTfeTeamAccess#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#id DataTfeTeamAccess#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeTeamAccessConfig(
            team_id=team_id,
            workspace_id=workspace_id,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="access")
    def access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "access"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "DataTfeTeamAccessPermissionsList":
        return typing.cast("DataTfeTeamAccessPermissionsList", jsii.get(self, "permissions"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeTeamAccessConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "team_id": "teamId",
        "workspace_id": "workspaceId",
        "id": "id",
    },
)
class DataTfeTeamAccessConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        team_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#team_id DataTfeTeamAccess#team_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#workspace_id DataTfeTeamAccess#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#id DataTfeTeamAccess#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "team_id": team_id,
            "workspace_id": workspace_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#team_id DataTfeTeamAccess#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#workspace_id DataTfeTeamAccess#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team_access#id DataTfeTeamAccess#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeTeamAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeTeamAccessPermissions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataTfeTeamAccessPermissions:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeTeamAccessPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeTeamAccessPermissionsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeTeamAccessPermissionsList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataTfeTeamAccessPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("DataTfeTeamAccessPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)


class DataTfeTeamAccessPermissionsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeTeamAccessPermissionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runs")
    def runs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runs"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runTasks")
    def run_tasks(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "runTasks"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sentinelMocks")
    def sentinel_mocks(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sentinelMocks"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateVersions")
    def state_versions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateVersions"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variables"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceLocking")
    def workspace_locking(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "workspaceLocking"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataTfeTeamAccessPermissions]:
        return typing.cast(typing.Optional[DataTfeTeamAccessPermissions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataTfeTeamAccessPermissions],
    ) -> None:
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeTeamConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "id": "id",
    },
)
class DataTfeTeamConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#name DataTfeTeam#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#organization DataTfeTeam#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#id DataTfeTeam#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#name DataTfeTeam#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#organization DataTfeTeam#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/team#id DataTfeTeam#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeTeamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeVariableSet(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariableSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/variable_set tfe_variable_set}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        variable_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        workspace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/variable_set tfe_variable_set} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#name DataTfeVariableSet#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#organization DataTfeVariableSet#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#id DataTfeVariableSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param variable_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#variable_ids DataTfeVariableSet#variable_ids}.
        :param workspace_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#workspace_ids DataTfeVariableSet#workspace_ids}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeVariableSetConfig(
            name=name,
            organization=organization,
            id=id,
            variable_ids=variable_ids,
            workspace_ids=workspace_ids,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetVariableIds")
    def reset_variable_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariableIds", []))

    @jsii.member(jsii_name="resetWorkspaceIds")
    def reset_workspace_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceIds", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="global")
    def global_(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "global"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableIdsInput")
    def variable_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "variableIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdsInput")
    def workspace_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "workspaceIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableIds")
    def variable_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "variableIds"))

    @variable_ids.setter
    def variable_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "variableIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIds")
    def workspace_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "workspaceIds"))

    @workspace_ids.setter
    def workspace_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "workspaceIds", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeVariableSetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "id": "id",
        "variable_ids": "variableIds",
        "workspace_ids": "workspaceIds",
    },
)
class DataTfeVariableSetConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        variable_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        workspace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#name DataTfeVariableSet#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#organization DataTfeVariableSet#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#id DataTfeVariableSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param variable_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#variable_ids DataTfeVariableSet#variable_ids}.
        :param workspace_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#workspace_ids DataTfeVariableSet#workspace_ids}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id
        if variable_ids is not None:
            self._values["variable_ids"] = variable_ids
        if workspace_ids is not None:
            self._values["workspace_ids"] = workspace_ids

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#name DataTfeVariableSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#organization DataTfeVariableSet#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#id DataTfeVariableSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#variable_ids DataTfeVariableSet#variable_ids}.'''
        result = self._values.get("variable_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def workspace_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variable_set#workspace_ids DataTfeVariableSet#workspace_ids}.'''
        result = self._values.get("workspace_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeVariableSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeVariables(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariables",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/variables tfe_variables}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        variable_set_id: typing.Optional[builtins.str] = None,
        workspace_id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/variables tfe_variables} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#id DataTfeVariables#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param variable_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#variable_set_id DataTfeVariables#variable_set_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#workspace_id DataTfeVariables#workspace_id}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeVariablesConfig(
            id=id,
            variable_set_id=variable_set_id,
            workspace_id=workspace_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetVariableSetId")
    def reset_variable_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariableSetId", []))

    @jsii.member(jsii_name="resetWorkspaceId")
    def reset_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="env")
    def env(self) -> "DataTfeVariablesEnvList":
        return typing.cast("DataTfeVariablesEnvList", jsii.get(self, "env"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraform")
    def terraform(self) -> "DataTfeVariablesTerraformList":
        return typing.cast("DataTfeVariablesTerraformList", jsii.get(self, "terraform"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(self) -> "DataTfeVariablesVariablesList":
        return typing.cast("DataTfeVariablesVariablesList", jsii.get(self, "variables"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableSetIdInput")
    def variable_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variableSetIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableSetId")
    def variable_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variableSetId"))

    @variable_set_id.setter
    def variable_set_id(self, value: builtins.str) -> None:
        jsii.set(self, "variableSetId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "id": "id",
        "variable_set_id": "variableSetId",
        "workspace_id": "workspaceId",
    },
)
class DataTfeVariablesConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        id: typing.Optional[builtins.str] = None,
        variable_set_id: typing.Optional[builtins.str] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#id DataTfeVariables#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param variable_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#variable_set_id DataTfeVariables#variable_set_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#workspace_id DataTfeVariables#workspace_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id
        if variable_set_id is not None:
            self._values["variable_set_id"] = variable_set_id
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#id DataTfeVariables#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#variable_set_id DataTfeVariables#variable_set_id}.'''
        result = self._values.get("variable_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/variables#workspace_id DataTfeVariables#workspace_id}.'''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeVariablesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesEnv",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataTfeVariablesEnv:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeVariablesEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeVariablesEnvList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesEnvList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataTfeVariablesEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("DataTfeVariablesEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)


class DataTfeVariablesEnvOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesEnvOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hcl")
    def hcl(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "hcl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "sensitive"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataTfeVariablesEnv]:
        return typing.cast(typing.Optional[DataTfeVariablesEnv], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataTfeVariablesEnv]) -> None:
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesTerraform",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataTfeVariablesTerraform:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeVariablesTerraform(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeVariablesTerraformList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesTerraformList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataTfeVariablesTerraformOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("DataTfeVariablesTerraformOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)


class DataTfeVariablesTerraformOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesTerraformOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hcl")
    def hcl(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "hcl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "sensitive"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataTfeVariablesTerraform]:
        return typing.cast(typing.Optional[DataTfeVariablesTerraform], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataTfeVariablesTerraform]) -> None:
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesVariables",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataTfeVariablesVariables:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeVariablesVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeVariablesVariablesList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesVariablesList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataTfeVariablesVariablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("DataTfeVariablesVariablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)


class DataTfeVariablesVariablesOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeVariablesVariablesOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hcl")
    def hcl(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "hcl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "sensitive"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataTfeVariablesVariables]:
        return typing.cast(typing.Optional[DataTfeVariablesVariables], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataTfeVariablesVariables]) -> None:
        jsii.set(self, "internalValue", value)


class DataTfeWorkspace(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspace",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/workspace tfe_workspace}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/workspace tfe_workspace} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#name DataTfeWorkspace#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#organization DataTfeWorkspace#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#id DataTfeWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#tag_names DataTfeWorkspace#tag_names}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeWorkspaceConfig(
            name=name,
            organization=organization,
            id=id,
            tag_names=tag_names,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTagNames")
    def reset_tag_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagNames", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowDestroyPlan")
    def allow_destroy_plan(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "allowDestroyPlan"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoApply")
    def auto_apply(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "autoApply"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileTriggersEnabled")
    def file_triggers_enabled(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "fileTriggersEnabled"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="globalRemoteState")
    def global_remote_state(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "globalRemoteState"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="operations")
    def operations(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "operations"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyCheckFailures")
    def policy_check_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "policyCheckFailures"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queueAllRuns")
    def queue_all_runs(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "queueAllRuns"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="remoteStateConsumerIds")
    def remote_state_consumer_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteStateConsumerIds"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resourceCount")
    def resource_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resourceCount"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runFailures")
    def run_failures(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "runFailures"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runsCount")
    def runs_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "runsCount"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="speculativeEnabled")
    def speculative_enabled(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "speculativeEnabled"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sshKeyId")
    def ssh_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshKeyId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="structuredRunOutputEnabled")
    def structured_run_output_enabled(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "structuredRunOutputEnabled"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformVersion")
    def terraform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformVersion"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerPatterns")
    def trigger_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerPatterns"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerPrefixes")
    def trigger_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerPrefixes"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcsRepo")
    def vcs_repo(self) -> "DataTfeWorkspaceVcsRepoList":
        return typing.cast("DataTfeWorkspaceVcsRepoList", jsii.get(self, "vcsRepo"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workingDirectory")
    def working_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDirectory"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagNamesInput")
    def tag_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagNamesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagNames")
    def tag_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagNames"))

    @tag_names.setter
    def tag_names(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "tagNames", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "id": "id",
        "tag_names": "tagNames",
    },
)
class DataTfeWorkspaceConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#name DataTfeWorkspace#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#organization DataTfeWorkspace#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#id DataTfeWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#tag_names DataTfeWorkspace#tag_names}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id
        if tag_names is not None:
            self._values["tag_names"] = tag_names

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#name DataTfeWorkspace#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#organization DataTfeWorkspace#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#id DataTfeWorkspace#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace#tag_names DataTfeWorkspace#tag_names}.'''
        result = self._values.get("tag_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeWorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeWorkspaceIds(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceIds",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids tfe_workspace_ids}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        organization: builtins.str,
        exclude_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        names: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids tfe_workspace_ids} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#organization DataTfeWorkspaceIds#organization}.
        :param exclude_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#exclude_tags DataTfeWorkspaceIds#exclude_tags}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#id DataTfeWorkspaceIds#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#names DataTfeWorkspaceIds#names}.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#tag_names DataTfeWorkspaceIds#tag_names}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeWorkspaceIdsConfig(
            organization=organization,
            exclude_tags=exclude_tags,
            id=id,
            names=names,
            tag_names=tag_names,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetExcludeTags")
    def reset_exclude_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeTags", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNames")
    def reset_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNames", []))

    @jsii.member(jsii_name="resetTagNames")
    def reset_tag_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagNames", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fullNames")
    def full_names(self) -> cdktf.StringMap:
        return typing.cast(cdktf.StringMap, jsii.get(self, "fullNames"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ids")
    def ids(self) -> cdktf.StringMap:
        return typing.cast(cdktf.StringMap, jsii.get(self, "ids"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="excludeTagsInput")
    def exclude_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludeTagsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="namesInput")
    def names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagNamesInput")
    def tag_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagNamesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="excludeTags")
    def exclude_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludeTags"))

    @exclude_tags.setter
    def exclude_tags(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "excludeTags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="names")
    def names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "names"))

    @names.setter
    def names(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "names", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagNames")
    def tag_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagNames"))

    @tag_names.setter
    def tag_names(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "tagNames", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceIdsConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "organization": "organization",
        "exclude_tags": "excludeTags",
        "id": "id",
        "names": "names",
        "tag_names": "tagNames",
    },
)
class DataTfeWorkspaceIdsConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        organization: builtins.str,
        exclude_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        names: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#organization DataTfeWorkspaceIds#organization}.
        :param exclude_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#exclude_tags DataTfeWorkspaceIds#exclude_tags}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#id DataTfeWorkspaceIds#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#names DataTfeWorkspaceIds#names}.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#tag_names DataTfeWorkspaceIds#tag_names}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if exclude_tags is not None:
            self._values["exclude_tags"] = exclude_tags
        if id is not None:
            self._values["id"] = id
        if names is not None:
            self._values["names"] = names
        if tag_names is not None:
            self._values["tag_names"] = tag_names

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#organization DataTfeWorkspaceIds#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exclude_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#exclude_tags DataTfeWorkspaceIds#exclude_tags}.'''
        result = self._values.get("exclude_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#id DataTfeWorkspaceIds#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#names DataTfeWorkspaceIds#names}.'''
        result = self._values.get("names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_ids#tag_names DataTfeWorkspaceIds#tag_names}.'''
        result = self._values.get("tag_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeWorkspaceIdsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeWorkspaceRunTask(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceRunTask",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task tfe_workspace_run_task}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        task_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task tfe_workspace_run_task} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param task_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#task_id DataTfeWorkspaceRunTask#task_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#workspace_id DataTfeWorkspaceRunTask#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#id DataTfeWorkspaceRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTfeWorkspaceRunTaskConfig(
            task_id=task_id,
            workspace_id=workspace_id,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enforcementLevel")
    def enforcement_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcementLevel"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskIdInput")
    def task_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskId")
    def task_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskId"))

    @task_id.setter
    def task_id(self, value: builtins.str) -> None:
        jsii.set(self, "taskId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceRunTaskConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "task_id": "taskId",
        "workspace_id": "workspaceId",
        "id": "id",
    },
)
class DataTfeWorkspaceRunTaskConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        task_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param task_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#task_id DataTfeWorkspaceRunTask#task_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#workspace_id DataTfeWorkspaceRunTask#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#id DataTfeWorkspaceRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "task_id": task_id,
            "workspace_id": workspace_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def task_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#task_id DataTfeWorkspaceRunTask#task_id}.'''
        result = self._values.get("task_id")
        assert result is not None, "Required property 'task_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#workspace_id DataTfeWorkspaceRunTask#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/d/workspace_run_task#id DataTfeWorkspaceRunTask#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeWorkspaceRunTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceVcsRepo",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataTfeWorkspaceVcsRepo:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTfeWorkspaceVcsRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTfeWorkspaceVcsRepoList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceVcsRepoList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataTfeWorkspaceVcsRepoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("DataTfeWorkspaceVcsRepoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)


class DataTfeWorkspaceVcsRepoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.DataTfeWorkspaceVcsRepoOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ingressSubmodules")
    def ingress_submodules(self) -> cdktf.IResolvable:
        return typing.cast(cdktf.IResolvable, jsii.get(self, "ingressSubmodules"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenId")
    def oauth_token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataTfeWorkspaceVcsRepo]:
        return typing.cast(typing.Optional[DataTfeWorkspaceVcsRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataTfeWorkspaceVcsRepo]) -> None:
        jsii.set(self, "internalValue", value)


class NotificationConfiguration(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.NotificationConfiguration",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration tfe_notification_configuration}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        destination_type: builtins.str,
        name: builtins.str,
        workspace_id: builtins.str,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration tfe_notification_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#destination_type NotificationConfiguration#destination_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#name NotificationConfiguration#name}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#workspace_id NotificationConfiguration#workspace_id}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_addresses NotificationConfiguration#email_addresses}.
        :param email_user_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_user_ids NotificationConfiguration#email_user_ids}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#enabled NotificationConfiguration#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#id NotificationConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#token NotificationConfiguration#token}.
        :param triggers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#triggers NotificationConfiguration#triggers}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#url NotificationConfiguration#url}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = NotificationConfigurationConfig(
            destination_type=destination_type,
            name=name,
            workspace_id=workspace_id,
            email_addresses=email_addresses,
            email_user_ids=email_user_ids,
            enabled=enabled,
            id=id,
            token=token,
            triggers=triggers,
            url=url,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @jsii.member(jsii_name="resetEmailUserIds")
    def reset_email_user_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailUserIds", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetTriggers")
    def reset_triggers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggers", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationTypeInput")
    def destination_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailUserIdsInput")
    def email_user_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailUserIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggersInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationType")
    def destination_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationType"))

    @destination_type.setter
    def destination_type(self, value: builtins.str) -> None:
        jsii.set(self, "destinationType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "emailAddresses", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailUserIds")
    def email_user_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailUserIds"))

    @email_user_ids.setter
    def email_user_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "emailUserIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        jsii.set(self, "token", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggers"))

    @triggers.setter
    def triggers(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "triggers", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        jsii.set(self, "url", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.NotificationConfigurationConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "destination_type": "destinationType",
        "name": "name",
        "workspace_id": "workspaceId",
        "email_addresses": "emailAddresses",
        "email_user_ids": "emailUserIds",
        "enabled": "enabled",
        "id": "id",
        "token": "token",
        "triggers": "triggers",
        "url": "url",
    },
)
class NotificationConfigurationConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        destination_type: builtins.str,
        name: builtins.str,
        workspace_id: builtins.str,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param destination_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#destination_type NotificationConfiguration#destination_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#name NotificationConfiguration#name}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#workspace_id NotificationConfiguration#workspace_id}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_addresses NotificationConfiguration#email_addresses}.
        :param email_user_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_user_ids NotificationConfiguration#email_user_ids}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#enabled NotificationConfiguration#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#id NotificationConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#token NotificationConfiguration#token}.
        :param triggers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#triggers NotificationConfiguration#triggers}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#url NotificationConfiguration#url}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "destination_type": destination_type,
            "name": name,
            "workspace_id": workspace_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if email_user_ids is not None:
            self._values["email_user_ids"] = email_user_ids
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if token is not None:
            self._values["token"] = token
        if triggers is not None:
            self._values["triggers"] = triggers
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def destination_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#destination_type NotificationConfiguration#destination_type}.'''
        result = self._values.get("destination_type")
        assert result is not None, "Required property 'destination_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#name NotificationConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#workspace_id NotificationConfiguration#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_addresses NotificationConfiguration#email_addresses}.'''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_user_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_user_ids NotificationConfiguration#email_user_ids}.'''
        result = self._values.get("email_user_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#enabled NotificationConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#id NotificationConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#token NotificationConfiguration#token}.'''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#triggers NotificationConfiguration#triggers}.'''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#url NotificationConfiguration#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OauthClient(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.OauthClient",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client tfe_oauth_client}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        api_url: builtins.str,
        http_url: builtins.str,
        organization: builtins.str,
        service_provider: builtins.str,
        id: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client tfe_oauth_client} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#api_url OauthClient#api_url}.
        :param http_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#http_url OauthClient#http_url}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#organization OauthClient#organization}.
        :param service_provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#service_provider OauthClient#service_provider}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#id OauthClient#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#key OauthClient#key}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#name OauthClient#name}.
        :param oauth_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#oauth_token OauthClient#oauth_token}.
        :param private_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#private_key OauthClient#private_key}.
        :param rsa_public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#rsa_public_key OauthClient#rsa_public_key}.
        :param secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#secret OauthClient#secret}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = OauthClientConfig(
            api_url=api_url,
            http_url=http_url,
            organization=organization,
            service_provider=service_provider,
            id=id,
            key=key,
            name=name,
            oauth_token=oauth_token,
            private_key=private_key,
            rsa_public_key=rsa_public_key,
            secret=secret,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetOauthToken")
    def reset_oauth_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthToken", []))

    @jsii.member(jsii_name="resetPrivateKey")
    def reset_private_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateKey", []))

    @jsii.member(jsii_name="resetRsaPublicKey")
    def reset_rsa_public_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRsaPublicKey", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenId")
    def oauth_token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiUrlInput")
    def api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpUrlInput")
    def http_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpUrlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenInput")
    def oauth_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthTokenInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rsaPublicKeyInput")
    def rsa_public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rsaPublicKeyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceProviderInput")
    def service_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceProviderInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="apiUrl")
    def api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiUrl"))

    @api_url.setter
    def api_url(self, value: builtins.str) -> None:
        jsii.set(self, "apiUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="httpUrl")
    def http_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpUrl"))

    @http_url.setter
    def http_url(self, value: builtins.str) -> None:
        jsii.set(self, "httpUrl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        jsii.set(self, "key", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthToken"))

    @oauth_token.setter
    def oauth_token(self, value: builtins.str) -> None:
        jsii.set(self, "oauthToken", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        jsii.set(self, "privateKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rsaPublicKey")
    def rsa_public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rsaPublicKey"))

    @rsa_public_key.setter
    def rsa_public_key(self, value: builtins.str) -> None:
        jsii.set(self, "rsaPublicKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        jsii.set(self, "secret", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceProvider")
    def service_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceProvider"))

    @service_provider.setter
    def service_provider(self, value: builtins.str) -> None:
        jsii.set(self, "serviceProvider", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.OauthClientConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "api_url": "apiUrl",
        "http_url": "httpUrl",
        "organization": "organization",
        "service_provider": "serviceProvider",
        "id": "id",
        "key": "key",
        "name": "name",
        "oauth_token": "oauthToken",
        "private_key": "privateKey",
        "rsa_public_key": "rsaPublicKey",
        "secret": "secret",
    },
)
class OauthClientConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        api_url: builtins.str,
        http_url: builtins.str,
        organization: builtins.str,
        service_provider: builtins.str,
        id: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        rsa_public_key: typing.Optional[builtins.str] = None,
        secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param api_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#api_url OauthClient#api_url}.
        :param http_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#http_url OauthClient#http_url}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#organization OauthClient#organization}.
        :param service_provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#service_provider OauthClient#service_provider}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#id OauthClient#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#key OauthClient#key}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#name OauthClient#name}.
        :param oauth_token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#oauth_token OauthClient#oauth_token}.
        :param private_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#private_key OauthClient#private_key}.
        :param rsa_public_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#rsa_public_key OauthClient#rsa_public_key}.
        :param secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#secret OauthClient#secret}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "api_url": api_url,
            "http_url": http_url,
            "organization": organization,
            "service_provider": service_provider,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id
        if key is not None:
            self._values["key"] = key
        if name is not None:
            self._values["name"] = name
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token
        if private_key is not None:
            self._values["private_key"] = private_key
        if rsa_public_key is not None:
            self._values["rsa_public_key"] = rsa_public_key
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def api_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#api_url OauthClient#api_url}.'''
        result = self._values.get("api_url")
        assert result is not None, "Required property 'api_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#http_url OauthClient#http_url}.'''
        result = self._values.get("http_url")
        assert result is not None, "Required property 'http_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#organization OauthClient#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_provider(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#service_provider OauthClient#service_provider}.'''
        result = self._values.get("service_provider")
        assert result is not None, "Required property 'service_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#id OauthClient#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#key OauthClient#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#name OauthClient#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#oauth_token OauthClient#oauth_token}.'''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#private_key OauthClient#private_key}.'''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rsa_public_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#rsa_public_key OauthClient#rsa_public_key}.'''
        result = self._values.get("rsa_public_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/oauth_client#secret OauthClient#secret}.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OauthClientConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Organization(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.Organization",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/organization tfe_organization}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        email: builtins.str,
        name: builtins.str,
        collaborator_auth_policy: typing.Optional[builtins.str] = None,
        cost_estimation_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        owners_team_saml_role_id: typing.Optional[builtins.str] = None,
        send_passing_statuses_for_untriggered_speculative_plans: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        session_remember_minutes: typing.Optional[jsii.Number] = None,
        session_timeout_minutes: typing.Optional[jsii.Number] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/organization tfe_organization} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#email Organization#email}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#name Organization#name}.
        :param collaborator_auth_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#collaborator_auth_policy Organization#collaborator_auth_policy}.
        :param cost_estimation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#cost_estimation_enabled Organization#cost_estimation_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#id Organization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owners_team_saml_role_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#owners_team_saml_role_id Organization#owners_team_saml_role_id}.
        :param send_passing_statuses_for_untriggered_speculative_plans: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#send_passing_statuses_for_untriggered_speculative_plans Organization#send_passing_statuses_for_untriggered_speculative_plans}.
        :param session_remember_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#session_remember_minutes Organization#session_remember_minutes}.
        :param session_timeout_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#session_timeout_minutes Organization#session_timeout_minutes}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = OrganizationConfig(
            email=email,
            name=name,
            collaborator_auth_policy=collaborator_auth_policy,
            cost_estimation_enabled=cost_estimation_enabled,
            id=id,
            owners_team_saml_role_id=owners_team_saml_role_id,
            send_passing_statuses_for_untriggered_speculative_plans=send_passing_statuses_for_untriggered_speculative_plans,
            session_remember_minutes=session_remember_minutes,
            session_timeout_minutes=session_timeout_minutes,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetCollaboratorAuthPolicy")
    def reset_collaborator_auth_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollaboratorAuthPolicy", []))

    @jsii.member(jsii_name="resetCostEstimationEnabled")
    def reset_cost_estimation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCostEstimationEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOwnersTeamSamlRoleId")
    def reset_owners_team_saml_role_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnersTeamSamlRoleId", []))

    @jsii.member(jsii_name="resetSendPassingStatusesForUntriggeredSpeculativePlans")
    def reset_send_passing_statuses_for_untriggered_speculative_plans(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendPassingStatusesForUntriggeredSpeculativePlans", []))

    @jsii.member(jsii_name="resetSessionRememberMinutes")
    def reset_session_remember_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionRememberMinutes", []))

    @jsii.member(jsii_name="resetSessionTimeoutMinutes")
    def reset_session_timeout_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionTimeoutMinutes", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="collaboratorAuthPolicyInput")
    def collaborator_auth_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collaboratorAuthPolicyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="costEstimationEnabledInput")
    def cost_estimation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "costEstimationEnabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ownersTeamSamlRoleIdInput")
    def owners_team_saml_role_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownersTeamSamlRoleIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sendPassingStatusesForUntriggeredSpeculativePlansInput")
    def send_passing_statuses_for_untriggered_speculative_plans_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "sendPassingStatusesForUntriggeredSpeculativePlansInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionRememberMinutesInput")
    def session_remember_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionRememberMinutesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionTimeoutMinutesInput")
    def session_timeout_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionTimeoutMinutesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="collaboratorAuthPolicy")
    def collaborator_auth_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collaboratorAuthPolicy"))

    @collaborator_auth_policy.setter
    def collaborator_auth_policy(self, value: builtins.str) -> None:
        jsii.set(self, "collaboratorAuthPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="costEstimationEnabled")
    def cost_estimation_enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "costEstimationEnabled"))

    @cost_estimation_enabled.setter
    def cost_estimation_enabled(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "costEstimationEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        jsii.set(self, "email", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ownersTeamSamlRoleId")
    def owners_team_saml_role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownersTeamSamlRoleId"))

    @owners_team_saml_role_id.setter
    def owners_team_saml_role_id(self, value: builtins.str) -> None:
        jsii.set(self, "ownersTeamSamlRoleId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sendPassingStatusesForUntriggeredSpeculativePlans")
    def send_passing_statuses_for_untriggered_speculative_plans(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "sendPassingStatusesForUntriggeredSpeculativePlans"))

    @send_passing_statuses_for_untriggered_speculative_plans.setter
    def send_passing_statuses_for_untriggered_speculative_plans(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "sendPassingStatusesForUntriggeredSpeculativePlans", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionRememberMinutes")
    def session_remember_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionRememberMinutes"))

    @session_remember_minutes.setter
    def session_remember_minutes(self, value: jsii.Number) -> None:
        jsii.set(self, "sessionRememberMinutes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sessionTimeoutMinutes")
    def session_timeout_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionTimeoutMinutes"))

    @session_timeout_minutes.setter
    def session_timeout_minutes(self, value: jsii.Number) -> None:
        jsii.set(self, "sessionTimeoutMinutes", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.OrganizationConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "email": "email",
        "name": "name",
        "collaborator_auth_policy": "collaboratorAuthPolicy",
        "cost_estimation_enabled": "costEstimationEnabled",
        "id": "id",
        "owners_team_saml_role_id": "ownersTeamSamlRoleId",
        "send_passing_statuses_for_untriggered_speculative_plans": "sendPassingStatusesForUntriggeredSpeculativePlans",
        "session_remember_minutes": "sessionRememberMinutes",
        "session_timeout_minutes": "sessionTimeoutMinutes",
    },
)
class OrganizationConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        email: builtins.str,
        name: builtins.str,
        collaborator_auth_policy: typing.Optional[builtins.str] = None,
        cost_estimation_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        owners_team_saml_role_id: typing.Optional[builtins.str] = None,
        send_passing_statuses_for_untriggered_speculative_plans: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        session_remember_minutes: typing.Optional[jsii.Number] = None,
        session_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#email Organization#email}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#name Organization#name}.
        :param collaborator_auth_policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#collaborator_auth_policy Organization#collaborator_auth_policy}.
        :param cost_estimation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#cost_estimation_enabled Organization#cost_estimation_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#id Organization#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owners_team_saml_role_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#owners_team_saml_role_id Organization#owners_team_saml_role_id}.
        :param send_passing_statuses_for_untriggered_speculative_plans: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#send_passing_statuses_for_untriggered_speculative_plans Organization#send_passing_statuses_for_untriggered_speculative_plans}.
        :param session_remember_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#session_remember_minutes Organization#session_remember_minutes}.
        :param session_timeout_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#session_timeout_minutes Organization#session_timeout_minutes}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "email": email,
            "name": name,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if collaborator_auth_policy is not None:
            self._values["collaborator_auth_policy"] = collaborator_auth_policy
        if cost_estimation_enabled is not None:
            self._values["cost_estimation_enabled"] = cost_estimation_enabled
        if id is not None:
            self._values["id"] = id
        if owners_team_saml_role_id is not None:
            self._values["owners_team_saml_role_id"] = owners_team_saml_role_id
        if send_passing_statuses_for_untriggered_speculative_plans is not None:
            self._values["send_passing_statuses_for_untriggered_speculative_plans"] = send_passing_statuses_for_untriggered_speculative_plans
        if session_remember_minutes is not None:
            self._values["session_remember_minutes"] = session_remember_minutes
        if session_timeout_minutes is not None:
            self._values["session_timeout_minutes"] = session_timeout_minutes

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#email Organization#email}.'''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#name Organization#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collaborator_auth_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#collaborator_auth_policy Organization#collaborator_auth_policy}.'''
        result = self._values.get("collaborator_auth_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cost_estimation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#cost_estimation_enabled Organization#cost_estimation_enabled}.'''
        result = self._values.get("cost_estimation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#id Organization#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owners_team_saml_role_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#owners_team_saml_role_id Organization#owners_team_saml_role_id}.'''
        result = self._values.get("owners_team_saml_role_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def send_passing_statuses_for_untriggered_speculative_plans(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#send_passing_statuses_for_untriggered_speculative_plans Organization#send_passing_statuses_for_untriggered_speculative_plans}.'''
        result = self._values.get("send_passing_statuses_for_untriggered_speculative_plans")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def session_remember_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#session_remember_minutes Organization#session_remember_minutes}.'''
        result = self._values.get("session_remember_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization#session_timeout_minutes Organization#session_timeout_minutes}.'''
        result = self._values.get("session_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationMembership(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.OrganizationMembership",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership tfe_organization_membership}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        email: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership tfe_organization_membership} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#email OrganizationMembership#email}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#organization OrganizationMembership#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#id OrganizationMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = OrganizationMembershipConfig(
            email=email,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="userId")
    def user_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        jsii.set(self, "email", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.OrganizationMembershipConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "email": "email",
        "organization": "organization",
        "id": "id",
    },
)
class OrganizationMembershipConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        email: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#email OrganizationMembership#email}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#organization OrganizationMembership#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#id OrganizationMembership#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "email": email,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def email(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#email OrganizationMembership#email}.'''
        result = self._values.get("email")
        assert result is not None, "Required property 'email' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#organization OrganizationMembership#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_membership#id OrganizationMembership#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationMembershipConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationModuleSharing(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.OrganizationModuleSharing",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing tfe_organization_module_sharing}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        module_consumers: typing.Sequence[builtins.str],
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing tfe_organization_module_sharing} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param module_consumers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#module_consumers OrganizationModuleSharing#module_consumers}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#organization OrganizationModuleSharing#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#id OrganizationModuleSharing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = OrganizationModuleSharingConfig(
            module_consumers=module_consumers,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="moduleConsumersInput")
    def module_consumers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "moduleConsumersInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="moduleConsumers")
    def module_consumers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "moduleConsumers"))

    @module_consumers.setter
    def module_consumers(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "moduleConsumers", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.OrganizationModuleSharingConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "module_consumers": "moduleConsumers",
        "organization": "organization",
        "id": "id",
    },
)
class OrganizationModuleSharingConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        module_consumers: typing.Sequence[builtins.str],
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param module_consumers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#module_consumers OrganizationModuleSharing#module_consumers}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#organization OrganizationModuleSharing#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#id OrganizationModuleSharing#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "module_consumers": module_consumers,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def module_consumers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#module_consumers OrganizationModuleSharing#module_consumers}.'''
        result = self._values.get("module_consumers")
        assert result is not None, "Required property 'module_consumers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#organization OrganizationModuleSharing#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_module_sharing#id OrganizationModuleSharing#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationModuleSharingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationRunTask(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.OrganizationRunTask",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task tfe_organization_run_task}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        url: builtins.str,
        category: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        hmac_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task tfe_organization_run_task} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#name OrganizationRunTask#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#organization OrganizationRunTask#organization}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#url OrganizationRunTask#url}.
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#category OrganizationRunTask#category}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#enabled OrganizationRunTask#enabled}.
        :param hmac_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#hmac_key OrganizationRunTask#hmac_key}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#id OrganizationRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = OrganizationRunTaskConfig(
            name=name,
            organization=organization,
            url=url,
            category=category,
            enabled=enabled,
            hmac_key=hmac_key,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetCategory")
    def reset_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategory", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetHmacKey")
    def reset_hmac_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHmacKey", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hmacKeyInput")
    def hmac_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hmacKeyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        jsii.set(self, "category", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hmacKey")
    def hmac_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hmacKey"))

    @hmac_key.setter
    def hmac_key(self, value: builtins.str) -> None:
        jsii.set(self, "hmacKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        jsii.set(self, "url", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.OrganizationRunTaskConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "url": "url",
        "category": "category",
        "enabled": "enabled",
        "hmac_key": "hmacKey",
        "id": "id",
    },
)
class OrganizationRunTaskConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        url: builtins.str,
        category: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        hmac_key: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#name OrganizationRunTask#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#organization OrganizationRunTask#organization}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#url OrganizationRunTask#url}.
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#category OrganizationRunTask#category}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#enabled OrganizationRunTask#enabled}.
        :param hmac_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#hmac_key OrganizationRunTask#hmac_key}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#id OrganizationRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
            "url": url,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if category is not None:
            self._values["category"] = category
        if enabled is not None:
            self._values["enabled"] = enabled
        if hmac_key is not None:
            self._values["hmac_key"] = hmac_key
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#name OrganizationRunTask#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#organization OrganizationRunTask#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#url OrganizationRunTask#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def category(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#category OrganizationRunTask#category}.'''
        result = self._values.get("category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#enabled OrganizationRunTask#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def hmac_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#hmac_key OrganizationRunTask#hmac_key}.'''
        result = self._values.get("hmac_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_run_task#id OrganizationRunTask#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationRunTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationToken(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.OrganizationToken",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/organization_token tfe_organization_token}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        organization: builtins.str,
        force_regenerate: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/organization_token tfe_organization_token} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#organization OrganizationToken#organization}.
        :param force_regenerate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#force_regenerate OrganizationToken#force_regenerate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#id OrganizationToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = OrganizationTokenConfig(
            organization=organization,
            force_regenerate=force_regenerate,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetForceRegenerate")
    def reset_force_regenerate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceRegenerate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="forceRegenerateInput")
    def force_regenerate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "forceRegenerateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="forceRegenerate")
    def force_regenerate(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "forceRegenerate"))

    @force_regenerate.setter
    def force_regenerate(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "forceRegenerate", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.OrganizationTokenConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "organization": "organization",
        "force_regenerate": "forceRegenerate",
        "id": "id",
    },
)
class OrganizationTokenConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        organization: builtins.str,
        force_regenerate: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#organization OrganizationToken#organization}.
        :param force_regenerate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#force_regenerate OrganizationToken#force_regenerate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#id OrganizationToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if force_regenerate is not None:
            self._values["force_regenerate"] = force_regenerate
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#organization OrganizationToken#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def force_regenerate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#force_regenerate OrganizationToken#force_regenerate}.'''
        result = self._values.get("force_regenerate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/organization_token#id OrganizationToken#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicySet(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.PolicySet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/policy_set tfe_policy_set}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        description: typing.Optional[builtins.str] = None,
        global_: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        policies_path: typing.Optional[builtins.str] = None,
        policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        slug: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vcs_repo: typing.Optional["PolicySetVcsRepo"] = None,
        workspace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/policy_set tfe_policy_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#name PolicySet#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#organization PolicySet#organization}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#description PolicySet#description}.
        :param global_: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#global PolicySet#global}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#id PolicySet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policies_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#policies_path PolicySet#policies_path}.
        :param policy_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#policy_ids PolicySet#policy_ids}.
        :param slug: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#slug PolicySet#slug}.
        :param vcs_repo: vcs_repo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#vcs_repo PolicySet#vcs_repo}
        :param workspace_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#workspace_ids PolicySet#workspace_ids}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = PolicySetConfig(
            name=name,
            organization=organization,
            description=description,
            global_=global_,
            id=id,
            policies_path=policies_path,
            policy_ids=policy_ids,
            slug=slug,
            vcs_repo=vcs_repo,
            workspace_ids=workspace_ids,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putVcsRepo")
    def put_vcs_repo(
        self,
        *,
        identifier: builtins.str,
        oauth_token_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        ingress_submodules: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#identifier PolicySet#identifier}.
        :param oauth_token_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#oauth_token_id PolicySet#oauth_token_id}.
        :param branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#branch PolicySet#branch}.
        :param ingress_submodules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#ingress_submodules PolicySet#ingress_submodules}.
        '''
        value = PolicySetVcsRepo(
            identifier=identifier,
            oauth_token_id=oauth_token_id,
            branch=branch,
            ingress_submodules=ingress_submodules,
        )

        return typing.cast(None, jsii.invoke(self, "putVcsRepo", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGlobal")
    def reset_global(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobal", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPoliciesPath")
    def reset_policies_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPoliciesPath", []))

    @jsii.member(jsii_name="resetPolicyIds")
    def reset_policy_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyIds", []))

    @jsii.member(jsii_name="resetSlug")
    def reset_slug(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSlug", []))

    @jsii.member(jsii_name="resetVcsRepo")
    def reset_vcs_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVcsRepo", []))

    @jsii.member(jsii_name="resetWorkspaceIds")
    def reset_workspace_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceIds", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcsRepo")
    def vcs_repo(self) -> "PolicySetVcsRepoOutputReference":
        return typing.cast("PolicySetVcsRepoOutputReference", jsii.get(self, "vcsRepo"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="globalInput")
    def global_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "globalInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policiesPathInput")
    def policies_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policiesPathInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyIdsInput")
    def policy_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "policyIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slugInput")
    def slug_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "slugInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcsRepoInput")
    def vcs_repo_input(self) -> typing.Optional["PolicySetVcsRepo"]:
        return typing.cast(typing.Optional["PolicySetVcsRepo"], jsii.get(self, "vcsRepoInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdsInput")
    def workspace_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "workspaceIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="global")
    def global_(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "global"))

    @global_.setter
    def global_(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "global", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policiesPath")
    def policies_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policiesPath"))

    @policies_path.setter
    def policies_path(self, value: builtins.str) -> None:
        jsii.set(self, "policiesPath", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyIds")
    def policy_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "policyIds"))

    @policy_ids.setter
    def policy_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "policyIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slug")
    def slug(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "slug"))

    @slug.setter
    def slug(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        jsii.set(self, "slug", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIds")
    def workspace_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "workspaceIds"))

    @workspace_ids.setter
    def workspace_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "workspaceIds", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.PolicySetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "description": "description",
        "global_": "global",
        "id": "id",
        "policies_path": "policiesPath",
        "policy_ids": "policyIds",
        "slug": "slug",
        "vcs_repo": "vcsRepo",
        "workspace_ids": "workspaceIds",
    },
)
class PolicySetConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        description: typing.Optional[builtins.str] = None,
        global_: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        policies_path: typing.Optional[builtins.str] = None,
        policy_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        slug: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vcs_repo: typing.Optional["PolicySetVcsRepo"] = None,
        workspace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#name PolicySet#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#organization PolicySet#organization}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#description PolicySet#description}.
        :param global_: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#global PolicySet#global}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#id PolicySet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policies_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#policies_path PolicySet#policies_path}.
        :param policy_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#policy_ids PolicySet#policy_ids}.
        :param slug: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#slug PolicySet#slug}.
        :param vcs_repo: vcs_repo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#vcs_repo PolicySet#vcs_repo}
        :param workspace_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#workspace_ids PolicySet#workspace_ids}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(vcs_repo, dict):
            vcs_repo = PolicySetVcsRepo(**vcs_repo)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if global_ is not None:
            self._values["global_"] = global_
        if id is not None:
            self._values["id"] = id
        if policies_path is not None:
            self._values["policies_path"] = policies_path
        if policy_ids is not None:
            self._values["policy_ids"] = policy_ids
        if slug is not None:
            self._values["slug"] = slug
        if vcs_repo is not None:
            self._values["vcs_repo"] = vcs_repo
        if workspace_ids is not None:
            self._values["workspace_ids"] = workspace_ids

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#name PolicySet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#organization PolicySet#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#description PolicySet#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#global PolicySet#global}.'''
        result = self._values.get("global_")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#id PolicySet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#policies_path PolicySet#policies_path}.'''
        result = self._values.get("policies_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#policy_ids PolicySet#policy_ids}.'''
        result = self._values.get("policy_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def slug(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#slug PolicySet#slug}.'''
        result = self._values.get("slug")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vcs_repo(self) -> typing.Optional["PolicySetVcsRepo"]:
        '''vcs_repo block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#vcs_repo PolicySet#vcs_repo}
        '''
        result = self._values.get("vcs_repo")
        return typing.cast(typing.Optional["PolicySetVcsRepo"], result)

    @builtins.property
    def workspace_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#workspace_ids PolicySet#workspace_ids}.'''
        result = self._values.get("workspace_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicySetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicySetParameter(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.PolicySetParameter",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter tfe_policy_set_parameter}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        key: builtins.str,
        policy_set_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        sensitive: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter tfe_policy_set_parameter} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#key PolicySetParameter#key}.
        :param policy_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#policy_set_id PolicySetParameter#policy_set_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#id PolicySetParameter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sensitive: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#sensitive PolicySetParameter#sensitive}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#value PolicySetParameter#value}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = PolicySetParameterConfig(
            key=key,
            policy_set_id=policy_set_id,
            id=id,
            sensitive=sensitive,
            value=value,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSensitive")
    def reset_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitive", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policySetIdInput")
    def policy_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policySetIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sensitiveInput")
    def sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "sensitiveInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        jsii.set(self, "key", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policySetId")
    def policy_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policySetId"))

    @policy_set_id.setter
    def policy_set_id(self, value: builtins.str) -> None:
        jsii.set(self, "policySetId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "sensitive"))

    @sensitive.setter
    def sensitive(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "sensitive", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        jsii.set(self, "value", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.PolicySetParameterConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "key": "key",
        "policy_set_id": "policySetId",
        "id": "id",
        "sensitive": "sensitive",
        "value": "value",
    },
)
class PolicySetParameterConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        key: builtins.str,
        policy_set_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        sensitive: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#key PolicySetParameter#key}.
        :param policy_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#policy_set_id PolicySetParameter#policy_set_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#id PolicySetParameter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sensitive: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#sensitive PolicySetParameter#sensitive}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#value PolicySetParameter#value}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "policy_set_id": policy_set_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id
        if sensitive is not None:
            self._values["sensitive"] = sensitive
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#key PolicySetParameter#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_set_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#policy_set_id PolicySetParameter#policy_set_id}.'''
        result = self._values.get("policy_set_id")
        assert result is not None, "Required property 'policy_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#id PolicySetParameter#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#sensitive PolicySetParameter#sensitive}.'''
        result = self._values.get("sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set_parameter#value PolicySetParameter#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicySetParameterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.PolicySetVcsRepo",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "oauth_token_id": "oauthTokenId",
        "branch": "branch",
        "ingress_submodules": "ingressSubmodules",
    },
)
class PolicySetVcsRepo:
    def __init__(
        self,
        *,
        identifier: builtins.str,
        oauth_token_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        ingress_submodules: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#identifier PolicySet#identifier}.
        :param oauth_token_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#oauth_token_id PolicySet#oauth_token_id}.
        :param branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#branch PolicySet#branch}.
        :param ingress_submodules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#ingress_submodules PolicySet#ingress_submodules}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "identifier": identifier,
            "oauth_token_id": oauth_token_id,
        }
        if branch is not None:
            self._values["branch"] = branch
        if ingress_submodules is not None:
            self._values["ingress_submodules"] = ingress_submodules

    @builtins.property
    def identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#identifier PolicySet#identifier}.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_token_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#oauth_token_id PolicySet#oauth_token_id}.'''
        result = self._values.get("oauth_token_id")
        assert result is not None, "Required property 'oauth_token_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#branch PolicySet#branch}.'''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_submodules(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/policy_set#ingress_submodules PolicySet#ingress_submodules}.'''
        result = self._values.get("ingress_submodules")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicySetVcsRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicySetVcsRepoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.PolicySetVcsRepoOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetIngressSubmodules")
    def reset_ingress_submodules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressSubmodules", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ingressSubmodulesInput")
    def ingress_submodules_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "ingressSubmodulesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenIdInput")
    def oauth_token_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthTokenIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        jsii.set(self, "branch", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        jsii.set(self, "identifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ingressSubmodules")
    def ingress_submodules(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "ingressSubmodules"))

    @ingress_submodules.setter
    def ingress_submodules(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "ingressSubmodules", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenId")
    def oauth_token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenId"))

    @oauth_token_id.setter
    def oauth_token_id(self, value: builtins.str) -> None:
        jsii.set(self, "oauthTokenId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PolicySetVcsRepo]:
        return typing.cast(typing.Optional[PolicySetVcsRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[PolicySetVcsRepo]) -> None:
        jsii.set(self, "internalValue", value)


class RegistryModule(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.RegistryModule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/registry_module tfe_registry_module}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        vcs_repo: "RegistryModuleVcsRepo",
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/registry_module tfe_registry_module} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param vcs_repo: vcs_repo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#vcs_repo RegistryModule#vcs_repo}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#id RegistryModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = RegistryModuleConfig(
            vcs_repo=vcs_repo,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putVcsRepo")
    def put_vcs_repo(
        self,
        *,
        display_identifier: builtins.str,
        identifier: builtins.str,
        oauth_token_id: builtins.str,
    ) -> None:
        '''
        :param display_identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#display_identifier RegistryModule#display_identifier}.
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#identifier RegistryModule#identifier}.
        :param oauth_token_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#oauth_token_id RegistryModule#oauth_token_id}.
        '''
        value = RegistryModuleVcsRepo(
            display_identifier=display_identifier,
            identifier=identifier,
            oauth_token_id=oauth_token_id,
        )

        return typing.cast(None, jsii.invoke(self, "putVcsRepo", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="moduleProvider")
    def module_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "moduleProvider"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcsRepo")
    def vcs_repo(self) -> "RegistryModuleVcsRepoOutputReference":
        return typing.cast("RegistryModuleVcsRepoOutputReference", jsii.get(self, "vcsRepo"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcsRepoInput")
    def vcs_repo_input(self) -> typing.Optional["RegistryModuleVcsRepo"]:
        return typing.cast(typing.Optional["RegistryModuleVcsRepo"], jsii.get(self, "vcsRepoInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.RegistryModuleConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "vcs_repo": "vcsRepo",
        "id": "id",
    },
)
class RegistryModuleConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        vcs_repo: "RegistryModuleVcsRepo",
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param vcs_repo: vcs_repo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#vcs_repo RegistryModule#vcs_repo}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#id RegistryModule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(vcs_repo, dict):
            vcs_repo = RegistryModuleVcsRepo(**vcs_repo)
        self._values: typing.Dict[str, typing.Any] = {
            "vcs_repo": vcs_repo,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def vcs_repo(self) -> "RegistryModuleVcsRepo":
        '''vcs_repo block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#vcs_repo RegistryModule#vcs_repo}
        '''
        result = self._values.get("vcs_repo")
        assert result is not None, "Required property 'vcs_repo' is missing"
        return typing.cast("RegistryModuleVcsRepo", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#id RegistryModule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryModuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.RegistryModuleVcsRepo",
    jsii_struct_bases=[],
    name_mapping={
        "display_identifier": "displayIdentifier",
        "identifier": "identifier",
        "oauth_token_id": "oauthTokenId",
    },
)
class RegistryModuleVcsRepo:
    def __init__(
        self,
        *,
        display_identifier: builtins.str,
        identifier: builtins.str,
        oauth_token_id: builtins.str,
    ) -> None:
        '''
        :param display_identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#display_identifier RegistryModule#display_identifier}.
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#identifier RegistryModule#identifier}.
        :param oauth_token_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#oauth_token_id RegistryModule#oauth_token_id}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "display_identifier": display_identifier,
            "identifier": identifier,
            "oauth_token_id": oauth_token_id,
        }

    @builtins.property
    def display_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#display_identifier RegistryModule#display_identifier}.'''
        result = self._values.get("display_identifier")
        assert result is not None, "Required property 'display_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#identifier RegistryModule#identifier}.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_token_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/registry_module#oauth_token_id RegistryModule#oauth_token_id}.'''
        result = self._values.get("oauth_token_id")
        assert result is not None, "Required property 'oauth_token_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryModuleVcsRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RegistryModuleVcsRepoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.RegistryModuleVcsRepoOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayIdentifierInput")
    def display_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayIdentifierInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenIdInput")
    def oauth_token_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthTokenIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="displayIdentifier")
    def display_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayIdentifier"))

    @display_identifier.setter
    def display_identifier(self, value: builtins.str) -> None:
        jsii.set(self, "displayIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        jsii.set(self, "identifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenId")
    def oauth_token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenId"))

    @oauth_token_id.setter
    def oauth_token_id(self, value: builtins.str) -> None:
        jsii.set(self, "oauthTokenId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RegistryModuleVcsRepo]:
        return typing.cast(typing.Optional[RegistryModuleVcsRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RegistryModuleVcsRepo]) -> None:
        jsii.set(self, "internalValue", value)


class RunTrigger(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.RunTrigger",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger tfe_run_trigger}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        sourceable_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger tfe_run_trigger} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param sourceable_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#sourceable_id RunTrigger#sourceable_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#workspace_id RunTrigger#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#id RunTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = RunTriggerConfig(
            sourceable_id=sourceable_id,
            workspace_id=workspace_id,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceableIdInput")
    def sourceable_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceableIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceableId")
    def sourceable_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceableId"))

    @sourceable_id.setter
    def sourceable_id(self, value: builtins.str) -> None:
        jsii.set(self, "sourceableId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.RunTriggerConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "sourceable_id": "sourceableId",
        "workspace_id": "workspaceId",
        "id": "id",
    },
)
class RunTriggerConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        sourceable_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param sourceable_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#sourceable_id RunTrigger#sourceable_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#workspace_id RunTrigger#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#id RunTrigger#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "sourceable_id": sourceable_id,
            "workspace_id": workspace_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def sourceable_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#sourceable_id RunTrigger#sourceable_id}.'''
        result = self._values.get("sourceable_id")
        assert result is not None, "Required property 'sourceable_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#workspace_id RunTrigger#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/run_trigger#id RunTrigger#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunTriggerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SentinelPolicy(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.SentinelPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy tfe_sentinel_policy}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enforce_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy tfe_sentinel_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#name SentinelPolicy#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#organization SentinelPolicy#organization}.
        :param policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#policy SentinelPolicy#policy}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#description SentinelPolicy#description}.
        :param enforce_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#enforce_mode SentinelPolicy#enforce_mode}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#id SentinelPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = SentinelPolicyConfig(
            name=name,
            organization=organization,
            policy=policy,
            description=description,
            enforce_mode=enforce_mode,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnforceMode")
    def reset_enforce_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforceMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enforceModeInput")
    def enforce_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforceModeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enforceMode")
    def enforce_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforceMode"))

    @enforce_mode.setter
    def enforce_mode(self, value: builtins.str) -> None:
        jsii.set(self, "enforceMode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        jsii.set(self, "policy", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.SentinelPolicyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "policy": "policy",
        "description": "description",
        "enforce_mode": "enforceMode",
        "id": "id",
    },
)
class SentinelPolicyConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        policy: builtins.str,
        description: typing.Optional[builtins.str] = None,
        enforce_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#name SentinelPolicy#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#organization SentinelPolicy#organization}.
        :param policy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#policy SentinelPolicy#policy}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#description SentinelPolicy#description}.
        :param enforce_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#enforce_mode SentinelPolicy#enforce_mode}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#id SentinelPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
            "policy": policy,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if enforce_mode is not None:
            self._values["enforce_mode"] = enforce_mode
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#name SentinelPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#organization SentinelPolicy#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#policy SentinelPolicy#policy}.'''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#description SentinelPolicy#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#enforce_mode SentinelPolicy#enforce_mode}.'''
        result = self._values.get("enforce_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/sentinel_policy#id SentinelPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SentinelPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SshKey(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.SshKey",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key tfe_ssh_key}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        key: builtins.str,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key tfe_ssh_key} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#key SshKey#key}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#name SshKey#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#organization SshKey#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#id SshKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = SshKeyConfig(
            key=key,
            name=name,
            organization=organization,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        jsii.set(self, "key", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.SshKeyConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "key": "key",
        "name": "name",
        "organization": "organization",
        "id": "id",
    },
)
class SshKeyConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        key: builtins.str,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#key SshKey#key}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#name SshKey#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#organization SshKey#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#id SshKey#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#key SshKey#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#name SshKey#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#organization SshKey#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/ssh_key#id SshKey#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SshKeyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Team(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.Team",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/team tfe_team}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        organization_access: typing.Optional["TeamOrganizationAccess"] = None,
        sso_team_id: typing.Optional[builtins.str] = None,
        visibility: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/team tfe_team} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#name Team#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#organization Team#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#id Team#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param organization_access: organization_access block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#organization_access Team#organization_access}
        :param sso_team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#sso_team_id Team#sso_team_id}.
        :param visibility: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#visibility Team#visibility}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamConfig(
            name=name,
            organization=organization,
            id=id,
            organization_access=organization_access,
            sso_team_id=sso_team_id,
            visibility=visibility,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putOrganizationAccess")
    def put_organization_access(
        self,
        *,
        manage_modules: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_policies: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_policy_overrides: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_providers: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_run_tasks: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_vcs_settings: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_workspaces: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param manage_modules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_modules Team#manage_modules}.
        :param manage_policies: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_policies Team#manage_policies}.
        :param manage_policy_overrides: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_policy_overrides Team#manage_policy_overrides}.
        :param manage_providers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_providers Team#manage_providers}.
        :param manage_run_tasks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_run_tasks Team#manage_run_tasks}.
        :param manage_vcs_settings: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_vcs_settings Team#manage_vcs_settings}.
        :param manage_workspaces: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_workspaces Team#manage_workspaces}.
        '''
        value = TeamOrganizationAccess(
            manage_modules=manage_modules,
            manage_policies=manage_policies,
            manage_policy_overrides=manage_policy_overrides,
            manage_providers=manage_providers,
            manage_run_tasks=manage_run_tasks,
            manage_vcs_settings=manage_vcs_settings,
            manage_workspaces=manage_workspaces,
        )

        return typing.cast(None, jsii.invoke(self, "putOrganizationAccess", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOrganizationAccess")
    def reset_organization_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationAccess", []))

    @jsii.member(jsii_name="resetSsoTeamId")
    def reset_sso_team_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsoTeamId", []))

    @jsii.member(jsii_name="resetVisibility")
    def reset_visibility(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisibility", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationAccess")
    def organization_access(self) -> "TeamOrganizationAccessOutputReference":
        return typing.cast("TeamOrganizationAccessOutputReference", jsii.get(self, "organizationAccess"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationAccessInput")
    def organization_access_input(self) -> typing.Optional["TeamOrganizationAccess"]:
        return typing.cast(typing.Optional["TeamOrganizationAccess"], jsii.get(self, "organizationAccessInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ssoTeamIdInput")
    def sso_team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoTeamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="visibilityInput")
    def visibility_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visibilityInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ssoTeamId")
    def sso_team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoTeamId"))

    @sso_team_id.setter
    def sso_team_id(self, value: builtins.str) -> None:
        jsii.set(self, "ssoTeamId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="visibility")
    def visibility(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visibility"))

    @visibility.setter
    def visibility(self, value: builtins.str) -> None:
        jsii.set(self, "visibility", value)


class TeamAccess(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamAccess",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/team_access tfe_team_access}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        team_id: builtins.str,
        workspace_id: builtins.str,
        access: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence["TeamAccessPermissions"]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/team_access tfe_team_access} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#team_id TeamAccess#team_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#workspace_id TeamAccess#workspace_id}.
        :param access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#access TeamAccess#access}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#id TeamAccess#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#permissions TeamAccess#permissions}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamAccessConfig(
            team_id=team_id,
            workspace_id=workspace_id,
            access=access,
            id=id,
            permissions=permissions,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence["TeamAccessPermissions"]],
    ) -> None:
        '''
        :param value: -
        '''
        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="resetAccess")
    def reset_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccess", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "TeamAccessPermissionsList":
        return typing.cast("TeamAccessPermissionsList", jsii.get(self, "permissions"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["TeamAccessPermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["TeamAccessPermissions"]]], jsii.get(self, "permissionsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="access")
    def access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "access"))

    @access.setter
    def access(self, value: builtins.str) -> None:
        jsii.set(self, "access", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamAccessConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "team_id": "teamId",
        "workspace_id": "workspaceId",
        "access": "access",
        "id": "id",
        "permissions": "permissions",
    },
)
class TeamAccessConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        team_id: builtins.str,
        workspace_id: builtins.str,
        access: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Union[cdktf.IResolvable, typing.Sequence["TeamAccessPermissions"]]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#team_id TeamAccess#team_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#workspace_id TeamAccess#workspace_id}.
        :param access: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#access TeamAccess#access}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#id TeamAccess#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#permissions TeamAccess#permissions}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "team_id": team_id,
            "workspace_id": workspace_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if access is not None:
            self._values["access"] = access
        if id is not None:
            self._values["id"] = id
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#team_id TeamAccess#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#workspace_id TeamAccess#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#access TeamAccess#access}.'''
        result = self._values.get("access")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#id TeamAccess#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["TeamAccessPermissions"]]]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#permissions TeamAccess#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["TeamAccessPermissions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamAccessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamAccessPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "runs": "runs",
        "run_tasks": "runTasks",
        "sentinel_mocks": "sentinelMocks",
        "state_versions": "stateVersions",
        "variables": "variables",
        "workspace_locking": "workspaceLocking",
    },
)
class TeamAccessPermissions:
    def __init__(
        self,
        *,
        runs: builtins.str,
        run_tasks: typing.Union[builtins.bool, cdktf.IResolvable],
        sentinel_mocks: builtins.str,
        state_versions: builtins.str,
        variables: builtins.str,
        workspace_locking: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        '''
        :param runs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#runs TeamAccess#runs}.
        :param run_tasks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#run_tasks TeamAccess#run_tasks}.
        :param sentinel_mocks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#sentinel_mocks TeamAccess#sentinel_mocks}.
        :param state_versions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#state_versions TeamAccess#state_versions}.
        :param variables: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#variables TeamAccess#variables}.
        :param workspace_locking: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#workspace_locking TeamAccess#workspace_locking}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "runs": runs,
            "run_tasks": run_tasks,
            "sentinel_mocks": sentinel_mocks,
            "state_versions": state_versions,
            "variables": variables,
            "workspace_locking": workspace_locking,
        }

    @builtins.property
    def runs(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#runs TeamAccess#runs}.'''
        result = self._values.get("runs")
        assert result is not None, "Required property 'runs' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def run_tasks(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#run_tasks TeamAccess#run_tasks}.'''
        result = self._values.get("run_tasks")
        assert result is not None, "Required property 'run_tasks' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    @builtins.property
    def sentinel_mocks(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#sentinel_mocks TeamAccess#sentinel_mocks}.'''
        result = self._values.get("sentinel_mocks")
        assert result is not None, "Required property 'sentinel_mocks' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state_versions(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#state_versions TeamAccess#state_versions}.'''
        result = self._values.get("state_versions")
        assert result is not None, "Required property 'state_versions' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def variables(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#variables TeamAccess#variables}.'''
        result = self._values.get("variables")
        assert result is not None, "Required property 'variables' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_locking(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_access#workspace_locking TeamAccess#workspace_locking}.'''
        result = self._values.get("workspace_locking")
        assert result is not None, "Required property 'workspace_locking' is missing"
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamAccessPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamAccessPermissionsList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamAccessPermissionsList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TeamAccessPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("TeamAccessPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[TeamAccessPermissions]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[TeamAccessPermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[TeamAccessPermissions]]],
    ) -> None:
        jsii.set(self, "internalValue", value)


class TeamAccessPermissionsOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamAccessPermissionsOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runsInput")
    def runs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runTasksInput")
    def run_tasks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "runTasksInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sentinelMocksInput")
    def sentinel_mocks_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sentinelMocksInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateVersionsInput")
    def state_versions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateVersionsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variablesInput")
    def variables_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variablesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceLockingInput")
    def workspace_locking_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "workspaceLockingInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runs")
    def runs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runs"))

    @runs.setter
    def runs(self, value: builtins.str) -> None:
        jsii.set(self, "runs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runTasks")
    def run_tasks(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "runTasks"))

    @run_tasks.setter
    def run_tasks(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "runTasks", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sentinelMocks")
    def sentinel_mocks(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sentinelMocks"))

    @sentinel_mocks.setter
    def sentinel_mocks(self, value: builtins.str) -> None:
        jsii.set(self, "sentinelMocks", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stateVersions")
    def state_versions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateVersions"))

    @state_versions.setter
    def state_versions(self, value: builtins.str) -> None:
        jsii.set(self, "stateVersions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variables")
    def variables(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variables"))

    @variables.setter
    def variables(self, value: builtins.str) -> None:
        jsii.set(self, "variables", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceLocking")
    def workspace_locking(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "workspaceLocking"))

    @workspace_locking.setter
    def workspace_locking(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "workspaceLocking", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, TeamAccessPermissions]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, TeamAccessPermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, TeamAccessPermissions]],
    ) -> None:
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "id": "id",
        "organization_access": "organizationAccess",
        "sso_team_id": "ssoTeamId",
        "visibility": "visibility",
    },
)
class TeamConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        id: typing.Optional[builtins.str] = None,
        organization_access: typing.Optional["TeamOrganizationAccess"] = None,
        sso_team_id: typing.Optional[builtins.str] = None,
        visibility: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#name Team#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#organization Team#organization}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#id Team#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param organization_access: organization_access block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#organization_access Team#organization_access}
        :param sso_team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#sso_team_id Team#sso_team_id}.
        :param visibility: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#visibility Team#visibility}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(organization_access, dict):
            organization_access = TeamOrganizationAccess(**organization_access)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id
        if organization_access is not None:
            self._values["organization_access"] = organization_access
        if sso_team_id is not None:
            self._values["sso_team_id"] = sso_team_id
        if visibility is not None:
            self._values["visibility"] = visibility

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#name Team#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#organization Team#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#id Team#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_access(self) -> typing.Optional["TeamOrganizationAccess"]:
        '''organization_access block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#organization_access Team#organization_access}
        '''
        result = self._values.get("organization_access")
        return typing.cast(typing.Optional["TeamOrganizationAccess"], result)

    @builtins.property
    def sso_team_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#sso_team_id Team#sso_team_id}.'''
        result = self._values.get("sso_team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visibility(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#visibility Team#visibility}.'''
        result = self._values.get("visibility")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamMember(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamMember",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/team_member tfe_team_member}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        team_id: builtins.str,
        username: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/team_member tfe_team_member} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#team_id TeamMember#team_id}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#username TeamMember#username}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#id TeamMember#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamMemberConfig(
            team_id=team_id,
            username=username,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        jsii.set(self, "username", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamMemberConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "team_id": "teamId",
        "username": "username",
        "id": "id",
    },
)
class TeamMemberConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        team_id: builtins.str,
        username: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#team_id TeamMember#team_id}.
        :param username: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#username TeamMember#username}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#id TeamMember#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "team_id": team_id,
            "username": username,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#team_id TeamMember#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#username TeamMember#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_member#id TeamMember#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamMemberConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamMembers(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamMembers",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/team_members tfe_team_members}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        team_id: builtins.str,
        usernames: typing.Sequence[builtins.str],
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/team_members tfe_team_members} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#team_id TeamMembers#team_id}.
        :param usernames: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#usernames TeamMembers#usernames}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#id TeamMembers#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamMembersConfig(
            team_id=team_id,
            usernames=usernames,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="usernamesInput")
    def usernames_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "usernamesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        jsii.set(self, "teamId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="usernames")
    def usernames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "usernames"))

    @usernames.setter
    def usernames(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "usernames", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamMembersConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "team_id": "teamId",
        "usernames": "usernames",
        "id": "id",
    },
)
class TeamMembersConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        team_id: builtins.str,
        usernames: typing.Sequence[builtins.str],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#team_id TeamMembers#team_id}.
        :param usernames: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#usernames TeamMembers#usernames}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#id TeamMembers#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "team_id": team_id,
            "usernames": usernames,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#team_id TeamMembers#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def usernames(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#usernames TeamMembers#usernames}.'''
        result = self._values.get("usernames")
        assert result is not None, "Required property 'usernames' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_members#id TeamMembers#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamMembersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamOrganizationAccess",
    jsii_struct_bases=[],
    name_mapping={
        "manage_modules": "manageModules",
        "manage_policies": "managePolicies",
        "manage_policy_overrides": "managePolicyOverrides",
        "manage_providers": "manageProviders",
        "manage_run_tasks": "manageRunTasks",
        "manage_vcs_settings": "manageVcsSettings",
        "manage_workspaces": "manageWorkspaces",
    },
)
class TeamOrganizationAccess:
    def __init__(
        self,
        *,
        manage_modules: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_policies: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_policy_overrides: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_providers: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_run_tasks: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_vcs_settings: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        manage_workspaces: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param manage_modules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_modules Team#manage_modules}.
        :param manage_policies: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_policies Team#manage_policies}.
        :param manage_policy_overrides: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_policy_overrides Team#manage_policy_overrides}.
        :param manage_providers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_providers Team#manage_providers}.
        :param manage_run_tasks: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_run_tasks Team#manage_run_tasks}.
        :param manage_vcs_settings: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_vcs_settings Team#manage_vcs_settings}.
        :param manage_workspaces: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_workspaces Team#manage_workspaces}.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if manage_modules is not None:
            self._values["manage_modules"] = manage_modules
        if manage_policies is not None:
            self._values["manage_policies"] = manage_policies
        if manage_policy_overrides is not None:
            self._values["manage_policy_overrides"] = manage_policy_overrides
        if manage_providers is not None:
            self._values["manage_providers"] = manage_providers
        if manage_run_tasks is not None:
            self._values["manage_run_tasks"] = manage_run_tasks
        if manage_vcs_settings is not None:
            self._values["manage_vcs_settings"] = manage_vcs_settings
        if manage_workspaces is not None:
            self._values["manage_workspaces"] = manage_workspaces

    @builtins.property
    def manage_modules(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_modules Team#manage_modules}.'''
        result = self._values.get("manage_modules")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def manage_policies(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_policies Team#manage_policies}.'''
        result = self._values.get("manage_policies")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def manage_policy_overrides(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_policy_overrides Team#manage_policy_overrides}.'''
        result = self._values.get("manage_policy_overrides")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def manage_providers(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_providers Team#manage_providers}.'''
        result = self._values.get("manage_providers")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def manage_run_tasks(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_run_tasks Team#manage_run_tasks}.'''
        result = self._values.get("manage_run_tasks")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def manage_vcs_settings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_vcs_settings Team#manage_vcs_settings}.'''
        result = self._values.get("manage_vcs_settings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def manage_workspaces(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team#manage_workspaces Team#manage_workspaces}.'''
        result = self._values.get("manage_workspaces")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamOrganizationAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamOrganizationAccessOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamOrganizationAccessOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetManageModules")
    def reset_manage_modules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManageModules", []))

    @jsii.member(jsii_name="resetManagePolicies")
    def reset_manage_policies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagePolicies", []))

    @jsii.member(jsii_name="resetManagePolicyOverrides")
    def reset_manage_policy_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagePolicyOverrides", []))

    @jsii.member(jsii_name="resetManageProviders")
    def reset_manage_providers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManageProviders", []))

    @jsii.member(jsii_name="resetManageRunTasks")
    def reset_manage_run_tasks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManageRunTasks", []))

    @jsii.member(jsii_name="resetManageVcsSettings")
    def reset_manage_vcs_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManageVcsSettings", []))

    @jsii.member(jsii_name="resetManageWorkspaces")
    def reset_manage_workspaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManageWorkspaces", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageModulesInput")
    def manage_modules_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "manageModulesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="managePoliciesInput")
    def manage_policies_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "managePoliciesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="managePolicyOverridesInput")
    def manage_policy_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "managePolicyOverridesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageProvidersInput")
    def manage_providers_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "manageProvidersInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageRunTasksInput")
    def manage_run_tasks_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "manageRunTasksInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageVcsSettingsInput")
    def manage_vcs_settings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "manageVcsSettingsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageWorkspacesInput")
    def manage_workspaces_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "manageWorkspacesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageModules")
    def manage_modules(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "manageModules"))

    @manage_modules.setter
    def manage_modules(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "manageModules", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="managePolicies")
    def manage_policies(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "managePolicies"))

    @manage_policies.setter
    def manage_policies(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "managePolicies", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="managePolicyOverrides")
    def manage_policy_overrides(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "managePolicyOverrides"))

    @manage_policy_overrides.setter
    def manage_policy_overrides(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "managePolicyOverrides", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageProviders")
    def manage_providers(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "manageProviders"))

    @manage_providers.setter
    def manage_providers(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "manageProviders", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageRunTasks")
    def manage_run_tasks(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "manageRunTasks"))

    @manage_run_tasks.setter
    def manage_run_tasks(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "manageRunTasks", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageVcsSettings")
    def manage_vcs_settings(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "manageVcsSettings"))

    @manage_vcs_settings.setter
    def manage_vcs_settings(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "manageVcsSettings", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="manageWorkspaces")
    def manage_workspaces(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "manageWorkspaces"))

    @manage_workspaces.setter
    def manage_workspaces(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "manageWorkspaces", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamOrganizationAccess]:
        return typing.cast(typing.Optional[TeamOrganizationAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamOrganizationAccess]) -> None:
        jsii.set(self, "internalValue", value)


class TeamOrganizationMember(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamOrganizationMember",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member tfe_team_organization_member}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        organization_membership_id: builtins.str,
        team_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member tfe_team_organization_member} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param organization_membership_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#organization_membership_id TeamOrganizationMember#organization_membership_id}.
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#team_id TeamOrganizationMember#team_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#id TeamOrganizationMember#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamOrganizationMemberConfig(
            organization_membership_id=organization_membership_id,
            team_id=team_id,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationMembershipIdInput")
    def organization_membership_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationMembershipIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationMembershipId")
    def organization_membership_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationMembershipId"))

    @organization_membership_id.setter
    def organization_membership_id(self, value: builtins.str) -> None:
        jsii.set(self, "organizationMembershipId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        jsii.set(self, "teamId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamOrganizationMemberConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "organization_membership_id": "organizationMembershipId",
        "team_id": "teamId",
        "id": "id",
    },
)
class TeamOrganizationMemberConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        organization_membership_id: builtins.str,
        team_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param organization_membership_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#organization_membership_id TeamOrganizationMember#organization_membership_id}.
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#team_id TeamOrganizationMember#team_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#id TeamOrganizationMember#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "organization_membership_id": organization_membership_id,
            "team_id": team_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def organization_membership_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#organization_membership_id TeamOrganizationMember#organization_membership_id}.'''
        result = self._values.get("organization_membership_id")
        assert result is not None, "Required property 'organization_membership_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#team_id TeamOrganizationMember#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_organization_member#id TeamOrganizationMember#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamOrganizationMemberConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamToken(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TeamToken",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/team_token tfe_team_token}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        team_id: builtins.str,
        force_regenerate: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/team_token tfe_team_token} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#team_id TeamToken#team_id}.
        :param force_regenerate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#force_regenerate TeamToken#force_regenerate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#id TeamToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TeamTokenConfig(
            team_id=team_id,
            force_regenerate=force_regenerate,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetForceRegenerate")
    def reset_force_regenerate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceRegenerate", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="forceRegenerateInput")
    def force_regenerate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "forceRegenerateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="forceRegenerate")
    def force_regenerate(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "forceRegenerate"))

    @force_regenerate.setter
    def force_regenerate(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "forceRegenerate", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        jsii.set(self, "teamId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TeamTokenConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "team_id": "teamId",
        "force_regenerate": "forceRegenerate",
        "id": "id",
    },
)
class TeamTokenConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        team_id: builtins.str,
        force_regenerate: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#team_id TeamToken#team_id}.
        :param force_regenerate: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#force_regenerate TeamToken#force_regenerate}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#id TeamToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "team_id": team_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if force_regenerate is not None:
            self._values["force_regenerate"] = force_regenerate
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#team_id TeamToken#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def force_regenerate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#force_regenerate TeamToken#force_regenerate}.'''
        result = self._values.get("force_regenerate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/team_token#id TeamToken#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformVersion(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TerraformVersion",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version tfe_terraform_version}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        sha: builtins.str,
        url: builtins.str,
        version: builtins.str,
        beta: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        deprecated: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        deprecated_reason: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        official: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version tfe_terraform_version} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param sha: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#sha TerraformVersion#sha}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#url TerraformVersion#url}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#version TerraformVersion#version}.
        :param beta: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#beta TerraformVersion#beta}.
        :param deprecated: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#deprecated TerraformVersion#deprecated}.
        :param deprecated_reason: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#deprecated_reason TerraformVersion#deprecated_reason}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#enabled TerraformVersion#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#id TerraformVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param official: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#official TerraformVersion#official}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = TerraformVersionConfig(
            sha=sha,
            url=url,
            version=version,
            beta=beta,
            deprecated=deprecated,
            deprecated_reason=deprecated_reason,
            enabled=enabled,
            id=id,
            official=official,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetBeta")
    def reset_beta(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBeta", []))

    @jsii.member(jsii_name="resetDeprecated")
    def reset_deprecated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprecated", []))

    @jsii.member(jsii_name="resetDeprecatedReason")
    def reset_deprecated_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeprecatedReason", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOfficial")
    def reset_official(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOfficial", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="betaInput")
    def beta_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "betaInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deprecatedInput")
    def deprecated_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "deprecatedInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deprecatedReasonInput")
    def deprecated_reason_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deprecatedReasonInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="officialInput")
    def official_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "officialInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="shaInput")
    def sha_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shaInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="beta")
    def beta(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "beta"))

    @beta.setter
    def beta(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "beta", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deprecated")
    def deprecated(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "deprecated"))

    @deprecated.setter
    def deprecated(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "deprecated", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deprecatedReason")
    def deprecated_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deprecatedReason"))

    @deprecated_reason.setter
    def deprecated_reason(self, value: builtins.str) -> None:
        jsii.set(self, "deprecatedReason", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="official")
    def official(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "official"))

    @official.setter
    def official(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "official", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sha")
    def sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha"))

    @sha.setter
    def sha(self, value: builtins.str) -> None:
        jsii.set(self, "sha", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        jsii.set(self, "url", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        jsii.set(self, "version", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TerraformVersionConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "sha": "sha",
        "url": "url",
        "version": "version",
        "beta": "beta",
        "deprecated": "deprecated",
        "deprecated_reason": "deprecatedReason",
        "enabled": "enabled",
        "id": "id",
        "official": "official",
    },
)
class TerraformVersionConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        sha: builtins.str,
        url: builtins.str,
        version: builtins.str,
        beta: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        deprecated: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        deprecated_reason: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        official: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param sha: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#sha TerraformVersion#sha}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#url TerraformVersion#url}.
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#version TerraformVersion#version}.
        :param beta: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#beta TerraformVersion#beta}.
        :param deprecated: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#deprecated TerraformVersion#deprecated}.
        :param deprecated_reason: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#deprecated_reason TerraformVersion#deprecated_reason}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#enabled TerraformVersion#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#id TerraformVersion#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param official: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#official TerraformVersion#official}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "sha": sha,
            "url": url,
            "version": version,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if beta is not None:
            self._values["beta"] = beta
        if deprecated is not None:
            self._values["deprecated"] = deprecated
        if deprecated_reason is not None:
            self._values["deprecated_reason"] = deprecated_reason
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if official is not None:
            self._values["official"] = official

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def sha(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#sha TerraformVersion#sha}.'''
        result = self._values.get("sha")
        assert result is not None, "Required property 'sha' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#url TerraformVersion#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#version TerraformVersion#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def beta(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#beta TerraformVersion#beta}.'''
        result = self._values.get("beta")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def deprecated(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#deprecated TerraformVersion#deprecated}.'''
        result = self._values.get("deprecated")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def deprecated_reason(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#deprecated_reason TerraformVersion#deprecated_reason}.'''
        result = self._values.get("deprecated_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#enabled TerraformVersion#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#id TerraformVersion#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def official(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/terraform_version#official TerraformVersion#official}.'''
        result = self._values.get("official")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformVersionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TfeProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.TfeProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe tfe}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        ssl_skip_verify: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe tfe} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#alias TfeProvider#alias}
        :param hostname: The Terraform Enterprise hostname to connect to. Defaults to app.terraform.io. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#hostname TfeProvider#hostname}
        :param ssl_skip_verify: Whether or not to skip certificate verifications. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#ssl_skip_verify TfeProvider#ssl_skip_verify}
        :param token: The token used to authenticate with Terraform Enterprise. We recommend omitting the token which can be set as credentials in the CLI config file. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#token TfeProvider#token}
        '''
        config = TfeProviderConfig(
            alias=alias,
            hostname=hostname,
            ssl_skip_verify=ssl_skip_verify,
            token=token,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetSslSkipVerify")
    def reset_ssl_skip_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSslSkipVerify", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sslSkipVerifyInput")
    def ssl_skip_verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "sslSkipVerifyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alias", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "hostname", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sslSkipVerify")
    def ssl_skip_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "sslSkipVerify"))

    @ssl_skip_verify.setter
    def ssl_skip_verify(
        self,
        value: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]],
    ) -> None:
        jsii.set(self, "sslSkipVerify", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))

    @token.setter
    def token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "token", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.TfeProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "hostname": "hostname",
        "ssl_skip_verify": "sslSkipVerify",
        "token": "token",
    },
)
class TfeProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        hostname: typing.Optional[builtins.str] = None,
        ssl_skip_verify: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#alias TfeProvider#alias}
        :param hostname: The Terraform Enterprise hostname to connect to. Defaults to app.terraform.io. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#hostname TfeProvider#hostname}
        :param ssl_skip_verify: Whether or not to skip certificate verifications. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#ssl_skip_verify TfeProvider#ssl_skip_verify}
        :param token: The token used to authenticate with Terraform Enterprise. We recommend omitting the token which can be set as credentials in the CLI config file. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#token TfeProvider#token}
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if hostname is not None:
            self._values["hostname"] = hostname
        if ssl_skip_verify is not None:
            self._values["ssl_skip_verify"] = ssl_skip_verify
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#alias TfeProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The Terraform Enterprise hostname to connect to. Defaults to app.terraform.io.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#hostname TfeProvider#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssl_skip_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Whether or not to skip certificate verifications.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#ssl_skip_verify TfeProvider#ssl_skip_verify}
        '''
        result = self._values.get("ssl_skip_verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''The token used to authenticate with Terraform Enterprise.

        We recommend omitting
        the token which can be set as credentials in the CLI config file.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe#token TfeProvider#token}
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TfeProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Variable(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.Variable",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/variable tfe_variable}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        category: builtins.str,
        key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        hcl: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        sensitive: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
        variable_set_id: typing.Optional[builtins.str] = None,
        workspace_id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/variable tfe_variable} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#category Variable#category}.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#key Variable#key}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#description Variable#description}.
        :param hcl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#hcl Variable#hcl}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#id Variable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sensitive: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#sensitive Variable#sensitive}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#value Variable#value}.
        :param variable_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#variable_set_id Variable#variable_set_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#workspace_id Variable#workspace_id}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = VariableConfig(
            category=category,
            key=key,
            description=description,
            hcl=hcl,
            id=id,
            sensitive=sensitive,
            value=value,
            variable_set_id=variable_set_id,
            workspace_id=workspace_id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHcl")
    def reset_hcl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHcl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSensitive")
    def reset_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitive", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetVariableSetId")
    def reset_variable_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariableSetId", []))

    @jsii.member(jsii_name="resetWorkspaceId")
    def reset_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hclInput")
    def hcl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "hclInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sensitiveInput")
    def sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "sensitiveInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableSetIdInput")
    def variable_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variableSetIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        jsii.set(self, "category", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hcl")
    def hcl(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "hcl"))

    @hcl.setter
    def hcl(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "hcl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        jsii.set(self, "key", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "sensitive"))

    @sensitive.setter
    def sensitive(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "sensitive", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        jsii.set(self, "value", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableSetId")
    def variable_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variableSetId"))

    @variable_set_id.setter
    def variable_set_id(self, value: builtins.str) -> None:
        jsii.set(self, "variableSetId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.VariableConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "category": "category",
        "key": "key",
        "description": "description",
        "hcl": "hcl",
        "id": "id",
        "sensitive": "sensitive",
        "value": "value",
        "variable_set_id": "variableSetId",
        "workspace_id": "workspaceId",
    },
)
class VariableConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        category: builtins.str,
        key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        hcl: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        sensitive: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        value: typing.Optional[builtins.str] = None,
        variable_set_id: typing.Optional[builtins.str] = None,
        workspace_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#category Variable#category}.
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#key Variable#key}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#description Variable#description}.
        :param hcl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#hcl Variable#hcl}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#id Variable#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sensitive: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#sensitive Variable#sensitive}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#value Variable#value}.
        :param variable_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#variable_set_id Variable#variable_set_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#workspace_id Variable#workspace_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "category": category,
            "key": key,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if hcl is not None:
            self._values["hcl"] = hcl
        if id is not None:
            self._values["id"] = id
        if sensitive is not None:
            self._values["sensitive"] = sensitive
        if value is not None:
            self._values["value"] = value
        if variable_set_id is not None:
            self._values["variable_set_id"] = variable_set_id
        if workspace_id is not None:
            self._values["workspace_id"] = workspace_id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#category Variable#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#key Variable#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#description Variable#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hcl(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#hcl Variable#hcl}.'''
        result = self._values.get("hcl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#id Variable#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#sensitive Variable#sensitive}.'''
        result = self._values.get("sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#value Variable#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#variable_set_id Variable#variable_set_id}.'''
        result = self._values.get("variable_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable#workspace_id Variable#workspace_id}.'''
        result = self._values.get("workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VariableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VariableSet(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.VariableSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/variable_set tfe_variable_set}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        description: typing.Optional[builtins.str] = None,
        global_: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        workspace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/variable_set tfe_variable_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#name VariableSet#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#organization VariableSet#organization}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#description VariableSet#description}.
        :param global_: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#global VariableSet#global}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#id VariableSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param workspace_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#workspace_ids VariableSet#workspace_ids}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = VariableSetConfig(
            name=name,
            organization=organization,
            description=description,
            global_=global_,
            id=id,
            workspace_ids=workspace_ids,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGlobal")
    def reset_global(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobal", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetWorkspaceIds")
    def reset_workspace_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspaceIds", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="globalInput")
    def global_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "globalInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdsInput")
    def workspace_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "workspaceIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="global")
    def global_(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "global"))

    @global_.setter
    def global_(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "global", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIds")
    def workspace_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "workspaceIds"))

    @workspace_ids.setter
    def workspace_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "workspaceIds", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.VariableSetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "description": "description",
        "global_": "global",
        "id": "id",
        "workspace_ids": "workspaceIds",
    },
)
class VariableSetConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        description: typing.Optional[builtins.str] = None,
        global_: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        workspace_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#name VariableSet#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#organization VariableSet#organization}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#description VariableSet#description}.
        :param global_: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#global VariableSet#global}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#id VariableSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param workspace_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#workspace_ids VariableSet#workspace_ids}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if description is not None:
            self._values["description"] = description
        if global_ is not None:
            self._values["global_"] = global_
        if id is not None:
            self._values["id"] = id
        if workspace_ids is not None:
            self._values["workspace_ids"] = workspace_ids

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#name VariableSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#organization VariableSet#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#description VariableSet#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#global VariableSet#global}.'''
        result = self._values.get("global_")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#id VariableSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/variable_set#workspace_ids VariableSet#workspace_ids}.'''
        result = self._values.get("workspace_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VariableSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Workspace(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.Workspace",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/workspace tfe_workspace}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        organization: builtins.str,
        agent_pool_id: typing.Optional[builtins.str] = None,
        allow_destroy_plan: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_apply: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_mode: typing.Optional[builtins.str] = None,
        file_triggers_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        global_remote_state: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        operations: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        queue_all_runs: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        remote_state_consumer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        speculative_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        ssh_key_id: typing.Optional[builtins.str] = None,
        structured_run_output_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        terraform_version: typing.Optional[builtins.str] = None,
        trigger_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        trigger_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        vcs_repo: typing.Optional["WorkspaceVcsRepo"] = None,
        working_directory: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/workspace tfe_workspace} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#name Workspace#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#organization Workspace#organization}.
        :param agent_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#agent_pool_id Workspace#agent_pool_id}.
        :param allow_destroy_plan: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#allow_destroy_plan Workspace#allow_destroy_plan}.
        :param auto_apply: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#auto_apply Workspace#auto_apply}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#description Workspace#description}.
        :param execution_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#execution_mode Workspace#execution_mode}.
        :param file_triggers_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#file_triggers_enabled Workspace#file_triggers_enabled}.
        :param global_remote_state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#global_remote_state Workspace#global_remote_state}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#id Workspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#operations Workspace#operations}.
        :param queue_all_runs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#queue_all_runs Workspace#queue_all_runs}.
        :param remote_state_consumer_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#remote_state_consumer_ids Workspace#remote_state_consumer_ids}.
        :param speculative_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#speculative_enabled Workspace#speculative_enabled}.
        :param ssh_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ssh_key_id Workspace#ssh_key_id}.
        :param structured_run_output_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#structured_run_output_enabled Workspace#structured_run_output_enabled}.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#tag_names Workspace#tag_names}.
        :param terraform_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#terraform_version Workspace#terraform_version}.
        :param trigger_patterns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_patterns Workspace#trigger_patterns}.
        :param trigger_prefixes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_prefixes Workspace#trigger_prefixes}.
        :param vcs_repo: vcs_repo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#vcs_repo Workspace#vcs_repo}
        :param working_directory: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#working_directory Workspace#working_directory}.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = WorkspaceConfig(
            name=name,
            organization=organization,
            agent_pool_id=agent_pool_id,
            allow_destroy_plan=allow_destroy_plan,
            auto_apply=auto_apply,
            description=description,
            execution_mode=execution_mode,
            file_triggers_enabled=file_triggers_enabled,
            global_remote_state=global_remote_state,
            id=id,
            operations=operations,
            queue_all_runs=queue_all_runs,
            remote_state_consumer_ids=remote_state_consumer_ids,
            speculative_enabled=speculative_enabled,
            ssh_key_id=ssh_key_id,
            structured_run_output_enabled=structured_run_output_enabled,
            tag_names=tag_names,
            terraform_version=terraform_version,
            trigger_patterns=trigger_patterns,
            trigger_prefixes=trigger_prefixes,
            vcs_repo=vcs_repo,
            working_directory=working_directory,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putVcsRepo")
    def put_vcs_repo(
        self,
        *,
        identifier: builtins.str,
        oauth_token_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        ingress_submodules: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#identifier Workspace#identifier}.
        :param oauth_token_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#oauth_token_id Workspace#oauth_token_id}.
        :param branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#branch Workspace#branch}.
        :param ingress_submodules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ingress_submodules Workspace#ingress_submodules}.
        '''
        value = WorkspaceVcsRepo(
            identifier=identifier,
            oauth_token_id=oauth_token_id,
            branch=branch,
            ingress_submodules=ingress_submodules,
        )

        return typing.cast(None, jsii.invoke(self, "putVcsRepo", [value]))

    @jsii.member(jsii_name="resetAgentPoolId")
    def reset_agent_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentPoolId", []))

    @jsii.member(jsii_name="resetAllowDestroyPlan")
    def reset_allow_destroy_plan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowDestroyPlan", []))

    @jsii.member(jsii_name="resetAutoApply")
    def reset_auto_apply(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoApply", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExecutionMode")
    def reset_execution_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionMode", []))

    @jsii.member(jsii_name="resetFileTriggersEnabled")
    def reset_file_triggers_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileTriggersEnabled", []))

    @jsii.member(jsii_name="resetGlobalRemoteState")
    def reset_global_remote_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobalRemoteState", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOperations")
    def reset_operations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperations", []))

    @jsii.member(jsii_name="resetQueueAllRuns")
    def reset_queue_all_runs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueAllRuns", []))

    @jsii.member(jsii_name="resetRemoteStateConsumerIds")
    def reset_remote_state_consumer_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteStateConsumerIds", []))

    @jsii.member(jsii_name="resetSpeculativeEnabled")
    def reset_speculative_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeculativeEnabled", []))

    @jsii.member(jsii_name="resetSshKeyId")
    def reset_ssh_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshKeyId", []))

    @jsii.member(jsii_name="resetStructuredRunOutputEnabled")
    def reset_structured_run_output_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStructuredRunOutputEnabled", []))

    @jsii.member(jsii_name="resetTagNames")
    def reset_tag_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagNames", []))

    @jsii.member(jsii_name="resetTerraformVersion")
    def reset_terraform_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerraformVersion", []))

    @jsii.member(jsii_name="resetTriggerPatterns")
    def reset_trigger_patterns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerPatterns", []))

    @jsii.member(jsii_name="resetTriggerPrefixes")
    def reset_trigger_prefixes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerPrefixes", []))

    @jsii.member(jsii_name="resetVcsRepo")
    def reset_vcs_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVcsRepo", []))

    @jsii.member(jsii_name="resetWorkingDirectory")
    def reset_working_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDirectory", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcsRepo")
    def vcs_repo(self) -> "WorkspaceVcsRepoOutputReference":
        return typing.cast("WorkspaceVcsRepoOutputReference", jsii.get(self, "vcsRepo"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="agentPoolIdInput")
    def agent_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentPoolIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowDestroyPlanInput")
    def allow_destroy_plan_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "allowDestroyPlanInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoApplyInput")
    def auto_apply_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "autoApplyInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionModeInput")
    def execution_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionModeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileTriggersEnabledInput")
    def file_triggers_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "fileTriggersEnabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="globalRemoteStateInput")
    def global_remote_state_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "globalRemoteStateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="operationsInput")
    def operations_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "operationsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organizationInput")
    def organization_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queueAllRunsInput")
    def queue_all_runs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "queueAllRunsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="remoteStateConsumerIdsInput")
    def remote_state_consumer_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "remoteStateConsumerIdsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="speculativeEnabledInput")
    def speculative_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "speculativeEnabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sshKeyIdInput")
    def ssh_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshKeyIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="structuredRunOutputEnabledInput")
    def structured_run_output_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "structuredRunOutputEnabledInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagNamesInput")
    def tag_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagNamesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformVersionInput")
    def terraform_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "terraformVersionInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerPatternsInput")
    def trigger_patterns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerPatternsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerPrefixesInput")
    def trigger_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerPrefixesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vcsRepoInput")
    def vcs_repo_input(self) -> typing.Optional["WorkspaceVcsRepo"]:
        return typing.cast(typing.Optional["WorkspaceVcsRepo"], jsii.get(self, "vcsRepoInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workingDirectoryInput")
    def working_directory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirectoryInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="agentPoolId")
    def agent_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentPoolId"))

    @agent_pool_id.setter
    def agent_pool_id(self, value: builtins.str) -> None:
        jsii.set(self, "agentPoolId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowDestroyPlan")
    def allow_destroy_plan(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "allowDestroyPlan"))

    @allow_destroy_plan.setter
    def allow_destroy_plan(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "allowDestroyPlan", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoApply")
    def auto_apply(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "autoApply"))

    @auto_apply.setter
    def auto_apply(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "autoApply", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionMode")
    def execution_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionMode"))

    @execution_mode.setter
    def execution_mode(self, value: builtins.str) -> None:
        jsii.set(self, "executionMode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fileTriggersEnabled")
    def file_triggers_enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "fileTriggersEnabled"))

    @file_triggers_enabled.setter
    def file_triggers_enabled(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "fileTriggersEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="globalRemoteState")
    def global_remote_state(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "globalRemoteState"))

    @global_remote_state.setter
    def global_remote_state(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "globalRemoteState", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="operations")
    def operations(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "operations"))

    @operations.setter
    def operations(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "operations", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @organization.setter
    def organization(self, value: builtins.str) -> None:
        jsii.set(self, "organization", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queueAllRuns")
    def queue_all_runs(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "queueAllRuns"))

    @queue_all_runs.setter
    def queue_all_runs(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "queueAllRuns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="remoteStateConsumerIds")
    def remote_state_consumer_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteStateConsumerIds"))

    @remote_state_consumer_ids.setter
    def remote_state_consumer_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "remoteStateConsumerIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="speculativeEnabled")
    def speculative_enabled(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "speculativeEnabled"))

    @speculative_enabled.setter
    def speculative_enabled(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "speculativeEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sshKeyId")
    def ssh_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshKeyId"))

    @ssh_key_id.setter
    def ssh_key_id(self, value: builtins.str) -> None:
        jsii.set(self, "sshKeyId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="structuredRunOutputEnabled")
    def structured_run_output_enabled(
        self,
    ) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "structuredRunOutputEnabled"))

    @structured_run_output_enabled.setter
    def structured_run_output_enabled(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "structuredRunOutputEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagNames")
    def tag_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagNames"))

    @tag_names.setter
    def tag_names(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "tagNames", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformVersion")
    def terraform_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "terraformVersion"))

    @terraform_version.setter
    def terraform_version(self, value: builtins.str) -> None:
        jsii.set(self, "terraformVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerPatterns")
    def trigger_patterns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerPatterns"))

    @trigger_patterns.setter
    def trigger_patterns(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "triggerPatterns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerPrefixes")
    def trigger_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerPrefixes"))

    @trigger_prefixes.setter
    def trigger_prefixes(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "triggerPrefixes", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workingDirectory")
    def working_directory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDirectory"))

    @working_directory.setter
    def working_directory(self, value: builtins.str) -> None:
        jsii.set(self, "workingDirectory", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.WorkspaceConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "name": "name",
        "organization": "organization",
        "agent_pool_id": "agentPoolId",
        "allow_destroy_plan": "allowDestroyPlan",
        "auto_apply": "autoApply",
        "description": "description",
        "execution_mode": "executionMode",
        "file_triggers_enabled": "fileTriggersEnabled",
        "global_remote_state": "globalRemoteState",
        "id": "id",
        "operations": "operations",
        "queue_all_runs": "queueAllRuns",
        "remote_state_consumer_ids": "remoteStateConsumerIds",
        "speculative_enabled": "speculativeEnabled",
        "ssh_key_id": "sshKeyId",
        "structured_run_output_enabled": "structuredRunOutputEnabled",
        "tag_names": "tagNames",
        "terraform_version": "terraformVersion",
        "trigger_patterns": "triggerPatterns",
        "trigger_prefixes": "triggerPrefixes",
        "vcs_repo": "vcsRepo",
        "working_directory": "workingDirectory",
    },
)
class WorkspaceConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        name: builtins.str,
        organization: builtins.str,
        agent_pool_id: typing.Optional[builtins.str] = None,
        allow_destroy_plan: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        auto_apply: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        execution_mode: typing.Optional[builtins.str] = None,
        file_triggers_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        global_remote_state: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        operations: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        queue_all_runs: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        remote_state_consumer_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        speculative_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        ssh_key_id: typing.Optional[builtins.str] = None,
        structured_run_output_enabled: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        tag_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        terraform_version: typing.Optional[builtins.str] = None,
        trigger_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        trigger_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        vcs_repo: typing.Optional["WorkspaceVcsRepo"] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#name Workspace#name}.
        :param organization: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#organization Workspace#organization}.
        :param agent_pool_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#agent_pool_id Workspace#agent_pool_id}.
        :param allow_destroy_plan: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#allow_destroy_plan Workspace#allow_destroy_plan}.
        :param auto_apply: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#auto_apply Workspace#auto_apply}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#description Workspace#description}.
        :param execution_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#execution_mode Workspace#execution_mode}.
        :param file_triggers_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#file_triggers_enabled Workspace#file_triggers_enabled}.
        :param global_remote_state: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#global_remote_state Workspace#global_remote_state}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#id Workspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#operations Workspace#operations}.
        :param queue_all_runs: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#queue_all_runs Workspace#queue_all_runs}.
        :param remote_state_consumer_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#remote_state_consumer_ids Workspace#remote_state_consumer_ids}.
        :param speculative_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#speculative_enabled Workspace#speculative_enabled}.
        :param ssh_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ssh_key_id Workspace#ssh_key_id}.
        :param structured_run_output_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#structured_run_output_enabled Workspace#structured_run_output_enabled}.
        :param tag_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#tag_names Workspace#tag_names}.
        :param terraform_version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#terraform_version Workspace#terraform_version}.
        :param trigger_patterns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_patterns Workspace#trigger_patterns}.
        :param trigger_prefixes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_prefixes Workspace#trigger_prefixes}.
        :param vcs_repo: vcs_repo block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#vcs_repo Workspace#vcs_repo}
        :param working_directory: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#working_directory Workspace#working_directory}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        if isinstance(vcs_repo, dict):
            vcs_repo = WorkspaceVcsRepo(**vcs_repo)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "organization": organization,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if agent_pool_id is not None:
            self._values["agent_pool_id"] = agent_pool_id
        if allow_destroy_plan is not None:
            self._values["allow_destroy_plan"] = allow_destroy_plan
        if auto_apply is not None:
            self._values["auto_apply"] = auto_apply
        if description is not None:
            self._values["description"] = description
        if execution_mode is not None:
            self._values["execution_mode"] = execution_mode
        if file_triggers_enabled is not None:
            self._values["file_triggers_enabled"] = file_triggers_enabled
        if global_remote_state is not None:
            self._values["global_remote_state"] = global_remote_state
        if id is not None:
            self._values["id"] = id
        if operations is not None:
            self._values["operations"] = operations
        if queue_all_runs is not None:
            self._values["queue_all_runs"] = queue_all_runs
        if remote_state_consumer_ids is not None:
            self._values["remote_state_consumer_ids"] = remote_state_consumer_ids
        if speculative_enabled is not None:
            self._values["speculative_enabled"] = speculative_enabled
        if ssh_key_id is not None:
            self._values["ssh_key_id"] = ssh_key_id
        if structured_run_output_enabled is not None:
            self._values["structured_run_output_enabled"] = structured_run_output_enabled
        if tag_names is not None:
            self._values["tag_names"] = tag_names
        if terraform_version is not None:
            self._values["terraform_version"] = terraform_version
        if trigger_patterns is not None:
            self._values["trigger_patterns"] = trigger_patterns
        if trigger_prefixes is not None:
            self._values["trigger_prefixes"] = trigger_prefixes
        if vcs_repo is not None:
            self._values["vcs_repo"] = vcs_repo
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#name Workspace#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def organization(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#organization Workspace#organization}.'''
        result = self._values.get("organization")
        assert result is not None, "Required property 'organization' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#agent_pool_id Workspace#agent_pool_id}.'''
        result = self._values.get("agent_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_destroy_plan(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#allow_destroy_plan Workspace#allow_destroy_plan}.'''
        result = self._values.get("allow_destroy_plan")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def auto_apply(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#auto_apply Workspace#auto_apply}.'''
        result = self._values.get("auto_apply")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#description Workspace#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#execution_mode Workspace#execution_mode}.'''
        result = self._values.get("execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_triggers_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#file_triggers_enabled Workspace#file_triggers_enabled}.'''
        result = self._values.get("file_triggers_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def global_remote_state(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#global_remote_state Workspace#global_remote_state}.'''
        result = self._values.get("global_remote_state")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#id Workspace#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operations(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#operations Workspace#operations}.'''
        result = self._values.get("operations")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def queue_all_runs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#queue_all_runs Workspace#queue_all_runs}.'''
        result = self._values.get("queue_all_runs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def remote_state_consumer_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#remote_state_consumer_ids Workspace#remote_state_consumer_ids}.'''
        result = self._values.get("remote_state_consumer_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def speculative_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#speculative_enabled Workspace#speculative_enabled}.'''
        result = self._values.get("speculative_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def ssh_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ssh_key_id Workspace#ssh_key_id}.'''
        result = self._values.get("ssh_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def structured_run_output_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#structured_run_output_enabled Workspace#structured_run_output_enabled}.'''
        result = self._values.get("structured_run_output_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def tag_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#tag_names Workspace#tag_names}.'''
        result = self._values.get("tag_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def terraform_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#terraform_version Workspace#terraform_version}.'''
        result = self._values.get("terraform_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_patterns Workspace#trigger_patterns}.'''
        result = self._values.get("trigger_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def trigger_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#trigger_prefixes Workspace#trigger_prefixes}.'''
        result = self._values.get("trigger_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vcs_repo(self) -> typing.Optional["WorkspaceVcsRepo"]:
        '''vcs_repo block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#vcs_repo Workspace#vcs_repo}
        '''
        result = self._values.get("vcs_repo")
        return typing.cast(typing.Optional["WorkspaceVcsRepo"], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#working_directory Workspace#working_directory}.'''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceRunTask(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.WorkspaceRunTask",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task tfe_workspace_run_task}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        enforcement_level: builtins.str,
        task_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task tfe_workspace_run_task} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param enforcement_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#enforcement_level WorkspaceRunTask#enforcement_level}.
        :param task_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#task_id WorkspaceRunTask#task_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#workspace_id WorkspaceRunTask#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#id WorkspaceRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = WorkspaceRunTaskConfig(
            enforcement_level=enforcement_level,
            task_id=task_id,
            workspace_id=workspace_id,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enforcementLevelInput")
    def enforcement_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enforcementLevelInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskIdInput")
    def task_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enforcementLevel")
    def enforcement_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enforcementLevel"))

    @enforcement_level.setter
    def enforcement_level(self, value: builtins.str) -> None:
        jsii.set(self, "enforcementLevel", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskId")
    def task_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskId"))

    @task_id.setter
    def task_id(self, value: builtins.str) -> None:
        jsii.set(self, "taskId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.WorkspaceRunTaskConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "enforcement_level": "enforcementLevel",
        "task_id": "taskId",
        "workspace_id": "workspaceId",
        "id": "id",
    },
)
class WorkspaceRunTaskConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        enforcement_level: builtins.str,
        task_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param enforcement_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#enforcement_level WorkspaceRunTask#enforcement_level}.
        :param task_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#task_id WorkspaceRunTask#task_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#workspace_id WorkspaceRunTask#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#id WorkspaceRunTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "enforcement_level": enforcement_level,
            "task_id": task_id,
            "workspace_id": workspace_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def enforcement_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#enforcement_level WorkspaceRunTask#enforcement_level}.'''
        result = self._values.get("enforcement_level")
        assert result is not None, "Required property 'enforcement_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#task_id WorkspaceRunTask#task_id}.'''
        result = self._values.get("task_id")
        assert result is not None, "Required property 'task_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#workspace_id WorkspaceRunTask#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_run_task#id WorkspaceRunTask#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceRunTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceVariableSet(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.WorkspaceVariableSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set tfe_workspace_variable_set}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        variable_set_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set tfe_workspace_variable_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param variable_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#variable_set_id WorkspaceVariableSet#variable_set_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#workspace_id WorkspaceVariableSet#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#id WorkspaceVariableSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = WorkspaceVariableSetConfig(
            variable_set_id=variable_set_id,
            workspace_id=workspace_id,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableSetIdInput")
    def variable_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "variableSetIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="variableSetId")
    def variable_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variableSetId"))

    @variable_set_id.setter
    def variable_set_id(self, value: builtins.str) -> None:
        jsii.set(self, "variableSetId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.WorkspaceVariableSetConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "variable_set_id": "variableSetId",
        "workspace_id": "workspaceId",
        "id": "id",
    },
)
class WorkspaceVariableSetConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        variable_set_id: builtins.str,
        workspace_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param variable_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#variable_set_id WorkspaceVariableSet#variable_set_id}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#workspace_id WorkspaceVariableSet#workspace_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#id WorkspaceVariableSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "variable_set_id": variable_set_id,
            "workspace_id": workspace_id,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def variable_set_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#variable_set_id WorkspaceVariableSet#variable_set_id}.'''
        result = self._values.get("variable_set_id")
        assert result is not None, "Required property 'variable_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#workspace_id WorkspaceVariableSet#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace_variable_set#id WorkspaceVariableSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceVariableSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.WorkspaceVcsRepo",
    jsii_struct_bases=[],
    name_mapping={
        "identifier": "identifier",
        "oauth_token_id": "oauthTokenId",
        "branch": "branch",
        "ingress_submodules": "ingressSubmodules",
    },
)
class WorkspaceVcsRepo:
    def __init__(
        self,
        *,
        identifier: builtins.str,
        oauth_token_id: builtins.str,
        branch: typing.Optional[builtins.str] = None,
        ingress_submodules: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
    ) -> None:
        '''
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#identifier Workspace#identifier}.
        :param oauth_token_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#oauth_token_id Workspace#oauth_token_id}.
        :param branch: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#branch Workspace#branch}.
        :param ingress_submodules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ingress_submodules Workspace#ingress_submodules}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "identifier": identifier,
            "oauth_token_id": oauth_token_id,
        }
        if branch is not None:
            self._values["branch"] = branch
        if ingress_submodules is not None:
            self._values["ingress_submodules"] = ingress_submodules

    @builtins.property
    def identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#identifier Workspace#identifier}.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def oauth_token_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#oauth_token_id Workspace#oauth_token_id}.'''
        result = self._values.get("oauth_token_id")
        assert result is not None, "Required property 'oauth_token_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#branch Workspace#branch}.'''
        result = self._values.get("branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress_submodules(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/workspace#ingress_submodules Workspace#ingress_submodules}.'''
        result = self._values.get("ingress_submodules")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceVcsRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceVcsRepoOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.WorkspaceVcsRepoOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBranch")
    def reset_branch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranch", []))

    @jsii.member(jsii_name="resetIngressSubmodules")
    def reset_ingress_submodules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngressSubmodules", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branchInput")
    def branch_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ingressSubmodulesInput")
    def ingress_submodules_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "ingressSubmodulesInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenIdInput")
    def oauth_token_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthTokenIdInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="branch")
    def branch(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branch"))

    @branch.setter
    def branch(self, value: builtins.str) -> None:
        jsii.set(self, "branch", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        jsii.set(self, "identifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ingressSubmodules")
    def ingress_submodules(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "ingressSubmodules"))

    @ingress_submodules.setter
    def ingress_submodules(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "ingressSubmodules", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="oauthTokenId")
    def oauth_token_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oauthTokenId"))

    @oauth_token_id.setter
    def oauth_token_id(self, value: builtins.str) -> None:
        jsii.set(self, "oauthTokenId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WorkspaceVcsRepo]:
        return typing.cast(typing.Optional[WorkspaceVcsRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[WorkspaceVcsRepo]) -> None:
        jsii.set(self, "internalValue", value)


__all__ = [
    "AgentPool",
    "AgentPoolConfig",
    "AgentToken",
    "AgentTokenConfig",
    "DataTfeAgentPool",
    "DataTfeAgentPoolConfig",
    "DataTfeIpRanges",
    "DataTfeIpRangesConfig",
    "DataTfeOauthClient",
    "DataTfeOauthClientConfig",
    "DataTfeOrganization",
    "DataTfeOrganizationConfig",
    "DataTfeOrganizationMembership",
    "DataTfeOrganizationMembershipConfig",
    "DataTfeOrganizationRunTask",
    "DataTfeOrganizationRunTaskConfig",
    "DataTfeOrganizations",
    "DataTfeOrganizationsConfig",
    "DataTfeOutputs",
    "DataTfeOutputsConfig",
    "DataTfeSlug",
    "DataTfeSlugConfig",
    "DataTfeSshKey",
    "DataTfeSshKeyConfig",
    "DataTfeTeam",
    "DataTfeTeamAccess",
    "DataTfeTeamAccessConfig",
    "DataTfeTeamAccessPermissions",
    "DataTfeTeamAccessPermissionsList",
    "DataTfeTeamAccessPermissionsOutputReference",
    "DataTfeTeamConfig",
    "DataTfeVariableSet",
    "DataTfeVariableSetConfig",
    "DataTfeVariables",
    "DataTfeVariablesConfig",
    "DataTfeVariablesEnv",
    "DataTfeVariablesEnvList",
    "DataTfeVariablesEnvOutputReference",
    "DataTfeVariablesTerraform",
    "DataTfeVariablesTerraformList",
    "DataTfeVariablesTerraformOutputReference",
    "DataTfeVariablesVariables",
    "DataTfeVariablesVariablesList",
    "DataTfeVariablesVariablesOutputReference",
    "DataTfeWorkspace",
    "DataTfeWorkspaceConfig",
    "DataTfeWorkspaceIds",
    "DataTfeWorkspaceIdsConfig",
    "DataTfeWorkspaceRunTask",
    "DataTfeWorkspaceRunTaskConfig",
    "DataTfeWorkspaceVcsRepo",
    "DataTfeWorkspaceVcsRepoList",
    "DataTfeWorkspaceVcsRepoOutputReference",
    "NotificationConfiguration",
    "NotificationConfigurationConfig",
    "OauthClient",
    "OauthClientConfig",
    "Organization",
    "OrganizationConfig",
    "OrganizationMembership",
    "OrganizationMembershipConfig",
    "OrganizationModuleSharing",
    "OrganizationModuleSharingConfig",
    "OrganizationRunTask",
    "OrganizationRunTaskConfig",
    "OrganizationToken",
    "OrganizationTokenConfig",
    "PolicySet",
    "PolicySetConfig",
    "PolicySetParameter",
    "PolicySetParameterConfig",
    "PolicySetVcsRepo",
    "PolicySetVcsRepoOutputReference",
    "RegistryModule",
    "RegistryModuleConfig",
    "RegistryModuleVcsRepo",
    "RegistryModuleVcsRepoOutputReference",
    "RunTrigger",
    "RunTriggerConfig",
    "SentinelPolicy",
    "SentinelPolicyConfig",
    "SshKey",
    "SshKeyConfig",
    "Team",
    "TeamAccess",
    "TeamAccessConfig",
    "TeamAccessPermissions",
    "TeamAccessPermissionsList",
    "TeamAccessPermissionsOutputReference",
    "TeamConfig",
    "TeamMember",
    "TeamMemberConfig",
    "TeamMembers",
    "TeamMembersConfig",
    "TeamOrganizationAccess",
    "TeamOrganizationAccessOutputReference",
    "TeamOrganizationMember",
    "TeamOrganizationMemberConfig",
    "TeamToken",
    "TeamTokenConfig",
    "TerraformVersion",
    "TerraformVersionConfig",
    "TfeProvider",
    "TfeProviderConfig",
    "Variable",
    "VariableConfig",
    "VariableSet",
    "VariableSetConfig",
    "Workspace",
    "WorkspaceConfig",
    "WorkspaceRunTask",
    "WorkspaceRunTaskConfig",
    "WorkspaceVariableSet",
    "WorkspaceVariableSetConfig",
    "WorkspaceVcsRepo",
    "WorkspaceVcsRepoOutputReference",
]

publication.publish()
