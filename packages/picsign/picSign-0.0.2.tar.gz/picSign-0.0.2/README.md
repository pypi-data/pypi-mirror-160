# image_encoding

## running
```
Sign Picture:
    sign your image by encoding a text in pixels of the image

Usage:
    sign (-w | --write) <image> <input> [-f -o OUT]
    sign (-r | --read) <image>
    sign (-h | --help)
    sign --version

Options:
    -w --write              use the program in write mode
    -r --read               use the program in read mode
    -h --help               show this help message and exit
    -f --file               encode a file in the image
    -o OUT --output OUT     output the image to a file [default: out]
Examples:
    sign -w image.png "Hello World"
    sign -r image.png
```

## building
for building standalone one file executable

`nuitka --standalone --onefile .\src\picSign\main.py`
see [nuitka](https://nuitka.net/docs/latest/UserGuide/GUI.html#standalone-mode) docs for more infos.