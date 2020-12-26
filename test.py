import os
from submit import extractTimestamp, search_day

if __name__ == '__main__':
    my_string = "SỐ GD: 000AC2212008001173 Ngày: 09/08/2020 19:36"

    list_char_date = ["/", "-", ":"]
    my_string = my_string.split()
    if len(my_string) > 1:
        index = None
        for i in range(len(my_string)):
            content = my_string[i]
            for char in list_char_date:
                number = content.count(char)
                if number >= 2:
                    index = i
                    break

        result = my_string[index-1] + ' ' + my_string[index]
        print(result)
    else:
        result = my_string[0]
        print(result)