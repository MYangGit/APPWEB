from TyPlotOnline.objects.mw_global_setting import CGlobalSetting

def get_font(current_font, font_family = None, font_size = None, font_italic = None, font_weight = None):
    font_family = current_font[0] if font_family == None else font_family
    font_size = current_font[1] if font_size == None else font_size
    font_italic = current_font[2] if font_italic == None else font_italic
    font_weight = current_font[3] if font_weight == None else font_weight

    font = (font_family, font_size, font_italic, font_weight)

    return font
