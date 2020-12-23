import os 

PRICES_PREPROCESS = {
    "Tổng": ["Tổng", "Tông", "Tống", "Tồng", "Tỗng", "Tộng"],
    "tổng": ["tổng", "tông", "tống", "tồng", "tỗng", "tộng"],
    "TỔNG": ["TỔNG", "TÔNG", "TỐNG", "TỒNG", "TỖNG", "TỘNG", "TĂNG"],
    "Cộng": ["Cộng", "Công", "Cồng", "Cỗng", "Cổng", "Cống"],
    "cộng": ["cộng", "công", "cồng", "cỗng", "cổng", "cống"],
    "cộng:": ["cộng:", "công:", "cồng:", "cỗng", "cổng:", "cống:"],
    "tiền": ["tiền", "tiến", "tiên", "tiển", "tiễn", "tiện"],
    "tiền:": ["tiền:", "tiến:", "tiên:", "tiển:", "tiễn:", "tiện:"],
    "Tiền": ["Tiền", "Tiến", "Tiên", "Tiển", "Tiễn", "Tiện"],
    "TIỀN": ["TIỀN", "TIẾN", "TIÊN", "TIỂN", "TIỄN", "TIỆN"],
    "TOÁN": ["TOÁN", "TOAN", "TOÀN", "TOẢN", "TOÃN", "TOẠN"],
    "Total": ["Total", "Sub Total", "sub total"],
    "": ["2", "1"],
    "Tong": ["Tong", "Tonn", "Tono"]
}

PRICES_CHAR = {
    ":": [":", ",", ";"],
    "VAT": ["VAT", "vat"],
    "đ": ["d", "đ"],
    "Đ": ["D", "Đ"],
    ",": ["."]
}

PREFIX_CHAR = {
    ":": [":", ",", ";"],
    "VAT": ["VAT", "vat"],
    "đ": ["d", "đ"],
    "Đ": ["D", "Đ"],
    ".": [". "]
}

a = "TỐNG TIẾN PHẢI T. TOÀN"
b = a.split()
for key, value in PRICES_PREPROCESS.items():
    for ele in value:
        for i in range(len(b)):
            char = b[i]
            if char == ele:
                b[i] = key
                break

a = ' '.join(map(str, b))
for key, value in PRICES_CHAR.items():
    for ele in value:
        index = a.find(ele)
        if index != -1:
            tmp = True
            a = a.replace(ele, key)
            break
print(a)