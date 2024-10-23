### Урок 1

#### Задание 1

Установить Python и IDE для работы

#### Задание 2

- Работаем в терминале
- Создайте каталог `first_project` для проекта и разверните виртуальное окружение Python в папке `venv` внутри каталога
- Создайте каталог `second_project` для проекта и разверните виртуальное окружение Python в папке `virtual` внутри каталога
- Создайте каталог `project_new` для проекта и разверните виртуальное окружение Python в папке `venv_new` внутри каталога
- Для каждого проекта последовательно активируйте и деактивируйте виртуальное окружение.

Решение:

```bash
mkdir first_project;
cd first_project;
python -m venv venv;

## Activation venv
# для Linux и MacOS
source venv/bin/activate;

# Activation venv для Windows
# venv\Scripts\activate

## Deactivation venv
deactivate;

cd ..

mkdir second_project;
cd second_project;
python -m venv virtual;

## Activation venv
# для Linux и MacOS
source virtual/bin/activate;

# Activation venv для Windows
# virtual\Scripts\activate

## Deactivation venv
deactivate;

cd ..

mkdir project_new;
cd project_new;
python -m venv venv_new;

## Activation venv для Linux и MacOS
source venv_new/bin/activate;

# Activation venv для Windows
# venv_new\Scripts\activate;

## Deactivation venv
deactivate;

cd ..

```

#### Задание 3

- Активируем виртуальное окружение первого из трех созданных проектов и устанавливаем в него модуль `requests`, используя `pip`.
- Проверяем установку выводом списка модулей в консоль.
- Сохраняем список в файл, проверяем результат и выходим из окружения.
- Активируем виртуальное окружение второго из трех созданных проектов и устанавливаем в него модуль `flask`, используя `pip`.
- Проверяем установку выводом списка модулей в консоль.
- Сохраняем список файл и выходим из окружения.
- Активируем третье виртуальное окружение.
- Устанавливаем в него модули из первого и второго проекта, используя ранее сохраненные в файлы списки модулей.
- Проверяем установку выводом списка модулей в консоль.

```bash
cd first_project;

## Activation venv для Linux и MacOS
source venv/bin/activate;

## Activation venv  для Windows
# venv\Scripts\activate;

pip install requests;
pip freeze;
pip freeze > requirements.txt;
deactivate;
cd ..

===========================
cd second_project;

## Activation venv
# для Linux и MacOS
source virtual/bin/activate;

# Activation venv для Windows
# virtual\Scripts\activate

pip install flask;
pip freeze;
pip freeze > requirements.txt;
deactivate;
cd ..

============================
cd project_new;

## Activation venv для Linux и MacOS
source venv_new/bin/activate;

# Activation venv для Windows
# venv_new\Scripts\activate;

pip install -r ../first_project/requirements.txt;
pip install -r ../second_project/requirements.txt;

pip freeze;
pip freeze > requirements.txt;
deactivate;
cd ..

```

#### Задание 4

- Работа в консоли в режиме интерпретатора Python.
- Решите квадратное уравнение 5х2-10х-400 = 0, последовательно сохраняя переменные a, b, c, d, x1 и x2.
- Попробуйте решить уравнение с другими значениями a, b, c.

```python
python
Python 3.12.6 (main, Sep  9 2024, 00:00:00) [GCC 14.2.1 20240801 (Red Hat 14.2.1-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> a = 5
>>> b = -10
>>> c = -400
>>> d = b**2-4*a*c
>>> x1 = (-b+d**0.5)/(2*a)
>>> x2 = (-b-d**0.5)/(2*a)
>>> x1
10.0
>>> x2
-8.0
>>> exit()


```

#### Задание 5

- Работа в консоли в режиме интерпретатора Python.
- Посчитайте сумму четных элементов от единицы до n, исключая кратные e.
- Используйте while и if.
- Попробуйте разные значения e и n.

```bash
python
Python 3.12.6 (main, Sep  9 2024, 00:00:00) [GCC 14.2.1 20240801 (Red Hat 14.2.1-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> n = 101
>>> e = 3
>>> s = 0
>>> count = 0
>>> while count < n:
...     count +=1
...     if count % e == 0:
...         continue
...     if count % 2 == 0:
...         s += count
... 
... 
>>> s
1734

```
