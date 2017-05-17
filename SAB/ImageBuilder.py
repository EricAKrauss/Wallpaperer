## requires library => use "pip install Image" and it will install all required libraries

import os

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def combineWallpaper(files):
    resWidth = 1440
    resHight = 810
    result = Image.new("RGB", (resWidth*len(files), resHight))
    for index, file in enumerate(files):
        path = os.path.expanduser(file)
        img = Image.open(path)
        img.thumbnail((resWidth, resHight), Image.ANTIALIAS)
        if img.size < (resWidth,resHight):
            x = index * resWidth + (resWidth - img.size[0]) // 2
            y = (resHight - img.size[1]) // 2
        else:
            x = index * resWidth
            y = 0
        w, h = img.size
        result.paste(img, (x, y, x + w, y + h))
    outPath = '/tmp/tmpBkg.jpg'
    result.save(outPath)
    result.close()
    img.close()
    return outPath

def overlayImage(wallpaper,file,justify,percentH,percentV):
    wp = Image.open(os.path.expanduser(wallpaper))
    img = Image.open(os.path.expanduser(file))
    
    wpWidth = wp.size[0]
    wpHight = wp.size[1]
    w,h = img.size
    
    if justify == 'LEFT':
        x = wpWidth * percentH // 100
    else:
        x = wpWidth * percentH // 100 - w
    y = wpHight * percentV // 100


    wp.paste(img, (x,y,x+w,y+h))
    img.close()
    outPath = '/tmp/tmpBkg.jpg'
    wp.save(outPath)
    wp.close()
    return outPath

def overlayText(wallpaper,string,justify,percentH,percentV):
    wp = Image.open(os.path.expanduser(wallpaper))

    wpWidth = wp.size[0]
    wpHight = wp.size[1]

    draw = ImageDraw.Draw(wp)
    font = ImageFont.truetype("ARLRDBD.TTF",25)
    
    w,h = font.getsize(string)

    if justify == 'left':
        x = wpWidth * percentH // 100
    else:
        x = wpWidth * percentH // 100 - w
    y = wpHight * percentV // 100

    draw.rectangle((x,y,x+w,y+h),fill="black")
    draw.text((x,y),string,(255,255,255),font)
    
    outPath = '/tmp/tmpBkg.jpg'
    wp.save(os.path.expanduser(outPath))
    wp.close()
    return outPath
    
if __name__ == "__main__":
    combineWallpaper(['a.jpg','c.jpg'])
    overlayImage('combineWallpaper.jpg','b.jpg','left',50,0)
    overlayText('a.jpg','This is some text','left',50,50)

   
