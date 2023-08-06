# picSign
a module to sign your image by encoding a text or a file in it.
can use as a python module or a command line tool.

## module

```python
from picsign.pic_sign import write_image, read_image
write_image(image, input, output_name, input_is_file)
read_image(image)
```

## running
```
Sign Picture:
    sign your image by encoding a text in pixels of the image

Usage:
    picSign (-w | --write) <image> <input> [-f -o OUT]
    picSign (-r | --read) <image>
    picSign (-h | --help)
    picSign --version

Options:
    -w --write              use the program in write mode
    -r --read               use the program in read mode
    -h --help               show this help message and exit
    -f --file               encode a file in the image
    -o OUT --output OUT     output the image to a file [default: out]
Examples:
    picSign -w image.png "Hello World"
    picSign -r image.png
```

## building
for building standalone one file executable

`nuitka --standalone --onefile .\src\picSign\main.py`
see [nuitka](https://nuitka.net/docs/latest/UserGuide/GUI.html#standalone-mode) docs for more infos.