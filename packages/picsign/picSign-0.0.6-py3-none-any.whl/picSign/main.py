import PIL.Image
from PIL import Image

from enum import Enum


def set_bit(bit: int, value: int) -> int:
    """
    Set the last bit to the given value
    """
    if int(bin(bit)[-1]) == value:
        return bit
    else:
        return bit ^ (1 << 0)


class Msg:
    STARTING_BITS = [(ord(j) >> k) & 1 for j in "$666$" for k in range(8 - 1, -1, -1)]
    ENDING_BITS = [(ord(j) >> k) & 1 for j in "&666&" for k in range(8 - 1, -1, -1)]
    MAX_MSG_SIZE = 32

    class ContentType(Enum):
        TEXT = 0
        FILE = 1

    def __init__(self, content, content_type: ContentType, file_name=None):
        self.file_name = file_name
        self.content = content
        self.content_type = content_type

    @property
    def content_size(self):
        return len(self.encode_content_size)

    @property
    def encode_content_size(self):
        return [len(self.content_bits) >> k & 1 for k in range(self.MAX_MSG_SIZE - 1, -1, -1)]

    @property
    def header_size(self):
        return len(self.STARTING_BITS) + len(self.encode_content_size) + len([self.content_type])

    @property
    def footer_size(self):
        return len(self.ENDING_BITS)

    @property
    def content_bits(self):
        """
        Convert the message to bits
        """
        if self.content_type == self.ContentType.TEXT:
            return [ord(j) >> k & 1 for j in self.content for k in range(8 - 1, -1, -1)]
        else:
            return [j >> k & 1 for j in self.content for k in range(8 - 1, -1, -1)]

    def build_msg(self):
        return self.STARTING_BITS + self.encode_content_size + [
            self.content_type.value] + self.content_bits + self.ENDING_BITS

    def write_to(self, image: PIL.Image.Image):
        """
        Write the message to the image
        """
        if self.content_type == self.ContentType.FILE:
            with open(self.content, "rb") as f:
                self.content = f.name.encode('utf-8') + b'\n' + f.read()

        if len(self.content_bits) + len(self.encode_content_size) + self.header_size + self.footer_size > image.size[
            0] * image.size[1]:
            raise Exception("The message is too long to fit in the image")

        msg = self.build_msg()
        for i in range(len(msg)):
            pixel = image.getpixel((i % image.width, i // image.width))
            image.putpixel((i % image.width, i // image.width), (pixel[0], pixel[1], set_bit(pixel[2], msg[i])))

    @staticmethod
    def read_from(image: PIL.Image.Image):
        """
        Read the message from the image
        """
        msg = []
        for i in range(image.width * image.height):
            pixel = image.getpixel((i % image.width, i // image.width))[2]
            msg.append(int(bin(pixel)[-1]))
        if msg[:len(Msg.STARTING_BITS)] == Msg.STARTING_BITS:
            del msg[:len(Msg.STARTING_BITS)]
            size = int("".join([str(i) for i in msg[:Msg.MAX_MSG_SIZE]]), 2)
            del (msg[:Msg.MAX_MSG_SIZE])
            content_type = Msg.ContentType(msg.pop(0))
            msg_bits = msg[:size]
            del msg[:size]
            if msg[:len(Msg.ENDING_BITS)] == Msg.ENDING_BITS:
                if content_type == Msg.ContentType.TEXT:
                    msg = [chr(int("".join([bin(j)[-1] for j in msg_bits[i:i + 8]]), 2)) for i in
                           range(0, len(msg_bits), 8)]
                    return Msg("".join(msg), content_type)
                else:
                    msg = bytes([int("".join([bin(j)[-1] for j in msg_bits[i:i + 8]]), 2) for i in
                                 range(0, len(msg_bits), 8)])
                    msg = msg.split(b'\n', 1)
                    return Msg(msg[1], content_type, msg[0].decode('utf-8'))
            else:
                raise Exception("No footer found")
        else:
            raise Exception("No header found")


def write_image(image, input, out='out', is_file=False):
    with Image.open(image) as im:
        msg = Msg(input, Msg.ContentType(is_file))
        msg.write_to(im)
        im.save(out + '.png', quality='keep')


def read_image(image):
    with Image.open(image) as im:

        msg = Msg.read_from(im)
        if msg.content_type == Msg.ContentType.TEXT:
            print(msg.content)
        else:
            with open('extracted__' + msg.file_name, 'wb') as content:
                content.write(msg.content)
