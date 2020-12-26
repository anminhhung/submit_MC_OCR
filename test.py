import os
from submit import extractTimestamp, search_day, LIST_DATE_DEF

if __name__ == '__main__':
    my_string = "13:41:39|||Ngay 12/06/2019|||Ma HD: EDAVACLUPANMY 14:05 25051"

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
    print("my string: ", my_string)
    if len(my_string) > 1:
        index = None
        for i in range(len(my_string)):
            flag = False
            content = my_string[i]
            for char in list_char_date:
                number = content.count(char)
                if number >= 2:
                    index = i
                    flag = True 
                    break
            
            if flag ==  True:
                break
        
        if index > 0:
            result = my_string[index-1] + ' ' + my_string[index]
        else:
            result = my_string[index]

        print("result: ", result)
        print("index: ", index)
        if index+1 < len(my_string):
            for char in list_char_date:
                number = my_string[index+1].count(char)
                if number >= 1:
                    result += ' ' + my_string[index+1]
                    break
        
        print(result)
    else:
        result = my_string[0]
        print(result)