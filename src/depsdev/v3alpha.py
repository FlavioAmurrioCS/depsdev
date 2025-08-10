from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Optional
from typing import Union

from depsdev.v3 import DepsDevClientV3
from depsdev.v3 import HashType
from depsdev.v3 import Incomplete
from depsdev.v3 import System
from depsdev.v3 import url_escape

if TYPE_CHECKING:
    from typing_extensions import Literal
    from typing_extensions import TypedDict

    class PurlDict(TypedDict):
        system: System | SystemLiteral
        name: str
        version: str

    SystemLiteral = Literal[
        "GO",
        "RUBYGEMS",
        "NPM",
        "CARGO",
        "MAVEN",
        "PYPI",
        "NUGET",
    ]

PUrlStr = str
PUrlWithVersionStr = str


class DepsDevClientV3Alpha(DepsDevClientV3):
    async def get_package(self, system: System, name: str) -> Incomplete:
        """
        GetPackage

        GET /v3alpha/systems/{packageKey.system}/packages/{packageKey.name}

        GetPackage returns information about a package, including a list of its available versions, with the default version marked if known.

        Example: /v3alpha/systems/npm/packages/%40colors%2Fcolors
        Path parameters

        packageKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        packageKey.name: string

            The name of the package.
        """  # noqa: E501
        return await self._requests(
            method="GET", url=f"/v3alpha/systems/{system}/packages/{url_escape(name)}"
        )

    async def get_version(self, system: System, name: str, version: str) -> Incomplete:
        """
        GetVersion

        GET /v3alpha/systems/{versionKey.system}/packages/{versionKey.name}/versions/{versionKey.version}

        GetVersion returns information about a specific package version, including its licenses and any security advisories known to affect it.

        Example: /v3alpha/systems/npm/packages/%40colors%2Fcolors/versions/1.5.0
        Path parameters

        versionKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        versionKey.name: string

            The name of the package.
        versionKey.version: string

            The version of the package.
        """  # noqa: E501
        return await self._requests(
            method="GET",
            url=f"/v3alpha/systems/{system}/packages/{url_escape(name)}/versions/{url_escape(version)}",
        )

    async def get_version_batch(
        self,
        requests: list[PurlDict],
        page_token: Optional[str] = None,  # noqa: UP045
    ) -> Incomplete:
        """
        GetVersionBatch

        POST /v3alpha/versionbatch

        GetVersionBatch performs GetVersion requests for a batch of versions. Large result sets may be paginated.

        Example:

        curl -d @- 'https://api.deps.dev/v3alpha/versionbatch' <<EOF
        {
        "requests":[
            {"versionKey":{"system":"NPM","name":"@colors/colors","version":"1.5.0"}},
            {"versionKey":{"system":"NUGET","name":"castle.core","version":"5.1.1"}}
        ]
        }
        EOF

        Request body

        requests[]: object[]

            The batch list of versions to return Version information for. Up to 5000 requests are allowed in a single batch.
        requests[].versionKey: object
        requests[].versionKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        requests[].versionKey.name: string

            The name of the package.
        requests[].versionKey.version: string

            The version of the package.
        pageToken: string

            If set, request the next page of the result set. It must be set to the page token provided by the previous version batch response. All other request fields must be the same as in the initial request.
        """  # noqa: E501
        payload = {
            "requests": [{"versionKey": x} for x in requests],
            "pageToken": page_token,
        }
        return await self._requests(method="POST", url="/v3alpha/versionbatch", json=payload)

    async def get_requirements(self, system: System, name: str, version: str) -> Incomplete:
        """
        GetRequirements

        GET /v3alpha/systems/{versionKey.system}/packages/{versionKey.name}/versions/{versionKey.version}:requirements

        GetRequirements returns the requirements for a given version in a system-specific format. Requirements are currently available for Maven, npm, NuGet, and RubyGems.

        Requirements are the dependency constraints specified by the version.

        Example: /v3alpha/systems/nuget/packages/castle.core/versions/5.1.1:requirements
        Path parameters

        versionKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        versionKey.name: string

            The name of the package.
        versionKey.version: string

            The version of the package.
        """  # noqa: E501
        return await self._requests(
            method="GET",
            url=f"/v3alpha/systems/{system}/packages/{url_escape(name)}/versions/{url_escape(version)}:requirements",
        )

    async def get_dependencies(self, system: System, name: str, version: str) -> Incomplete:
        """
        GetDependencies

        GET /v3alpha/systems/{versionKey.system}/packages/{versionKey.name}/versions/{versionKey.version}:dependencies

        GetDependencies returns a resolved dependency graph for the given package version. Dependencies are currently available for Go, npm, Cargo, Maven and PyPI.

        Dependencies are the resolution of the requirements (dependency constraints) specified by a version.

        The dependency graph should be similar to one produced by installing the package version on a generic 64-bit Linux system, with no other dependencies present. The precise meaning of this varies from system to system.

        Example: /v3alpha/systems/npm/packages/react/versions/18.2.0:dependencies
        Path parameters

        versionKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        versionKey.name: string

            The name of the package.
        versionKey.version: string

            The version of the package.
        """  # noqa: E501
        return await self._requests(
            method="GET",
            url=f"/v3alpha/systems/{system}/packages/{url_escape(name)}/versions/{url_escape(version)}:dependencies",
        )

    async def get_dependents(self, system: System, name: str, version: str) -> Incomplete:
        """
        GetDependents

        GET /v3alpha/systems/{versionKey.system}/packages/{versionKey.name}/versions/{versionKey.version}:dependents

        GetDependents returns information about the number of distinct packages known to depend on the given package version. Dependent counts are currently available for Go, npm, Cargo, Maven and PyPI.

        Dependent counts are derived from the dependency graphs computed by deps.dev, which means that only public dependents are counted. As such, dependent counts should be treated as indicative of relative popularity rather than precisely accurate.
        Path parameters

        versionKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        versionKey.name: string

            The name of the package.
        versionKey.version: string

            The version of the package.
        """  # noqa: E501
        return await self._requests(
            method="GET",
            url=f"/v3alpha/systems/{system}/packages/{url_escape(name)}/versions/{url_escape(version)}:dependents",
        )

    async def get_capabilities(self, system: System, name: str, version: str) -> Incomplete:
        """
        GetCapabilities

        GET /v3alpha/systems/{versionKey.system}/packages/{versionKey.name}/versions/{versionKey.version}:capabilities

        GetCapabilityRequest returns counts for direct and indirect calls to Capslock capabilities for a given package version. Currently only available for Go.
        Path parameters

        versionKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        versionKey.name: string

            The name of the package.
        versionKey.version: string

            The version of the package.
        """  # noqa: E501
        return await self._requests(
            method="GET",
            url=f"/v3alpha/systems/{system}/packages/{url_escape(name)}/versions/{url_escape(version)}:capabilities",
        )

    async def get_project(self, project_id: str) -> Incomplete:
        """
        GetProject

        GET /v3alpha/projects/{projectKey.id}

        GetProject returns information about projects hosted by GitHub, GitLab, or BitBucket, when known to us.

        Example: /v3alpha/projects/github.com%2Ffacebook%2Freact
        Path parameters

        projectKey.id: string

            A project identifier of the form github.com/user/repo, gitlab.com/user/repo, or bitbucket.org/user/repo.
        """  # noqa: E501
        return await self._requests(method="GET", url=f"/v3alpha/projects/{url_escape(project_id)}")

    async def get_project_batch(
        self,
        project_ids: list[str],
        page_token: Optional[str] = None,  # noqa: UP045
    ) -> Incomplete:
        """
        GetProjectBatch

        POST /v3alpha/projectbatch

        GetProjectBatch performs GetProjectBatch requests for a batch of projects. Large result sets may be paginated.

        Example:

        curl -d @- 'https://api.deps.dev/v3alpha/projectbatch' <<EOF
        {
        "requests":[
            {"projectKey":{"id":"github.com/facebook/react"}},
            {"projectKey":{"id":"github.com/angular/angular"}}
        ]
        }
        EOF

        Request body

        requests[]: object[]

            The batch list of projects to return Project information for. Up to 5000 requests are allowed in a single batch.
        requests[].projectKey: object
        requests[].projectKey.id: string

            A project identifier of the form github.com/user/repo, gitlab.com/user/repo, or bitbucket.org/user/repo.
        pageToken: string

            If set, request the next page of the result set. It must be set to the page token provided by the previous project batch response. All other request fields must be the same as in the initial request.
        """  # noqa: E501
        payload = {
            "requests": [{"projectKey": {"id": x}} for x in project_ids],
            "pageToken": page_token,
        }
        return await self._requests(method="POST", url="/v3alpha/projectbatch", json=payload)

    async def get_project_package_versions(self, project_id: str) -> Incomplete:
        """
        GetProjectPackageVersions

        GET /v3alpha/projects/{projectKey.id}:packageversions

        GetProjectPackageVersions returns known mappings between the requested project and package versions. At most 1500 package versions are returned. Mappings which were derived from attestations are served first.

        Example: /v3alpha/projects/github.com%2Ffacebook%2Freact:packageversions
        Path parameters

        projectKey.id: string

            A project identifier of the form github.com/user/repo, gitlab.com/user/repo, or bitbucket.org/user/repo.
        """  # noqa: E501
        return await self._requests(
            method="GET", url=f"/v3alpha/projects/{url_escape(project_id)}:packageversions"
        )

    async def get_advisory(self, advisory_id: str) -> Incomplete:
        """
        GetAdvisory

        GET /v3alpha/advisories/{advisoryKey.id}

        GetAdvisory returns information about security advisories hosted by OSV.

        Example: /v3alpha/advisories/GHSA-2qrg-x229-3v8q
        Path parameters

        advisoryKey.id: string

            The OSV identifier for the security advisory.
        """
        return await self._requests(
            method="GET", url=f"/v3alpha/advisories/{url_escape(advisory_id)}"
        )

    async def get_similarly_named_packages(self, system: System, name: str) -> Incomplete:
        """
        GetSimilarlyNamedPackages

        GET /v3alpha/systems/{packageKey.system}/packages/{packageKey.name}:similarlyNamedPackages

        GetSimilarlyNamedPackages returns packages with names that are similar to the requested package. This similarity relation is computed by deps.dev.

        Example: /v3alpha/systems/npm/packages/jost:similarlyNamedPackages
        Path parameters

        packageKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        packageKey.name: string

            The name of the package.

        """  # noqa: E501
        return await self._requests(
            method="GET",
            url=f"/v3alpha/systems/{system}/packages/{url_escape(name)}:similarlyNamedPackages",
        )

    async def query(
        self,
        hash_type: Optional[HashType] = None,  # noqa: UP045
        hash_value: Optional[str] = None,  # noqa: UP045
        system: Optional[System] = None,  # noqa: UP045
        name: Optional[str] = None,  # noqa: UP045
        version: Optional[str] = None,  # noqa: UP045
    ) -> Incomplete:
        """
        Query

        GET /v3alpha/query

        Query returns information about multiple package versions, which can be specified by name, content hash, or both. If a hash was specified in the request, it returns the artifacts that matched the hash.

        Querying by content hash is currently supported for npm, Cargo, Maven, NuGet, PyPI, and RubyGems. It is typical for hash queries to return many results; hashes are matched against multiple release artifacts (such as JAR files) that comprise package versions, and any given artifact may appear in several package versions.

        Examples:

            /v3alpha/query?hash.type=SHA1&hash.value=ulXBPXrC%2FUTfnMgHRFVxmjPzdbk%3D
            /v3alpha/query?versionKey.system=NPM&versionKey.name=react&versionKey.version=18.2.0

        Query parameters

        hash.type: string

            The function used to produce this hash.

            Can be one of MD5, SHA1, SHA256, SHA512.
        hash.value: string

            A hash value.
        versionKey.system: string

            The package management system containing the package.

            Can be one of GO, RUBYGEMS, NPM, CARGO, MAVEN, PYPI, NUGET.
        versionKey.name: string

            The name of the package.
        versionKey.version: string

            The version of the package.
        """  # noqa: E501
        params = {
            "hash.type": hash_type.value if hash_type else None,
            "hash.value": hash_value,
            "versionKey.system": system.value if system else None,
            "versionKey.name": name,
            "versionKey.version": version,
        }
        params = {k: v for k, v in params.items() if v is not None}  # Filter out None values
        return await self._requests(method="GET", url="/v3alpha/query", params=params)  # type: ignore[arg-type,unused-ignore]

    async def purl_lookup(self, purl: Union[PUrlStr, PUrlWithVersionStr]) -> Incomplete:  # noqa: UP007
        """
        PurlLookup

        GET /v3alpha/purl/{purl}

        PurlLookup searches for a package or package version specified via purl, and returns the corresponding result from GetPackage or GetVersion as appropriate.

        For a package lookup, the purl should be in the form pkg:type/namespace/name for a namespaced package name, or pkg:type/name for a non-namespaced package name.

        For a package version lookup, the purl should be in the form pkg:type/namespace/name@version, or pkg:type/name@version.

        Extra fields in the purl must be empty, otherwise the request will fail. In particular, there must be no subpath or qualifiers.

        Supported values for type are cargo, gem, golang, maven, npm, nuget, and pypi. Further details on types, and how to form purls of each type, can be found in the purl spec.

        Special characters in purls must be percent-encoded. This is described in detail by the purl spec.

        Examples:

            /v3alpha/purl/pkg%3Anpm%2F%2540colors%2Fcolors
            /v3alpha/purl/pkg%3Anpm%2F%2540colors%2Fcolors%401.5.0

        Path parameters

        purl: string

            The purl to search for.
        """  # noqa: E501
        return await self._requests(method="GET", url=f"/v3alpha/purl/{url_escape(purl)}")

    async def purl_lookup_batch(
        self,
        purls: list[PUrlWithVersionStr],
        page_token: Optional[str] = None,  # noqa: UP045
    ) -> Incomplete:
        """
        PurlLookupBatch

        POST /v3alpha/purlbatch

        PurlLookupBatch performs PurlLookup requests for a batch of purls. This endpoint only supports version lookups. Purls in requests must include a version field.

        Supported purl forms are pkg:type/namespace/name@version for a namespaced package name, or pkg:type/name@version for a non-namespaced package name.

        Extra fields in the purl must be empty, otherwise the request will fail. In particular, there must be no subpath or qualifiers.

        Large result sets may be paginated.

        Example:

        curl -d @- 'https://api.deps.dev/v3alpha/purlbatch' <<EOF
        {
        "requests":[
            {"purl":"pkg:npm/%40colors/colors@1.5.0"},
            {"purl":"pkg:nuget/castle.core@5.1.1"}
        ]
        }
        EOF

        Request body

        requests[]: object[]

            The batch list of purls to search for. Up to 5000 requests are allowed in a single batch.
        requests[].purl: string

            The purl to search for.
        pageToken: string

            If set, request the next page of the result set. It must be set to the page token provided by the previous purl lookup batch response. All other request fields must be the same as in the initial request.
        """  # noqa: E501
        payload = {"requests": [{"purl": x} for x in purls], "pageToken": page_token}
        return await self._requests(method="POST", url="/v3alpha/purlbatch", json=payload)

    async def query_container_images(self, chain_id: str) -> Incomplete:
        """
        QueryContainerImages

        GET /v3alpha/querycontainerimages/{chainId}

        QueryContainerImages searches for container image repositories on DockerHub that match the requested OCI Chain ID. At most 1000 image repositories are returned.

        An image repository is identifier (eg. 'tensorflow') that refers to a collection of images.

        An OCI Chain ID is a hashed encoding of an ordered sequence of OCI layers. For further details see the OCI Chain ID spec.
        Path parameters

        chainId: string

            An OCI Chain ID referring to an ordered sequence of OCI layers.
        """  # noqa: E501
        return await self._requests(
            method="GET", url=f"/v3alpha/querycontainerimages/{url_escape(chain_id)}"
        )


if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        client = DepsDevClientV3Alpha()
        system = System.NPM
        name = "@colors/colors"
        version = "1.5.0"
        project_id = "github.com/facebook/react"
        advisory_id = "GHSA-2qrg-x229-3v8q"
        print(await client.get_package(system, name))
        print(await client.get_version(system, name, version))
        print(await client.get_requirements(system, name, version))
        print(await client.get_dependencies(system, name, version))
        print(await client.get_project(project_id))
        print(await client.get_project_package_versions(project_id))
        print(await client.get_advisory(advisory_id))

        print(
            await client.query(
                system=System.NPM,
                name="react",
                version="18.2.0",
            )
        )

        print(
            await client.get_version_batch(
                [
                    {"system": "NPM", "name": "@colors/colors", "version": "1.5.0"},
                    {"system": "NUGET", "name": "castle.core", "version": "5.1.1"},
                ]
            )
        )
        print(await client.get_dependents(system, name, version))
        # print(await client.get_capabilities(system, name, version))
        print(
            await client.get_project_batch(
                ["github.com/facebook/react", "github.com/angular/angular"]
            )
        )

        purl1 = "pkg:npm/@colors/colors"
        purl2 = "pkg:npm/@colors/colors@1.5.0"
        print(await client.get_similarly_named_packages(system, name))
        print(await client.purl_lookup(purl1))
        print(await client.purl_lookup_batch([purl2]))
        # print(await client.query_container_images(""))

    asyncio.run(main())
