import os
from datetime import datetime, timedelta, timezone

from cement import Controller, ex, shell
from cement.utils.version import get_version_banner

from ..core.exc import AkinonCLIError, AkinonCLIWarning
from ..core.version import get_version
from . import PaginationEnum

VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


class Projects(Controller):
    class Meta:
        label = 'project'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the project controller namespace'

    @ex(
        help='Project List Command',
        arguments=[PaginationEnum.ARG],
    )
    def list(self):
        response = self.app.client.get_projects(qs={"page": getattr(self.app.pargs, PaginationEnum.KEY)})
        self.app.render(
            data=response.data,
            rows=response.data.get('results', []),
            headers={'pk': 'ID', 'slug': 'Slug', 'name': 'Name'},
            is_succeed=response.is_succeed,
        )

    @ex(
        help='Project Create Command',
        arguments=[
            (
                ['name'],
                {
                    'help': 'Project name',
                    'action': 'store',
                },
            ),
            (
                ['slug'],
                {
                    'help': 'Project slug',
                    'action': 'store',
                },
            ),
            (
                ['--mainapp-required'],
                {
                    'help': 'if main app is required. Choose main app required as true.',
                    'action': 'store_true',
                    'dest': 'is_main_app_required',
                },
            ),
            (
                ['--mainapp-initialize'],
                {
                    'help': 'Allow you to initialize main app automatically.',
                    'action': 'store_true',
                    'dest': 'initialize_main_app',
                },
            ),
        ],
    )
    def create(self):
        data = {
            'name': self.app.pargs.name,
            'slug': self.app.pargs.slug,
            'is_main_app_required': self.app.pargs.is_main_app_required,
            'initialize_default_app_on_creation': self.app.pargs.initialize_main_app,
        }
        response = self.app.client.create_project(data)
        if response.is_succeed:
            self.app.render("Project has been created.", renderer_type='text')
        else:
            self.app.render(response.data['slug'][0], renderer_type='text')

    @ex(
        help='Project Update Command',
        arguments=[
            (
                ['id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['name'],
                {
                    'help': 'New project name',
                    'action': 'store',
                },
            ),
        ],
    )
    def update(self):
        p_id = self.app.pargs.id
        data = {
            'name': self.app.pargs.name,
        }
        response = self.app.client.update_project(p_id, data)
        if response.is_succeed:
            self.app.render("Project has been updated.", renderer_type='text')
        else:
            self.app.render(response.data, renderer_type='text')


class ProjectApps(Controller):
    class Meta:
        label = 'projectapp'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the project app controller namespace'

    @ex(
        help='Project App List Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            PaginationEnum.ARG,
        ],
    )
    def list(self):
        p_id = self.app.pargs.project_id
        response = self.app.client.get_project_apps(p_id=p_id, qs={"page": getattr(self.app.pargs, PaginationEnum.KEY)})
        rows = response.data.get('results', [])
        for row in rows:
            row['app'] = row['app']['name']
            row['project'] = row['project']['name']
            row['env'] = ''
            for key, value in row['custom_env'].items():
                row['env'] += f'{key}={value}\n'
        self.app.render(
            data=response.data,
            rows=response.data.get('results', []),
            headers={
                'pk': 'ID',
                'project': 'Project',
                'app': 'App',
                'url': 'URL',
                'created_date': 'Created Date',
                'env': 'ENV Variables',
            },
            is_succeed=response.is_succeed,
        )

    @ex(
        help='Project App Add or Update Environment Value Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['project_app_id'],
                {
                    'help': 'Project App ID',
                    'action': 'store',
                },
            ),
            (['env_variables'], {'help': 'Environment Variables (KEY=VALUE)', 'action': 'store', 'nargs': '+'}),
            (
                ['--deploy'],
                {
                    'help': "Redeploy the current version to activate environment variable changes.",
                    'action': 'store_true',
                    'dest': 'deploy',
                    'default': False,
                },
            ),
        ],
    )
    def add_env(self):
        p_id = self.app.pargs.project_id
        pa_id = self.app.pargs.project_app_id
        new_env_variables = dict([tuple(env.split('=', maxsplit=1)) for env in self.app.pargs.env_variables])
        response = self.app.client.update_project_app_custom_env(p_id, pa_id, data=new_env_variables)
        project_app = self.app.client.get_project_app(p_id, pa_id)
        if response.is_succeed:
            if self.app.pargs.deploy:
                current_deployment_tag = {'tag': project_app.data['current_deployment']['version']}
                self.app.client.deploy_project_app(p_id, pa_id, data=current_deployment_tag)

            row = response.data
            row['env'] = ''
            row['pk'] = project_app.data['pk']
            row['created_date'] = project_app.data['created_date']
            row['app'] = project_app.data['app']['name']
            row['project'] = project_app.data['project']['name']
            for key, value in row['custom_env'].items():
                row['env'] += f'{key}={value}\n'

            self.app.render(
                data=response.data,
                rows=[row],
                headers={
                    'pk': 'ID',
                    'project': 'Project',
                    'app': 'App',
                    'created_date': 'Created Date',
                    'env': 'ENV Variables',
                },
                is_succeed=response.is_succeed,
            )
        else:
            self.app.render(response.data, renderer_type='text')

    @ex(
        help='Project App Remove Environment Value Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['project_app_id'],
                {
                    'help': 'Project App ID',
                    'action': 'store',
                },
            ),
            (['env_keys'], {'help': 'Keys', 'action': 'store', 'nargs': '+'}),
            (
                ['--deploy'],
                {
                    'help': "Redeploy the current version to activate environment variable changes.",
                    'action': 'store_true',
                    'dest': 'deploy',
                    'default': False,
                },
            ),
        ],
    )
    def remove_env(self):
        p_id = self.app.pargs.project_id
        pa_id = self.app.pargs.project_app_id
        env_keys_to_delete = self.app.pargs.env_keys
        response = self.app.client.delete_project_app_custom_env(p_id, pa_id, data=env_keys_to_delete)
        project_app = self.app.client.get_project_app(p_id, pa_id)

        if response.is_succeed:
            if self.app.pargs.deploy:
                current_deployment_tag = {'tag': project_app.data['current_deployment']['version']}
                self.app.client.deploy_project_app(p_id, pa_id, data=current_deployment_tag)

            row = response.data
            row['env'] = ''
            row['pk'] = project_app.data['pk']
            row['created_date'] = project_app.data['created_date']
            row['app'] = project_app.data['app']['name']
            row['project'] = project_app.data['project']['name']

            for key, value in row['custom_env'].items():
                row['env'] += f'{key}={value}\n'

            self.app.render(
                response.data,
                rows=[row],
                headers={
                    'pk': 'ID',
                    'project': 'Project',
                    'app': 'App',
                    'created_date': 'Created Date',
                    'env': 'ENV Variables',
                },
                is_succeed=response.is_succeed,
            )
        else:
            self.app.render(response.data, renderer_type='text')

    @ex(
        help='Project App Add Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['app_id'],
                {
                    'help': 'App ID',
                    'action': 'store',
                },
            ),
        ],
    )
    def add(self):
        p_id = self.app.pargs.project_id
        app_id = self.app.pargs.app_id
        data = {'app': app_id}
        response = self.app.client.get_relatable_project_apps(app_id=app_id, project_id=p_id)
        if response.is_succeed and response.data:
            app = response.data[0]['app']
            project_apps = response.data[0]['project_apps']
            if not project_apps:
                self.app.render(
                    f"App needs a {app['name']} app. Please install a {app['name']} first.", renderer_type='text'
                )
                return

            print(f"This application needs to be related with a {app['name']}.")
            options = []
            for project_app in project_apps:
                options.append(str(project_app['pk']))
                print(f"{project_app['pk']} - {project_app['name']}")

            p = shell.Prompt(f"Enter one of your project app id or exit with (control + c)", options=options)
            child_project_app = p.prompt()
            data.update(extra_data={"child_project_app": child_project_app})

        response = self.app.client.create_project_app(p_id, data)
        if response.is_succeed:
            self.app.render("App has been added to the project.", renderer_type='text')
        else:
            self.app.render(response.data, renderer_type='text')

    @ex(
        help='Project App Deploy Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['project_app_id'],
                {
                    'help': 'Project App ID',
                    'action': 'store',
                },
            ),
            (
                ['tag'],
                {
                    'help': 'Tag',
                    'action': 'store',
                },
            ),
        ],
    )
    def deploy(self):
        p_id = self.app.pargs.project_id
        pa_id = self.app.pargs.project_app_id
        data = {'tag': self.app.pargs.tag}
        response = self.app.client.deploy_project_app(p_id, pa_id, data=data)

        if response.is_succeed:
            self.app.render("ProjectApp deployment has been started.", renderer_type='text')
        else:
            self.app.render(response.data['non_field_errors'], renderer_type='text')

    @ex(
        help='Multiple Project App Deploy Command',
        arguments=[
            (
                ['app_id'],
                {
                    'help': 'Application ID',
                    'action': 'store',
                },
            ),
            (
                ['tag'],
                {
                    'help': 'App Version',
                    'action': 'store',
                },
            ),
            (
                ['--project-apps'],
                {
                    'help': 'Project App IDs',
                    'action': 'store',
                    'nargs': '+',
                    'default': [],
                },
            ),
            (
                ['--deploy-all'],
                {
                    'help': "Deploys all project apps with given app_id and tag.",
                    'action': 'store_true',
                    'dest': 'deploy_all',
                    'default': False,
                },
            ),
        ],
    )
    def deploy_multiple(self):
        data = {
            'tag': self.app.pargs.tag,
            'project_apps': self.app.pargs.project_apps or [],
            'deploy_all': self.app.pargs.deploy_all,
        }
        response = self.app.client.deploy_multiple_project_apps(self.app.pargs.app_id, data)
        if response.is_succeed:
            self.app.render("ProjectApp deployments have been started.", renderer_type='text')
        else:
            self.app.render(response.data["non_field_errors"], renderer_type='text')

    @ex(
        help='Project App Deployment List Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['project_app_id'],
                {
                    'help': 'Project App ID',
                    'action': 'store',
                },
            ),
        ],
    )
    def deployments(self):
        p_id = self.app.pargs.project_id
        pa_id = self.app.pargs.project_app_id
        response = self.app.client.get_project_app_deployments(p_id, pa_id)
        self.app.render(
            data=response.data,
            rows=response.data.get('results', []),
            headers={'pk': 'ID', 'version': 'Version', 'status': 'Status', 'created_date': 'Created Date'},
            is_succeed=response.is_succeed,
        )

    @ex(
        help='Project App Deployment Log List Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['project_app_id'],
                {
                    'help': 'Project App ID',
                    'action': 'store',
                },
            ),
            (['deployment_id'], {'help': 'Deployment ID', 'action': 'store'}),
        ],
    )
    def deployment_logs(self):
        p_id = self.app.pargs.project_id
        pa_id = self.app.pargs.project_app_id
        deployment_id = self.app.pargs.deployment_id
        response = self.app.client.get_project_app_deployment_logs(p_id, pa_id, deployment_id=deployment_id)
        self.app.render(
            data=response.data, rows=response.data, renderer_type="pipeline_log", is_succeed=response.is_succeed
        )

    @ex(
        help='Attach Certificate to Project App',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['project_app_id'],
                {
                    'help': 'Project App ID',
                    'action': 'store',
                },
            ),
            (
                ['certificate_id'],
                {
                    'help': 'Certificate ID',
                    'action': 'store',
                },
            ),
        ],
    )
    def attach_certificate(self):
        p_id = self.app.pargs.project_id
        pa_id = self.app.pargs.project_app_id
        data = {'certificate': self.app.pargs.certificate_id}
        response = self.app.client.update_project_app(p_id, pa_id, data=data)

        if response.is_succeed:
            self.app.render("Certificate has been attached to project app.", renderer_type='text')
        else:
            self.app.render(response.data['non_field_errors'], renderer_type='text')

    @ex(
        help='Detach Certificate to Project App',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (
                ['project_app_id'],
                {
                    'help': 'Project App ID',
                    'action': 'store',
                },
            ),
        ],
    )
    def detach_certificate(self):
        p_id = self.app.pargs.project_id
        pa_id = self.app.pargs.project_app_id
        data = {'certificate': None}
        response = self.app.client.update_project_app(p_id, pa_id, data=data)

        if response.is_succeed:
            self.app.render("Certificate has been detached from project app.", renderer_type='text')
        else:
            self.app.render(response.data['non_field_errors'], renderer_type='text')

    @ex(
        help='Get Project App Logs',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (['project_app_id'], {'help': 'Project App ID', 'action': 'store'}),
            (['-p', '--process'], {'help': 'Process type', 'action': 'store', 'dest': "process_type", 'default': ''}),
        ],
    )
    def logs(self):
        process_type = self.app.pargs.process_type or []
        if process_type:
            process_type = [process_type]

        project_id = self.app.pargs.project_id
        project_app_id = self.app.pargs.project_app_id
        data = {"applications": process_type}

        response = self.app.client.get_project_app_logs(
            project_id=project_id,
            project_app_id=project_app_id,
            data=data,
        )
        rows = response.data.get('items', [])
        for row in rows:
            if 'message' not in row:
                row['message'] = ""

        if len(rows) > 0:
            self.app.render(
                renderer_type="realtime_log",
                data=response.data,
                rows=rows,
                is_succeed=response.is_succeed,
            )
        else:
            self.app.render("No logs found in 1 minute", renderer_type="text")

    @ex(
        help='Export Project App Logs',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (['project_app_id'], {'help': 'Project App ID', 'action': 'store'}),
            (['-d', '--dates'], {'help': 'Dates (YYYY-MM-DD)', 'action': 'store', 'dest': 'dates', 'default': ''}),
            (['-p', '--process'], {'help': 'Process type', 'action': 'store', 'default': ''}),
            (
                ['-s', '--start_date'],
                {'help': 'Start date (YYYY-MM-DD HH:MM)', 'action': 'store', 'dest': 'start_date'},
            ),
            (['-e', '--end_date'], {'help': 'End date (YYYY-MM-DD HH:MM)', 'action': 'store', 'dest': 'end_date'}),
        ],
    )
    def export_logs(self):
        project_id = self.app.pargs.project_id
        project_app_id = self.app.pargs.project_app_id
        dates = self.app.pargs.dates
        applications = self.app.pargs.process
        start_date = self.app.pargs.start_date
        end_date = self.app.pargs.end_date

        if dates and (start_date or end_date):
            raise AkinonCLIError("--dates and (--start_date or --end_date) filters cannot be used together.")

        if start_date and end_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d %H:%M")
                datetime.strptime(end_date, "%Y-%m-%d %H:%M")
            except:
                raise AkinonCLIError("start_date and end_date must be in the format 'YYYY-MM-DD HH:MM'")

        try:
            response = self.app.client.export_project_app_logs(
                project_id=project_id,
                project_app_id=project_app_id,
                dates=dates,
                applications=applications,
                start_date=start_date,
                end_date=end_date,
            )
        except AkinonCLIError as e:
            if e.response.status_code == 406:
                raise AkinonCLIWarning(e.response.json()['non_field_errors'])
            else:
                raise

        self.app.render(response.data['message'], renderer_type='text')


class Addons(Controller):
    class Meta:
        label = 'addon'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the addon controller namespace'

    @ex(
        help='Addon List Command',
        arguments=[
            (
                ['project_id'],
                {
                    'help': 'Project ID',
                    'action': 'store',
                },
            ),
            (['project_app_id'], {'help': 'Project App ID', 'action': 'store'}),
        ],
    )
    def list(self):
        response = self.app.client.get_addons(
            project_id=int(self.app.pargs.project_id), project_app_id=int(self.app.pargs.project_app_id)
        )
        self.app.render(
            data=response.data,
            rows=response.data.get('results', []),
            headers={
                "pk": "ID",
                "addon_type_relation": "Addon Type Relation",
                "project_app": "Project App ID",
                "is_alive": "Is Alive",
                "config": "Config",
                "remote_url": "Remote URL",
                "status": "Status",
                "is_provisioned": "Is Provisioned",
            },
            is_succeed=response.is_succeed,
        )
