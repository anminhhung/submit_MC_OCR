import os
from submit import extractTimestamp, search_day

if __name__ == '__main__':
    my_string = "11-18-08/2020 20:40:00|||NGÀY HẾT HAN: 2021/12/31"

    list_char_date = ["/", "-", ":"]
    if my_string.find('|||') != -1:
        new_string = my_string.split('|||')
        my_string = []
        for string in new_string:
            string = string.split()
            for ele in string:
                my_string.append(ele)
    else:
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
            print("index: ", index)
            for char in list_char_date:
                number = my_string[index+1].count(char)
                if number >= 1:
                    result += ' ' + my_string[index+1]
                    break
            
            print(result)
        else:
            result = my_string[0]
            print(result)