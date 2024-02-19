# импорт нужных модулей
from PyQt5.QtWidgets import QMessageBox
import pathlib
import csv
from pathlib import Path
import os
import docx
from docx import Document
from Warning import Ui_MainWindow3
from MainWinfowPr import Ui_MainWindow
from Dict import Ui_MainWindow2
from Hand_delete import Ui_MainWindow10
import sys
from PyPDF2 import PdfReader
from PyQt5.QtWidgets import QApplication, QMainWindow
import threading
from datetime import datetime
user = os.getlogin()
from threading import Timer
from Choice import Ui_Dialog
import PyPDF2
import pdfminer
from pdfminer.high_level import extract_text
import docx2txt

# переменная, в которой хранится название файла с запрещённым контентом

document = ''

# лист возможных корневых директорий в Windows

list_of_paths = ['A:/', 'B:/', 'D:/', 'C:/', 'E:/', 'F:/', 'G:/', 'H:/', 'I:/', 'J:/', 'K:/', 'L:/', 'M:/', 'N:/',
                 'O:/', 'P/:', 'Q:/', 'R:/', 'S:/', 'T:/', 'U:/', 'V:/', 'W:/', 'X:/', 'Y:/', 'Z:/', '/']

# лист возможных директорий кэша браузера в Linux

list_of_unix_paths = [f"/home/{user}/.cache/mozilla/firefox/", f"/home/{user}/.mozilla/firefox/*.default*/*.sqlite" f"/home/{user}/.mozilla/firefox/*default*/",
                      f"/home/{user}/.config/google-chrome/Default/", f"/home/{user}/.cache/google-chrome", f"/home/{user}/.cache/yandex-browser/Default/Cache/",
                      f"/home/{user}/.mozilla/firefox/*.default/Cache/", f"/home/{user}/.cache/chromium/Default/Cache/"]

# лист возможных директорий кэша браузера в Windows

list_of_windows_paths = [f"C:/Users/{user}/AppData/Local/Opera Software/Opera Stable/Cache/", f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data/Default/Cache/",
                         f"C:/Users/{user}/AppData/Local/Mozilla/Firefox/Profiles/*.default/cache2/entries/",
                         f"C:/Users/{user}/AppData/Local/Yandex/YandexBrowser/User Data/Default/Cache/", f"C:/Users/{user}/AppData/Local/Microsoft/Windows/INetCache/",
                         f"C:/Users/{user}/AppData/Local/Microsoft/Windows/Temporary Internet Files/"]

# лист директорий, которые могут иметь важные системные файлы

bad_list = ['C:/Windows/SystemApps', 'C:/Windows/WinSxS/', 'C:/Windows/servicing/']
bad_words = []

# добавляем в список bad_words запрещённые термины и сокращения из dict.txt (словаря)
with open('dict.txt', mode='r', encoding='utf-8') as f:
    a = f.readlines()
    a = ' '.join(a)
    a = a.split(', ')
    a = ' '.join(a)
    a = a.split()
    for i in a:
        bad_words.append(i)

# инициализируем глобальные переменные
# const указывает на автоматическое/ручное удаление файлов
# type_of_os имеет в себе тип операционной системы
# count и count2 показывают, сколько файлов было проверено и сколько удалено
# count_of_start нужна для определения первого запуска 2-го потока с функциями индексации и нахождения файлов


const = True
alt = True
type_of_os = os.name
count = 0
count2 = 0
condition = False
count_of_start = 0
global_set = set()

# класс основного окна


class MainWindow(QMainWindow, Ui_MainWindow):

    # инициализация графического интерфейса

    def __init__(self):
        super().__init__()
        self.setupUi1(self)
        global thr1
        global condition
        global global_set
        global alt

        # переменная, в которой будет состояние программы (на паузе/работает)

        self.condition = condition

        # подключение кнопок к функциям при нажатии

        self.selectButton.clicked.connect(self.change_window)
        self.exitButton.clicked.connect(self.exit_from_work)
        self.warnButton.clicked.connect(lambda: self.limits(True))
        self.pushButton_6.clicked.connect(lambda: self.limits(False))
        self.pauseButton.clicked.connect(self.pause)
        self.pushButton.clicked.connect(self.hand_delete)

        # переменные, которые будут открывать окна

        self.b = ChoiceWindow()
        self.a = DictWindow()
        self.c = Hand_delete_window()

        # проверка наличия файлов с запрещённым контентом при настройках ручного удаления


        self.t = Timer(10, self.check_global_set(global_set))

        # представление о статусе работы программы пользователю

        if len(global_set) > 0:
            self.check_global_set(global_set)
        if self.condition == False:
            self.label_2.setText('Статус: Сервис не работает. Автоматическое удаление файлов.')
        else:
            self.label_2.setText('Статус: Сервис работает')
        self.label.setText(f'Файлов найдено: {len(global_set)}. Удалено: {count}')

        # проверка остановки потока

        if thr1.is_alive() == False and condition == True:
            thr1 = threading.Thread(target=check_files, daemon=True)
            thr1.start()

    # функция проверки наличия файлов с запрещённым контентом при настройках ручного удаления

    def check_global_set(self, ch):
        if len(global_set) > 0:
            self.b.show()



     # функция изменения окна

    def change_window(self):
        self.close()
        self.a.show()

    # функция настройки приложения (автоматическое/ручное удаление файлов)

    def limits(self, not_delete=False):
        global const
        if not_delete == False:
            const = False
            if self.condition == False:
                self.label_2.setText('Статус: Сервис не  работает.' + ' Автоматическое удаление файлов')
            else:
                self.label_2.setText('Статус: Сервис работает.' + ' Автоматическое удаление файлов')
        else:
            const = True
            if self.condition == False:
                self.label_2.setText('Статус: Сервис не работает.' + ' Удаление файлов в ручном режиме')
            else:
                self.label_2.setText('Статус: Сервис работает.' + ' Удаление файлов в ручном режиме')


    # функция паузы (останавливаем поток проверки или запускаем его)

    def pause(self):
        global thr1
        global condition
        if thr1.is_alive():

            # останавливаем поток

            self.condition = False
            condition = False
            if const == True:
                self.label_2.setText('Статус: Сервис не работает. ' + 'Удаление файлов в ручном режиме')
            elif const == False:
                self.label_2.setText('Статус: Сервис не работает. ' + 'Автоматическое удаление файлов')
            with open('log.txt', mode='a', encoding='utf-8') as f:
                f.write(f'\nСервис поставлен на паузу {datetime.now()}')
            self.pauseButton.setText('Запуск')
        else:

            # запускаем поток

            global count_of_start
            self.condition = True
            condition = True
            with open('log.txt', mode='a', encoding='utf-8') as f:
                f.write(f'\nСервис продолжил свою работу {datetime.now()}')
            if const == True:
                self.label_2.setText('Статус: Сервис работает. ' + 'Удаление файлов в ручном режиме')
            elif const == False:
                self.label_2.setText('Статус: Сервис работает. ' + 'Автоматическое удаление файлов')

            thr1 = threading.Thread(target=check_files, daemon=True)
            thr1.start()
            self.pauseButton.setText('Пауза')
            Timer(10, self.check_global_set(global_set))


    def hand_delete(self):
        self.close()
        self.c.show()
        with open('Strange_files.txt', mode='r', encoding='utf-8') as f:
            a = f.read()
            a = a.split('\n')
            self.c.plainTextEdit.setPlainText('\n'.join(a))


    # функция ухода из программы

    def exit_from_work(self):
        with open('log.txt', mode='a', encoding='utf-8') as f:
            f.write(f'\nСервис прекратил свою работу {datetime.now()}')
        sys.exit()


# функция проверки состояния приложения

def check_condition():
    if condition == False:
        return False
    return True



# окно оповещения пользователя о том, что был найден запрещённый контент в файле (вызывается при определённых настройках)

class ChoiceWindow(QMainWindow, Ui_Dialog):

    # инициализация класса и его переменных

    def __init__(self):
        super().__init__()
        global document
        self.setupUi3(self)

        # подключение кнопок к функциям

        self.pushButton.clicked.connect(lambda: self.delete_or_not(False))
        self.pushButton_2.clicked.connect(lambda: self.delete_or_not(True))
        self.label_2.setText(f'Файл D:/Тест/OK.txt содержит запрещённую информацию!')

    # функция выбора (удалять файл или нет)

    def delete_or_not(self, choose=False):
        global const
        global count2
        global document

        # если выполняется условие, то файл удаляется

        if not choose:
            with open('log.txt', mode='a', encoding='utf-8') as f:
                f.write(f'\nБыл удалён {document} в {datetime.now()}')
            os.remove(document)
            global_set.remove(document)
            count2 += 1
            document = ''
        self.close()

    # функция перехода в основное окно

    def change_window(self):
        global main_window
        main_window.show()



# класс словаря

class DictWindow(QMainWindow, Ui_MainWindow2):

    # инициализируем класс и его переменные

    def __init__(self):
        super().__init__()
        self.setupUi2(self)
        global bad_words

        # подключаем кнопки к функциям

        self.pushButton.clicked.connect(self.change_window)
        self.pushButton_2.clicked.connect(self.rebuild_dict)
        self.pushButton_3.clicked.connect(self.add_words)
        self.plainTextEdit.setPlainText('\n'.join(bad_words))


    # функция добавления слов в словарь

    def add_words(self):
        # добавляется слово, написанное в поле добавления слова
        with open('dict.txt', mode='a', encoding='utf-8') as tezt:
            global bad_words
            tezt.write(f'\n{self.textEdit.toPlainText()}')

        # словарь изменяется и сохраняется

        with open('dict.txt', mode='r', encoding='utf-8') as tegt:
            a = tegt.readlines()
            a = ' '.join(a)
            a = a.split('\n')
            a = ' '.join(a)
            a = a.split()
            a.sort()
            bad_words = []
            for i in a:
                bad_words.append(i)
            self.plainTextEdit.setPlainText('\n'.join(bad_words))


    # функция изменения словаря

    def rebuild_dict(self):
        with open('dict.txt', mode='w', encoding='utf-8') as tet:
            global bad_words
            tet.write(f'{self.plainTextEdit.toPlainText()}')

        # словарь, который был отредактирован в поле изменяется и сохраняется

        with open('dict.txt', mode='r', encoding='utf-8') as teg:
            a = teg.readlines()
            a = ' '.join(a)
            a = a.split('\n')
            a = ' '.join(a)
            a = a.split()
            a.sort()
            bad_words = []
            for i in a:
                bad_words.append(i)
            self.plainTextEdit.setPlainText('\n'.join(bad_words))


    # функция изменения окна (переход из окна словаря в основное окно)

    def change_window(self):
        global main_window
        self.close()
        main_window.show()


#Ручное удаление файлов


class Hand_delete_window(QMainWindow, Ui_MainWindow10):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global global_set
        self.pushButton.clicked.connect(self.change_window)
        self.delete_files_button.clicked.connect(self.delete)
        self.pushButton_2.clicked.connect(self.save_list)
        with open('Strange_files.txt', mode='r', encoding='utf-8') as q:
            a = q.read()
            a = a.split('\n')
            self.plainTextEdit.setPlainText('\n'.join(a))


    # Выйти в главное окно :)

    def change_window(self):
        global main_window
        self.close()
        main_window.show()

    # Удалить файлы

    def delete(self):
        with open('Strange_files.txt', mode='r', encoding='utf-8') as f:
            a = f.read()
            a = a.split('\n')
            list_of_del_files = []
            for i in a:
                list_of_del_files.append(i)
                try:
                    if os.path.exists(i):
                        os.remove(i)
                except:
                    pass
            try:
                with open('log.txt', mode='a', encoding='utf-8') as file:
                    for i in list_of_del_files:
                        file.write(i)
                        file.write(f' был удалён в {datetime.now()}')
                        file.write('\n')
            except:
                pass
        with open('Strange_files.txt', mode='w', encoding='utf-8') as f:
            f.write('')
        self.plainTextEdit.setPlainText('')

    # Сохранить список файлов для удаления

    def save_list(self):
        with open('Strange_files.txt', mode='r+', encoding='utf-8') as f:
            try:
                f.write(f'{self.plainTextEdit.toPlainText()}')
            except:
                pass



# функция поиска файлов

def check_files():
    global count
    count = 0
    global bad_list
    directories = set()
    global condition

    # проверка на тип операционной системы и добавление возможных катологов кэша

    if type_of_os == 'nt':
        for j in list_of_windows_paths:
            aboba = check_condition()
            if aboba == False:
                break
            else:
                directories.add(j)
    else:
        for k in list_of_unix_paths:
            if check_condition() == False:
                break
            else:
                directories.add(k)

    # рекурсивный поиск файлов и добавление в сет всех файлов, подходящих по расширению

    for i in list_of_paths:
        aboba = check_condition()
        if aboba == False:
            break
        path = Path(i)
        for x in path.rglob("*"):

            # проверка на расширение файлов

            if 'Strange_files.txt' not in str(x) and 'requirements.txt' not in str(x) and '.txt' in str(x) or '.pdf' in str(x) or '.csv' in str(x) or '.docx' in str(x)\
                    and 'dict.txt' not in str(x) and 'log.txt' not in str(x) and '$RECYCLE.BIN' not in str(x) and 'C:/Windows/SystemApps' not in str(x) and 'C:/Windows/WinSxS/' not in (str(x)) and 'C:/Windows/servicing/' not in str(x) and 'C:/Program Files/Windows NT/' not in str(x) and 'D:/Program Files (x86)/Steam/' not in str(x) and 'D:/Program Files/Epic Games/' not in str(x):
                if check_condition() == False:
                    break
                else:

                    # проверка на наличие катологов, которые могут хранить нужные системные файлы

                    if '$RECYCLE.BIN' not in str(x) and 'SystemApps' not in str(x) and 'WinSxS' not in (str(x)) and 'NT' not in str(x) and 'Steam' not in str(x) and 'Epic Games' not in str(x) and 'Common Files' not in str(x) and 'AppData' not in str(x) and 'SWS' not in str(x) and 'Adobe' not in str(x) and 'servicing' not in str(x) and 'Microsoft Office' not in str(x) and 'SYSTEM.SAV' not in str(x) and 'Pycharm' not in str(x) and 'PROEKT' not in str(x) and 'Razer' not in str(x) and 'Minecraft' not in str(x) and 'Intel' not in str(x) and 'Git' not in str(x) and 'System32' not in str(x) and 'SysWOW64' not in str(x) and 'HP' not in str(x):
                        a = os.path.split(str(x))
                        b = a[0].replace('\\', '/') + '/' + a[1]
                        directories.add(b)
                        count += 1
    aboba = check_condition()
    if aboba == True:


        # запуск проверки файлов

        index_of_files(directories)


# функция проверки файлов

def index_of_files(files):
    global const
    global count2
    global document
    global condition
    global warn
    global main_window
    global alt
    global thr4
    global global_set

    # проверка на то, было ли поставлено приложение на паузу

    for file in files:
        if not condition:
            break
        else:

            if os.name == 'nt' and str(file)[0] == '/':
                pass

            # проверка на наличие файла в системе

            elif os.path.exists(file):

                # проверка на расширение файла

                if '.txt' in file and 'dict.txt' not in file and 'log.txt' not in file and 'Strange_files.txt' not in file:
                    failik = ''
                    try:
                        with open(file, mode='r', encoding='utf-8') as f:
                            a = f.read()
                            b = str(f)
                            b = b.replace(f"<_io.TextIOWrapper name='{f.name}' mode='r' encoding='", '')
                            b = b.replace("'>", '')
                            a = a.encode(b)
                            a = a.decode('utf-8')
                            failik = a
                    except:
                        try:
                            with open(file, mode='r') as f:
                                a = f.read()
                                failik = a
                        except:
                            pass

                    # Greate
                    failik = failik.lower()
                    for j in bad_words:
                        if j in failik:

                            # проверка настроек сервиса

                            # автоматическое удаление
                            if const == False:
                                try:
                                    os.remove(file)
                                    with open('log.txt', mode='a', encoding='utf-8') as filik:
                                        filik.write(str(file))
                                        filik.write('\n')
                                    break
                                except:
                                    pass

                            # ручное удаление
                            else:
                                with open('Strange_files.txt', mode='a', encoding='utf-8') as q:
                                    q.write(file + '\n')
                                break

                # проверка расширения файла ОК

                elif '.csv' in file:
                    failik = ''
                    try:
                        with open(file, mode='r', encoding='utf-8') as f:
                            a = f.read()
                            b = str(f)
                            b = b.replace(f"<_io.TextIOWrapper name='{f.name}' mode='r' encoding='", '')
                            b = b.replace("'>", '')
                            a = a.encode(b)
                            a = a.decode('utf-8')
                            failik = a
                    except:
                        try:
                            with open(file, mode='r') as f:
                                a = f.read()
                                failik = a
                        except:
                            pass
                    failik = failik.lower()
                    for j in bad_words:
                        if j in failik:

                            # проверка действий в зависимости от настроек сервиса

                            # автоматическое удаление

                            if const == False:
                                try:
                                    os.remove(file)
                                    with open('log.txt', mode='a', encoding='utf-8') as filik:
                                        filik.write(str(file))
                                        filik.write('\n')
                                    break
                                except:
                                    pass
                            else:
                                with open('Strange_files.txt', mode='a', encoding='utf-8') as f:
                                    f.write(file + '\n')
                                break

                # проверка расширения файла

                elif '.pdf' in file:
                    failik = ''
                    try:
                        a = extract_text(file)
                        a = str(a)
                        a = a.lower()
                        failik = a
                    except:
                        pass
                    for j in bad_words:
                        if j in failik:

                            # проверка действий в зависимости от настроек сервиса

                            # автоматическое удаление файла

                            if const == False:
                                try:
                                    os.remove(file)
                                    with open('log.txt', mode='a', encoding='utf-8') as filik:
                                        filik.write(str(file))
                                        filik.write('\n')
                                    break
                                except:
                                    pass
                            else:
                                with open('Strange_files.txt', mode='a', encoding='utf-8') as f:
                                    f.write(file + '\n')
                                break

                # проверка расширения файла

                elif '.docx' in file:
                    failik = ''
                    try:
                        text = docx2txt.process(file)
                        text=str(text)
                        text=text.lower()
                        failik=text
                    except:
                        pass
                    for j in bad_words:
                        if j in failik:
                            # проверка действий в зависимости от настроек сервиса

                            # автоматическое удаление файла

                            if const == False:
                                try:
                                    os.remove(file)
                                    with open('log.txt', mode='a', encoding='utf-8') as filik:
                                        filik.write(str(file))
                                        filik.write('\n')
                                    break
                                except:
                                    pass
                            else:
                                with open('Strange_files.txt', mode='a', encoding='utf-8') as f:
                                    f.write(file + '\n')
                                break
    check_files()


# инициализация 2-го потока

thr1 = threading.Thread(target=check_files, daemon=False)

# запуск программы


if __name__ == '__main__':
    with open('log.txt', mode='a', encoding='utf-8') as f:
        f.write(f'\nСервис запущен в {datetime.now()}')
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    choice_window = ChoiceWindow()
    sys.exit(app.exec_())


