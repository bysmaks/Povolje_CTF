from PIL import Image

def extract_lsb_message_from_green(image_path):
    # Открываем изображение
    img = Image.open(image_path)
    pixels = img.load()

    # Хранение битов сообщения
    bits = []

    # Перебираем пиксели
    for y in range(img.height):
        for x in range(img.width):
            # Извлекаем только зелёный канал
            g = pixels[x, y][1]
            
            # Получаем наименее значимый бит зелёного канала
            bits.append(g & 1)

    # Группируем биты в байты и переводим их в символы
    message = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        byte_value = int("".join(map(str, byte)), 2)
        
        # Если байт - нулевой, это конец сообщения
        if byte_value == 0:
            break
        
        message += chr(byte_value)

    return message

message = extract_lsb_message_from_green("path/to/vestochka.jpg")
print(message)

# Строка из повестки
res = "info_that_will_help_you" 
# Числа из инструкции друга
nums = [42, 58, 32, 10, 62, 7, 13, 62, 29, 44, 40, 16, 3, 25, 45, 55, 1, 9, 3, 58, 24, 28, 16]

for i in range(len(res)):
    print(chr(ord(res[i]) ^ nums[i]), end="")