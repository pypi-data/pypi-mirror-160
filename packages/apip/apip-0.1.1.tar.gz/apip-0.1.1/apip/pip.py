from .package import Package
from . import errors
import asyncio
import aiohttp
import re


class Client:
    """
    The main class for the apip API wrapper. This class is used to interact with the Pip and PyPi API.

    :param index: The index to install the package from.
    :type index: str

    """
    def __init__(self, index="https://pypi.org/simple"):
        self._index = index

    @property
    def index(self):
        """
        Returns the index to install the package from.

        :return: The index to install the package from.
        :rtype: str
        """
        return self._index

    async def list(self):
        """
        Lists all installed packages and returns them in a list of Package objects.

        :return: A list of Package objects for all installed packages.
        :rtype: list
        """
        packages = []
        output = asyncio.create_subprocess_shell(
            ["pip", "list"],
            stdout=asyncio.subprocess.PIPE
        )
        output = output.stdout.decode()
        output = ' '.join(output.splitlines()[2:])
        output = re.findall('(?! )[a-zA-Z\d\.\-]*', output)
        it = iter(output)
        joined = [[a, b] for a, b in zip(it, it)]
        for index, item in enumerate(joined):
            if item == "":
                output.pop(index)
                continue
            packages.append(Package(item[0], item[1]))
        return packages

    async def get(self, package):
        """
        Returns a Package object for a given package name. Queries data from the PyPi API.

        :param package: The name of the package to get.
        :type package: str
        :return: A Package object for the given package.
        :rtype: Package
        :raises PackageNotFoundException: The package was not found.
        """
        async with aiohttp.ClientSession() as client:
            async with client.get(f"https://pypi.org/pypi/{package}/json") as response:
                if response.status == 404:
                    raise errors.PackageNotFoundException(
                        f"{package} is not a valid package!"
                    )
                data = await response.json()
                return Package(data["info"]["name"], data["version"], data["info"]["author"], data["info"]["summary"],
                               data["info"]["description"], data["info"]["license"], data["info"]["home_page"],
                               data["info"]["keywords"], data["info"]["docs_url"])
