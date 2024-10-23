"""
Напишите функцию группового переименования файлов. Она должна:
a. Принимать параметр желаемое конечное имя файлов. При переименовании в конце имени добавляется порядковый номер.
b. Принимать параметр количество цифр в порядковом номере.
c. Принимать параметр расширение исходного файла. Переименование должно работать только для этих файлов внутри каталога.
d. Принимать параметр расширение конечного файла.
e. Принимать диапазон сохраняемого оригинального имени. Например для диапазона [3, 6] берутся буквы с 3 по 6 из исходного имени файла.
К ним прибавляется желаемое конечное имя, если оно передано. Далее счётчик файлов и расширение.
"""

import os


def rename_files(desired_final_name, num_digits, original_ext, final_ext, original_name_range):
    files = [f for f in os.listdir() if f.endswith(original_ext)]

    counter = 1

    for file in files:
        original_name = os.path.splitext(file)[0]
        original_name_keep = original_name[original_name_range[0] - 1:original_name_range[1]]
        new_name = f"{original_name_keep}{desired_final_name}{str(counter).zfill(num_digits)}.{final_ext.replace('.', '')}"
        os.rename(file, new_name)
        counter += 1


if __name__ == '__main__':
    rename_files("new_name", 3, ".txt", ".docx", [3, 6])
