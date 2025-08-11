# flake8: noqa: E501
from __future__ import annotations

import asyncio
import itertools
import os
import shutil
import subprocess
import sys
from typing import TYPE_CHECKING
from typing import NamedTuple

from rich.console import Console
from rich.table import Table

from depsdev.osv import OSVClientV1

if TYPE_CHECKING:
    from collections.abc import Iterable

    from depsdev.osv import OSVVulnerability
    from depsdev.osv import V1Query
    from depsdev.v3alpha import PurlDict


class MavenPackage(NamedTuple):
    group: str
    artifact: str
    version: str
    type: str
    classifier: str
    optional: bool = False

    @classmethod
    def parse(cls, line: str) -> MavenPackage:
        package, *rest = line.split()
        is_optional = bool(rest)
        group, artifact, _type, version, *classifier = package.split(":")
        return cls(
            group=group,
            artifact=artifact,
            version=version,
            type=_type,
            classifier="" if not classifier else classifier[0],
            optional=is_optional,
        )

    def purl_dict(self) -> PurlDict:
        return {"name": f"{self.group}:{self.artifact}", "version": self.version, "system": "MAVEN"}

    def purl(self) -> str:
        return f"pkg:maven/{self.group}/{self.artifact}@{self.version}"


def extract_packages_from_maven_dependency_tree(lines: Iterable[str]) -> list[MavenPackage]:
    stage1 = (x.rstrip() for x in lines if x.strip())
    stage2 = itertools.dropwhile(lambda x: not x.startswith("[INFO] --- "), stage1)
    stage3 = itertools.takewhile(
        lambda x: not x.startswith(
            "[INFO] ------------------------------------------------------------------------"
        ),
        stage2,
    )
    stage4 = itertools.islice(stage3, 1, None)  # Skip the first line
    stage5 = (x[7:] for x in stage4)
    stage6 = (x.split("- ", maxsplit=1)[-1] for x in stage5)
    stage7 = (MavenPackage.parse(line) for line in stage6)
    return list(stage7)
    # return [x.purl() for x in stage7]


def get_version_fix(vuln: OSVVulnerability) -> str | None:
    for affected in vuln.get("affected", []):
        for _range in affected.get("ranges", []):
            for event in _range.get("events", []):
                if "fixed" in event:
                    return event["fixed"]
    return None


async def get_vulns(purls: list[str], osv_client: OSVClientV1) -> dict[str, list[OSVVulnerability]]:
    queries: list[V1Query] = [
        {
            "package": {"purl": purl},
        }
        for purl in purls
    ]
    result = await osv_client.querybatch({"queries": queries})
    r = {k: [x["id"] for x in v["vulns"]] for k, v in zip(purls, result["results"]) if v}
    all_result = await asyncio.gather(
        *[osv_client.get_vuln(vuln_id) for vuln_id in itertools.chain.from_iterable(r.values())]
    )
    look_up = {vuln["id"]: vuln for vuln in all_result}
    return {purl: [look_up[vuln_id] for vuln_id in vuln_ids] for purl, vuln_ids in r.items()}


async def main_inner() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Analyse Maven dependencies for vulnerabilities.")
    _ = parser.parse_args()

    packages: list[MavenPackage] = []
    if not os.isatty(0):
        packages.extend(extract_packages_from_maven_dependency_tree(sys.stdin))
    else:
        if not os.path.exists("pom.xml"):
            print(
                "No input provided. Please pipe Maven dependency tree output to this script or run it in a directory with a pom.xml file."
            )
            return 1
        executable = "./mvnw" if os.path.exists("./mvnw") else shutil.which("mvn")
        if not executable:
            print(
                "Maven executable not found. Please ensure Maven is installed and available in your PATH."
            )
            return 1
        result = subprocess.run(  # noqa: ASYNC221, S603
            [executable, "dependency:tree"], capture_output=True, text=True, check=True
        )
        if result.returncode != 0:
            print(
                "Failed to run Maven dependency tree. Ensure Maven is installed and the command is correct."
            )
            print(result.stderr)
            return 1
        packages.extend(extract_packages_from_maven_dependency_tree(result.stdout.splitlines()))

    packages.extend(
        [MavenPackage("org.yaml", "snakeyaml", "1.19", "jar", "")]
    )  # For testing purposes
    print(f"Analysing {len(packages)} packages...")
    console = Console()

    osv_client = OSVClientV1()

    results = await get_vulns([pkg.purl() for pkg in packages], osv_client)
    print(f"Found {len(results)} packages with advisories.")

    for purl, advisories in results.items():
        table = Table(title=purl)

        table.add_column("Id")
        table.add_column("Summary", style="cyan", no_wrap=True)
        table.add_column("Fixed", style="magenta")

        for vuln in advisories:
            table.add_row(
                f"[link=https://github.com/advisories/{vuln['id']}]{vuln['id']}[/link]",
                vuln["summary"],
                get_version_fix(vuln) or "unknown",
            )
        console.print(table)
    return 0


def main() -> int:
    return asyncio.run(main_inner())


if __name__ == "__main__":
    raise SystemExit(main())
