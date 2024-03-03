from PyQtUIkit.themes.theme import KitTheme, KitPalette

basic_theme = KitTheme({
    'Transparent': KitPalette('#00000000', '#00000030', '#00000060', '#222222'),

    'Main': KitPalette('#FFFFFF', '#DFE1E5', '#CFDEFC', '#222222'),
    'Bg': KitPalette('#ECF5F9', '#CBCDCF', '#5283C9', '#222222'),
    'Menu': KitPalette('#F7F8FA', '#DFE1E5', '#3573F0', '#222222'),
    'Border': KitPalette('#BFC0C2', '#A6A7A8', '#52AFDE', '#222222'),
}, is_dark=False)

builtin_themes = {
    'Light': basic_theme,
    'Dark': KitTheme({
        'Transparent': KitPalette('#00000000', '#00000030', '#00000060', '#F0F0F0'),
        'Main': KitPalette('#2B2D30', '#3E4145', '#2E436E', '#F0F0F0'),
        'Bg': KitPalette('#141517', '#222345', '#323466', '#F0F0F0'),
        'Menu': KitPalette('#1F2024', '#4E5157', '#3573F0', '#F0F0F0'),
        'Border': KitPalette('#474747', '#595959', '#2D63CC', '#F0F0F0'),
    },
        basic_theme,
        is_dark=True),

    'Orange': KitTheme({
        'Transparent': KitPalette('#00000000', '#00000030', '#00000060', '#000000'),
        'Main': KitPalette('#F2D7AD', '#F2CE9C', '#FFCB99', '#000000'),
        'Bg': KitPalette('#F0F0F0', '#E3D2C8', '#E3C3AE', '#000000'),
        'Menu': KitPalette('#F28B41', '#E3823D', '#E0651B', '#000000'),
        'Border': KitPalette('#F27F10', '#FF960E', '#F05B1A', '#000000'),
    },
        basic_theme,
        is_dark=False),

    'Winter': KitTheme({
        'Transparent': KitPalette('#00000000', '#00000030', '#00000060', '#191C42'),
        'Main': KitPalette('#B4D2FA', '#93BBFA', '#4BA7FA', '#191C42'),
        'Bg': KitPalette('#EEEEEE', '#D1D1D1', '#7798C7', '#191C42'),
        'Menu': KitPalette('#7798C7', '#5787C7', '#2971C7', '#191C42'),
        'Border': KitPalette('#191C42', '#142842', '#0C3D9C', '#191C42'),
    },
        basic_theme,
        is_dark=False),

}
