import asyncio
import json
import logging
import platform
import re
import typing
from asyncio import Lock
from collections import defaultdict
from hashlib import md5
from logging import getLogger
from os import environ
from pathlib import Path

import aiohttp
from dask import config
from importlib_metadata import distributions
from packaging import specifiers, version
from typing_extensions import TypedDict

logger = getLogger("coiled.auto_env")
subdir_datas = {}
cache_dir = Path(config.PATH) / "coiled-cache"


class PackageInfo(TypedDict):
    name: str
    version: str
    include: bool


class CondaPackageInfo(PackageInfo):
    channel: str


class PipPackageInfo(PackageInfo):
    pass


class CondaPackage:
    def __init__(self, meta_json: typing.Dict):
        self.name = meta_json["name"]
        self.version = meta_json["version"]
        self.subdir = meta_json["subdir"]
        channel_regex = f"(.*)/(.*)/{self.subdir}"
        result = re.match(channel_regex, meta_json["channel"])
        assert result
        self.channel_url = result.group(1) + "/" + result.group(2)
        self.channel = result.group(2)


def any_patch_specifier(pkg_version: version.Version) -> specifiers.SpecifierSet:
    return specifiers.SpecifierSet(f"~={pkg_version.major}.{pkg_version.minor}")


class RepoCache:
    # This is not thread safe if there are multiple loops
    channel_memory_cache: typing.DefaultDict[
        str, typing.DefaultDict[str, typing.Dict]
    ] = defaultdict(lambda: defaultdict(dict))

    def __init__(self):
        self.lock = Lock()

    async def fetch(self, channel: str) -> typing.Dict[str, typing.Dict]:
        channel_filename = Path(md5(channel.encode("utf-8")).hexdigest()).with_suffix(
            ".json"
        )
        async with self.lock:
            # check again once we have the lock in case
            # someone beat us to it
            if not self.channel_memory_cache.get(channel):
                if not cache_dir.exists():
                    cache_dir.mkdir(parents=True)
                channel_fp = cache_dir / channel_filename
                headers = {}
                channel_cache_meta_fp = channel_fp.with_suffix(".meta_cache")
                if channel_fp.exists():
                    with channel_cache_meta_fp.open("r") as cache_meta_f:
                        channel_cache_meta = json.load(cache_meta_f)
                    headers["If-None-Match"] = channel_cache_meta["etag"]
                    headers["If-Modified-Since"] = channel_cache_meta["mod"]
                async with aiohttp.ClientSession() as client:
                    resp = await client.get(
                        channel + "/" + "repodata.json", headers=headers
                    )
                    if resp.status == 304:
                        logger.info(f"Loading cached conda repodata for {channel}")
                        data = json.loads(channel_fp.read_text())
                    else:
                        logger.info(f"Downloading fresh conda repodata for {channel}")
                        data = await resp.json()
                        channel_fp.write_text(json.dumps(data))
                        channel_cache_meta_fp.write_text(
                            json.dumps(
                                {
                                    "etag": resp.headers["Etag"],
                                    "mod": resp.headers["Last-Modified"],
                                }
                            )
                        )
                    for pkg in data["packages"].values():
                        self.channel_memory_cache[channel][pkg["name"]][
                            pkg["version"]
                        ] = pkg
                return self.channel_memory_cache[channel]
            else:
                return self.channel_memory_cache[channel]


async def handle_conda_package(pkg_fp: Path, cache: RepoCache):
    pkg = CondaPackage(json.load(pkg_fp.open("r")))
    try:
        parsed_version = version.parse(pkg.version)
        if isinstance(parsed_version, version.LegacyVersion):
            parsed_version = None
            weaker_specifier = None
        else:
            weaker_specifier = any_patch_specifier(parsed_version)
    except version.InvalidVersion:
        parsed_version = None
        weaker_specifier = None
    package_info: CondaPackageInfo = {
        "channel": pkg.channel,
        "name": pkg.name,
        "version": pkg.version,
        "include": True,
    }
    if parsed_version:
        package_info["version"] = f"{parsed_version.major}.{parsed_version.minor}.*"
    if pkg.subdir != "noarch":
        repo_data = await cache.fetch(channel=pkg.channel_url + "/linux-64")
        if repo_data.get(pkg.name):
            version_match = False
            for available_version in repo_data[pkg.name]:
                if weaker_specifier and available_version in weaker_specifier:
                    version_match = True
                    break
            if not version_match:
                package_info["include"] = False
                logger.warning(
                    f"Package {pkg.name} is not available for linux-64 and has been omitted"
                )
        else:
            package_info["include"] = False
            logger.warning(
                f"Package {pkg.name} is not available for linux-64 and has been omitted"
            )
    return package_info


async def iterate_conda_packages(prefix: Path):
    conda_meta = prefix / "conda-meta"
    cache = RepoCache()

    if conda_meta.exists() and conda_meta.is_dir():
        packages = await asyncio.gather(
            *[
                handle_conda_package(metafile, cache)
                for metafile in conda_meta.iterdir()
                if metafile.suffix == ".json"
            ]
        )
        return {pkg["name"]: pkg for pkg in packages}
    else:
        return {}


async def create_conda_env_approximation():
    conda_default_env = environ.get("CONDA_DEFAULT_ENV")
    conda_prefix = environ.get("CONDA_PREFIX")
    if conda_default_env and conda_prefix:
        logger.info(f"Conda environment detected: {conda_default_env}")
        conda_env: typing.Dict[str, CondaPackageInfo] = {}
        return await iterate_conda_packages(prefix=Path(conda_prefix))
    else:
        # User is not using conda, we should just grab their python version
        # so we know what to install
        conda_env: typing.Dict[str, CondaPackageInfo] = {
            "python": {
                "name": "python",
                "version": platform.python_version(),
                "include": True,
                "channel": "conda-forge",
            }
        }
    return conda_env


def create_pip_env_approximation() -> typing.Dict[str, PipPackageInfo]:
    pip_env: typing.Dict[str, PipPackageInfo] = {}
    for dist in distributions():
        installer = dist.read_text("INSTALLER")
        name = dist.metadata.get("Name")
        if not name:
            logger.warning(f"Omitting package missing name, located at {dist._path}")
        if installer:
            installer = installer.rstrip()
            if installer == "pip":
                try:
                    parsed_version = version.parse(dist.version)
                    if isinstance(parsed_version, version.LegacyVersion):
                        v = dist.version
                    else:
                        v = f"{parsed_version.major}.{parsed_version.minor}.*"
                except version.InvalidVersion:
                    v = dist.version
                # TODO: see if we can do the same check as conda
                # for the package availability on the target architecture
                # should drop things without bdist/wheel
                pip_env[name] = {
                    "name": name,
                    "version": v,
                    "include": True,
                }
            elif not installer == "conda":
                logger.warning(
                    f"{name} was installed by the unrecognized installer {installer} and has been omitted"
                )
        # else:
        #     logger.warning(f"{name} has no recognized installer and has been omitted")
    return pip_env


async def create_environment_approximation() -> typing.Tuple[
    typing.List[PipPackageInfo], typing.List[CondaPackageInfo]
]:
    # TODO: path deps
    # TODO: private conda channels
    # TODO: remote git deps (public then private)
    # TODO: detect pre-releases and only set --pre flag for those packages
    loop = asyncio.get_running_loop()

    conda_env_future = asyncio.create_task(create_conda_env_approximation())
    pip_env_future = loop.run_in_executor(None, create_pip_env_approximation)
    conda_env = await conda_env_future
    pip_env = await pip_env_future
    for required_dep in ["dask", "distributed", "bokeh"]:
        if required_dep not in conda_env and required_dep not in pip_env:
            raise ValueError(
                f"{required_dep} is not detected your environment. You must install these packages"
            )
    return list(pip_env.values()), list(conda_env.values())


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(level=logging.INFO)
    asyncio.run(create_environment_approximation())
