"""Monks challenge"""
import argparse
import logging
import sys
import uuid
from pathlib import Path

from PIL import Image


def im_has_alpha(img_arr):
    """
    returns True for Image with alpha channel
    """
    channel = img_arr.info.get("transparency")
    return channel is not None


def overlay(i_overlay, output):
    """
    overlay a given image on top of the source.
    """
    try:
        overlay_image = Image.open(i_overlay)
        if not im_has_alpha(overlay_image):
            return None, "the overlay image must be transparent . RGBA mode"
        print("Overlaying this beautiful image with this amazing png")
        output.paste(overlay_image.convert("RGBA"),
                                     mask=overlay_image.convert("RGBA"))
        overlay_image.close()
    except FileNotFoundError as file_error:
        print("I didn't find the image, are you sure is the right place? ")
        return None, str(file_error)
    except TypeError as type_error:
        print('Did you send an image input and a overlay image type?')
        return None, str(type_error)
    except OSError as os_error:
        print('Image format error')
        return None, str(os_error)
    except AttributeError as attribute_error:
        print('Did yo send two images?')
        return None, str(attribute_error)
    return output, None


def rotate(rotation, image):
    """
    rotate N degrees.
    """
    try:
        output = image.rotate(rotation)
        print("Changing to black and white")
    except FileNotFoundError as file_error:
        print("I didn't find the image, are you sure is the right place? ")
        return None, str(file_error)
    except TypeError as type_error:
        print('Did you send an image type and a rotation int?')
        return None, str(type_error)
    except AttributeError as attribute_error:
        print('Did you send an image and a rotation int?')
        return None, str(attribute_error)
    return output, None


def gray_scale(image):
    """
    convert the given image to black and white.
    """
    try:
        output = image.convert('LA')
        print("Changing to black and white")
    except FileNotFoundError as file_error:
        print("I didn't find the image, are you sure is the right place? " + str(file_error))
        return None, str(file_error)
    except TypeError as type_error:
        print('Did you send an image to gray scale it?')
        return None, str(type_error)
    except OSError as os_error:
        print("I do not see a file here" + str(os_error))
        return None, str(os_error)
    return output, None


def monks_filter(parser, options):  # pylint: disable=too-many-branches
    """
    Case arguments
    """
    image = Image.new(mode="RGBA", size=(0, 0))
    try:
        args = parser.parse_args(options)
        if args.input is None:
            return "Missing image input"
        original = Image.open(args.input)
        image = original.copy()
        original.close()
        error = None
        for option in options:
            if image is None:
                print("Something went wrong")
                logging.exception(error)
            if option in "-f" or option in "--file":
                continue
            if option in "-r" or option in "--rotate":
                image, error = rotate(args.num, image)
            elif option in "-o" or option in "--overlay":
                image, error = overlay(args.filename, image)
            elif option in "-g" or option in "--gray_scale":
                image, error = gray_scale(image)
            elif option in "-n" or option in "--name" or option in "-e" or option in "--extension":
                continue
            elif isinstance(option, str) and args.name is not None or args.type \
                    is not None or args.num is not None:
                continue
        monks_filter_result = set_output(args, image)
    except ValueError as value_error:
        logging.error(str(value_error))
        monks_filter_result = "I don't manage this kind of extension, " \
                              "you can send me jpg/png files if you want"
        image.close()
    except AttributeError as attribute_error:
        logging.error(str(attribute_error))
        monks_filter_result = "Missing parameters"
        image.close()
    except FileNotFoundError as file_not_found:
        logging.error(str(file_not_found))
        monks_filter_result = "I didn't find your file, are you sure you put the wright path?"
        image.close()
    except BaseException as exception:  # pylint: disable=broad-except
        logging.error(str(exception))
        monks_filter_result = "Missing argument!"
        image.close()
    return monks_filter_result


def set_output(arguments, image):
    """
    Setting name image output and saving file
    :param arguments: parser
    :param image: image to save
    :return:
    """
    name = str(uuid.uuid4())
    output_type = "jpg"
    directory = "/tmp/images/"
    if arguments.name is not None and isinstance(arguments.name, str):
        name = arguments.name
    if arguments.type is not None and "jpg" in arguments.type or "png" in arguments.type:
        output_type = arguments.type
    if arguments.directory is not None and isinstance(arguments.directory, str):
        directory = arguments.directory
    Path(directory).mkdir(parents=True, exist_ok=True)
    image.convert('RGB').save(directory + name + "." + output_type)
    image.close()
    return 'OUTPUT:' + directory + name + "." + output_type


def create_parser():
    """
    Creates the parser with the options for the user
    :return: Parser object
    """
    parser_args = argparse.ArgumentParser(description='Process images according to the '
                                                      'selected filters')
    parser_args.add_argument('-f', '--file', action='store', dest='input',
                        help='file to change')
    parser_args.add_argument("-r", "--rotate", action='store', type=int, dest="num",
                        help="rotate an image")
    parser_args.add_argument("-o", "--overlay", action='store', dest="filename",
                        help="overlying the input image with an a transparent png image")
    parser_args.add_argument("-g", "--gray_scale", dest="grayscale", action='store_true',
                        help="changing to black and white.")
    parser_args.add_argument("-e", "--extension", dest="type", action='store',
                        help="choose your type output. It could be png or jpg")
    parser_args.add_argument("-n", "--name_output", dest="name", action='store',
                        help="choose your name output image. "
                             "If you don't is going to be an uuid4 name")
    parser_args.add_argument("-d", "--directory", dest="directory", action='store',
                        help="choose where do you want to send the image. "
                             "If you don't is going to be in /tmp/images/."
                             "Please send it with the / at the end")
    return parser_args


if __name__ == '__main__':
    print("Let see what we're going to do")
    parser_arguments = create_parser()
    opts = sys.argv[1:]
    result = monks_filter(parser_arguments, opts)
    print(result)
