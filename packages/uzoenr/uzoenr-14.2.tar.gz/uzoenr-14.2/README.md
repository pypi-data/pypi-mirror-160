# uzoenr

uzoenr - уникальный текстовый браузер:
он умеет читать FB2-книги и подписываться на RSS-ленты.

## Uzoenr 14

Добавлена возможность использования произвольных поисковых машин, их перечисление идет в секции Search; вместо поискового запроса надо ставить вот такие фигурные скобки: `{}` .
Также добавлена возможность задания адреса без задания протокола HTTP/HTTPS.

## Uzoenr 12

Появилась функция поиска с учётом морфологии русского языка.
Также добавлена возможность интерактивного просмотра списка команд.

### Uzoenr 12.1

Исправление ошибок.

## uzoenr-11.0.1

Исправлено несколько критичных ошибок.

## Лицензия (GNU GPL 3+)

````
Uzoenr - text web browser
Copyright (C) 2022 uzoenr
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
````

## Использование
````
uzoenr
python3 -m uzoenr.uzoenr
````

````
#Использование в IDLE/GEANY
from uzoenr.uzoenr import start
start()
````

### Встраивание

````
from uzoenr.uzoenr import Engine
...
parser = Engine()
parser.feed(data)
return parser.data()
````

## Команды:

**ПРЕДУПРЕЖДЕНИЕ: БЕЗ JAVASCRIPT ФОРМЫ МОГУТ НЕ РАБОТАТЬ!**

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
