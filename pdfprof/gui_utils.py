import FreeSimpleGUI as sg


class GuiUitils:

    @staticmethod
    def get_sg():
        return sg

    def popup(self, message):
        sg.popup(message)