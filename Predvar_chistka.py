import os
import tkinter as tk
from tkinter import filedialog as fd
from pathlib import Path
from hashlib import sha256
from PIL import Image
import imagehash
import cv2
import fitz  # PyMuPDF
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
import exifread
from datetime import datetime
from shutil import move
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from moviepy.editor import VideoFileClip






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
    print('Шаг 1 из 6 Информация по папке')
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
    print('Шаг 2 из 6 Поиск и удаление полных дубликатов')
    delete_duplicates(name)


# Действия, которые нужно выполнить при нажатии на кнопку "Далее"

if choice1 in ['Да', 'да']:
    root2 = tk.Tk()

    next_button2 = tk.Button(root2, text="Далее 2", command=on_next_button_click2)
    next_button2.pack()

    root2.mainloop()


# 3 этап

"""
def find_similar_images(directory, threshold=1000):
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
def on_next_button_click3():
    print('Шаг 3 из 7 Поиск похожих фото')
    similar_images = find_similar_images(name, threshold=1000)
    for img_file, similar_files in similar_images.items():
        if similar_files:
            print("Похожие фото:")
            print(img_file)
            for file_path in similar_files:
                print(file_path)
                print()


from PIL import Image
import os
from imagehash import average_hash
from collections import defaultdict
import shutil

def find_and_delete_similar_images(folder_path, similarity_threshold=5000):
    image_hashes = defaultdict(list)

    # Проход по всем файлам в папке
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Игнорирование неизображений
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            continue

        # Вычисление хэша изображения
        with Image.open(file_path) as img:
            hash_value = str(average_hash(img))

        # Добавление хэша в список для соответствующего хэша
        image_hashes[hash_value].append(file_path)

    # Поиск и удаление похожих изображений
    for hash_value, file_paths in image_hashes.items():
        if len(file_paths) > 1:
            print(f"Похожие изображения с хэшем {hash_value} найдены:")
            for i, file_path in enumerate(file_paths):
                print(f"{i + 1}. {file_path}")

            # Удаление похожих изображений, оставив только одно
            for file_path in file_paths[1:]:
                os.remove(file_path)
                print(f"Изображение {file_path} удалено.")

    print("Процесс завершен.")


def on_next_button_click3():
    print('Шаг 3 из 6 Поиск похожих фото')
    folder_path = name
    find_and_delete_similar_images(folder_path)
"""
"""
def compare_images(image1, image2):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    (score, diff) = ssim(gray1, gray2, full=True)
    return score

def find_and_delete_similar_images(directory, threshold):
    images = os.listdir(directory)
    for i in range(len(images)):
        for j in range(i+1, len(images)):
            image1 = os.path.join(directory, images[i])
            image2 = os.path.join(directory, images[j])
            similarity = compare_images(image1, image2)
            if similarity > threshold:
                print(f"Deleting similar images: {images[i]} and {images[j]}")
                os.remove(image2)


def on_next_button_click3():
    print('Шаг 3 из 6 Поиск похожих фото')
    directory = name
    threshold = 0.8  # Порог сходства изображений
    find_and_delete_similar_images(directory, threshold)


# Действия, которые нужно выполнить при нажатии на кнопку "Далее"

if choice2 in ['да']:
    root3 = tk.Tk()

    next_button3 = tk.Button(root3, text="Далее 3", command=on_next_button_click3)
    next_button3.pack()

    root3.mainloop()

"""
#4 этап

def is_blurry(image_path):
    # Функция, определяющая, является ли изображение размытым
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.Laplacian(gray, cv2.CV_64F).var()
    return blur < 100  # Порог размытия, который можно настроить

def process_images(folder_path):
    # Функция для обработки изображений в папке
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, filename)
            if is_blurry(image_path):
                os.remove(image_path)
                print(f"Удалено размытое изображение: {filename}")

def process_pdfs(folder_path):
    # Функция для обработки PDF-документов в папке
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            doc = fitz.open(pdf_path)
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images(full=True)
                for img_index, img_info in enumerate(image_list):
                    img_index += 1
                    image = page.get_pixmap(image_index=img_index)
                    image_path = f"{pdf_path}_page{page_num + 1}_img{img_index}.png"
                    image.save(image_path)
                    if is_blurry(image_path):
                        os.remove(image_path)
                        print(f"Удалено размытое изображение из PDF: {filename} - страница {page_num + 1}, изображение {img_index}")
            doc.close()


def on_next_button_click4():
    print('Шаг 4 из 6 Удаление размытых фото и документов')
    if __name__ == "__main__":
        folder_path = name
        process_images(folder_path)
        process_pdfs(folder_path)


# Действия, которые нужно выполнить при нажатии на кнопку "Далее"

root4 = tk.Tk()
next_button4 = tk.Button(root4, text="Далее 4", command=on_next_button_click4)
next_button4.pack()
root4.mainloop()



#5 этап

def resize_images(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if os.path.getsize(filepath) > 20 * 1024 * 1024:  # Проверяем размер файла (в байтах)
                img = Image.open(filepath)
                width, height = img.size
                new_size = (int(width * 0.7), int(height * 0.7))  # Уменьшаем размер на 30%
                img = img.resize(new_size, Image.ANTIALIAS)
                img.save(filepath)

def convert_videos(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if os.path.getsize(filepath) > 200 * 1024 * 1024:  # Проверяем размер файла (в байтах)
                video = VideoFileClip(filepath)
                video.write_videofile(filepath.replace('.mp4', '_converted.mp4'))  # Конвертируем видео




def on_next_button_click5():
    print('Шаг 5 из 6 Уменьшение размеров фото и видео')
    directory = name
    resize_images(directory)
    convert_videos(directory)


# Действия, которые нужно выполнить при нажатии на кнопку "Далее"

root5 = tk.Tk()
next_button5 = tk.Button(root5, text="Далее 5", command=on_next_button_click5)
next_button5.pack()
root5.mainloop()


#этап 6

def get_creation_date(filepath):
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f, stop_tag="EXIF DateTimeOriginal")
        if 'EXIF DateTimeOriginal' in tags:
            date_str = str(tags['EXIF DateTimeOriginal'])
            date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
            return date.year
        else:
            return None

def organize_files(source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    for filename in os.listdir(source_directory):
        filepath = os.path.join(source_directory, filename)

        if os.path.isfile(filepath):
            year = get_creation_date(filepath)
            if year is None:
                while True:
                    input_date = input(f"Укажите дату создания файла {filename} (гггг-мм-дд): ")
                    try:
                        date = datetime.strptime(input_date, '%Y-%m-%d')
                        year = date.year
                        break
                    except ValueError:
                        print("Неверный формат даты. Пожалуйста, введите дату в формате гггг-мм-дд.")

            year_directory = os.path.join(destination_directory, str(year))
            if not os.path.exists(year_directory):
                os.makedirs(year_directory)

            move(filepath, os.path.join(year_directory, filename))


def on_next_button_click6():
    print('Шаг 6 из 6 Уменьшение размеров фото и видео')
    source_directory = name
    destination_directory = name
    organize_files(source_directory, destination_directory)



# Действия, которые нужно выполнить при нажатии на кнопку "Далее"

root6 = tk.Tk()
next_button6 = tk.Button(root6, text="Далее 6", command=on_next_button_click6)
next_button6.pack()
root6.mainloop()


print("Организация окончена")