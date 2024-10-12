from PIL import Image
task1 = Image.open("task1.png")
start_color = tuple([int(i) for i in input("Введи начальный цвет: ").split()])
finish_color = tuple([int(i) for i in input("Введи целевой цвет: ").split()])
res = Image.new('RGB', (100, 100))
for x in range(100):
    for y in range(100):
        color = task1.getpixel((x, y))
        if  color == start_color and x + y != 99 and x != y:
            res.putpixel((x, y), finish_color)
        else:
            res.putpixel((x, y), color)
task1.close()
res.save("task1.png", "PNG")
