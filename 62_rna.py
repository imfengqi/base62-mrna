import tkinter as tk
from tkinter import messagebox


# 定義base62字符集
base62_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

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
    result = "AUG"  # 起始子
    for char in message:
        if char not in char_to_codon:
            raise ValueError(f"非法字符:{char},只能輸入base62字符哦 (-_-;)")
        result += char_to_codon[char]
    result += "UAA"  # 終止子
    return result

# 將RNA密碼子解碼為消息


def decode_from_rna(rna_codons):

    if not rna_codons.startswith("AUG") or not rna_codons.endswith("UAA"):
        raise ValueError("完整的mRNA序列應包含起始子AUG和終止子UAA")

    body = rna_codons[3:-3]  # 去掉起始子與終止子
    if not body:
        raise ValueError("mRNA信息序列不能為空")

    if len(body) % 3 != 0:
        raise ValueError("無效的mRNA序列（包含不完整的密碼子）")

    for c in body:
        if c not in "ACGU":
            raise ValueError(f"無效的RNA鹼基: {c}")

    chars = [codon_to_char.get(body[i:i+3], "?")
             for i in range(0, len(body), 3)]
    return ''.join(chars)


# GUI應用程序
class RNAEncoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RNA編碼器")

        self.label = tk.Label(root, text="輸入文本或RNA序列（文本請符合base62字符）:")
        self.label.pack()

        self.entry = tk.Entry(root, width=50, font=("Arial", 14))
        self.entry.pack()

        self.encode_button = tk.Button(
            root, text="將文本編碼為RNA", command=self.encode_message)
        self.encode_button.pack()

        self.decode_button = tk.Button(
            root, text="將RNA序列解碼為文本", command=self.decode_rna)
        self.decode_button.pack()

        self.result_label = tk.Label(
            root, text="")
        self.result_label.pack()

        self.copy_button = tk.Button(
            root, text="複製結果",
            command=self.copy_result,
        )
        self.copy_button.pack()

    def encode_message(self):
        message = self.entry.get()
        try:
            rna_sequence = encode_to_rna(message)
            self.result_label.config(text=f"編碼結果: {rna_sequence}")
        except ValueError as e:
            messagebox.showerror("錯誤", str(e))

    def decode_rna(self):
        rna_sequence = self.entry.get()
        try:
            message = decode_from_rna(rna_sequence)
            self.result_label.config(text=f"解碼結果: {message}")
        except ValueError as e:
            messagebox.showerror("錯誤", str(e))

    def copy_result(self):
        result = self.result_label.cget("text")
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("複製成功", "結果已複製到剪貼板")
        else:
            messagebox.showwarning("失敗", "沒有結果可供複製")


if __name__ == "__main__":
    root = tk.Tk()
    app = RNAEncoderApp(root)
    root.mainloop()
