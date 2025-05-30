# 定義base62字符集
base62_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz"

# 定義RNA密碼子
# 這裡排除了起始密碼子AUG和終止密碼子UAA
rna_codons = [a+b+c
              for a in "ACGU"
              for b in "ACGU"
              for c in "ACGU"
              if a+b+c not in ["AUG", "UAA"]
              ]

# 確保有62個RNA密碼子
assert len(rna_codons) == 62

# 建立字符到RNA密碼子的映射
char_to_codon = dict(zip(base62_chars, rna_codons))
codon_to_char = {v: k for k, v in char_to_codon.items()}

# 將消息編碼為RNA密碼子


def encode_to_rna(message):
    codons = ["AUG"]  # 起始密碼子
    for ch in message:
        if ch not in char_to_codon:
            raise ValueError(f"非法字符: {ch}")
        codons.append(char_to_codon[ch])
    codons.append("UAA")  # 終止密碼子
    return " ".join(codons)

# 將RNA密碼子解碼為消息


def decode_from_rna(rna_string):
    codons = rna_string.strip().split()
    if codons[0] != "AUG" or codons[-1] != "UAA":
        raise ValueError("完整的mRNA序列必須以起始子AUG開始,並以終止子UAA結束")
    message = ""
    for codon in codons[1:-1]:  # 排除起始和終止密碼子
        if codon not in codon_to_char:
            raise ValueError(f"非法RNA密碼子: {codon}")
        message += codon_to_char[codon]
    return message


# 測試編碼和解碼功能
text = "J38H"
encoded_rna = encode_to_rna(text)
print("編碼後的RNA序列:", encoded_rna)
decoded_text = decode_from_rna(encoded_rna)
print("解碼後的文本:", decoded_text)

# 測試非法字符處理
try:
    encode_to_rna("Hello@World")
except ValueError as e:
    print("錯誤:", e)

# 測試非法RNA密碼子處理
try:
    decode_from_rna("AUG XYZ UAA")
except ValueError as e:
    print("錯誤:", e)
