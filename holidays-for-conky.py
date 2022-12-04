#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# test

import locale
import warnings
import feedparser
import time
import pathlib

# задаем локаль
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
# выключаем предупреждения
warnings.filterwarnings("ignore")
# сегодняшний день
localtime = time.localtime(time.time())
curtime = localtime[2]
# путь к скрипту
path = pathlib.Path(__file__).parent.resolve()

# получаем данные
'''news_feeds = feedparser.parse(
 	"http://www.calend.ru/img/export/today-holidays.rss")'''
news_feeds = feedparser.parse(f"{path}/today-holidays.rss")

# определяем начальное форматирование строк
start_pos = "${voffset -8}${alignc}"
# записываем в файл начальную настройку
with open("/tmp/holidays.txt", "w") as file:
    file.write("${color ffff00}${font Arial Narrow:size=13}")

def main():
	# начало счетчика
    t_end = 0
    # читаем все фиды с конца
    for entry in news_feeds.entries[::-1]:
    	# выбираем заголовки
        title = entry['title']
        # выбираем категорию праздника
        term = entry.tags[0]['term']
        # получаем дату праздника
        cur_dat = int(entry['title'][:15].split()[0])
        # проверяем соответствие даты и категории
        # как пример: "Православные праздники" или "Международные праздники"
        if (cur_dat == curtime
			and term == "Праздники России"
        	or term == "Праздники славян"
        	or term == "Профессиональные праздники"
        	# удаляем из списка не российские
        	and term != "в России"):
            t_end += 1
            # ограничиваем вывод пятью записями
            # при необходимости полного вывода 
            # или меняем 5 на int(len(entry))
            if t_end == 5:
                break
            # отрезаем дату в заголовке
            titles = f"{title[17:]}"
            # выводим контроль
            print(f"{titles}")
            # пишем полученное в файл
            output_file = open("/tmp/holidays.txt", "a")
            output_file.write(start_pos + f"{titles}\n")

if __name__ == "__main__":
    main()
