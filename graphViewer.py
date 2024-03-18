import argparse
import io
from PIL import Image
import shutil


def main ():
    parser = argparse.ArgumentParser (description = "graphViewer")
    parser.add_argument ('-p', '--print', action = 'store_true', help = '直接显示文件而不进行更复杂的处理')
    parser.add_argument ('file_path', type = str, help = '要处理的文件名')
    args = parser.parse_args ()
    imgObj = loadImg (args.file_path)
    if (imgObj == None): exit ()
    if (args.print):
        render_img (imgObj, False)
        exit()
    render_img (imgObj, True)
    exit()

def viewer_img (): 
    return

def viewer_vid ():
    return

def render_img (imgObj, cover):
    if imgObj is None: 
        print("Error: imgObj is None")
        return
    width_src, height_src = getTerminalSize ()
    width, height = calWHAuto (imgObj.width, imgObj.height, width_src, height_src)
    if (cover == False):
        height -= 1
    imgObj = imgObj.resize ((width, height), Image.Resampling.LANCZOS)
    for y in range (imgObj.height):
        for x in range (imgObj.width):
            r, g, b = imgObj.getpixel ((x, y))
            if (cover):
                printColorBlock_xy (x, y, r, g, b)
            else:
                printColorBlock (r, g, b)
        if (cover == False):
            print("")
    return

def loadImg (filePath):
    try:
        with open (filePath, "rb") as file:
            imgData = file.read ()
        imageObj = Image.open (io.BytesIO (imgData))
        return (imageObj)
    except IOError as e:
        print (f"Error: {e}, 图片加载失败")
        return (None)

def getTerminalSize ():
    size = shutil.get_terminal_size (fallback = (80, 24))
    return (size.columns, size.lines)

def calWHAuto (width_img, height_img, width_src, height_src):
    width_new = height_src / height_img * width_img
    height_new = height_src
    if (width_new > width_src / 2):
        height_new = (width_src / 2) / width_img * height_img
        width_new = width_src / 2
    return (round (width_new * 2), round (height_new))

def printColorBlock (r, g, b):
    print(f"\x1b[48;2;{r};{g};{b}m \x1b[0m", end="")

def printColorBlock_xy (x, y, r, g, b):
    print(f"\x1b[{y};{x}H", end="")
    print(f"\x1b[48;2;{r};{g};{b}m", end="")
    print(" ", end="")
    print("\x1b[0m", end="")

def main_debug ():
    imgObj = loadImg ("t3.jpg")
    while (True):
        render_img (imgObj, True)


if (__name__ == "__main__"):
    main ()
