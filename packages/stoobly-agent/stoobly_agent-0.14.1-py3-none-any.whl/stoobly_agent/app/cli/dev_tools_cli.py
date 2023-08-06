import click
import pdb

from stoobly_agent.lib.orm.migrate_service import migrate as database_migrate
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.orm.trace_request import TraceRequest

@click.group(
  epilog="Run 'stoobly-agent dev-tools COMMAND --help' for more information on a command.",
  help="Access developer tools"
)
@click.pass_context
def dev_tools(ctx):
    pass

@dev_tools.command()
def debug(**kwargs):
  pdb.set_trace()

@dev_tools.command()
def migrate():
  database_migrate()