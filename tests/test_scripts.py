from src.mscripts import MergerScripts
from PIL import Image

class TestScripts():
    @classmethod
    def setup_class(cls):
        """
        """
        cls.images = list()
        cls.images.append(Image.open('img/puzzle.ico'))
        cls.images.append(Image.open('img/include.png'))


    @classmethod
    def teardown_class(cls):
        """
        """        

    def test_findfolderpath(self):
        expected = 'E:\\folder1\workdir\\'
        actual = MergerScripts.find_folderpath(r'E:\folder1\workdir\merger.py')
        assert expected == actual

    def test_findfilename(self):
        expected = 'merger.py'
        actual = MergerScripts._find_filename(r'E:\folder1\workdir\merger.py')
        assert expected == actual

    def test_formfilepath(self):
        expected = 'merger.py.png'
        actual = MergerScripts.form_filepathstr(r'merger.py')
        assert expected == actual

    def test_find_max_width(self):
        expected = 256
        actual = MergerScripts.find_max_width(self.images)
        assert expected == actual

    def test_find_max_height(self):
        expected = 256
        actual = MergerScripts.find_max_height(self.images)
        assert expected == actual


