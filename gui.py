import os
import pathlib

import PySimpleGUI as sg

from .converter import Converter


class Window:
    def __init__(self):
        self.app_path = pathlib.Path(__file__).parent.resolve()
        self.images_path = os.path.join(self.app_path, "images")
        self.settings_file = os.path.join(self.app_path, "settings.json")
        sg.user_settings_filename(filename=self.settings_file)
        print(sg.user_settings_filename())

        self.layout = self.create_layout()
        self.window = sg.Window("PDF Converter", self.layout)
        self.window_event_handler()

    def message_and_raise(self, message):
        sg.popup(message)
        raise ValueError(message)

    def create_layout(self):
        decrypt_frame_layout = [
            [
                sg.Frame(
                    title="Decryption",
                    key="-DECRYPT-FRAME-",
                    layout=[
                        [
                            sg.Text("Password: "),
                            sg.Input(key="-DECRYPT-PASSWORD-", password_char="*"),
                        ],
                        [
                            sg.Text("Decrypted File Name: "),
                            sg.Input(key="-DECRYPT-FILENAME-"),
                        ],
                        [sg.Button("Convert", key="-CONVERT-")],
                    ],
                    visible=False,
                ),
            ]
        ]

        return [
            [
                sg.Input(key="-FILE-", visible=False, enable_events=True, disabled=True),
                sg.FileBrowse(
                    button_text="Select File",
                ),
            ],
            [sg.Image(key="-ENCRYPTED-ICON-", filename=f"{self.images_path}\\lock-16.png", visible=False)],
            [
                sg.Text("", key="-SELECTED-FILENAME-LABEL-"),
            ],
            [decrypt_frame_layout],
            [sg.Button("Exit")],
        ]

    # sg.Combo(sg.user_settings_get_entry('-filenames-', []),
    #                 default_value=sg.user_settings_get_entry('-last filename-', ''),
    #                 size=(50, 1), key='-FILENAME-'),

    def window_event_handler(self):
        while True:
            event, values = self.window.read()
            # print(values)
            if event in [sg.WIN_CLOSED, "Exit"]:
                break
            elif event == "-FILE-":
                if not self.handle_file_selection_event(values):
                    # Handle file selection failure
                    continue

                if file_name_label := self.window["-SELECTED-FILENAME-LABEL-"]:
                    file_name_label.update(value=self.selected_filename)
                    self.set_converter(self.selected_filename)
                    self.encrypted = self.converter.is_encrypted()

                    if enc_icon := self.window["-ENCRYPTED-ICON-"]:
                        enc_icon.update(visible=self.encrypted)

                    if frame := self.window["-DECRYPT-FRAME-"]:
                        frame.update(visible=self.encrypted)

            elif event == "-CONVERT-":
                try:

                    if self.encrypted:
                        password = self.window["-DECRYPT-PASSWORD-"]
                        # password = sg.popup_get_text("Password", password_char="*")
                        self.converter.convert_protected_pdf(self.selected_filename, password)
                        print(password)
                except Exception as e:
                    print(e)
                    continue

    def handle_file_selection_event(self, values):
        selected_filename = values["-FILE-"]
        self.set_selected_filename(selected_filename)

        if not self.selected_filename:
            return False

        # if convert_button := self.window["-CONVERT-"]:
        #     convert_button.update(disabled=False)

        return True

    def set_selected_filename(self, filename):
        self.selected_filename = filename

    def set_converter(self, filename):
        self.converter = Converter(self.selected_filename)

    # sg.user_settings_get_entry('-fn', [])
    # if event == 'Go':
    #     sg.user_settings_set_entry('-filenames-',
    #                                list(set(sg.user_settings_get_entry('-filenames-', []) + [values['-FILENAME-'], ])))
    #     if values:
    #         sel_pdf_file = values['-FILENAME-']
    #         password = values['-PW-']
    #         print(sel_pdf_file)

    #         try:
    #             convert_protected_pdf(sel_pdf_file, password)
    #         except Exception as e:
    #             print(e)
    #             continue

    #     sg.user_settings_set_entry('-last filename-', values['-FILENAME-'])
    #     window['-FILENAME-'].update(values=list(set(sg.user_settings_get_entry('-filenames-', []))))

    # elif event == 'Clear':
    #     sg.user_settings_set_entry('-filenames-', [])
    #     sg.user_settings_set_entry('-last filename-', '')
    #     window['-FILENAME-'].update(values=[], value='')
