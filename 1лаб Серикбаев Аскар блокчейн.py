iin = input("Введите первые 11 цифр ИИН: ")
if len(iin) != 11 or not iin.isdigit():
    print("Ошибка: нужно ввести ровно 11 цифр")
    exit()

digits = [int(x) for x in iin]

# 1 проход
w1 = [1,2,3,4,5,6,7,8,9,10,11]
s1 = 0
for i in range(11):
    s1 += digits[i] * w1[i]
k1 = s1 % 11

if k1 < 10:
    print("контрольный разряд:", k1)
else:

# 2 проход
    w2 = [3,4,5,6,7,8,9,10,11,1,2]
    s2 = 0
    for i in range(11):
        s2 += digits[i] * w2[i]
    k2 = s2 % 11
    if k2 < 10:
        print("контрольный разряд:", k2)
    else:
        print("ИИН неверный")

