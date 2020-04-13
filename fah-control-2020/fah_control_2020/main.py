import PySimpleGUI as sg

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


def get_window_size():
    return (WINDOW_WIDTH, WINDOW_HEIGHT)


def run():
    sg.ChangeLookAndFeel('Material2')
    menu = sg.Menu([
        ['&Configure'],
        ['&Preferences'],
        ['&Exit'],
        ['&About']
    ], tearoff=True)
    client_listing = sg.Frame(title='Clients', layout=[
        [
            sg.Table(
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                headings=[
                    'Name',
                    'Status',
                    'Address',
                ],
                values=[
                    ['Listbox 1', 'Listbox 1', 'Listbox 1'],
                    ['Listbox 2', 'Listbox 2', 'Listbox 2'],
                    ['Listbox 2', 'Listbox 2', 'Listbox 2']
                ],
                size=(WINDOW_WIDTH / 3, WINDOW_HEIGHT)
            ),

        ],
    ])

    client_detail_status_tab_content = [sg.Text('Status', size=get_window_size())]
    client_detail_system_tab_content = [sg.Text('System Info', size=get_window_size())]
    client_detail_log_tab_content = [sg.Text('Log',  size=get_window_size())]

    client_detail = sg.Frame(
        title='Client',
        layout=[
            [sg.Text('Client: Client1')],
            [
                sg.TabGroup(
                    layout=[
                        [sg.Tab(title='Status', layout=[
                            client_detail_status_tab_content,
                        ])],
                        [sg.Tab(title='System info', layout=[
                            client_detail_system_tab_content
                        ])],
                        [sg.Tab(title='Log', layout=[
                            client_detail_log_tab_content
                        ])],
                    ])
            ],
        ],
    )

    layout = [
        [menu],
        [
            client_listing,
            client_detail
        ],
    ]
    window = sg.Window(
        title='FAH controller',
        layout=layout,
        grab_anywhere=False,
        resizable=True,
        size=(WINDOW_WIDTH, WINDOW_HEIGHT)
    )
    event, values = window.read()
    window.close()


if __name__ == '__main__':
    run()
