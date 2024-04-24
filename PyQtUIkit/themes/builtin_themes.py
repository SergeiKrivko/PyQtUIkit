from PyQtUIkit.core.font import KitFont
from PyQtUIkit.themes.theme import KitTheme, KitPalette

basic_theme = KitTheme({
    'Transparent': KitPalette('#00000000', '#30000000', '#60000000', '#222222'),

    'Main': KitPalette('#FFFFFF', '#DFE1E5', '#CFDEFC', '#222222'),
    'Bg': KitPalette('#ECF5F9', '#CBCDCF', '#5283C9', '#222222'),
    'Menu': KitPalette('#C4CBCF', '#9DA3A6', '#3B81F0', '#222222'),
    'Border': KitPalette('#BFC0C2', '#A6A7A8', '#52AFDE', '#222222'),
    'Success': KitPalette('#B3D635', '#D0FA3E', '#41D431', '#222222', '#2A8018'),
    'Warning': KitPalette('#E3C920', '#CFB71D', '#C7891E', '#222222', '#AB8618'),
    'Danger': KitPalette('#E33838', '#FC3E3E', '#FC1414', '#222222', '#B51702'),
}, {
    'default': KitFont('Roboto', 9, 10, 14, 20),
    'italic': KitFont('Roboto', 9, 10, 14, 20, italic=True),
    'bold': KitFont('Roboto', 9, 10, 14, 20, bold=True),
    'strike': KitFont('Roboto', 9, 10, 14, 20, strike=True),
    'mono': KitFont('Roboto Mono', 9, 10, 14, 20)
},
    is_dark=False)

builtin_themes = {
    'Light': basic_theme,
    'Dark': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#F0F0F0'),
        'Main': KitPalette('#2B2D30', '#3E4145', '#2E436E', '#F0F0F0'),
        'Bg': KitPalette('#141517', '#222345', '#323466', '#F0F0F0'),
        'Menu': KitPalette('#1F2024', '#4E5157', '#3573F0', '#F0F0F0'),
        'Border': KitPalette('#474747', '#595959', '#2D63CC', '#F0F0F0'),
        'Success': KitPalette('#214514', '#295419', '#397523', '#F0F0F0', '#2A8018'),
        'Warning': KitPalette('#B8901A', '#A17E17', '#8C6E14', '#F0F0F0', '#D9AA1F'),
        'Danger': KitPalette('#690B0B', '#7A0D0D', '#B31414', '#F0F0F0', '#FA2A08'),
    },
        inherit=basic_theme,
        is_dark=True),

    'Orange': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#000000'),
        'Main': KitPalette('#F2D7AD', '#F2CE9C', '#FFCB99', '#000000'),
        'Bg': KitPalette('#F0F0F0', '#E3D2C8', '#E3C3AE', '#000000'),
        'Menu': KitPalette('#F28B41', '#E3823D', '#E0651B', '#000000'),
        'Border': KitPalette('#F27F10', '#FF960E', '#F05B1A', '#000000'),
    },
        inherit=basic_theme,
        is_dark=False),

    'Winter': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#191C42'),
        'Main': KitPalette('#B4D2FA', '#93BBFA', '#4BA7FA', '#191C42'),
        'Bg': KitPalette('#EEEEEE', '#D1D1D1', '#7798C7', '#191C42'),
        'Menu': KitPalette('#7798C7', '#5787C7', '#2971C7', '#191C42'),
        'Border': KitPalette('#191C42', '#142842', '#0C3D9C', '#191C42'),
    },
        inherit=basic_theme,
        is_dark=False),

    'Autumn': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#FFD29E'),
        'Main': KitPalette('#481E14', '#5E271A', '#8A3926', '#FFD29E'),
        'Bg': KitPalette('#0C0C0C', '#171717', '#3B1810', '#FFD29E'),
        'Menu': KitPalette('#9B3922', '#C2472B', '#481E14', '#FFD29E'),
        'Border': KitPalette('#F2613F', '#DE593A', '#C44F33', '#FFD29E'),
        'Success': KitPalette('#214514', '#295419', '#397523', '#F0F0F0', '#2A8018'),
        'Warning': KitPalette('#B8901A', '#A17E17', '#8C6E14', '#F0F0F0', '#D9AA1F'),
        'Danger': KitPalette('#690B0B', '#7A0D0D', '#B31414', '#F0F0F0', '#FA2A08'),
    },
        inherit=basic_theme,
        is_dark=True),

    'Space': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#F0F0F0'),
        'Main': KitPalette('#1B1A55', '#242373', '#2E2C91', '#F0F0F0'),
        'Bg': KitPalette('#070F2B', '#0B1845', '#0F2261', '#F0F0F0'),
        'Menu': KitPalette('#535C91', '#454C78', '#363C5E', '#F0F0F0'),
        'Border': KitPalette('#9290C3', '#7C7AA6', '#5451A6', '#F0F0F0'),
        'Success': KitPalette('#214514', '#295419', '#397523', '#F0F0F0', '#2A8018'),
        'Warning': KitPalette('#B8901A', '#A17E17', '#8C6E14', '#F0F0F0', '#D9AA1F'),
        'Danger': KitPalette('#690B0B', '#7A0D0D', '#B31414', '#F0F0F0', '#FA2A08'),
    },
        inherit=basic_theme,
        is_dark=True),

    'Fresh': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#F0F0F0'),
        'Main': KitPalette('#393E46', '#494F59', '#6C7585', '#F0F0F0'),
        'Bg': KitPalette('#222831', '#323A47', '#2A2B47', '#F0F0F0'),
        'Menu': KitPalette('#00ADB5', '#008D94', '#0370A1', '#1D1B38'),
        'Border': KitPalette('#787878', '#949494', '#6A7394', '#F0F0F0'),
        'Success': KitPalette('#214514', '#295419', '#397523', '#F0F0F0', '#2A8018'),
        'Warning': KitPalette('#B8901A', '#A17E17', '#8C6E14', '#F0F0F0', '#D9AA1F'),
        'Danger': KitPalette('#690B0B', '#7A0D0D', '#B31414', '#F0F0F0', '#FA2A08'),
    },
        inherit=basic_theme,
        is_dark=True),

    'Rain': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#000000'),
        'Main': KitPalette('#DCD6F7', '#B9B1F5', '#D69CF5', '#0E0E24'),
        'Bg': KitPalette('#F4EEFF', '#E3D2C8', '#E3C3AE', '#0E0E24'),
        'Menu': KitPalette('#424874', '#65539C', '#9756A3', '#C0C0FF'),
        'Border': KitPalette('#A6B1E1', '#959EC9', '#C23EF0', '#0E0E24'),
    },
        inherit=basic_theme,
        is_dark=False),

    'Coffee': KitTheme({
        'Transparent': KitPalette('#00FFFFFF', '#30FFFFFF', '#60FFFFFF', '#000000'),
        'Main': KitPalette('#E5B299', '#E5A07B', '#E57D61', '#140F0D'),
        'Bg': KitPalette('#B4846C', '#E3D2C8', '#E3C3AE', '#140F0D'),
        'Menu': KitPalette('#FCDEC0', '#FCB99E', '#FCA576', '#42302A'),
        'Border': KitPalette('#7D5A50', '#61463E', '#612A1E', '#140F0D'),
    },
        inherit=basic_theme,
        is_dark=False),
}
