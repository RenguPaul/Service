import os
import shutil
from pathlib import Path
ok = True
list_of_paths_w = ['A:/', 'B:/', 'C:/', 'D:/', 'E:/', 'F:/', 'G:/', 'H:/', 'I:/', 'J:/', 'K:/', 'L:/', 'M:/', 'N:/',
                 'O:/', 'P/:', 'Q:/', 'R:/', 'S:/', 'T:/', 'U:/', 'V:/', 'W:/', 'X:/', 'Y:/', 'Z:/']
list_of_paths_l = '/'
flag = True
encoding = [
'utf-8',
'cp500',
'utf-16',
'GBK',
'windows-1251',
'ASCII',
'US-ASCII',
'Big5'
]
def index_files(files):
    global encoding
    a = set()
    try:
        for file in files:
            if not condition:
                break
            else:
                if '.txt' in file:
                    with open(file, mode='r') as f:
                        a = a.decode('cp1251')
                        pr
                        a = f.read()
                        a = a.lower()
                        for i in dict_of_bad_words:
                            if i in a:
                                os.remove(file)
                                break
                if '.csv' in file:

    except PermissionError:
        pass
    except:
        pass
def check_files():
    a = set()
    try:
        count = 0
        if os.name == 'nt':
            for i in list_of_paths_w:
                if flag == False:
                    break
                print("OK")
                p = Path(i)
                for x in p.rglob('*'):
                    if '$RECYCLE.BIN' in str(x) or '\Windows' in str(x) not in str(x) or 'dict.txt' in str(x) \
                            or 'log.txt' in str(x):
                        pass
                    elif '.txt' in str(x) or '.csv' in str(x) or '.docx' in str(x) or '.pdf' in str(x):
                        count += 1
                        a.add(str(x).replace('\\', '/'))
                    if flag == False:
                        break
        elif os.name == 'posix':
            p = Path("/")
            for x in p.rglob('*'):
                if  'dict.txt' in str(x) or 'log.txt' in str(x):
                    pass
                elif '.txt' in str(x) or '.csv' in str(x) or '.docx' in str(x) or '.pdf' in str(x):
                    count += 1
                    a.add(str(x).replace('\\', '/'))
                if flag == False:
                    break

            print(count, a)
    except PermissionError:
        pass
    except:
        pass
    index_files(a)

check_files()
