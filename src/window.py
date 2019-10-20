from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
import os
import database
import image_tools
import PIL
class window (object):
    def __init__ (self):
        self.window = Tk()
        self.window.geometry ('600x450')
        self.db_dir_name = os.path.dirname (os.path.abspath (__file__))
        self.go_to_select_db_window ()
        self.window.mainloop ()

    def clear_window (self):
        for l in self.window.grid_slaves ():
            l.destroy ()
    def update_db_dir_path (self):
        self.db_dir_name = filedialog.askdirectory (initialdir = self.db_dir_name)
        if (not self.db_dir_name.endswith ('/')):
            self.db_dir_name += '/'
        self.db_dir_name_label.configure (text = self.db_dir_name)

        self.update_db_list ()

    def update_db_list (self):
        db_list = []
        for f in os.listdir (self.db_dir_name):
            if (f.endswith ('.db')):
                db_list.append (f)
        db_list.append ('select db file')

        self.database_combo['values'] = tuple (db_list)

    def add_images_dialog (self):
        images_dir_path = filedialog.askdirectory (initialdir = self.db_dir_name)
        self.db.set_images (image_tools.parse_image_dir (images_dir_path))

    def open_database (self, db_name):
        if db_name == '' or db_name == 'select db file':
            
            return False
        if not db_name.endswith ('.db'):
            db_name += '.db'
        self.db = database.image_database (self.db_dir_name + db_name)
        return True
    
    def add_prop (self, prop_name):
        self.db.add_column (prop_name)

    def update_image (self):
        image = PIL.Image.open (self.img_list[self.curr_image_id][1])
        self.image = PIL.ImageTk.PhotoImage (image)
        self.image_sprite = Label (self.window, image = self.image)

    def go_to_next_img (self)):
        if (curr_image_id < len (self.img_list) - 1):
            curr_image_id += 1
        self.update_image ()
        self.db.update_prop (
    def go_to_image_prop_window (self, prop_name):
        self.clear_window ()

        self.img_list = self.db.get_data_by_prop (prop_name)
        self.curr_image_id = 0
        
        self.update_imgae ()
        self.image_sprite.grid (row = 0, column = 1)
       
        self.image_prop_label = Label (self.sindow, text = 'Enter value of property')
        self.image_prop_label.grid (row = 1, column = 0)

        self.image_prop_val_entry = Entry (self.window, width = 14)
        self.image_prop_val_entry.grid (row = 2, column = 0)

        self.next_img_btn = Button (self.window, text = 'next image', command = lambda: self.go_to_next_img ())
        self.next_img_btn.grid (row = 3, column = 2)

        self.prev_img_btn = Button (self.window, text = 'previous image', command = lambda: self.go_to_prev_img ())
        self.prev_img_btn.grid (row = 3, column = 1)

        self.back_btn = Button (sefl.window, text = 'Back', command = lambda: self.go_to_change_prop_window ())
        self.back_btn.grid (row = 3, column = 0)

    def go_to_change_prop_window (self):
        self.clear_window ()
        
        self.prop_label = Label (self.window, text = 'Select property:')
        self.prop_label.grid (row = 0, column = 0)

        self.prop_combo = Combobox (self.window)
        self.prop_combo.grid (row = 1, column = 0)
        self.prop_combo['values'] = self.db.get_column_names ()
        self.prop_combo.current (0)

        self.next_btn = Button (self.window, text = 'Next')
        self.next_btn.grid (row = 2, column = 1)

        self.back_btn = Button (self.window, text = 'Back', command = lambda: self.go_to_db_conf_window ())
        self.back_btn.grid (row = 2, column = 0)


    def go_to_add_prop_window (self):
        self.clear_window ()

        self.prop_name_label = Label (self.window, text = 'Enter property name')
        self.prop_name_label.grid (row = 0, column = 0)

        self.prop_name_entry = Entry (self.window, width = 14)
        self.prop_name_entry.grid (row = 1, column = 0)

        self.ok_btn = Button (self.window, text = 'Ok', command = lambda: self.add_prop (self.prop_name_entry.get ()) if (self.prop_name_entry.get () != '') else messagebox.showinfo ('Error', 'Please enter correct prop name'))
        self.ok_btn.grid (row = 2, column = 1)
        
        self.back_btn = Button (self.window, text = 'Back', command = lambda: self.go_to_conf_window ())
        self.back_btn.grid (row = 2, column = 0)

    def go_to_create_db_window (self):
        self.clear_window ()

        self.db_name_label = Label (self.window, text = 'Enter database name')
        self.db_name_label.grid (row = 0, column = 0)

        self.db_name_entry = Entry (self.window, width = 14)
        self.db_name_entry.grid (row = 1, column = 0)

        self.next_btn = Button (self.window, text = 'next', command= lambda: self.go_to_conf_db_window () if (self.open_database (self.db_name_entry.get ())) else messagebox.showinfo ('Error', 'Please enter correct db name'))
        self.next_btn.grid (row = 2, column = 1)

        self.back_to_db_list_btn = Button (self.window, text = 'Back to db list', command= lambda: self.go_to_select_db_window ())
        self.back_to_db_list_btn.grid (row = 2, column = 0)

    def go_to_conf_db_window (self):
        self.clear_window ()

        self.save_btn = Button (self.window, text = 'Save database', command = lambda: self.db.save ())
        self.save_btn.grid (row = 0, column = 0)

        self.add_prop_btn = Button (self.window, text = 'Add property', command = lambda: self.go_to_add_prop_window ())
        self.add_prop_btn.grid (row = 1, column = 0)

        self.add_images_btn = Button (self.window, text = 'Add images', command = lambda: self.add_images_dialog ())
        self.add_images_btn.grid (row = 2, column = 0)

        self.change_prop_btn = Button (self. window, text = 'Change poperty', command = lambda: self.go_to_change_prop_window ())
        self.change_prop_btn.grid (row = 3, column = 0)

        self.generate_btn = Button (self.window, text = 'Generate outputs', command = lambda: messagebox.showinfo ('Error', 'not yet'))
        self.generate_btn.grid (row = 4, column = 0)

        self.back_to_db_list_btn = Button (self.window, text = 'back to db list', command = lambda: self.go_to_select_db_window ())
        self.back_to_db_list_btn.grid (row = 5, column = 0)

    def go_to_select_db_window (self):
        self.clear_window ()

        self.db_dir_name_label = Label (self.window, text = self.db_dir_name)
        self.db_dir_name_label.grid (row = 0, column = 0)

        self.db_dir_name_btn = Button (self.window, text = 'chose database dir', command = lambda: self.update_db_dir_path())
        self.db_dir_name_btn.grid (row = 0, column = 1)

        self.select_label = Label (self.window, text = 'Select database:')   
        self.select_label.grid (row = 1, column = 0)

        self.database_combo = Combobox (self.window)
        self.database_combo['values'] = ('select\ db\ file')
        self.database_combo.current (0)
        self.database_combo.grid (row = 2, column = 0)
        self.update_db_list ()

        self.new_btn = Button (self.window, text = 'new db', command= lambda: self.go_to_create_db_window())
        self.new_btn.grid(row = 3, column = 0)

        self.next_btn = Button (self.window, text = 'next', command= lambda: self.go_to_conf_db_window() if (self.open_database (self.database_combo.get ())) else messagebox.showinfo ('Error', 'Please enter correct db name'))
            
        self.next_btn.grid (row = 3, column = 1)

if __name__ == '__main__':
    w = window ()
