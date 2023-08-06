import traceback
from pathlib import Path
from fridaay import *
from .doc import PipeBookDoc
import importlib.resources

import toga
from toga.constants import COLUMN
from toga.style import Pack
APP_NAME = 'PipeBook'
APP_ID = 'com.igwet.app.pipebook'
APP_ICON = '/Users/ernest/Developer/pipebook/pipebook/resources/pipebook2.png'
DEMO_PIPE="demo_pets"

class PipeBookApp(toga.App):

    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def open_document(self, fname):
        name = str(fname)
        self.label.text = f"File to open: {name}"
        path, ext = name.split(".")
        yml = load_yaml(path)
        doc = PipeBookDoc(self, name, yml)
        return doc

    def load_demo(self, name=DEMO_PIPE):
        pipe_path = path_resource(PKG_ID, PIPE_FOLDER)
        yml = load_yaml(name, pipe_path)
        doc = PipeBookDoc(self, name, yml)
        return doc

    async def action_info_dialog(self, widget):
        await self.main_window.info_dialog(APP_NAME, f'Welcome to {APP_NAME}')
        self.label.text = 'The next-generation data notebook for resilient, production-ready data pipelines.'

    async def action_open_file_filtered_dialog(self, widget):
        try:
            fname = await self.main_window.open_file_dialog(
                title=f"Open {APP_NAME} YAML file",
                multiselect=False,
                file_types=['yml'],
            )
            if fname is not None:
                self.open_document(fname)
            else:
                self.label.text = "No file selected!"
        except ValueError:
            self.label.text = "Open file dialog was canceled"

    async def exit_handler(self, app):
        # Return True if app should close, and False if it should remain open
        if await self.main_window.confirm_dialog(APP_NAME, 'Are you sure you want to quit?'):
            print(f"Label text was '{self.label.text}' when you quit the app")
            return True
        else:
            self.label.text = 'Exit canceled'
            return False

    def set_window_label_text(self, num_windows):
        self.window_label.text = f"{num_windows} secondary window(s) open"

    def startup(self):
        # Set up main window
        self.registry = Registry()
        self.main_window = toga.MainWindow(title=self.name)
        self.on_exit = self.exit_handler

        # Label to show responses.
        self.label = toga.Label('Ready.', style=Pack(padding_top=20))
        self.window_label = toga.Label('', style=Pack(padding_top=20))
        self.window_counter = 0
        self.close_attempts = set()
        self.set_window_label_text(0)

        btn_style = Pack(flex=1)
        btn_info = toga.Button('Info', on_press=self.action_info_dialog, style=btn_style)
        btn_open_filtered = toga.Button(
            'Open PipeBook YAML',
            on_press=self.action_open_file_filtered_dialog,
            style=btn_style
        )
        btn_clear = toga.Button('Clear', on_press=self.do_clear, style=btn_style)

        # Outermost box
        box = toga.Box(
            children=[
                btn_info,
                btn_open_filtered,
                btn_clear,
                self.label,
                self.window_label
            ],
            style=Pack(
                flex=1,
                direction=COLUMN,
                padding=10
            )
        )

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()
        self.load_demo()

def main():
    return PipeBookApp(APP_NAME, APP_ID, icon=APP_ICON)

if __name__ == '__main__':
    app = main()
    app.main_loop()
