from datetime import timedelta
from pathlib import Path

from cement import App, TestApp
from cement.core.exc import CaughtSignal
from tinydb import TinyDB

from akinoncli.client.client import AkinonCloudClient
from akinoncli.controllers.account import Certificates, Domains
from akinoncli.controllers.applications import Applications, ApplicationTypes
from akinoncli.controllers.auth import Auth
from akinoncli.controllers.base import Base
from akinoncli.controllers.clusters import KubeMetricMonitor
from akinoncli.controllers.projects import Addons, ProjectApps, Projects
from akinoncli.controllers.public_keys import PublicKeys
from akinoncli.core.exc import AkinonCLIError, AkinonCLIWarning
from akinoncli.core.version import get_version
from akinoncli.ext.output_renderer import AkinonOutputHandler
from akinoncli.ext.update_checker import ThrottledUpdateChecker, TinyDbStorage

db_path = Path('~/.akinoncli/db.json').expanduser().resolve()


def get_db() -> TinyDB:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(db_path)


def check_updates(*_):
    db = get_db()
    checker = ThrottledUpdateChecker(package_name='akinoncli', duration=timedelta(hours=1), storage=TinyDbStorage(db))
    new_version = checker.check(current_version=get_version())
    if not new_version:
        return
    print('A new version is available: {}'.format(new_version.version))


def extend_tinydb(app):
    app.extend('db', get_db())


def extend_client(app):
    urls_table = app.db.table('urls')
    base_url = 'http://localhost:8000/api/v1/'
    if len(urls_table) > 0:
        base_url = urls_table.get(doc_id=1).get('base_url')
    user = app.db.get(doc_id=1)
    token = None
    if user:
        token = user.get('token')
    app.extend('client', AkinonCloudClient(base_url, token))


class AkinonCLI(App):
    """Akinon CLI primary application."""

    class Meta:
        label = 'akinoncli'

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'akinon_output_handler'

        # register handlers
        handlers = [
            AkinonOutputHandler,
            Base,
            Auth,
            # Clusters,
            Projects,
            ProjectApps,
            Applications,
            # ApplicationUsers,
            ApplicationTypes,
            PublicKeys,
            # Users,
            # Roles,
            Domains,
            Certificates,
            Addons,
            KubeMetricMonitor,
        ]

        hooks = [
            ('pre_setup', check_updates),
            ('post_setup', extend_tinydb),
            ('post_setup', extend_client),
        ]


class AkinonCLITest(TestApp, AkinonCLI):
    """A sub-class of AkinonCLI that is better suited for testing."""

    class Meta:
        label = 'akinoncli'


def main():
    with AkinonCLI() as app:
        try:
            app.run()

        except AssertionError as e:
            print(f'AssertionError > {e.args[0]}')
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except AkinonCLIError as e:
            app.log.error(f'{e.message}')
            app.exit_code = 1

            if e.response is not None:
                app.log.error(e.response.text)
            if app.debug is True:
                import traceback

                traceback.print_exc()
        except AkinonCLIWarning as e:
            app.log.warning(f'{e.message}')
        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print(f'\n{e}')
            app.exit_code = 0


if __name__ == '__main__':
    main()
