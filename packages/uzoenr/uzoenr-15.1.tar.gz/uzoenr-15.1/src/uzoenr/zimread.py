from uzoenr.uzoenr import Engine
from libzim.reader import Archive
from libzim.search import Query, Searcher
from libzim.suggestion import SuggestionSearcher
from sys import argv, exit
import os.path
def start(zf):
    zim = Archive(zf)
    # eng = Engine()
    # entry = zim.get_entry_by_path(zim.main_entry.get_item().path)
    # eng.feed(bytes(entry.get_item().content).decode("UTF-8"))
    return zim
# print(eng.data)
def getHomepage(z):
    eng = Engine()
    entry = z.get_entry_by_path(z.main_entry.get_item().path)
    eng.feed(bytes(entry.get_item().content).decode("UTF-8"))
    return [i.strip() for i in eng.data.split('\n') if len(i.strip()) > 0]

def load(z, p):
    eng = Engine()
    entry = z.get_entry_by_path(p)
    eng.feed(bytes(entry.get_item().content).decode("UTF-8"))
    return [i.strip() for i in eng.data.split('\n') if len(i.strip()) > 0]


def cmdline(zf):
    zw = start(zf)
    page = getHomepage(zw)
    while True:
        cmd = input('? ')
        try:
            com = [int(i) for i in cmd]
            if len(com) == 2:
                print('\n'.join(page[com[0]:com[1]+1]))
            elif len(com) == 1:
                print('\n'.join(page[com[0]:]))
        except:
            if cmd == 'q':
                exit(0)
            elif cmd[0] == 'l':
                try:
                    page = load(zw, cmd[1:])
                except Exception as e:
                    print("ошибка: ", type(e), ' - ', e)
            elif cmd == 'a':
                try:
                    with open(os.path.expanduser("~")+"/.uzoenr/library/zim/"+cmd[1:], 'w') as f:
                        f.write('\n'.join(page))
                except Exception as e:
                    print("ошибка: ", type(e), ' - ', e)
                else:
                    print("ошибка: неизвестная команда")

def main():
    cmdline(argv[1])

if __name__ == "__main__":
    main()
