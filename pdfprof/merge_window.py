import os

import FreeSimpleGUI as sg

FILE_NAME_LABEL = "-SELECTED-FILENAME-LABEL-"
DECRYPT_FILENAME = "-DECRYPT-FILENAME-"
DECRYPT_PASSWORD = "-DECRYPT-PASSWORD-"
PREVIEW_BUTTON = "-PREVIEW-"
FILE_1 = "-FILE-1-"
FILE_2 = "-FILE-2-"

class MergeWindow:
    def __init__(self):
        self.layout = self.create_window_layout()
        self.window = self.create_window()
        self.handle_events()

    def create_window_layout(self):
        return [
            [
                [
                    sg.Text("File 1: "),
                    sg.Input(
                        key=FILE_1, visible=True, enable_events=True, disabled=True
                    ),
                    sg.FileBrowse(button_text="Select File"),
                ],
                [
                    sg.Text("", k="-FILE-1-NAME-"),
                ],
                [
                    sg.Text("File 2: "),
                    sg.Input(
                        key=FILE_2, visible=True, enable_events=True, disabled=True
                    ),
                    sg.FileBrowse(button_text="Select File"),
                ],
                [
                    sg.Text("", k="-FILE-2-NAME-"),
                ],
            ],
            [sg.Button("Merge", key="-MERGE-")],
        ]

    def create_window(self):
        return sg.Window("Merge", [self.layout], modal=True)

    def handle_events(self):
        while True:
            event, values = self.window.read()
            if event in ["Exit", sg.WIN_CLOSED]:
                break

            elif event in [FILE_1, FILE_2]:
                self.handle_file_selection_event(event, values)

        self.window.close()

    def handle_file_selection_event(self, event, values):
        self.window[f"{event}NAME-"].update(value=os.path.basename(values[event]))
