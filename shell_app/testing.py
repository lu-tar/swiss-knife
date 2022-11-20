bin_train = "00000000000000000000000000000000"
mask = 15
bin_train = bin_train.replace("0","1",mask)
first_oct = int(bin_train[0:8],2)
second_oct = int(bin_train[8:16],2)
third_oct = int(bin_train[16:24],2)
fourth_oct = int(bin_train[24:32],2)

print ("%s.%s.%s.%s" % (first_oct, second_oct, third_oct, fourth_oct))