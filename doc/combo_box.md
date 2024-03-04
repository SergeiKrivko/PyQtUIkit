# `KitComboBox`

Виджет, позволяющий выбрать одно из предложенных значений

Наследует `QPushButton`

```python
from PyQtUIkit.widgets import KitComboBox

combo_box = KitComboBox('item 1', 'item 2', 'item 3', 'item 4', 'item 5')
```
![img.png](img/img_8.png)
![img_1.png](img/img_9.png)


```python
from PyQtUIkit.widgets import KitComboBox, KitComboBoxItem

combo_box = KitComboBox()
for i in range(100):
    combo_box.addItem(KitComboBoxItem(f"Item {i + 1}", i, icon='python'))
combo_box.type = 2
```
![img_2.png](img/img_10.png)
![img_3.png](img/img_11.png)

### Параметры:

- `main_palette` (`KitPalette`, по умолчанию `'Transparent'`)
- `border` (`int`, по умолчанию 0)
- `radius` (`int`, по умолчанию 4)
- `type` (1 или 2)

[◀ На главную страницу](..%2Freadme.md)
