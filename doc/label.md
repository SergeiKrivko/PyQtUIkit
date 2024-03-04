# `KitLabel`

Виджет для отображения текста

Наследует `QLabel`

```python
from PyQtUIkit.widgets import KitLabel

label = KitLabel("KitLabel")
```
![img.png](img/img.png) 


```python
from PyQtUIkit.widgets import KitLabel

label = KitLabel("KitLabel")
label.main_palette = 'Main'
label.setContentsMargins(10, 5, 10, 5)
```
![img_1.png](img/img_1.png) 

### Параметры:

- `main_palette` (`KitPalette`, по умолчанию `'Transparent'`)
- `border` (`int`, по умолчанию 0)
- `radius` (`int`, по умолчанию 4)

[◀ На главную страницу](..%2Freadme.md)
