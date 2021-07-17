class MergerScripts():
    @staticmethod
    def find_folderpath(argv):
        """
        tries to read directory path out of ./src/folder.dat \\
        or finds working directory path out of given sys.argv[0]
        """
        index = argv.rfind('\\') + 1
        folderpath = argv[:index]
        
        try:
            folderpath = MergerScripts.open_saved_fpath(folderpath)
        except FileNotFoundError:
            pass

        return folderpath

    @staticmethod
    def open_saved_fpath(folderpath):
       with open(f'{folderpath}src/folder.dat', 'r', encoding='utf-8') as f:
           return f.read()

    @staticmethod
    def _find_filename(fpath):
        """
        'C:\\folder\\result.png' -> 'result.png'
        """
        index = fpath.rfind('\\') + 1
        if index == -1 or index == len(fpath):
            return ''
        else:    
            return fpath[index:]

    @staticmethod
    def make_default_file_path(filepath_str, extension):
        """
        'C:\\folder\\', 'png' -> 'C:\\folder\\result.png'
        """
        name = MergerScripts._find_filename(filepath_str)
        if name == '':
            return f'{filepath_str}result.{extension}'
        elif name[-4:].upper() == f'.{extension.upper()}':
            return filepath_str
        else:
            return f'{filepath_str}.{extension}'

    @staticmethod
    def concatenate_h(imglist, bgcolor, Image):
        """
        horizontal concatenation of PIL Images list
        """
        concat_img = imglist[0]
        for im2 in imglist[1:]:
            im1 = concat_img
            height = im1.height if im1.height >= im2.height else im2.height                    
            concat_img = Image.new('RGB', (im1.width + im2.width, height), bgcolor)
            concat_img.paste(im1, (0, 0))
            concat_img.paste(im2, (im1.width, 0))
        return concat_img

    @staticmethod
    def concatenate_v(imglist, bgcolor, Image):
        """
        vertical concatenation of PIL Images list
        """
        concat_img = imglist[0]
        for im2 in imglist[1:]:
            im1 = concat_img
            width = im1.width if im1.width >= im2.width else im2.width	
            concat_img = Image.new('RGB', (width, im1.height + im2.height), bgcolor)
            concat_img.paste(im1, (0, 0))
            concat_img.paste(im2, (0, im1.height))
        return concat_img

    @staticmethod
    def find_max_width(image_list):
        """
        returns int value of max width in PIL images list
        """
        max_width = 0
        for f in image_list:
            img_width = f.width
            if img_width > max_width:
                max_width = img_width
        return max_width

    @staticmethod
    def find_max_height(image_list):
        """
        returns int value of max height in PIL images list
        """
        max_height = 0
        for f in image_list:
            img_height = f.height
            if img_height > max_height:
                max_height = img_height
        return max_height

    @staticmethod
    def find_min_width(image_list):
        """
        returns int value of min width in PIL images list
        """
        min_width = image_list[0].width
        for f in image_list:
            img_width = f.width
            if img_width < min_width:
                min_width = img_width
        return min_width

    @staticmethod
    def find_min_height(image_list):
        """
        returns int value of min height in PIL images list
        """
        min_height = image_list[0].height
        for f in image_list:
            img_height = f.height
            if img_height < min_height:
                min_height = img_height
        return min_height

    @staticmethod
    def resize_all_tomax(image_list, length, Image, is_vertical):
        """
        resizes all image by width if is_vertical <- True \\
        resizes all image by height if is_vertical <- False
        """
        result = list()
        if is_vertical: 
            max_width = length
            for i in range(len(image_list)):
                current = image_list[i]
                if current.width < max_width:
                    _size = (round(max_width), round(current.height * max_width / current.width))
                    current = current.resize(_size, Image.ANTIALIAS)
                result.append(current)
        else:
            max_height = length
            for i in range(len(image_list)):
                current = image_list[i]
                if current.height < max_height:
                    _size = (round(current.width * max_height / current.height), round(max_height))
                    current = current.resize(_size, Image.ANTIALIAS)            
                result.append(current)

        return result

    @staticmethod
    def change_folder_strip_ext(file_names, folder):
        """
        folder = C:/new folder/ \\
        'D:/images/name.png' -> 'C:/new folder/name'
        """
        result = [e[e.rfind('/') + 1:] for e in file_names]
        result = [e[:e.rfind('.')] for e in result]
        result = [folder + e for e in result]
        return result

    @staticmethod
    def resize_percents(file_names, folder, width, height, ext):
        """
        """
        from PIL import Image

        image_list = [Image.open(e) for e in file_names]
        file_names = MergerScripts.change_folder_strip_ext(file_names, folder)

        if width == None and height:
            width_percent = height / 100
            height_percent = height / 100
        
        elif height == None and width:
            width_percent = width / 100
            height_percent = width / 100
        
        elif width == None and height == None:
            width_percent = height_percent = 1
        
        else:
            width_percent = width / 100
            height_percent = height / 100

        for i, current in enumerate(image_list):
            if width_percent == 1 and height_percent == 1:
                resized_img = current
            else:
                _size = (round(current.width * width_percent), round(current.height * height_percent))
                resized_img = current.resize(_size, Image.ANTIALIAS)

            if ext=='PNG':
                resized_img.save(f'{file_names[i]}.png', 'PNG')
            else:
                resized_img.save(f'{file_names[i]}.jpg', 'JPEG')

    @staticmethod
    def resize_pixels(file_names, folder, width, height, ext):
        """
        """
        from PIL import Image

        image_list = [Image.open(e) for e in file_names]
        file_names = MergerScripts.change_folder_strip_ext(file_names, folder)

        for i, current in enumerate(image_list):

            if width == None and height:
                ratio = height / current.height
                new_width = round(current.width * ratio)
                new_height = height
            
            elif height == None and width:
                ratio = width / current.width
                new_width = width
                new_height = round(current.height * ratio)

            if width == None and height == None:
                resized_img = current
            else:
                _size = (new_width, new_height)
                resized_img = current.resize(_size, Image.ANTIALIAS)

            if ext=='PNG':
                resized_img.save(f'{file_names[i]}.png', 'PNG')
            else:
                resized_img = resized_img.convert('RGB')
                resized_img.save(f'{file_names[i]}.jpg', 'JPEG')

    @staticmethod
    def create_pdf(file_names, folder, dpi):
        from PIL import Image

        image = Image.open(file_names[0])
        other_images = [Image.open(fn).convert('RGB') for fn in file_names[1:]]

        image.save(f'{folder}', save_all=True, resolution=dpi, append_images=other_images)