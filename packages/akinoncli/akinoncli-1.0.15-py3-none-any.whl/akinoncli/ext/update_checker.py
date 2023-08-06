import dataclasses
import datetime
import typing

import requests
import tinydb.table
from packaging.version import Version
from tinydb import TinyDB


class Storage(typing.Protocol):
    """
    A generic kv storage interface
    """

    def get(self, key: str) -> typing.Optional[typing.Any]:
        ...

    def set(self, key: str, value) -> None:
        ...


class InMemoryStorage(dict):
    """
    A simple in-memory storage implementation
    """

    get = dict.__getitem__
    set = dict.__setitem__


class TinyDbStorage:
    """
    A storage implementation using tinydb
    """

    def __init__(self, db: tinydb.TinyDB, table: str = 'kv'):
        self.db = db
        self.table = db.table(table)

    def get(self, key: str):
        doc: dict = self.table.get(doc_id=1)
        if doc is None:
            return None
        return doc.get(key)

    def set(self, key: str, value) -> None:
        doc: dict = self.table.get(doc_id=1)
        if doc is None:
            doc = {}
            self.table.insert(doc)
        doc[key] = value
        self.table.update(doc, doc_ids=[1])


@dataclasses.dataclass()
class VersionInfo:
    """
    A class to hold the version information for a package.
    """

    package_name: str
    version: Version
    release_date: datetime.datetime


class UpdateChecker(typing.Protocol):
    """
    A generic update checker interface
    """

    def check(self, current_version: str) -> typing.Optional[VersionInfo]:
        ...


class PypiUpdateChecker:
    """
    Checks for updates on PyPI.
    """

    def __init__(self, package_name: str, timeout: int = 2):
        """
        :param package_name: The name of the package to check for updates.
        :param timeout: The timeout for the requests.
        """
        self.package_name = package_name
        self.timeout = timeout

    def check(self, current_version: str) -> typing.Optional[VersionInfo]:
        """
        Check if there is a new version of the package and returns the new version if there is.
        """
        releases = self.get_releases()
        if not releases:
            return None

        last_release = sorted(releases, key=lambda it: it.version)[-1]

        if last_release.version <= Version(current_version):
            return None

        return last_release

    def get_releases(self) -> typing.List[VersionInfo]:
        url = f'https://pypi.org/pypi/{self.package_name}/json'
        try:
            res = requests.get(url, timeout=self.timeout)
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.RequestException:
            # don't let pypi errors prevent regular usage
            return []

        return [
            VersionInfo(
                package_name=self.package_name,
                version=Version(version),
                release_date=datetime.datetime.fromisoformat(it['upload_time']),
            )
            for version, (it, *_) in data['releases'].items()
        ]


class ThrottledUpdateChecker:
    """
    Checks for updates every `duration` seconds.
    """

    def __init__(
        self,
        package_name: str,
        storage: Storage,
        duration: datetime.timedelta,
        checker: typing.Optional[UpdateChecker] = None,
    ):
        """
        :param package_name: The name of the package to check for updates.
        :param db: The database to store the last check time in.
        :param duration: The time between checks.
        """
        self.checker = checker or PypiUpdateChecker(package_name)
        self.storage = storage
        self.duration = duration

    def check(self, current_version: str) -> typing.Optional[VersionInfo]:
        """
        Checks if there is a new version of the package if the last check was more than `duration` ago.
        """
        check_ts: str = self.storage.get('last_update_check')

        if not check_ts:
            checked_at = datetime.datetime.fromtimestamp(0)
        else:
            checked_at = datetime.datetime.fromisoformat(check_ts)

        elapsed = datetime.datetime.now() - checked_at
        if elapsed < self.duration:
            return None

        self.storage.set('last_update_check', datetime.datetime.now().isoformat())
        return self.checker.check(current_version)


if __name__ == '__main__':
    c = ThrottledUpdateChecker('akinoncli', TinyDbStorage(TinyDB('db.json')), datetime.timedelta(seconds=10))
    print(c.check('0.0.1'))
