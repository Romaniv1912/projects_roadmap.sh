import click
from click_default_group import DefaultGroup

from ..services.repo import AppJsonRepo


with_repo = click.make_pass_decorator(AppJsonRepo)


@click.group(cls=DefaultGroup, default="task", default_if_no_args=True)
@click.option("--db", type=click.STRING, default="db.json", help="Database file path")
@click.pass_context
def cli(ctx: click.Context, db: str):
    conn = AppJsonRepo(db)
    ctx.with_resource(conn)

    ctx.obj = conn
