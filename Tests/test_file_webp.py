from helper import unittest, PillowTestCase, hopper

from PIL import Image, WebPImagePlugin

try:
    from PIL import _webp
    HAVE_WEBP = True
except ImportError:
    HAVE_WEBP = False


class TestFileWebp(PillowTestCase):

    def setUp(self):
        if not HAVE_WEBP:
            return

        self.rgb_mode = "RGB"

    def test_unsupported(self):
        if HAVE_WEBP:
            WebPImagePlugin.SUPPORTED = False

        file_path = "Tests/images/hopper.webp"
        self.assert_warning(UserWarning,
            lambda: self.assertRaises(IOError, Image.open, file_path))

        if HAVE_WEBP:
            WebPImagePlugin.SUPPORTED = True

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_version(self):
        _webp.WebPDecoderVersion()
        _webp.WebPDecoderBuggyAlpha()

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_read_rgb(self):
        """
        Can we read a RGB mode WebP file without error?
        Does it have the bits we expect?
        """

        image = Image.open("Tests/images/hopper.webp")

        self.assertEqual(image.mode, self.rgb_mode)
        self.assertEqual(image.size, (128, 128))
        self.assertEqual(image.format, "WEBP")
        image.load()
        image.getdata()

        # generated with:
        # dwebp -ppm ../../Tests/images/hopper.webp -o hopper_webp_bits.ppm
        self.assert_image_similar_tofile(
            image, 'Tests/images/hopper_webp_bits.ppm', 1.0)

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_write_rgb(self):
        """
        Can we write a RGB mode file to webp without error.
        Does it have the bits we expect?
        """

        temp_file = self.tempfile("temp.webp")

        hopper(self.rgb_mode).save(temp_file)
        image = Image.open(temp_file)

        self.assertEqual(image.mode, self.rgb_mode)
        self.assertEqual(image.size, (128, 128))
        self.assertEqual(image.format, "WEBP")
        image.load()
        image.getdata()

        # generated with: dwebp -ppm temp.webp -o hopper_webp_write.ppm
        self.assert_image_similar_tofile(
            image, 'Tests/images/hopper_webp_write.ppm', 12.0)

        # This test asserts that the images are similar. If the average pixel
        # difference between the two images is less than the epsilon value,
        # then we're going to accept that it's a reasonable lossy version of
        # the image. The old lena images for WebP are showing ~16 on
        # Ubuntu, the jpegs are showing ~18.
        target = hopper(self.rgb_mode)
        self.assert_image_similar(image, target, 12.0)

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_write_unsupported_mode_L(self):
        """
        Saving a black-and-white file to WebP format should work, and be
        similar to the original file.
        """

        temp_file = self.tempfile("temp.webp")
        hopper("L").save(temp_file)
        image = Image.open(temp_file)

        self.assertEqual(image.mode, self.rgb_mode)
        self.assertEqual(image.size, (128, 128))
        self.assertEqual(image.format, "WEBP")

        image.load()
        image.getdata()
        target = hopper("L").convert(self.rgb_mode)

        self.assert_image_similar(image, target, 10.0)

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_write_unsupported_mode_P(self):
        """
        Saving a palette-based file to WebP format should work, and be
        similar to the original file.
        """

        temp_file = self.tempfile("temp.webp")
        hopper("P").save(temp_file)
        image = Image.open(temp_file)

        self.assertEqual(image.mode, self.rgb_mode)
        self.assertEqual(image.size, (128, 128))
        self.assertEqual(image.format, "WEBP")

        image.load()
        image.getdata()
        target = hopper("P").convert(self.rgb_mode)

        self.assert_image_similar(image, target, 50.0)

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_WebPEncode_with_invalid_args(self):
        """
        Calling encoder functions with no arguments should result in an error.
        """

        if _webp.HAVE_WEBPANIM:
            self.assertRaises(TypeError, _webp.WebPAnimEncoder)
        self.assertRaises(TypeError, _webp.WebPEncode)

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_WebPDecode_with_invalid_args(self):
        """
        Calling decoder functions with no arguments should result in an error.
        """

        if _webp.HAVE_WEBPANIM:
            self.assertRaises(TypeError, _webp.WebPAnimDecoder)
        self.assertRaises(TypeError, _webp.WebPDecode)

    @unittest.skipIf(not HAVE_WEBP, "WebP support not installed")
    def test_no_resource_warning(self):
        file_path = "Tests/images/hopper.webp"
        image = Image.open(file_path)

        temp_file = self.tempfile("temp.webp")
        self.assert_warning(None, image.save, temp_file)


if __name__ == '__main__':
    unittest.main()
