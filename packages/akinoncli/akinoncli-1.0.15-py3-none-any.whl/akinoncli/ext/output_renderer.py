import rich
from cement.core.output import OutputHandler
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table


class BaseRenderer:
    def __init__(self, *args, **kwargs):
        self.run_validations(*args, **kwargs)
        self.output = self.render(*args, **kwargs)

    def run_validations(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass


class TableRenderer(BaseRenderer):
    def run_validations(self, *args, **kwargs):
        rows = kwargs.get('rows')
        assert rows is not None
        assert isinstance(rows, list)

        headers = kwargs.get('headers')
        assert headers is not None
        assert isinstance(headers, dict)

    def render(self, *args, **kwargs):
        headers = kwargs.get('headers')
        column_kwargs = kwargs.get('column_kwargs', {})
        table_kwargs = kwargs.get('table_kwargs', {})
        rows = kwargs.get('rows')
        table = Table(expand=True, show_lines=True, **table_kwargs)
        for key, header in headers.items():
            table.add_column(header, overflow="fold", **column_kwargs.get(key, {}))

        for datum in rows:
            row = list()
            for col in headers.keys():
                value = datum[col]
                if isinstance(value, bool):
                    value = 'Yes' if value else 'No'
                row.append(str(value))
            table.add_row(*row)

        console = Console(highlight=False)
        console.print(table)


class RealtimeLogRenderer(BaseRenderer):
    def run_validations(self, *args, **kwargs):
        rows = kwargs.get('rows')
        assert rows is not None
        assert isinstance(rows, list)

    def render(self, *args, **kwargs):
        rows = kwargs.get('rows')
        text = ''
        for row in rows:
            text += f'[bold]{row.get("application_type")}:[/bold] {row.get("message")}\n'

        console = Console(highlight=False)
        console.print(text)


class TextRenderer(BaseRenderer):
    def render(self, data, *args, **kwargs):
        print(data)


class RichRenderer(BaseRenderer):
    console = Console()

    def render(self, *args, **kwargs):
        self.console.print(*args, **kwargs)


class PipelineLogRenderer(BaseRenderer):
    def render(self, *args, **kwargs):
        rows = kwargs.get('rows', [])
        if not rows:
            rich.print(Panel("No log found."))
        for row in rows:
            rich.print(Panel(f'{escape(row.get("log_data"))}', title=f"[bold][red]{row.get('created_date')}[/]"))


class AkinonOutputHandler(OutputHandler):
    renderers = {
        "text": TextRenderer,
        "rich": RichRenderer,
        "realtime_log": RealtimeLogRenderer,
        "table": TableRenderer,
        "pipeline_log": PipelineLogRenderer,
    }

    class Meta:
        label = 'akinon_output_handler'

    def render(self, data, *args, renderer_type: str = 'table', is_succeed: bool = False, **kwargs):
        kwargs.pop('template', None)
        if is_succeed or renderer_type == 'text':
            self.renderers.get(renderer_type)(data, *args, **kwargs)
        else:
            self.app.log.error(data)
