import dataclasses
from typing import Optional

import click
from tabulate import tabulate

from .types import TaskResult

from ..controllers.tasks import TaskCRUD, TaskStatus
from .core import cli, with_repo, AppJsonRepo

__all__ = "tasks"


@dataclasses.dataclass
class TaskContext:
    show: int
    crud: TaskCRUD


@cli.group("task")
@click.option(
    "--show",
    "-s",
    type=click.INT,
    default=0,
    help="Show only priority result that >= the number",
)
@with_repo
@click.pass_context
def task_cli(ctx: click.Context, conn: AppJsonRepo, show: int):
    """Manage tasks entries"""
    ctx.obj = TaskContext(show=show, crud=TaskCRUD(conn.db.TASKS))


@task_cli.command("add")
@click.option(
    "--status",
    type=click.Choice(TaskStatus),
    default=TaskStatus.TODO,
    help="The status of the task",
)
@click.argument("description", type=click.STRING)
@click.pass_obj
def add(ctx: TaskContext, description: str, status: TaskStatus):
    """Add a task to the task tracker"""
    return TaskResult(msg="Task is created!", value=ctx.crud.add(description, status))


@task_cli.command("update")
@click.argument("task_id", type=click.INT)
@click.argument("description", type=click.STRING)
@click.pass_obj
def update(ctx: TaskContext, task_id: int, description: str):
    """Update a task in the task tracker"""
    return TaskResult(
        msg="Task is updated!", value=ctx.crud.update(task_id, desc=description)
    )


@task_cli.command("mark")
@click.argument("task_id", type=click.INT)
@click.argument("status", type=click.Choice(TaskStatus))
@click.pass_obj
def update_status(ctx: TaskContext, task_id: int, status: TaskStatus):
    """Update task status to <status> in the task tracker"""
    return TaskResult(
        msg="Task is updated!", value=ctx.crud.update(task_id, status=status)
    )


@task_cli.command("mark-in-progress")
@click.argument("task_id", type=click.INT)
@click.pass_obj
def mark_in_progress(ctx: TaskContext, task_id: int):
    """Update task status to IN_PROGRESS in the task tracker"""
    return TaskResult(
        msg="Task is updated!",
        value=ctx.crud.update(task_id, status=TaskStatus.IN_PROGRESS),
    )


@task_cli.command("mark-done")
@click.argument("task_id", type=click.INT)
@click.pass_obj
def mark_done(ctx: TaskContext, task_id: int):
    """Update task status to DONE in the task tracker"""
    return TaskResult(
        msg="Task is updated!", value=ctx.crud.update(task_id, status=TaskStatus.DONE)
    )


@task_cli.command("delete")
@click.argument("task_id", type=click.INT)
@click.pass_obj
def delete(ctx: TaskContext, task_id: int):
    """Delete a task in the task tracker"""
    return TaskResult(msg="Task is deleted!", value=ctx.crud.delete(task_id))


@task_cli.command("list")
@click.argument("status", type=click.Choice(TaskStatus), default=None, required=False)
@click.pass_obj
def get_list(ctx: TaskContext, status: Optional[TaskStatus]):
    """List tasks in the task tracker"""

    return TaskResult(
        priority=100, value=ctx.crud.get_list([status] if status else None)
    )


@task_cli.result_callback()
@click.pass_obj
def print_result(ctx: TaskContext, result: TaskResult, **_):
    if result.msg:
        click.echo(result.msg)
        click.echo()

    if not result.value:
        return

    if ctx.show > result.priority:
        return

    if not isinstance(result.value, list):
        items = (result.value.model_dump(mode="json"),)
    else:
        items = map(lambda x: x.model_dump(mode="json"), result.value)

    table = tabulate(items, headers="keys", tablefmt="orgtbl")
    click.echo(table)
