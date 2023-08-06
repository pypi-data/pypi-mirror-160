import getpass

from cement import Controller, ex
from cement.utils.version import get_version_banner

from akinoncli.core.exc import AkinonCLIError

from ..core.version import get_version

VERSION_BANNER = """
CLI for Akinon Cloud Commerce %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


class Auth(Controller):
    class Meta:
        label = 'auth'
        stacked_type = 'embedded'
        stacked_on = 'base'
        description = 'this is the auth controller namespace'

    @ex(help='Login Command')
    def login(self):
        if self.app.client.token:
            raise AkinonCLIError(
                "You have already logged in. If you would like to "
                "change your credentials please run 'logout' command"
            )

        email = input('Email:')
        password = getpass.getpass(prompt='Password:')
        data = {
            'email': email,
            'password': password,
        }

        response = self.app.client.login(data)
        if response.is_succeed:
            self.app.db.insert(
                {
                    "token": response.data["token"],
                    "account": response.data["account"],
                }
            )
            self.app.render(
                f"Welcome {response.data['first_name']} {response.data['last_name']}",
                renderer_type='text',
            )
        else:
            self.app.render(response.data["non_field_errors"][0], renderer_type='text')

    @ex(
        help='Logout Command',
        arguments=[],
    )
    def logout(self):
        if self.app.client.token:
            self.app.db.remove(doc_ids=[1])
