a = int(input())
b = int(input())
c = int(input())

d = b**2 - (4*a*c)
if d > 0:
    x1 = (-b + (d ** 0.5))/(2*a)
    x2 = (-b - (d ** 0.5))/(2*a)
    print('Корни уравнения: x1 = ', x1, ' x2 = ', x2)
else:
    if d == 0:
        x = -b/(2*a)
        print('Корень уравнения - x = ', x)
    else:
        if d < 0:
            print('Корней нет')