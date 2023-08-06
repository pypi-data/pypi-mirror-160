# Copyright (c) Meta Platforms, Inc. and affiliates.
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import defaultdict
import argparse
import aiohttp
import asyncio
import os
import sys
from pathlib import Path
import re

from util import KernelVersion
from vmtest.download import VMTEST_GITHUB_RELEASE, available_kernel_releases
from vmtest.githubapi import AioGitHubApi

async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cache-directory",
        metavar="DIR",
        type=Path,
        default="build/vmtest",
        help="directory to cache API calls in",
    )
    args = parser.parse_args()

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    if GITHUB_TOKEN is None:
        sys.exit("GITHUB_TOKEN environment variable is not set")
    async with aiohttp.ClientSession(trust_env=True) as session:
        gh = AioGitHubApi(session, GITHUB_TOKEN)
        github_release = await gh.get_release_by_tag(
            *VMTEST_GITHUB_RELEASE, cache=args.cache_directory / "github_release.json"
        )

        grouped_assets = defaultdict(list)
        pattern = re.compile(r"kernel-(?P<major_minor>[0-9]+\.[0-9]+)\.(?P<patch_rc>[0-9]+(?:-rc[0-9]+)?)-vmtest(?P<vmtest>[0-9]+)\.(?P<flavor>[^.]+)\.(?P<arch>[^.]+)\.tar\.zst")
        for asset in github_release["assets"]:
            match = pattern.fullmatch(asset["name"])
            if not match and asset["name"].startswith("kernel-"):
                assert False, TODO
            grouped_assets[(match.group("major_minor"), match.group("flavor"), match.group("arch"))].append((match.group("vmtest") + "." + match.group("patch_rc"), asset))

        to_delete = []
        for assets in grouped_assets.values():
            assets.sort(key=lambda x: KernelVersion(x[0]), reverse=True)
            to_delete.extend(asset for version, asset in assets[2:])

        for asset in to_delete:
            print("Deleting")
            import pprint
            pprint.pprint(asset)
            await gh._request("DELETE", asset["url"], headers={**gh._headers, "Accept": "application/vnd.github+json"})


if __name__ == "__main__":
    asyncio.run(main())
