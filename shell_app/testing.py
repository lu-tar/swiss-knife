mask = 24
bin_train = [[00000000],[00000000],[0000000],[00000000]]
bin_train = ["0000000000000000000000000000000"]

i = 0
while i < len(bin_train):
    decimale = 0
    potenza = 1
    while bin_train[i][0]>0:
        resto = bin_train[i][0]%10
        bin_train[i][0] = bin_train[i][0]//10
        decimale += resto*potenza
        potenza = potenza*2
    print(decimale)
    i = i + 1