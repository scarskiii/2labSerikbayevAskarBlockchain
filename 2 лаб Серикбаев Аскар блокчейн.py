import hashlib

iin = input("Введите свой ИИН (12 цифр): ")

if len(iin) != 12 or not iin.isdigit():
    print("Ошибка: нужно ввести ровно 12 цифр")
    exit()

number = 0

while True:
    text = iin + str(number)
    hash_value = hashlib.sha256(text.encode()).hexdigest()

    if hash_value.startswith("00"):
        print("Найдено")
        print("Входное значение:", text)
        print("Хэш:", hash_value)
        break

    number += 1

