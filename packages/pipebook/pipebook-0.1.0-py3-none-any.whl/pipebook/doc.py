from fridaay import Pipe
from .io import obj2tree
from .view import FrameView

import toga
from toga.sources import TreeSource
from toga.sources.tree_source import Node
from toga.constants import COLUMN, ROW
from toga.style import Pack

class PipeBookDoc():

    def __init__(self, app, name, yml):
        self.app = app
        self.name = name
        self.yaml = yml
        self.source = obj2tree(yml)
        self.pipe = Pipe(app.registry, yml)
        self.frames = []
        self.startup()

    # Pipe Run functions

    async def do_run(self, widget):
        self.pipe.run()
        self.frames = [FrameView(self.app, n, d) for n,d in self.pipe.data.items()]

    # Table callback functions
    def on_select_handler(self, widget, node):
        if node is not None and node.name:
            self.label.text = f'You selected node: {node.name}'
            self.btn_remove.enabled = True
        else:
            self.label.text = 'No node selected'
            self.btn_remove.enabled = False

    # Button callback functions
    def insert_handler(self, widget, **kwargs):
        self.tree.data

    def remove_handler(self, widget, **kwargs):
        selection = self.tree.selection
        if selection.title:
            self.tree.data.remove(selection)

    def startup(self):
        # Set up doc window

        self.app.window_counter += 1
        self.window = toga.Window(title=self.name)
        # Both self.windows.add() and self.windows += work:
        self.app.windows += self.window

        # Label to show responses.
        self.label = toga.Label('Ready.', style=Pack(padding=10))

        self.tree = toga.Tree(
            headings=self.source._accessors,
            style=Pack(flex=1)
        )
        self.tree.data = self.source

        # Buttons
        btn_style = Pack(flex=1, padding=10)

        self.btn_insert = toga.Button('Insert Row', on_press=self.insert_handler, style=btn_style)
        self.btn_remove = toga.Button('Remove Row', enabled=False, on_press=self.remove_handler, style=btn_style)
        self.btn_box = toga.Box(children=[self.btn_insert, self.btn_remove], style=Pack(direction=ROW))
        self.btn_run = toga.Button('Run and Show Frames', on_press=self.do_run, style=btn_style)

        # Outermost box
        outer_box = toga.Box(
            children=[self.btn_run, self.btn_box, self.tree, self.label],
            style=Pack(
                flex=1,
                direction=COLUMN,
            )
        )

        # Add the content on the main window
        self.window.content = outer_box

        # Show the main window
        self.window.show()
