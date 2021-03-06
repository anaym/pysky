# Приложение-визуализатор небесной сферы
Приложение разработано в качестве лабораторной работы по курсу "Языки сценариев" ИМКН УрФУ, 2016-2017 (ФИИТ, 2 курс)

### Автор:
Антон Толстов, [aka Anaym](http://atolstov.com), education@atolstov.com

### Системные требования (минимальные и выше):
+   Python 3.5.2
+   PyQt 5            (pip install pyqt5) - библиотека GUI
+   JDCal             (pip install jdcal) - библиотека работы с юлианским календарём

## ВНИМАНИЕ
Для ввода значений в меню (координаты, время, ускорение, ...):

1. Поставьте курсор в соответствующее поле
2. Перейдите в режим редактирования нажав Enter. Поле должно стать серым
3. Введите новое значение
4. Для подтверждения нажмите Enter еще раз. Поле станет белым, и если значение корректно - оно изменится

### Декомпозиция:
+ ___geometry___ - модуль с необходимыми геометрическими примитивами, для описания небесной сферы
    + _nvector.py_ - описывает произвольный immutable n-мерный вектор
    + _equatorial.py_ - описывает вектор в экваториальной системе координат, а так же его преобр-е в горизонтальную
    + _horizontal.py_ - описывает вектор в горизонтальной системе координат, а так же его преобр-е в декартовую
    + _vector.py_ - описывает вектор в декартовой системе координат
    + _angle_helpers.py_ - описывает вспомогательные функции и декораторы для работы с углами
    + _sky_math.py_ - описывает математику необходимую для небесной сферы
+ ___graphics___ - модуль для работы с графикой
    + __autogui__ - модуль-обертка над pyqt5 для более удобного преобразования полей классов в виджеты
    + __renderer__ - модуль описывающий рендеринг небесной сферы
        + _camera.py_ - описывает камеру (угол взгляда)
        + _watcher.py_ - описывает наблюдателя (координаты, время)
        + _settings.py_ - настройки рендеринга
        + _projector.py_ - проецирование небесной сферы на плоскость на основе настроек наблюдателя
        + _renderer.py_ - рендеринг небесной сферы на плоскость на основе настроек наблюдателя
    + __sky_viewers__ - модуль описывающий оконный вариант программы
+ ___stars___ - модуль работы со звездами и небесной сферой
    + _stars_ - база данных со звёздами северного полушария
    + _star.py_ - описывает звезду/небесное тело
    + _skydatebase.py_ - база данных звезд, с фильтром по созвездиям 
    + _parser.py_ - парсер текстовой базы звезд
    + _star_time.py_ - описывает звездное время
+ ___tests___ - модуль с unit-тестами
+ ___program.py___ - основной файл для запуска
+ ___requrements.py___ - модуль работы с зависимостями
+ ___sound.py___ - небольшой аудиоплеер
+ ___task.py___ - парсер входных аргументов
+ ____utility.py___ - общие вспомогательные функции

### Пример запуска
    python program.py
    python program.py -c
    python program.py -c -d "29.11.16 9:31"
    python program.py -c -d "30.11.16 18:20:41" --constellations Andromeda Camelopardalis
    python sound.py "resources\Still Alive.mp3"
    
### Управление
    WASDQE - вращение камеры
    F - переключение полноэкранного режима
    M - переключение видимости меню
    N - переключение видимости фильтра
    I - сохранение текущего изображения
    R - перерендерить
    Space - переключение паузы
    Esc - выход
    Мышь с зажатой левой клавишей - вращение камеры (лево-право - вращение в горизонтальной плоскости, вверх-вниз - в вертикальной)
    Двойной клик по названию созвездия - ориентация на созвездие
    Двойной клик по звезде - ориентация на звезду
    Наведение курсора на звезду - Созвездие, Имя звезды, Спектральный класс, Магнитуда в виде всплывающей подсказки


### Условные обозначения
    Синяя [линия] окружность - [направление на] северный полюс
    Оранжевая [линия] окружность - [направление на] южный полюс
    Зеленая [линия] окружность - [направление на] взгляд под углом 90` вверх
    Голубая окружность - вектор взгляда
    Фиолетовая окружность - вектор наблюдателя

### Краткое описание принципа работы
1. Преобразование координат для отрисовки
    + __Входные данные__: Координаты звезд в экваториальной системе координат
    + _Поворачиваем небесную сферу с учетом текущего времени и координат_: Экваториальные координаты
    + _Преобразуем в декартову систему координат_: Декартовы координаты
    + _Применяем проецирование для отрисовки на экране_: Спроецированные координаты
    + _Применяем искажение рыбьего глаза для улучшения наглядности_: Экранные координаты
2. Построение визуализации
    + Изображение рендериться в классе Renderer
    + Sky - автоперерисовывающаяся со временем небесная сфера
    + ControllableSky : Sky - визуализация с меню управления
    + FilterableSky : ControllableSky - фильтрация по магнитуде/созвездию
    + KeyControllableSky : FilterableSky - визуализауия с управлением с клавиатуры
    + MouseControllableSky : KeyControllableSky - визуализация, поддерживающая управление мышью
    + NamedSky : MouseControllableSky - подсказки о звездах

### Примеры вывода:

![Sky](examples/1.jpg?raw=true "Sky")
![Andromeda](examples/2.jpg?raw=true "Andromeda")
