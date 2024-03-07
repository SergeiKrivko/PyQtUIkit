# `KitSpinner`

Наследует `QWidget`

```python
from PyQtUIkit.widgets import KitSpinner

spinner = KitSpinner()
```
![img_20.png](img%2Fimg_20.png)
![img.png](img/img_21.png)

```python
from PyQtUIkit.widgets import KitSpinner

spinner = KitSpinner()
spinner.main_palette = 'Main'
spinner.setContentsMargins(10, 5, 10, 5)
```
![img_1.png](img/img_22.png)
![img_2.png](img/img_23.png)

### Параметры:

- `main_palette` (`KitPalette`, по умолчанию `'Transparent'`)
- `size` (`int`, по умолчанию 30)
- `width` (`int`, по умолчанию 4)
- `speed` (Время одного оборота в миллисекундах: `int`, по умолчанию 1000)

[◀ На главную страницу](..%2Freadme.md)
