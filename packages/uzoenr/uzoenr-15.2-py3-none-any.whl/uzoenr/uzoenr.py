# Uzoenr - a web browser with CLI interface.
# Copyright (C) 2022 Uzoenr
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import requests, os.path, os, configparser
from html.parser import HTMLParser
from uzoenr.fb2 import FB2
from uzoenr.rss import rss
from uzoenr.morpho import morphology

hello = """
Uzoenr Copyright (C) 2022 Uzoenr
This program comes with ABSOLUTELY NO WARRANTY; for details open `about:warranty' page.
This is free software, and you are welcome to redistribute it
under certain conditions; open `about:copyright' page for details.

Введи h для получения списка команд.

На запрос получения адреса ничего не вводи, если хочешь открыть домашнюю страницу

"""

warranty = """
15. Disclaimer of Warranty.

THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

16. Limitation of Liability.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
"""

copy = """
uzoenr - a web browser with CLI interface.
Copyright (C) 2022 uzoenr

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

helpstring = """

* `l url` - грузить страницу (**БЕЗ** пробелов)
* `num num` (num - числа) - показать часть документа (первое число должно быть меньше второго)
* `num` - показать часть документа, начиная с <num>
* `d<url> <filename>` (url - URL; filename - имя файла) - скачать файл
* `q` - выход
* `B<bm>` - открыть закладку
* `b<bm> <url>` - добавить закладку
* `F<name> <data>` - ввод формы
* `f<url>` - отправка формы
* `H<url>` - установить домашнюю страницу
* `R<file>` - открыть FB2-книгу
* `s<data>` - искать
* `p<name> <value>` - сохранить место на странице с именем <name> и номером строки <value>
* `P<name>` - открыть строку с именем <name> на текущей странице
* `!<name>` - открыть закладку на нужной строке
* `L<url> <name>` - скачать книгу по адресу <url> в библиотеку
* `r<name>` - открыть книгу из библиотеки
* `a<file>` - сохранить страницу в файл библиотеки file
* `+<name> <url>` - подписаться на RSS-ленту url и дать ей имя <name>
* `?<feed>` - открыть ленту feed
* `o` - обновить RSS-ленты
* `O<name>` - открыть сохраненную ленту с именем
* `S<слово>` - поиск на странице с учётом морфологии русского языка
* `h` - показ этой справки
* `W<сайт> <запрос>` - поиск в интернете на сайте, указанном в секции Search под именем <сайт>, с запросом <запрос>

"""


class Engine(HTMLParser):
    """ HTML parsing engine. Use feed method to generate a text from your web page. """
    data = ""
    permit = False
    def handle_starttag(self, tag, attrs):
        self.permit = (lambda tag: tag not in ["style", 'script'] or tag in ["a", "form", "input"])(tag)
        if tag == 'a':
           try:
               url = dict(attrs)["href"]
               self.data = self.data + "<" + url + " "
           except:
               pass
        elif tag == "form":
            try:
                url = dict(attrs)["action"]
                met = dict(attrs)["method"]
                self.data = self.data + "\n[[FORM "+url+' '+met+'\n'
            except:
                pass
        elif tag == "input":
            try:
                name = dict(attrs)["name"]
                self.data = self.data + "(INPUT "+name+")\n"
            except KeyError:
                try:
                    tp = dict(attrs)['type']
                    if tp=='submit':
                        self.data = self.data + "(INPUT =OK=)\n"
                except:
                    pass
        elif tag == "img":
            try:
                name = dict(attrs)["alt"]
                self.data = self.data + "{IMG "+name+"}\n"
            except:
                self.data = self.data + "{?!IMG}\n"
    def handle_endtag(self, tag):
        if tag == "a":
            self.data = self.data + "///>"
        elif tag in ["br", "li"]:
            self.data = self.data + "\n\n"
        elif tag == "form":
            self.data = self.data + "]]\n"
    def handle_data(self, data):
        if self.permit:
            self.data = self.data + data

def readbook(fb2):
    """ Read FB2 book. """
    engine = FB2()
    with open(fb2) as f:
        engine.feed(f.read())
    return engine.finish()

val = {}
head = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36'}
# d = urllib.parse.urlencode(val).encode('utf-8')
def load(url):
    """ Load and parse the URL. Please use this function to load the web page. """
    if url == "about:warranty":
        return warranty.split("\n")
    if url == "about:copyright":
        return copy.split("\n")
    if url == "about:rule":
        return """
«Человек есть мера всех вещей существующих, что они существуют, и несуществующих, что они не существуют»
(Протагор)
""".split("\n")
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://"+url
        page = requests.get(url, headers=head).text
    except:
        cfg = configparser.ConfigParser()
        cfg.read(os.path.expanduser("~")+"/.uzoenr/bm.ini")
        enginename = cfg['Setup']['Default search']
        engine = cfg['Search'][enginename]
        page = requests.get(engine.format(url), headers=head).text
    b = Engine()
    b.feed(page)
    page = [i.strip() for i in b.data.split("\n") if len(i.strip()) > 0]
    return page
def searchweb(engine, query):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser("~")+"/.uzoenr/bm.ini")
    return load(cfg['Search'][engine].format(query))
def setupme():
    """ Generate a config for uzoenr. """
    os.mkdir(os.path.expanduser("~")+"/.uzoenr")
    os.mkdir(os.path.expanduser("~"+"/.uzoenr/library"))
    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini", "w") as f:
        cfg = configparser.ConfigParser()
        cfg["Bookmark"] = {"warranty":"about:warranty",
                           "copy":"about:copyright"}
        cfg.write(f)
def start():
    """ Entry function for uzoenr. """
    global d
    global val
    print(hello)
    if not os.path.exists(os.path.expanduser("~")+"/.uzoenr/"):
        setupme()
    elif not os.path.exists(os.path.expanduser("~")+"/.uzoenr/bm.ini"):
        with open(os.path.expanduser("~")+"/.uzoenr/bm.ini", "w") as f:
            cfg = configparser.ConfigParser()
            cfg["Bookmark"] = {"warranty":"about:warranty",
                               "copy":"about:copyright"}
            cfg.write(f)
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser("~")+"/.uzoenr/bm.ini")
    try:
        turl = input("Адрес: ")
        if len(turl) == 0:
            page = load(cfg["Setup"]["Homepage"])
        else:
            page = load(turl)
    except:
        try:
            page = load(cfg["Setup"]["Homepage"])
        except:
            print("Неизвестный адрес и не загружена домашняя страница")
            page = load("about:copyright")
    while True:
        cmd = input('? ')
        if len(cmd) == 0:
            continue
        if cmd == "q":
            break
        try:
            cmd2 = cmd.split(" ")
            print("\n".join(page[int(cmd2[0]):int(cmd2[1])+1]))
        except:
            if cmd == "h":
                print(helpstring)
            elif cmd[0] == "l":
                try:
                    page = load(cmd[1:])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "d":
                try:
                    param = cmd[1:].split(" ")
                    download(param[0], param[1])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "B":
                param = cmd[1:]
                try:
                    page = load(cfg["Bookmark"][param])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == 'b':
                param = cmd[1:].split(" ")
                try:
                    cfg["Bookmark"][param[0]] = param[1]
                except Exception as e:
                    print("ошибка: ", e)
                    continue
                print("Закладка создана")
                with open(os.path.expanduser("~")+"/.uzoenr/bm.ini","w") as f:
                    cfg.write(f)
                print("Закладки сохранены")
            elif cmd[0] == "F":
                param = cmd[1:].split(" ")
                try:
                    val[param[0]] = param[1]
                except:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "f":
                try:
                    with requests.Session() as s:
                        b = Engine()
                        p = s.post(cmd[1:], headers=val).text
                        b.feed(p)
                        page = b.data.split('\n')
                    # d = urllib.parse.urlencode(val).encode("ascii")
                    # page = load(cmd[1:])
                    # val = {}
                    # d = urllib.parse.urlencode(val).encode("ascii")
                except Exception as e:
                    try:
                        with requests.Session() as s:
                            b = Engine()
                            p = s.get(cmd[1:], headers=val).text
                            b.feed(p)
                            page = b.data.split('\n')
                    except Exception as ee:
                        print("ошибка: ", type(e), '\n', type(ee))
                        continue
            elif cmd[0] == "H":
                try:
                    cfg["Setup"] = {"Homepage":cmd[1:]}
                    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini",'w') as f:
                        cfg.write(f)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "R":
                try:
                    page = readbook(cmd[1:]).split("\n")
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "r":
                try:
                    page = readbook(os.path.expanduser("~")+"/.uzoenr/library/"+cmd[1:]).split("\n")
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "s":
                try:
                    res = [[str(i), page[i]] for i in range(len(page)) if cmd[1:] in page[i]]
                    print("\n".join(["\t".join(i) for i in res]))
                except Excepfion as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "p":
                param = cmd[1:].split(" ")
                try:
                    if "Point" not in cfg:
                        cfg["Point"] = {}
                    cfg["Point"][param[0]] = str(int(param[1]))
                    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini","w") as f:
                        cfg.write(f)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "P":
                try:
                    point = int(cfg["Point"][cmd[1:]])
                    print(point, page[point])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "!":
                try:
                    point = int(cfg["Point"][cmd[1:]])
                    url = cfg["Bookmark"][cmd[1:]]
                    page = load(url)
                    print(point, "\n", "\n".join(page[point:]))
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == 'L':
                try:
                    param = cmd[1:].split(' ')
                    download(param[0], os.path.expanduser("~")+"/.uzoenr/library/"+param[1])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "a":
                try:
                    with open(os.path.expanduser("~")+"/.uzoenr/library/"+cmd[1:], "w") as f:
                        f.write("\n".join(page))
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "+":
                try:
                    param = cmd[1:].split(" ")
                    if "Feed" not in cfg:
                        cfg["Feed"] = {}
                    cfg["Feed"][param[0]] = param[1]
                    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini","w") as f:
                        cfg.write(f)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "?":
                try:
                    url = cfg["Feed"][cmd[1:]]
                    page = loadfeed(url)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "o":
                try:
                    for feedname in cfg["Feed"]:
                        download(cfg["Feed"][feedname], "/../"+feedname)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "O":
                try:
                    parser = rss()
                    with open(os.path.expanduser("~")+"/.uzoenr/"+cmd[1:]) as f:
                        parser.feed(f.read())
                    page = [i for i in parser.finish().split("\n") if len(i.strip()) > 0]
                except Exception as e:
                    print("ошибка: ",e)
                    continue
            elif cmd[0] == 'S':
                try:
                    g = morphology(cmd[1:])
                    for word in g:
                       res = [[str(i), page[i]] for i in range(len(page)) if word in page[i].lower()]
                       print(word)
                       print("\n".join(["\t".join(i) for i in res]))
                except Exception as e:
                    print("ошибка: ", type(e), " - ", e)
                    continue
            elif cmd[0] == 'W':
                try:
                    g = cmd[1:].split(' ')
                    g = [g[0], ' '.join(g[1:])]
                    page = searchweb(g[0], g[1])
                except Exception as e:
                    print("ошибка: ", type(e), " - ", e)
                    continue
            elif cmd.isdigit():
                try:
                    print("\n".join(page[int(cmd):]))
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            else:
                print("Неизвестная команда")
                continue
def download(url, fname):
    """ Download and save the file from the web. """
    with open(os.path.expanduser("~")+"/.uzoenr/library/"+fname, "wb") as fp:
        fp.write(requests.get(url, headers=head).content)
    print("Файл загружен")
def loadfeed(url):
    """ Load and parse the RSS feed. """
    parser = rss()
    parser.feed(requests.get(url, headers=head).text)
    return [i.strip() for i in parser.finish().split("\n") if len(i.strip()) > 0]


if __name__ == "__main__":
    start()
