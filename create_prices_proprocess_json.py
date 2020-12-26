import os 

SELLER_PREPROCESS = {
    "MINIMART ANAN": ["MINIMARTANAN"],
    "Vincommerce": ["Wincommerce", "UnCommerce", "InCommerce", "YinCommerce"],
    "Payoo": ["Payoos", "Pay?bi:"],
    "CẨM": ["CÁM"],
    "PHẢ": ["PHÁNG"],
    "Co.op": ["Co-op"],
    "&BÉ": ["8BS"]
}

ADDRESS_PREPROCESS = {
    "ĐC": ["ĐO", "Đ0", "Đo"],
    "đc": ["đo", "đ0"],
    "PHẢ": ["PHÀ", "PHI"],
    "Sủi": ["Súi"],
    "Lâm": ["Làm"],
    "PHỐ": ["PHÓ", "PHÔ"],
    "MỎ": ["MÔ"],
    "Cẩm": ["Câm", "Cảm", "Căm", "Cảm", "chm", "Càm"],
    "Phả": ["Phá", "Pha"],
    "Phả,": ["Pha,"],
    "CẨM": ["CÁM"],
    "Thôn": ["Thón"],
    "QNH": ["ONH", "NHI", "VIN4", "VIH"],
    "+": ["?", "4"],
    "VM+": ["VIÀ", "VM4", "VIM", "VM", "VINT", "MMA", "VINH"],
    "Phú": ["Phủ"],
    "Niên": ["Nien"],
    "Số": ["shi", "Só"],
    "QN": ["ON", "GN"],
    "ĐC:": ["Đo:", "Đó"],
    "GD-TC": ["GI-TC"],
    "Sơn": ["San"],
    "TỔ": ["TỐ"],
    "P.": ["A."],
    "Q.Nam": ["0.Nam"]
}

TIME_PREPROCESS = {
    "Ngày": ["Ngãy", "Ngãy:"],
    "Ngay:": ["Nosyn"]
}

PRICES_PREPROCESS = {
    "Tổng": ["Tổng", "Tông", "Tống", "Tồng", "Tỗng", "Tộng", "Tổna", "tiền mặt"],
    "tổng": ["tổng", "tông", "tống", "tồng", "tỗng", "tộng", "tổna"],
    "TỔNG": ["TỔNG", "TÔNG", "TỐNG", "TỒNG", "TỖNG", "TỘNG", "TĂNG", "CHI"],
    "Cộng": ["Cộng", "Công", "Cồng", "Cỗng", "Cổng", "Cống"],
    "cộng": ["cộng", "công", "cồng", "cỗng", "cổng", "cống"],
    "cộng:": ["cộng:", "công:", "cồng:", "cỗng", "cổng:", "cống:"],
    "tiền": ["tiền", "tiến", "tiên", "tiển", "tiễn", "tiện", "thuo"],
    "tiền:": ["tiền:", "tiến:", "tiên:", "tiển:", "tiễn:", "tiện:"],
    "Tiền": ["Tiền", "Tiến", "Tiên", "Tiển", "Tiễn", "Tiện"],
    "TIỀN": ["TIỀN", "TIẾN", "TIÊN", "TIỂN", "TIỄN", "TIỆN"],
    "TOÁN": ["TOÁN", "TOAN", "TOÀN", "TOẢN", "TOÃN", "TOẠN"],
    "Total": ["Total", "Sub Total", "sub total", "Gross Total", "GROSS TOTAL"],
    "": ["2", "1", "THÁN"],
    "Tong": ["Tong", "Tonn", "Tono"],
    "quầy": ["quáy.", "quáy", "quây"],
    "QUẦY": ["QUÁY.", "QUÁY", "QUÂY"]
}

PRICES_CHAR = {
    "VAT": ["VAT", "vat"],
    "đ": ["d", "đ"],
    "Đ": ["D", "Đ"],
    ",": ["."]
}

PREFIX_CHAR = {
    ":": [":", ",", ";", "."],
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