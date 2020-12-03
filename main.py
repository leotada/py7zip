import multiprocessing

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from zipcontroller import ZipController


class Py7zip(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Py7zip")
        self.set_default_size(800, 400)
        self.file_list = []

        box0 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box1 = Gtk.Box(spacing=10)
        box0.add(box1)
        self.add(box0)

        button_add_file = Gtk.Button("Adicionar Arquivo")
        button_add_file.connect("clicked", self.on_file_clicked)
        box1.add(button_add_file)

        button_add_folder = Gtk.Button("Adicionar Pasta")
        button_add_folder.connect("clicked", self.on_folder_clicked)
        box1.add(button_add_folder)

        self.entry_name = Gtk.Entry()
        self.entry_name.set_placeholder_text("Nome do arquivo de saída")
        self.entry_name.set_width_chars(50)
        box1.add(self.entry_name)

        button_output = Gtk.Button("Pasta de saída")
        button_output.connect("clicked", self.on_output_folder_clicked)
        box1.add(button_output)

        label_threads = Gtk.Label("Threads")
        box1.add(label_threads)

        self.button_threads = Gtk.SpinButton()
        self.button_threads.set_numeric(True)
        self.button_threads.set_range(1, 32)
        self.button_threads.set_increments(1, 1)
        self.button_threads.set_value(multiprocessing.cpu_count())
        box1.add(self.button_threads)

        self.store = Gtk.ListStore(str)
        tree = Gtk.TreeView(self.store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Arquivos", renderer, text=0)
        tree.append_column(column)
        box0.pack_start(tree, True, True, 0)

        box_bottom_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box0.add(box_bottom_buttons)

        button_compress = Gtk.Button("Comprimir")
        button_compress.connect("clicked", self.compress)
        box_bottom_buttons.add(button_compress)

        button_clear = Gtk.Button("Limpar")
        button_clear.connect("clicked", self.clean)
        box_bottom_buttons.add(button_clear)

    def clean(self, widget):
        self.file_list.clear()
        self.store.clear()

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Selecione um arquivo", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_select_multiple(True)

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_list += dialog.get_filenames()
            for i in dialog.get_filenames():
                self.store.append([i])

        dialog.destroy()

    def add_filters(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Selecione uma pasta", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        dialog.set_select_multiple(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_list += dialog.get_filenames()
            for filename in dialog.get_filenames():
                self.store.append([filename])

        dialog.destroy()

    def on_output_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Selecione uma pasta de saída", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        dialog.set_select_multiple(False)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            output_filename = dialog.get_filename()
            if not output_filename.endswith('.7z'):
                output_filename = output_filename + '.7z'
            self.entry_name.set_text(output_filename)
        dialog.destroy()

    def compress(self, widget):
        output = self.entry_name.get_text()
        if len(self.file_list) > 0 and output != '':
            multithread = self.button_threads.get_value_as_int()
            ZipController().compress(self.file_list, output, multithread)

if __name__ == '__main__':
    app_window = Py7zip()
    app_window.connect("delete-event", Gtk.main_quit)
    app_window.show_all()
    Gtk.main()
