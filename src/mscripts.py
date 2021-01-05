class MergerScripts():
    @staticmethod
    def find_folderpath(argv):
        """
        finds working directory path out of given sys.argv[0]
        """
        index = argv.rfind('\\') + 1
        folderpath = argv[:index]
        return folderpath

    @staticmethod
    def _find_filename(fpath):
        """
        'C:\\folder\result.png' -> 'result.png'
        """
        index = fpath.rfind('\\') + 1
        if index == -1 or index == len(fpath):
            return ''
        else:    
            return fpath[index:]

    @staticmethod
    def form_filepathstr(filepath_str):
        """
        'C:\\folder\result' -> 'C:\\folder\result.png'
        """
        name = MergerScripts._find_filename(filepath_str)
        if name == '':
            return f'{filepath_str}result.png'
        elif name[-4:].upper() == '.PNG':
            return filepath_str
        else:
            return f'{filepath_str}.png'

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
