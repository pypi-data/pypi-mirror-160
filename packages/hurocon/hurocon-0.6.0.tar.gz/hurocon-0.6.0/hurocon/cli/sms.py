import click
from click_didyoumean import DYMGroup

from .cli_base import cli
from ..implementation import isms


@cli.group(cls=DYMGroup)
def sms():
    """ SMS commands """
    pass


@sms.command('send')
@click.option('-n', '--number', default='', help='Number that message will be sent to.')
@click.option('-t', '--text', default='', help='Text of the message to be sent.')
def sms_send(number: str, text: str):
    """ Send plain-text sms to specified number """
    isms.sms_send_impl(number, text)


@sms.command('count')
def sms_count_all():
    """ Get overall information about stored sms messages """
    isms.sms_count_all_impl()


@sms.command('list')
@click.option(
    '--page-depth', '-D', 'page_depth',
    default=1, show_default=True, type=int,
    help='Depth of pages to be fetched if available.'
)
@click.option(
    '--content-trim', '-C', 'content_trim',
    default=40, show_default=True, type=int,
    help='Trim the message content to specified number of characters.'
)
def sms_list(page_depth: int, content_trim: int):
    """ List all sms messages content and other meta-data """
    isms.sms_list_impl(page_depth, content_trim)


@sms.command('view')
@click.argument('message_index', type=int)
@click.option(
    '--page-depth', '-D', 'page_depth',
    default=1, show_default=True, type=int,
    help='Depth of pages to be fetched if available.'
)
@click.option(
    '--dont-mark-read', '-M', 'msg_dont_mark_read',
    is_flag=True, help='Do not mark viewed message as read.'
)
def sms_view(message_index: int, page_depth: int, msg_dont_mark_read: bool):
    """
    Show message by index

    Message indexes can be fetched using the "sms list" command
    """
    isms.sms_view_impl(message_index, page_depth, msg_dont_mark_read)
