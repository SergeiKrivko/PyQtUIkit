# `KitToggle`

Виджет-переключатель

Наследует `QWidget`

```python
from PyQtUIkit.widgets import KitToggle

toggle = KitToggle()
```
![img.png](img/img_16.png)
![img_1.png](img/img_17.png)

```python
from PyQtUIkit.widgets import KitToggle

toggle = KitToggle()
toggle.mode = 'm'
```
![img_1.png](img/img_14.png)
![img.png](img/img_15.png)

```python
from PyQtUIkit.widgets import KitToggle

toggle = KitToggle()
toggle.mode = 'l'
```
![img_2.png](img/img_18.png)
![img_3.png](img/img_19.png)

### Параметры:

- `main_palette` (`KitPalette`, по умолчанию `'Menu'`)
- `rail_palette` (`KitPalette`, по умолчанию `'Main'`)
- `mode` (`l`, `m` или`s`. По умолчанию `l`)

### Сигналы:

- `stateChanged`

### Методы:

- `state` Возвращает True, если элемент активен, иначе False
- `setState` устанавливает значение

[◀ На главную страницу](..%2Freadme.md)
