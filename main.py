import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess


class FileChooserWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="FileChooser Example")
        self.file_list = []

        box = Gtk.Box(spacing=6)
        self.add(box)

        button1 = Gtk.Button("Adicionar Arquivo")
        button1.connect("clicked", self.on_file_clicked)
        box.add(button1)

        button2 = Gtk.Button("Adicionar Pasta")
        button2.connect("clicked", self.on_folder_clicked)
        box.add(button2)

        self.entry_name = Gtk.Entry()
        self.entry_name.set_text("basic")
        box.add(self.entry_name)

        button3 = Gtk.Button("Comprimir")
        button3.connect("clicked", self.compress)
        box.add(button3)

    def compress(self, widget):
        if len(self.file_list) > 0:
            call = ["7za", "a", self.entry_name.get_text() + ".7z"]
            for i in self.file_list:
                call.append(str(i))
            subprocess.check_call(call)
            print("Done")
        else:
            print("Selecione um arquivo.")

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_select_multiple(True)

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            self.file_list += dialog.get_filenames()
            print("Files selected: ", dialog.get_filenames())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        dialog.set_select_multiple(True)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            self.file_list += dialog.get_filenames()
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

win = FileChooserWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
