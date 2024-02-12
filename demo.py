def prime(num, fc=0):
    for value in range(1, num+1):
        if num % value == 0:
            fc += 1

    return fc == 2


num = 2
count = 5
while (count != 0):
    if prime(num):
        print(num)
        num += 1
        count -= 1
    else:
        num += 1

        
