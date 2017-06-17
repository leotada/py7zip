import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
import threading


class Py7zip(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Py7zip")
        self.set_default_size(800, 400)
        self.file_list = []

        box0 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box1 = Gtk.Box(spacing=10)
        box0.add(box1)
        self.add(box0)

        button1 = Gtk.Button("Adicionar Arquivo")
        button1.connect("clicked", self.on_file_clicked)
        box1.add(button1)

        button2 = Gtk.Button("Adicionar Pasta")
        button2.connect("clicked", self.on_folder_clicked)
        box1.add(button2)

        self.entry_name = Gtk.Entry()
        # self.entry_name.set_text("basic")
        self.entry_name.set_placeholder_text("Nome do arquivo de saída")
        self.entry_name.set_width_chars(50)
        box1.add(self.entry_name)

        button3 = Gtk.Button("Comprimir")
        button3.connect("clicked", self.compress)
        box1.add(button3)

        self.checkbox_multi = Gtk.CheckButton("Multithread")
        self.checkbox_multi.set_active(True)
        box1.add(self.checkbox_multi)

        self.store = Gtk.ListStore(str)
        tree = Gtk.TreeView(self.store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Arquivos", renderer, text=0)
        tree.append_column(column)
        box0.pack_start(tree, True, True, 0)

        button4 = Gtk.Button("Limpar")
        button4.connect("clicked", self.clean)
        box0.add(button4)

    def do_subprocess(self, call):
        subprocess.check_call(call)
        self.entry_name.set_text("Pronto!")

    def start_thread(self, call):
        t = threading.Thread(target=self.do_subprocess, kwargs={'call': call})
        t.start()

    def compress(self, widget):
        if len(self.file_list) > 0:
            outname = self.entry_name.get_text() if self.entry_name.get_text() != '' else 'defaultname'
            multi = self.checkbox_multi.get_active()
            call = ["7za", "a", "-r", "-t7z", "-m0=LZMA2",
                    "-mmt=on" if multi else "-mmt=off",
                    outname + ".7z"]
            for i in self.file_list:
                call.append(str(i))
            # call
            self.start_thread(call)
            print("Done")
        else:
            print("Selecione um arquivo.")

    def clean(self, widget):
        self.file_list.clear()
        self.store.clear()

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
            for i in dialog.get_filenames():
                self.store.append([i])
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
            for i in dialog.get_filenames():
                self.store.append([i])
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

win = Py7zip()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
