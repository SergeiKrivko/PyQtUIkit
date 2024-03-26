from PyQtUIkit.themes.theme import KitTheme, KitPalette

basic_theme = KitTheme({
    'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#222222'),

    'Main': KitPalette('#FFFFFF', '#DFE1E5', '#CFDEFC', '#222222'),
    'Bg': KitPalette('#ECF5F9', '#CBCDCF', '#5283C9', '#222222'),
    'Menu': KitPalette('#C4CBCF', '#9DA3A6', '#3B81F0', '#222222'),
    'Border': KitPalette('#BFC0C2', '#A6A7A8', '#52AFDE', '#222222'),
    'Success': KitPalette('#B3D635', '#D0FA3E', '#41D431', '#222222'),
    'SuccessText': KitPalette('#00FFFFFF', text='#2A8018'),
    'Warning': KitPalette('#E3C920', '#CFB71D', '#C7891E', '#222222'),
    'WarningText': KitPalette('#00FFFFFF', text='#AB8618'),
    'Danger': KitPalette('#E33838', '#FC3E3E', '#FC1414', '#222222'),
    'DangerText': KitPalette('#00FFFFFF', text='#B51702'),

    'Font': 'Roboto',
    'FontMono': 'Roboto Mono',
    'FontSizeSmall': 9,
    'FontSizeMedium': 10,
    'FontSizeBig': 14,
    'FontSizeMono': 10,
}, is_dark=False)

builtin_themes = {
    'Light': basic_theme,
    'Dark': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#F0F0F0'),
        'Main': KitPalette('#2B2D30', '#3E4145', '#2E436E', '#F0F0F0'),
        'Bg': KitPalette('#141517', '#222345', '#323466', '#F0F0F0'),
        'Menu': KitPalette('#1F2024', '#4E5157', '#3573F0', '#F0F0F0'),
        'Border': KitPalette('#474747', '#595959', '#2D63CC', '#F0F0F0'),
        'Success': KitPalette('#214514', '#295419', '#397523', '#F0F0F0'),
        'SuccessText': KitPalette('#00FFFFFF', text='#2A8018'),
        'Warning': KitPalette('#B8901A', '#A17E17', '#8C6E14', '#F0F0F0'),
        'WarningText': KitPalette('#00FFFFFF', text='#D9AA1F'),
        'Danger': KitPalette('#690B0B', '#7A0D0D', '#B31414', '#F0F0F0'),
        'DangerText': KitPalette('#00FFFFFF', text='#B51702'),
    },
        basic_theme,
        is_dark=True),

    'Orange': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#000000'),
        'Main': KitPalette('#F2D7AD', '#F2CE9C', '#FFCB99', '#000000'),
        'Bg': KitPalette('#F0F0F0', '#E3D2C8', '#E3C3AE', '#000000'),
        'Menu': KitPalette('#F28B41', '#E3823D', '#E0651B', '#000000'),
        'Border': KitPalette('#F27F10', '#FF960E', '#F05B1A', '#000000'),
    },
        basic_theme,
        is_dark=False),

    'Winter': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#191C42'),
        'Main': KitPalette('#B4D2FA', '#93BBFA', '#4BA7FA', '#191C42'),
        'Bg': KitPalette('#EEEEEE', '#D1D1D1', '#7798C7', '#191C42'),
        'Menu': KitPalette('#7798C7', '#5787C7', '#2971C7', '#191C42'),
        'Border': KitPalette('#191C42', '#142842', '#0C3D9C', '#191C42'),
    },
        basic_theme,
        is_dark=False),

}
