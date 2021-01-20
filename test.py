import random
from submit import extractTimestamp

my_string = "SỐ GD: 000AB2212008003195 Ngày: 13/08/2020-08:52"

# string_tmp = my_string.lower()
list_time = my_string.split()
if len(list_time) > 3:
    time = extractTimestamp(my_string)
else:
    time =  my_string

print("time: ", time)