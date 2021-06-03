"""
Test for monks filter unittest
"""
import unittest
from PIL import Image
import monks_filter
import os


class MonkTestCases(unittest.TestCase):
    """
    Monks tests
    """

    def setUp(self):
        """
        Set up parser
        """
        self.parser = monks_filter.create_options()

    def test_rotate_wrong_argument(self):
        """
        Test wrong arguments in rotate def
        """
        path = os.path.abspath('input.jpg')
        i = Image.open(path)
        result, error = monks_filter.rotate('a', i)
        i.close()
        self.assertEqual('not all arguments converted during string formatting', error)
        self.assertEqual(None, result)

    def test_rotate_error(self):
        """
        Test error in rotate def
        """
        result, error = monks_filter.rotate('40', 'errorimage.jpg')
        self.assertEqual("'str' object has no attribute 'rotate'", error)
        self.assertEqual(None, result)

    def test_rotate_ok(self):
        """
        Test ok rotate def
        """
        path = os.path.abspath('input.jpg')
        i = Image.open(path)
        result, error = monks_filter.rotate(40, i)
        i.close()
        self.assertEqual(error, None)
        self.assertIsNotNone(result)

    def test_overlay_missing_argument(self):
        """
        Test missing arguments in overlay def
        """
        path = os.path.abspath('input.jpg')
        i = Image.open(path)
        result, error = monks_filter.overlay("", i)
        i.close()
        self.assertEqual("\'str\' object has no attribute \'read\'", error)
        self.assertIsNone(result)

    def test_overlay_error(self):
        """
        Test errors in overlay def
        """
        path = os.path.abspath('input.jpg')
        with Image.open(path) as image:
            result, error = monks_filter.overlay("input.jpg", image)
        self.assertEqual('the overlay image must be transparent . RGBA mode', error)
        self.assertIsNone(result)

    def test_overlay_ok(self):
        """
        Test everything ok in overlay def
        """
        path = os.path.abspath('input.jpg')
        path1 = os.path.abspath('python.png')
        i = Image.open(path)
        result, error = monks_filter.overlay(path1, i)
        i.close()
        self.assertEqual(None, error)
        self.assertIsNotNone(result)

    def test_gray_scale_ok(self):
        """
        Test everything ok in gray scale def
        """
        path = os.path.abspath('input.jpg')
        i = Image.open(path)
        monks_filter.gray_scale(image=i)
        i.close()
        self.assertEqual(True, True)

    def test_missing_all_arguments(self):
        """
        Test missing all args in options array
        """
        options = []
        result = monks_filter.monks_filter(self.parser, options=options)
        self.assertEqual(result, "Missing image input")

    def test_multiple_arguments_missing_argument(self):
        """
        Test missing multiple args in options array
        """
        path = os.path.abspath('input.jpg')
        options = [path, '-r']
        result = monks_filter.monks_filter(self.parser, options=options)
        self.assertEqual("Missing argument!", result)

    def test_multiple_arguments_error(self):
        """
        Test errors in monks filter def
        """
        path = os.path.abspath('input.jpg')
        options = ['-f', "/tmp/images/input.asd", '-g']
        result = monks_filter.monks_filter(self.parser, options=options)
        self.assertEqual("I didn't find your file, are you sure you put the wright path?", result)

    def test_missing_file(self):
        """
        Test missing file in options array
        """
        path = os.path.abspath('python.png')
        options = ['-r', '-o', path]
        result = monks_filter.monks_filter(self.parser, options=options)
        self.assertEqual("Missing argument!", result)

    # def test_multiple_arguments_ok(self):
    #     """
    #     Test everything ok in the monks filter def
    #     """
    #     path = os.path.abspath('input.jpg')
    #     options = ['-f', path, '-r', '40', "-n", "hola", "-e", "jpg"]
    #     result = monks_filter.monks_filter(self.parser, options=options)
    #     self.assertEqual("OUTPUT: /tmp/images/hola.jpg", result)
    #
    # def test_multiple_arguments_png_ok(self):
    #     """
    #     Test everything ok in the monks filter def
    #     """
    #     path = os.path.abspath('input.jpg')
    #     options = ['-f', path, '-r', '40', "-n", "hola", "-e", "png"]
    #     result = monks_filter.monks_filter(self.parser, options=options)
    #     self.assertEqual("OUTPUT: /tmp/images/hola.png", result)


if __name__ == '__main__':
    unittest.main()
