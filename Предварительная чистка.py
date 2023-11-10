import os
import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
from hashlib import sha256
from PIL import Image
import imagehash

print('Выбор настроек')
print()
print('Выберите папку в которой нужно найти и удалить дубликаты')


# создаем кнопку для выбора пользователем файлы
def callback():
    global name
    name = fd.askdirectory()


errmsg = 'Error!'
tk.Button(text='Choose folder',
          command=callback).pack(fill=tk.X)
tk.mainloop()

choice1 = input(
    'Желаете ли вы найти и удалить полные дубликаты(ответить "да" в случае согласия и "нет" в противоположном: ').lower()
while choice1 not in ['да', 'нет']:
    choice1 = input('Ошибка, введите значение снова: ')
choice2 = input(
    'Желаете ли вы найти и удалить похожие фото(ответить "да" в случае согласия и "нет" в противоположном: ').lower()
while choice2 not in ['да', 'нет']:
    choice2 = input('Ошибка, введите значение снова: ')
choice3 = input(
    'Желаете ли вы найти и удалить фото документов или размытые фото(ответить "да" в случае согласия и "нет" в противоположном: ').lower()
while choice3 not in ['да', 'нет']:
    choice3 = input('Ошибка, введите значение снова: ')


# 1 этап
def on_next_button_click1():
    # Действия, которые нужно выполнить при нажатии на кнопку "Далее"
    print('Шаг 1 из 7 Информация по папке')
    print('Папка: ', name)
    size = round(os.path.getsize(name) / 2 ** 30, 8)
    print('Размер: ', size, 'Гб')
    folder = Path(name)
    print('Количество файлов: ', len(list(folder.rglob("*"))))
    # print('Количество файлов: ', len(os.listdir(name)))


root1 = tk.Tk()

next_button1 = tk.Button(root1, text="Далее 1", command=on_next_button_click1)
next_button1.pack()

root1.mainloop()


# 2 этап
# функция удаления дублей
def find_duplicates(directory):
    duplicates = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_hash = sha256(f.read()).hexdigest()
                if file_hash in duplicates:
                    duplicates[file_hash].append(file_path)
                else:
                    duplicates[file_hash] = [file_path]
    return duplicates


def delete_duplicates(directory):
    duplicates = find_duplicates(directory)
    for file_hash, duplicate_files in duplicates.items():
        if len(duplicate_files) > 1:
            for file_path in duplicate_files[1:]:
                os.remove(file_path)
                print("Файл удален:", file_path)


# кнопка

def on_next_button_click2():
    print('Шаг 2 из 7 Поиск и удаление полных дубликатов')
    delete_duplicates(name)


# Действия, которые нужно выполнить при нажатии на кнопку "Далее"

if choice1 in ['Да', 'да']:
    root2 = tk.Tk()

    next_button2 = tk.Button(root2, text="Далее 2", command=on_next_button_click2)
    next_button2.pack()

    root2.mainloop()


# 3 этап

def find_similar_images(directory, threshold=100):
    hash_dict = {}
    similar_images = {}
    file_path = None
    # Создаем словарь хешей для всех изображений в папке
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                img = Image.open(f)
                img_hash = str(imagehash.phash(img))
                if img_hash in hash_dict:
                    hash_dict[img_hash].append(file_path)
                else:
                    hash_dict[img_hash] = [file_path]

    # Ищем похожие изображения
    for img_hash, file_paths in hash_dict.items():
        if len(file_paths) > 1:
            for i, file_path in enumerate(file_paths):
                if file_path not in similar_images:
                    similar_images[file_path] = []
                    for j in range(i + 1, len(file_paths)):
                        similarity = imagehash.numeric_diff(img_hash, imagehash.phash(Image.open(file_paths[j])))
                        if similarity < threshold:
                            similar_images[file_path].append(file_paths[j])

    return similar_images


# кнопка
def on_next_button_click3():
    print('Шаг 3 из 7 Поиск похожих фото')
    similar_images = find_similar_images(name, threshold=100)
    for img_file, similar_files in similar_images.items():
        if similar_files:
            print("Похожие фото:")
            print(img_file)
            for file_path in similar_files:
                print(file_path)
                print()


# Действия, которые нужно выполнить при нажатии на кнопку "Далее"

if choice2 in ['да']:
    root3 = tk.Tk()

    next_button3 = tk.Button(root3, text="Далее 3", command=on_next_button_click3)
    next_button3.pack()

    root3.mainloop()