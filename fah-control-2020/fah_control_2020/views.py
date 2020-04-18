from typing import List

import PySimpleGUI as sg  # noqa


class FAHAbstract(object):
    def __init__(self):
        self._gui = None

    @property
    def gui(self):
        return self._gui


class FAHClientDetail(FAHAbstract):
    def __init__(self):
        super().__init__()
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
        )
        selected_work_unit_max_size = 1000
        selected_work_unit_column = [
            [sg.Text('PRCG'), sg.Text('content')],
            [sg.Text('Folding Slot ID'), sg.Text('content')],
            [sg.Text('Work Queue ID'), sg.Text('content')],
            [sg.Text('Status'), sg.Text('content')],
            [
                sg.Text('Progress'),
                sg.ProgressBar(1000, orientation='h', size=(selected_work_unit_max_size, 20), key='progbar')
            ],
            [sg.Text('ETA'), sg.Text('content')],
            [sg.Text('Base Credit'), sg.Text('content')],
            [sg.Text('Estimated Credit'), sg.Text('content')],
            [sg.Text('Estimated PPD'), sg.Text('content')],
            [sg.Text('Estimated TPF'), sg.Text('content')],
            [sg.Text('Project'), sg.Text('content')],
            [sg.Text('FahCore'), sg.Text('content')],
            [sg.Text('Waiting On'), sg.Text('content')],
            [sg.Text('Attempts'), sg.Text('content')],
            [sg.Text('Next Attempt'), sg.Text('content')],
            [sg.Text('Assigned'), sg.Text('content')],
            [sg.Text('Timeout'), sg.Text('content')],
            [sg.Text('Expiration'), sg.Text('content')],
            [sg.Text('Work Server'), sg.Text('content')],
            [sg.Text('Collection Server'), sg.Text('content')],
            [sg.Sizer(h_pixels=selected_work_unit_max_size, v_pixels=1000)],
        ]
        client_detail_status_tab_content = [
            sg.Frame(title='', border_width=0, layout=[
                [
                    sg.Button(STR_FOLD, size=button_size),
                    sg.Button(STR_PAUSE, size=button_size),
                    sg.Button(STR_FINISH, size=button_size),
                    sg.Frame(title='Folding Power', layout=[
                        [
                            sg.Slider(range=(1, 3), orientation='h', size=(1000, 10), default_value=2, tick_interval=1)
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
                    sg.Frame(title='Points Per Day', layout=[
                        [sg.Text(text='1234')]
                    ]),
                ],
                [
                    sg.Frame(title='Folding Slots', layout=[
                        [client_detail_status_tab_content_foldings_slots],
                        [client_detail_status_tab_content_work_queue],
                        [sg.Sizer(v_pixels=1000)],
                    ]),
                    sg.Frame(title='Selected Work Unit', layout=selected_work_unit_column),
                ]
            ]),
        ]

        client_detail_system_tab_content = [sg.Text('System Info', size=(30, 20))]
        client_detail_log_tab_content = [sg.Text('Log', size=(30, 20))]

        self._gui = sg.Frame(
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


class FAHClientListing(FAHAbstract):
    def __init__(self, width: int, height: int):
        super().__init__()
        client_listing = sg.Table(
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
        )
        self._gui = sg.Frame(title='Clients', layout=[
            [client_listing], [sg.Sizer(v_pixels=1000)]
        ])


class FAHMenu(FAHAbstract):
    def __init__(self):
        super().__init__()
        self._gui = sg.Menu([
            ['&Configure'],
            ['&Preferences'],
            ['&Exit'],
            ['&About']
        ], tearoff=True)

    @property
    def gui(self):
        return self._gui


class FAHWindow(FAHAbstract):
    def __init__(self, width: int, height: int, title: str = 'FAH controller'):
        super().__init__()
        self.title = title

        self.menu = FAHMenu()
        self.client_listing = FAHClientListing(width=30, height=100)
        self.client_detail = FAHClientDetail()

        self._layout: List[List[sg.Element]] = [
            [self.menu.gui],
            [
                self.client_listing.gui,
                self.client_detail.gui
            ],
        ]
        self.width = width
        self.height = height

    def __enter__(self):
        self._gui = sg.Window(
            title=self.title,
            layout=self._layout,
            grab_anywhere=False,
            resizable=True,
            size=(self.width, self.height)
        )
        return self

    def run(self):
        event, values = self._gui.read()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._gui.close()
        self._gui = None
