from PIL import Image
image = Image.open("smile.png")
x, y = image.size
for i in range(y):
    for j in range(x):
        pix = image.getpixel((j, i))
        if pix != (255, 232, 58) and pix != (0, 0, 0):
            print(chr(pix[0]) + chr(pix[1]) + chr(pix[2]), end='')

        
