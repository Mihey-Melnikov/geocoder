# geocoder
###### Версия 3.14
###### Автор: Мельников Михей
###### Группа: ФТ-203
___
### Описание
Геокодер. На вход подается адрес в свободном формате.  
На выходе список всех подходящих адресов.
___
### Требования
Python версии не ниже 3.5
___
### Состав проекта
- `./data` папка с базой данных и другими файлами
- `./tests` папка с тестами
- `address.py` класс, описывающий хранение одного дома
- `data_base.py` класс, отвечающий за работу с базой данных
- `gui.py` класс, отвечающий за работу графического приложения
- `main.py` файл запуска приложения
- `preprocessor.py` модуль, запускающий преподготовку базы данных
- `request_parser.py` модуль, который парсит запросы пользователей  
- `README.md` описание  
___
### Правила работы с приложением
1. Запустите `main.py`
2. Если у вас не установлена база данных, перейдите **База данных > Сформировать базу данных**
3. Выберите файл с раширением `.osm`
4. Чтобы начать поиск, введите в поисковой строке адрес в формате _Город Улица Дом_. Без знаков препинания. Геокодер толерантен к ренистру.
5. Нажмите **Найти** или _Enter_.
6. Выберите двойным нажатием подходящий вам адрес из списка.
7. Скопируйте данные выбранного дома или всех домов.
___
### Принцип построения базы
1. Из файла формата `.xml` строятся вспомогательные таблицы `nodes` 
и `ways`. По этим таблицам формируем иоговую таблицу `geo`, по 
которой будем искать адреса.  
2. Для улучшенного поиска создается дополнительная таблица `cities`, 
со столбцами `id/city/streets`. `city` - город, `streets` - все 
улицы города в полном формате.  
3. При поиске адреса входная строка парсится по пробелам и каждое слово 
ищется по таблице. Если находим город - по оставшимся данным ищем 
полное название улицы из строки `streets`.
4. Это позволяет найти адрес при неполном вводе: `город улица`, 
`улица дом`, `город улица дом`.
___


 
