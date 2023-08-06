from __future__ import annotations
from . import errors
import subprocess
import asyncio

class Package:
    """
    A base class that wraps around Pip packages

    :param name: The name of the package.
    :type name: str
    :param version: The version of the package.
    :type version: str
    :attr name: The name of the package.
    :attr version: The version of the package.
    """
    def __init__(self, name: str, version: str, author: str, summary: str, description: str, maintainer: str,
                 license: str, author_email: str, classifiers: list, homepage: str, keywords: str, docs: str):
        self._name = name
        self._version = version
        self._author = author
        self._summary = summary
        self._description = description
        self._license = license
        self._author_email = author_email
        self._classifiers = classifiers
        self._homepage = homepage
        self._keywords = keywords
        self._docs = docs
        self._maintainer = maintainer

    @property
    def name(self):
        """
        Returns the name of the package.

        :return: The name of the package.
        :rtype: str
        """
        return self._name

    @property
    def index(self):
        """
        Returns the index URL for the package.

        :return: The index URL for the package.
        :rtype: str
        """
        return "https://pypi.org/simple"

    @property
    def version(self):
        """
        Returns the version of the package.

        :return: The version of the package.
        :rtype: str
        """
        return self._version

    @property
    def author(self):
        """
        Returns the author of the package.

        :return: The author of the package.
        :rtype: str
        """
        return self._author

    @property
    def summary(self):
        """
        Returns the summary of the package.

        :return: The summary of the package.
        :rtype: str
        """
        return self._summary

    @property
    def license(self):
        """
        Returns the license of the package.

        :return: The license of the package.
        :rtype: str
        """
        return self._license

    @property
    def maintainer(self):
        """
        Returns the maintainer of the package.

        :return: The maintainer of the package.
        :rtype: str
        """
        return self._maintainer

    @property
    def description(self):
        """
        Returns the description of the package.

        :return: The description of the package.
        :rtype: str
        """
        return self._description

    @property
    def author_email(self):
        """
        Returns the author email of the package.

        :return: The author email of the package.
        :rtype: str
        """
        return self._author_email

    @property
    def classifiers(self):
        """
        Returns the classifiers of the package.

        :return: The classifiers of the package.
        :rtype: list
        """
        return self._classifiers

    @property
    def homepage(self):
        """
        Returns the homepage of the package.

        :return: The homepage of the package.
        :rtype: str
        """
        return self._homepage

    @property
    def docs(self):
        """
        Returns the documentation URL of the package.

        :return: The documentation URL of the package.
        :rtype: str
        """
        return self._docs

    @property
    def issue_tracker(self):
        """
        Returns the issue tracker of the package.

        :return: The issue tracker of the package.
        :rtype: str
        """
        return self._issue_tracker

    def _err_checking(self, output):
        """
        Checks the output of a subprocess.run call for errors.

        :param output: The output of a subprocess.run call.
        :type output: str
        :raises PackageNotFoundException: The package was not found.
        :raises VersionNotFoundException: The version was not found.
        :raises ConnectionException: The connection to PyPi was unsuccessful.
        """
        name = self.name
        name += f"=={self._version}"
        not_found = f"ERROR: Could not find a version that satisfies the requirement {name} (from versions: {self._version}) \
        \nERROR: No matching distribution found for {name}"
        if not_found in output:
            raise errors.PackageNotFoundException(
                f"{name} is not a valid package!"
            )
        not_found = f"ERROR: No matching distribution found for {name}=={self._version}"
        if not_found in output:
            raise errors.VersionNotFoundException(
                f"{self._version} does not exist!"
            )
        invalid_connection = f"WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) \
        after connection broken by "
        not_found = f"ERROR: Could not find a version that satisfies the requirement {name} (from versions: {self._version})\
                \nERROR: No matching distribution found for {name}"
        if invalid_connection in output and not_found in output:
            raise errors.ConnectionException(
                f"PyPi could not be reached! Full error: {output}"
            )
        not_installable = f"ERROR: Directory '{name}' is not installable. Neither setup.py nor 'pyproject.toml' found."
        if not_installable in output:
            raise errors.PackageNotFoundException(
                f"{name} is not a valid package!"
            )

    async def install(self):
        """
        Installs a package through the Pip API. Returns a Package object for the installed package.

        :return: A Package object for the installed package.
        :rtype: Package
        :raises PackageNotFoundException: The package was not found.
        :raises self.VersionNotFoundException: The version was not found.
        :raises ConnectionException: The connection to PyPi was unsuccessful.
        """
        empty = ""
        version_str = f"=={self._version}"
        command = f"pip install --index-url {self.index} {self._name}{version_str if self._version else empty}"
        out = await asyncio.create_subprocess_shell(command, stderr=asyncio.subprocess.PIPE)
        self._err_checking(out.stderr.decode())

    def uninstall(self, name):
        """
        Uninstalls a package through the Pip API.

        :param name: The name of the package to uninstall.
        :raises PackageNotFoundException: The package was not found.
        """
        out = await asyncio.create_subprocess_shell(f"pip uninstall {name} -y", stderr=asyncio.subprocess.PIPE)
        out = out.stderr.decode()
        not_installable = f"ERROR: Directory '{name}' is not installable. Neither setup.py nor 'pyproject.toml' \
                          found."
        if not_installable in out:
            raise errors.PackageNotFoundException(
                f"{name} is not a valid package!"
            )
        invalid_package = f"WARNING: Skipping {name} as it is not installed."
        if invalid_package in out:
            raise errors.PackageNotFoundException(
                f"{name} is not installed!"
            )

    def __str__(self):
        """
        Returns the name and version of the package.

        :return: The name and version of the package.
        :rtype: str
        """
        return f"{self._name}=={self._version}"

    def __repr__(self):
        """
        Returns a representation of the package.

        :return: A representation of the package.
        :rtype: str
        """
        return f"Package({self._name.__repr__()}, {self._version.__repr__()}, author={self._author.__repr__()}, summary={self._summary.__repr__()}, description={self._description.__repr__()}, license={self._license.__repr__()})"
