from PIL import Image
from random import randint
from time import sleep
s1 = [int(i) for i in b'4#1,\x07f/d;b\x08fb\x08']
def dum():
    for i in range(3):
        print('.', end='')
        sleep(1)
    print()

def pause():
    global s1
    for i in range(len(s1)):
        s1[i] = s1[i] ^ 73
    for i in range(1, 21):
        print(i)
        sleep(1)
s2 = [int(i) for i in b"\x19g#\x08\x10gg\x13\x08'\x1fg9d*"]
for i in range(len(s2)):
        s2[i] = s2[i] ^ 52
def main():
    task1 = Image.new('RGB', (100, 100))
    start_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    finish_color = (randint(0, 255), randint(0, 255), randint(0, 255))
    task_pixels = []
    global s2
    global s1
    for i in range(len(s2)):
        s2[i] = s2[i] ^ 73
    for x in range(100):
        for y in range(100):
            if randint(1, 10) > 7:
                task1.putpixel((x, y), start_color)
                task_pixels.append((x, y))
            else:   
                task1.putpixel((x, y), (randint(0, 255), randint(0, 255), randint(0, 255)))
    for i in range(len(s1)):
        s1[i] = s1[i] ^ 52
    task1.save("task1.png", "PNG")
    print("Сейчас я дам тебе разноцветный забор. Перекрась пожалуйста все пиксели цвета " + str(start_color[0]) + ' ' + str(start_color[1]) + ' ' + str(start_color[2]) + ' в цвет ' + str(finish_color[0]) + ' ' + str(finish_color[1]) + ' ' + str(finish_color[2]) + ', кроме тех, что лежат на одной из диагоналей картинки. На работу у тебя есть 20 секунд, время пошло!!!')
    pause()
    task1 = Image.open("task1.png")
    for i in range(len(s1)):
        s1[i] = s1[i] ^ 42
    for x in range(100):
        for y in range(100):
            color = task1.getpixel((x, y))
            if (x, y) in task_pixels:
                if x + y == 99 or x == y:
                    if task1.getpixel((x, y)) != start_color:
                        print("К сожалению ты не справился.")
                        input()
                        return 0
                elif task1.getpixel((x, y)) != finish_color:
                    print("К сожалению ты не справился.")
                    input()
                    return 0
    for i in range(len(s2)):
        s2[i] = s2[i] ^ 42
    print("Ты справился с задачей!")
    print(''.join([chr(i) for i in s1]) + ''.join([chr(i) for i in s2]))
    input()
main()
