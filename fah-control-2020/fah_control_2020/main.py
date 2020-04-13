import PySimpleGUI as sg  # noqa

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480


def get_window_size():
    return WINDOW_WIDTH, WINDOW_HEIGHT


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
                    ['Col 1', 'Col 2', 'Col 3'],
                    ['Col 1', 'Col 2', 'Col 3'],
                    ['Col 1', 'Col 2', 'Col 3'],
                ],
                size=(WINDOW_WIDTH / 3, WINDOW_HEIGHT)
            ),

        ],
    ])

    STR_FOLD = 'Fold'
    STR_PAUSE = 'Pause'
    STR_FINISH = 'Finish'
    longest_label_width = max([len(STR_FOLD), len(STR_PAUSE), len(STR_FINISH)])
    button_size = (longest_label_width, 4)

    client_detail_status_tab_content_foldings_slots = sg.Table(
        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
        headings=[
            'ID',
            'Status',
            'Description',
        ],
        values=[
            ['Col 1', 'Col 2', 'Col 3'],
            ['Col 1', 'Col 2', 'Col 3'],
            ['Col 1', 'Col 2', 'Col 3'],
        ],
        size=(WINDOW_WIDTH, 20),
    )
    client_detail_status_tab_content_work_queue = sg.Table(
        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
        headings=[
            'ID',
            'Status',
            'Progress',
            'ETA',
            'Credit',
            'PRCG',
        ],
        values=[
            ['Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5', 'Col 6'],
            ['Col 1', 'Col 2', 'Col 3', 'Col 4', 'Col 5', 'Col 6'],
        ],
        size=(WINDOW_WIDTH, 20),
    )
    client_detail_status_tab_content = [
        sg.Frame(title='', border_width=0, layout=[
            [
                sg.Button(STR_FOLD, size=button_size),
                sg.Button(STR_PAUSE, size=button_size),
                sg.Button(STR_FINISH, size=button_size),
                sg.Frame(title='Folding Power', layout=[
                    [
                        sg.Slider(range=(1, 3), orientation='h', size=(30, 10), default_value=2, tick_interval=1)
                    ]
                ]),
            ],
            [
                sg.Frame(title='Identity', layout=[
                    [
                        sg.Text('Name', size=(5, 1), pad=(1, 0)),
                        sg.Text('<user>', size=(6, 1)),
                        sg.Text('Team', size=(5, 1), pad=(1, 0)),
                        sg.Text('<team>', size=(6, 1)),
                    ],
                ]),
                sg.Frame(title='Points Per Day', element_justification='right', layout=[
                    [sg.Text(text='1234')]
                ]),
            ],
            [
                sg.Frame(title='Folding Slots', layout=[
                    [client_detail_status_tab_content_foldings_slots],
                    [client_detail_status_tab_content_work_queue],
                ]),
                sg.Frame(title='Selected Work Unit', layout=[
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('PRCG'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Folding Slot ID'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Work Queue ID'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Status'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Progress'), sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('ETA'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Base Credit'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Estimated Credit'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Estimated PPD'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Estimated TPF'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 5), layout=[[sg.Text('Project'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('FahCore'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Waiting On'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Attempts'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Next Attempt'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Assigned'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Timeout'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Expiration'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 5), layout=[[sg.Text('Work Server'), sg.Text('content')]])],
                    [sg.Frame(title='', border_width=0, pad=(0, 0), layout=[[sg.Text('Collection Server'), sg.Text('content')]])],
                ]),
            ]
        ]),
    ]

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
                    ]
                )
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

