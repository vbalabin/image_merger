import sys
import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import askopenfilenames, askdirectory
from PIL import Image

# every project's class has its own module
from src.bscale import BinaryScale
from src.blabel import BinaryLabel
from src.mentry import MergerEntry

# resizing and concatenating scripts are stored as static methods
from src.mscripts import MergerScripts


class ImageMerger():
    bg_color = '#ffffff'
    folder = MergerScripts.find_folderpath(sys.argv[0])
    folder = MergerScripts.form_filepathstr(folder)
    
    def __init__(self, master):
        self.master = master
        self.configure_main_window()
        self.mainframe = self.add_mainframe(master)
        self.grid = self.add_grid(self.mainframe, 14, 6)
        self.lb01 = self.add_label(0, 1, self.mainframe, 'Concatenate Vertically')
        self.bs_concat = self.add_biscale(0, 0, self.mainframe, self.lb01, 'Concatenate Vertically', 
                                                                'Concatenate Horizontally')
        self.lb02 = self.add_label(1, 1, self.mainframe, 'Resize to Max')
        self.bs_resize = self.add_biscale(1, 0, self.mainframe, self.lb02, 'Resize to Max', 'Do not Resize')
        self.lb03 = self.add_label(2, 1, self.mainframe, 'Background Color')
        self.lb04 = self.add_label(4, 0, self.mainframe, 'Files:')
        self.lb04.configure(font=('Consolas', '12', 'bold'), padx=3)
        self.colorbtn = self.add_color_btn(self.grid[2][0])
        self.lstbox = self.add_listbox(5, 0, self.mainframe)
        self.inputbtn = self.add_inputbtn(self.grid[4][4])
        self.excludebtn = self.add_excludebtn(self.grid[4][5])
        self.lb05 = self.add_label(10, 0, self.mainframe, 'Output Path:')
        self.lb05.configure(font=('Consolas', '12', 'bold'), padx=3)
        self.direntry = self.add_outputdir_entry(11, 0, self.mainframe, self.folder)
        self.outputdir_btn = self.add_outputdir_btn(self.grid[11][5])
        self.outputdir_btn = self.add_process_btn(13, 2, self.mainframe)

    def configure_main_window(self):
        """
        main window properties
        """
        self.master.title('ImageFiles Merger')
        _icon_path = r"img/puzzle.ico"
        self.master.iconbitmap(_icon_path)
        self.master.geometry('320x440')
        self.master.configure(bg='LightSteelBlue')
        self.master.resizable(False, False)

    def add_mainframe(self, master):
        """
        all elements are placed on a single Frame
        """
        _frame = tk.LabelFrame(master, width=300, height=420)
        _frame.propagate(False)
        _frame.pack(side=tk.BOTTOM, pady=8)
        return _frame

    def add_grid(self, master, sizex=8, sizey=8):
        """
        creates a table structure on a given frame
        """
        result = list()
        for i in range(sizex):
            result.append(list())
            tk.Grid.rowconfigure(master, i, weight=0)
            for j in range(sizey):
                frame = tk.Frame(master, width=50, height=30, bg='LightSteelBlue')
                frame.grid(row=i, column=j, sticky=tk.NSEW)
                tk.Grid.columnconfigure(master, j, weight=0)
                result[i].append(frame)
        return result

    def _call_clrchooser(self):
        """
        uses tkinter.dialogs colorchooser \\
        sets self.bg_color
        """
        _clr = colorchooser.askcolor()
        self.colorbtn.configure(background=_clr[1])
        self.bg_color = _clr[1]

    def add_color_btn(self, master):
        """
        if "do not resize" flag is set \\
        selecting concatenated image bg color is often needed
        """
        _btn = tk.Button(master, text='', background=self.bg_color, width=3, height=1, 
                command=self._call_clrchooser)
        master.propagate(False)
        _btn.pack(pady=8)
        return _btn

    def add_biscale(self, row_index, column_index, master, lbl, truestr, falsestr):
        """
        biscale(BinaryScale) is a customized Scale \\
        it acts like simple "on/off" lever for an inner variable \\
        and changes related Label text by onclick event
        """
        _scale = BinaryScale(master=master, strvalue=lbl, truestr=truestr, falsestr=falsestr, 
                orient='horizontal', from_=0, to=1)
        _scale.configure(background='Teal', length=25, width=8, highlightbackground='DarkSlateBlue', 
                borderwidth=0, sliderrelief=tk.FLAT, troughcolor='AliceBlue', sliderlength=15, 
                highlightthickness=2, showvalue=0)
        _scale.grid(row=row_index, column=column_index)
        return _scale

    def add_label(self, row_index, column_index, master, txt):
        """
        """
        _label = BinaryLabel(master=master, initialstr=txt, background='LightSteelBlue', 
                font=('Consolas', '14', 'bold'))
        _label.grid(row=row_index, column=column_index, columnspan=5, sticky=tk.W)
        return _label

    def add_listbox(self, rowindex, columnindex, master):
        """
        """
        lbox = tk.Listbox(master, bg='AliceBlue', height=4)
        lbox.grid(row=rowindex, column=columnindex, columnspan=6, rowspan=4, sticky=tk.NSEW)
        return lbox

    def _call_selectfiles(self):
        """
        calls tkinter.dialogs askopenfilenames \\
        if listbox cursor is active file names should be placed after it \\
        """
        _curpos = self.lstbox.curselection()
        filelist = askopenfilenames(filetypes=(("image files", "*.png *.jpg *.jpeg *.gif"),))
        if len(_curpos):
            _curpos = 1 + int(_curpos[0])
            for i, name in enumerate(filelist):
                self.lstbox.insert(i + _curpos, name)
        else:
            for name in filelist:
                self.lstbox.insert(tk.END, name)             

    def add_inputbtn(self, master):
        """
        '+' sign button
        """
        master.propagate(False)
        _btn = tk.Button(master, activebackground='AliceBlue', command=self._call_selectfiles)
        _btn.img = tk.PhotoImage(file=r"img/include.png")
        _btn.configure(image=_btn.img)
        _btn.pack(padx=5, pady=3)
        return _btn

    def _call_excludefile(self):
        """
        """
        _curpos = self.lstbox.curselection()
        if len(_curpos):
            self.lstbox.delete(_curpos)

    def add_excludebtn(self, master):
        """
        '-' sign button
        """
        master.propagate(False)
        _btn = tk.Button(master, activebackground='AliceBlue', command=self._call_excludefile)
        _btn.img = tk.PhotoImage(file=r"img/exclude.png")
        _btn.configure(image=_btn.img)        
        _btn.pack(padx=5, pady=3)
        return _btn

    def add_outputdir_entry(self, rowindex, columnindex, master, txt):
        """
        """
        _entry = MergerEntry(master=master, initialstr=txt, bg='AliceBlue')
        _entry.grid(row=rowindex, column=columnindex, columnspan=5, sticky=tk.NSEW, padx=3, pady=4)
        return _entry

    def _call_askdir(self):
        """
        always returns *.png string
        """
        _path = askdirectory()
        _path = ['\\' if e == '/' else e for e in _path]
        _path.append('\\')
        _path = MergerScripts.form_filepathstr(''.join(_path))
        self.direntry.variable = _path

    def add_outputdir_btn(self, master):
        """
        """
        master.propagate(False)
        _btn = tk.Button(master, text='<<', activebackground='AliceBlue', 
                font=('Consolas', '14', 'bold'), command=self._call_askdir)
        _btn.pack(padx=5, pady=3)
        return _btn

    def _call_process_files(self):
        """
        depending on activated flags different combination of scripts is called
        """
        file_names = self.lstbox.get(0, tk.END)
        if len(file_names) < 2: return

        file_list = [Image.open(e) for e in file_names]

        if self.bs_resize.variable: 
            if self.bs_concat.variable:
                max_width = MergerScripts.find_max_width(file_list)
                file_list = MergerScripts.resize_all_tomax(file_list, max_width, 
                                                    Image, is_vertical=True)
            else:
                max_height = MergerScripts.find_max_height(file_list)
                file_list = MergerScripts.resize_all_tomax(file_list, max_height, 
                                                    Image, is_vertical=False)
            
        if self.bs_concat.variable: 
            result_image = MergerScripts.concatenate_v(file_list, self.bg_color, Image)
        else:
            result_image = MergerScripts.concatenate_h(file_list, self.bg_color, Image)
        
        _path = self.direntry.variable
        _path = MergerScripts.form_filepathstr(_path)
        self.direntry.variable = _path        
        result_image.save(f'{self.direntry.variable}', 'PNG')
        

    def add_process_btn(self, rowindex, columnindex, master):
        """
        """
        _frame = tk.Frame(master, width=100, height=30, background='LightSteelBlue')
        _frame.grid(row=rowindex, column=columnindex, columnspan=2)
        _frame.propagate(False)
        _btn = tk.Button(_frame, text='Process', activebackground='AliceBlue', 
                font=('Consolas', '14', 'bold'), command=self._call_process_files)
        _btn.pack(padx=5, pady=3)
        return _btn              

if __name__ == "__main__":
    root = tk.Tk()
    im = ImageMerger(root)
    root.mainloop()
