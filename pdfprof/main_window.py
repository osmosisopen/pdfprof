import io
import os
import pathlib

import FreeSimpleGUI as sg
from PIL import Image

from pdfprof.decrypter import Decrypter
from pdfprof.merge_window import MergeWindow

# from pdfprof.merge_window import MergeWindow
from pdfprof.pdf_processor import PdfProcessor

FILE_NAME_LABEL = "-SELECTED-FILENAME-LABEL-"
DECRYPT_FILENAME = "-DECRYPT-FILENAME-"
DECRYPT_PASSWORD = "-DECRYPT-PASSWORD-"
PREVIEW_BUTTON = "-PREVIEW-"
MAIN_FILE = "-MAIN-FILE-"


class MainWindow:
    def __init__(self):
        self.app_path = pathlib.Path(__file__).parent.resolve()
        self.images_path = os.path.join(self.app_path, "images")
        self.settings_file = os.path.join(self.app_path, "settings.json")
        sg.user_settings_filename(filename=self.settings_file)

        self.layout = self.create_layout()
        self.window = self.create_window()
        location = sg.user_settings_get_entry("-location-", (None, None))
        self.file_name_label = self.window[FILE_NAME_LABEL]
        self.decrypt_frame = self.window["-DECRYPT-FRAME-"]
        self.decrypt_password = self.window[DECRYPT_PASSWORD]
        self.decrypt_filename = self.window[DECRYPT_FILENAME]
        self.preview_button = self.window[PREVIEW_BUTTON]
        self.merge_button = self.window["-MERGE-"]
        self.window_event_handler()

    def prepare_preview(self):
        file_pages = {}
        try:
            page_count = self.doc.page_count
            # .get_displaylist()
            for pno in range(page_count):
                page = self.doc[pno]
                pix = page.get_pixmap()
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                with io.BytesIO() as bio:
                    img.save(bio, format="PNG")
                    del img
                    file_pages[pno] = bio.getvalue()

            return file_pages
        except Exception as e:
            self.message_and_raise(str(e))

        return file_pages

    def create_merge_window(self):
        MergeWindow()

    def create_window(self):
        return sg.Window(
            "PDF Prof",
            self.layout,
            size=(None, None),
            resizable=True,
            # enable_close_attempted_event=True,
            location=sg.user_settings_get_entry("-location-", (None, None)),
        )

    def create_preview_window(self, image_data):  # file_pages
        image_column = [
            [sg.Image(key="-IMAGE-", data=data), sg.Text(pno + 1)]
            for pno, data in image_data.items()
        ]

        preview_layout = [
            [
                sg.Column(image_column, scrollable=True, vertical_scroll_only=True),
            ]
        ]

        window = sg.Window(
            title="Preview",
            layout=[preview_layout],
            resizable=True,
        )
        while True:
            event, values = window.read()
            if event in ["Exit", sg.WIN_CLOSED]:
                break

        window.close()

    def message_and_raise(self, message, raise_exception=True):
        sg.popup(message)
        if raise_exception:
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
                            sg.Input(key=DECRYPT_PASSWORD, password_char="*"),
                        ],
                        [
                            sg.Text("Decrypted File Name: "),
                            sg.Input(key=DECRYPT_FILENAME),
                        ],
                        [sg.Button("Convert", key="-CONVERT-")],
                    ],
                    visible=False,
                ),
            ]
        ]

        return [
            [sg.Button("Merge PDF Files", key="-MERGE-")],
            [
                sg.Input(
                    key=MAIN_FILE, visible=True, enable_events=True, disabled=True
                ),
                sg.FileBrowse(button_text="Select File"),
            ],
            [
                sg.Text("", key=FILE_NAME_LABEL),
                sg.Button("Preview", key=PREVIEW_BUTTON, visible=False),
                # sg.Image(key="-ENCRYPTED-ICON-", filename=f"{self.images_path}\\lock-16.png", visible=False)
            ],
            [decrypt_frame_layout],
            # [sg.Button("Exit")],
        ]

    def window_event_handler(self):
        while True:
            event, values = self.window.read()
            # print(values)
            if event in [sg.WIN_CLOSED, "Exit"]:
                break

            # if event in ("Exit", sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            #     sg.user_settings_set_entry("-location-", self.window.current_location())
            #     break
            elif event == MAIN_FILE:
                self.handle_file_selection(values)
            elif event == PREVIEW_BUTTON:
                try:
                    image_data = self.prepare_preview()
                    self.create_preview_window(image_data)  # (file_pages)
                except Exception as e:
                    print(e)
            elif event == "-CONVERT-":
                self.handle_convert()
            elif event == "-MERGE-":
                self.create_merge_window()

        self.window.close()

    def handle_file_selection(self, values):
        if not self.handle_file_selection_event(values):
            return

        if not self.file_name_label:
            return

        self.file_name_label.update(value=self.selected_filename)

        # if enc_icon := self.window["-ENCRYPTED-ICON-"]:
        #     enc_icon.update(visible=self.doc.is_encrypted)

        if not self.decrypt_frame:
            return

        if self.doc.is_encrypted and self.decrypt_password:
            self.decrypt_password.SetFocus(True)

        self.decrypt_frame.update(visible=self.doc.is_encrypted)

        if not self.preview_button:
            return

        self.preview_button.update(visible=not self.doc.is_encrypted)

    def handle_convert(self):
        try:
            if not self.doc.is_encrypted:
                self.message_and_raise("Cannot convert unencrypted file")

            if not self.decrypt_filename or not self.decrypt_password:
                self.message_and_raise("Please provide valid filename/password")
                return

            Decrypter(self.selected_file).decrypt_protected_pdf(
                self.decrypt_password.get(), self.decrypt_filename.get()
            )

        except Exception as e:
            self.message_and_raise(e, raise_exception=False)

    def handle_file_selection_event(self, values):
        selected_file = values[MAIN_FILE]
        self.selected_file = selected_file
        self.selected_filename = os.path.basename(selected_file)
        self.doc = PdfProcessor(self.selected_file).get_doc()

        return bool(self.selected_filename)
