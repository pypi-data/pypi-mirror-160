from huawei_lte_api.Client import Client

from ..core.io import printx, prettify
from ..core.connection import HRC_Connection


# Special functions

def get_sms_list_deep(page_depth: int = 1) -> dict:
    """
    SMS deep scanning function

    :param page_depth: Depth of pages to be fetched and scanned, defaults to 1
    :return: Dictionary with all messages
    """
    messages_all = {
        'Count': 0,
        'Messages': {
            'Pages': [
                # page_0[[message_0, message_1]], page_1[[...]]...
            ]
        }
    }

    for selected_page in range(1, 2 if page_depth <= 1 else page_depth + 1):
        with HRC_Connection() as conn:
            messages_current_page = Client(conn).sms.get_sms_list(
                page=selected_page
            )

        if messages_current_page['Count'] == '0':
            break

        messages_all['Count'] = str(
            int(messages_all['Count']) + int(messages_current_page['Count'])
        )

        messages_all['Messages']['Pages'].append(
            messages_current_page['Messages']['Message']
        )

    return messages_all


# CLI calls implementation

def sms_send_impl(number: str, text: str):
    if len(number) == 0:
        number = input('Number: ')
    if len(text) == 0:
        text = input('Text: ')

    try:
        with HRC_Connection() as router_con:
            send_status = Client(router_con).sms.send_sms(
                [number],
                text
            )

        if send_status.lower() == 'ok':
            printx('SMS sent successfully to {}'.format(number),
                   limit_line_length=True)
        else:
            printx('SMS was not sent, reason: "{}"'.format(send_status),
                   limit_line_length=True)
    except Exception as e:
        printx('Execution failed, reason: "{}"'.format(e),
               limit_line_length=True)


def sms_count_all_impl():
    try:
        with HRC_Connection() as conn:
            sms_count_dict = Client(conn).sms.sms_count()
    except Exception as e:
        cli_output = prettify('Can not get sms information, reason: "{}"'.format(e))
    else:
        cli_output = ''
        for key, value in sms_count_dict.items():
            cli_output += '• {}: {}\n'.format(key, value)
        cli_output = cli_output[:-1]

    printx(cli_output)


def sms_list_impl(page_depth: int, content_trim: int):
    printx('Fetching Messages...'
           '\n• Settings: '
           '\n  • Page Depth: {}'
           '\n  • Content Preview Length: {}\n'
           .format(page_depth, content_trim)
           )
    try:
        cli_output_arr = []
        cli_output = ''

        response = get_sms_list_deep(page_depth)
        response_pages = response['Messages']['Pages']

        for message_page in range(len(response_pages)):
            cli_output_arr.append('• Page: {}; Count: {}\n'
                                  .format(message_page + 1,
                                          len(response_pages[message_page]))
                                  )

            for msg in response_pages[message_page]:
                cli_output_arr[message_page] += '  • Index: {}\n    From: {}\n    When: {}\n    Content: {}\n'.format(
                    msg['Index'], msg['Phone'], msg['Date'], msg['Content'][:content_trim] + '...'
                )

    except Exception as e:
        cli_output = prettify('Can not fetch messages list, reason: "{}"'.format(e))

    else:
        for page in cli_output_arr:
            cli_output += page
        cli_output = cli_output[:-1]  # Cut the ending "\n"

    printx(cli_output)


def sms_view_impl(message_index: int, page_depth: int, msg_dont_mark_read: bool):
    response = {}

    try:
        response = get_sms_list_deep(page_depth)
    except Exception as e:
        cli_output = 'Can not fetch messages list, reason: "{}"'.format(e)
    else:
        message_matched = {}
        for page in response['Messages']['Pages']:
            for message in page:
                if str(message_index) == message['Index']:
                    message_matched = message
                    break

        if len(message_matched) > 0:
            if not msg_dont_mark_read:
                try:
                    with HRC_Connection() as conn:
                        Client(conn).sms.set_read(message_matched['Index'])
                except Exception:
                    # ! This event SHOULD be logged when logging
                    # ! system will be done
                    pass

            cli_output = '• Index: {}\n• From: {}\n• When: {}\n• Content: {}' \
                         .format(message_matched['Index'], message_matched['Phone'],
                                 message_matched['Date'], message_matched['Content'])
        else:
            cli_output = prettify('• Message with id "{}" was not found'.format(message_index))

    printx(cli_output)
