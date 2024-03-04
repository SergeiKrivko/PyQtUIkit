# `KitIconButton`

Квадратная кнопка с иконкой

Наследует `QPushButton`

```python
from PyQtUIkit.widgets import KitIconButton

button = KitIconButton('python')
```
![img.png](img/img_5.png)

```python
from PyQtUIkit.widgets import KitIconButton

button = KitIconButton()
button.icon = 'google'
button.size = 50
button.border = 0
button.radius = 15
```
![img.png](img/img_6.png)

### Параметры:

- `main_palette` (`KitPalette`, по умолчанию `'Main'`)
- `icon` (`str` (из встроенной коллекции иконок) или `KitIcon` (из файла))
- `size` (`int`, по умолчанию 24)
- `border` (`int`, по умолчанию 1)
- `radius` (`int`, по умолчанию 4)

[◀ На главную страницу](..%2Freadme.md)
