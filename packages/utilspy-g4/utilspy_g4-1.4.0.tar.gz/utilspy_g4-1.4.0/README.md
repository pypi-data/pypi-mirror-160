![Language](https://img.shields.io/badge/English-brigthgreen)

# utilspy

![PyPI](https://img.shields.io/pypi/v/utilspy-g4)
![PyPI - License](https://img.shields.io/pypi/l/utilspy-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utilspy-g4)


Small utils for python

***

## Installation

### Package Installation from PyPi

```bash
$ pip install utilspy-g4
```

### Package Installation from Source Code

The source code is available on [GitHub](https://github.com/Genzo4/utilspy).  
Download and install the package:

```bash
$ git clone https://github.com/Genzo4/utilspy
$ cd utilspy
$ pip install -r requirements.txt
$ pip install .
```

***

## Utils

- ### addExt
Add extension to path.

Support Windows and Linux paths.

```python
from utilspy_g4 import addExt

path = '/test/test.png'
ext = '2'
newPath = addExt(path, ext)     # newPath = '/test/test.2.png'
```

- ### compareFrames
Compare 2 frames.

```python
from utilspy_g4 import compareFrames

is_equal = compareFrames('path_to_frame_1.png', 'path_to_frame_2.png')
```

- ### delExt
Del extension from path.

Support Windows and Linux paths.

```python
from utilspy_g4 import delExt

path = '/test/test.png'
newPath = delExt(path)     # newPath = '/test/test'

path = '/test/test.2.png'
newPath = delExt(path)     # newPath = '/test/test.2'

path = '/test/test.2.png'
newPath = delExt(path, 2)     # newPath = '/test/test'
```

- ### templatedRemoveFiles
Remove files by template

```python
from utilspy_g4 import templatedRemoveFiles

templatedRemoveFiles('/tmp/test_*.txt')
```

- ### getExt
Get extension from path.

Support Windows and Linux paths.

```python
from utilspy_g4 import getExt

path = '/test/test.png'
ext = getExt(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = getExt(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = getExt(path, 2)     # ext = 'jpeg'

path = '/test/test.jpeg.png'
ext = getExt(path, 0)     # ext = ''
```

***

[Changelog](https://github.com/Genzo4/utilspy/blob/main/CHANGELOG.md)

***

![Language](https://img.shields.io/badge/Русский-brigthgreen)

# utilspy

![PyPI](https://img.shields.io/pypi/v/utilspy-g4)
![PyPI - License](https://img.shields.io/pypi/l/utilspy-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utilspy-g4)

Небольшие утилитки для Python.

***

## Установка

### Установка пакета с PyPi

```bash
$ pip install utilspy-g4
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/utilspy).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/utilspy
$ cd utilspy
$ pip install -r requirements.txt
$ pip install .
```

***

## Утилиты

- ### addExt
Добавляет дополнительное расширение файла перед его последним расширением.

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import addExt

path = '/test/test.png'
ext = '2'
newPath = addExt(path, ext)     # newPath = '/test/test.2.png'
```

- ### compareFrames
Сравнение двух кадров (изображений).

```python
from utilspy_g4 import compareFrames

is_equal = compareFrames('path_to_frame_1.png', 'path_to_frame_2.png')
```

- ### delExt
Удаляет одно или несколько расширений файла

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import delExt

path = '/test/test.png'
newPath = delExt(path)     # newPath = '/test/test'

path = '/test/test.2.png'
newPath = delExt(path)     # newPath = '/test/test.2'

path = '/test/test.2.png'
newPath = delExt(path, 2)     # newPath = '/test/test'
```

- ### templatedRemoveFiles
Удаление файлов по шаблону

```python
from utilspy_g4 import templatedRemoveFiles

templatedRemoveFiles('/tmp/test_*.txt')
```

- ### getExt
Возвращает расширение файла.
Можно указать какое по счёту расширение надо вернуть.

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import getExt

path = '/test/test.png'
ext = getExt(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = getExt(path)     # ext = 'png'

path = '/test/test.jpeg.png'
ext = getExt(path, 2)     # ext = 'jpeg'

path = '/test/test.jpeg.png'
ext = getExt(path, 0)     # ext = ''
```

***

[Changelog](https://github.com/Genzo4/utilspy/blob/main/CHANGELOG.md)
