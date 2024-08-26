import tkinter as tk
from tkinter.filedialog import askopenfilename

from dustmaker.level import Level
from dustmaker.dfreader import DFReader
from dustmaker.dfwriter import DFWriter


class GuiWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('Dustforce Level Thumbnail Editor')

        ###### ROW 0 ######
        self.choose_level = tk.Label(self.root, text='Dustforce Level:', font='Helvetica 14 bold')
        self.choose_level.grid(column=0, row=0, sticky=tk.W)
        self.level_name = tk.Label(self.root, text='N/A', font='Helvetica 14')
        self.level_name.grid(column=1, row=0, sticky=tk.W)
        self.button1 = tk.Button(self.root, text='Choose Level', fg='black', command=self.browse_1,
                                 font='Helvetica 12 bold')
        self.button1.grid(column=2, row=0, sticky=tk.W)

        ###### ROW 1 ######
        self.new_image = tk.Label(self.root, text='Image (382x182):', font='Helvetica 14 bold')
        self.new_image.grid(column=0, row=1, sticky=tk.W)
        self.thumbnail_name = tk.Label(self.root, text='N/A', font='Helvetica 14')
        self.thumbnail_name.grid(column=1, row=1, sticky=tk.W)
        self.button2 = tk.Button(self.root, text='Choose Image', fg='black', command=self.browse_2,
                                 font='Helvetica 12 bold')
        self.button2.grid(column=2, row=1, sticky=tk.W)

        ###### CONVERT BUTTON ######
        self.button3 = tk.Button(self.root, text='Convert!', command=self.convert,
                                 font='Helvetica 12 bold')
        self.button3.grid(column=3, row=0, rowspan=2, sticky=tk.W, ipady=20)

        ###### ROW 2 ######
        self.status_text = tk.Label(self.root, text='Status: Waiting for conversion...', font='Helvetica 14 bold')
        self.status_text.grid(column=2, row=2, columnspan=2, sticky=tk.NW)

        # File Path Stuff
        self.level_path = None
        self.thumbnail_path = None

    def browse_1(self):
        """Browser window for getting Dustforce Level path"""
        self.level_path = askopenfilename(title='Choose the Dustforce Level to be replaced')
        file_path_short = self.level_path.rsplit('/', 1)  # Returns a list
        self.level_name.configure(text=file_path_short[-1])
        self.status_text.configure(text='Status: Waiting for conversion...')

    def browse_2(self):
        """Browser window for getting new image path"""
        self.thumbnail_path = askopenfilename(title='Choose an image to be used (382x182)')
        file_path_short = self.thumbnail_path.rsplit('/', 1)  # Returns a list
        self.thumbnail_name.configure(text=file_path_short[-1])
        self.status_text.configure(text='Status: Waiting for conversion...')

    def convert(self):
        """Load the DF Level, update the thumbnail, and save the modified Level."""
        level = self.load_level()
        self.update_level_image(level)

    def load_level(self) -> Level:
        try:
            with DFReader(open(self.level_path, 'rb')) as level_reader:
                level = level_reader.read_level()
            return level
        except (FileNotFoundError, TypeError):
            pass

    def update_level_image(self, level: Level):  # Image must be .png and 382x182
        try:
            if self.thumbnail_path.endswith('.png'):
                with open(self.thumbnail_path, 'rb') as f:
                    new_image_bytes = f.read()
                level.sshot = new_image_bytes
                with DFWriter(open(self.level_path, "wb")) as level_writer:
                    level_writer.write_level(level)

                self.status_text.configure(text='Status: Conversion completed!')

            else:
                self.status_text.configure(text='Status: Error! Check file types')
        except AttributeError:
            pass


def run():
    root = tk.Tk()
    GuiWindow(root)
    root.mainloop()


if __name__ == '__main__':
    run()
