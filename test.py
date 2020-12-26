import os
from submit import extractTimestamp

# my_string = "Số GD: 000AB2212008002615 Ngày: 10/08/2020-18:22 thuy nha"

# my_string = my_string.split()
# for content in my_string:
#     print("content: ", content)
#     print("type: ", type(content))
#     try:
#         res = extractTimestamp(my_string)
#         print(res)
#     except Exception as e:
#         print("bug in preprocess time: ", e)
#         print("Guess Content Not Time")

with open("seller_dictionary.txt") as f:
    content = f.readlines()
LIST_SELLER_DEF = [x.strip() for x in content] 

with open("seller.txt", "a+") as f:
    for content in LIST_SELLER_DEF:
        content = content.lower()
        f.write("{}\n".format(content))