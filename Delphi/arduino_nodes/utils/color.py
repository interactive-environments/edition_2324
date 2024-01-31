def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


def rgb_to_hsl(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0
    max_color = max(r, g, b)
    min_color = min(r, g, b)
    l = (max_color + min_color) / 2
    s = 0
    h = 0

    if max_color != min_color:
        if l < 0.5:
            s = (max_color - min_color) / (max_color + min_color)
        else:
            s = (max_color - min_color) / (2.0 - max_color - min_color)
        if r == max_color:
            h = (g - b) / (max_color - min_color)
        elif g == max_color:
            h = 2.0 + (b - r) / (max_color - min_color)
        else:
            h = 4.0 + (r - g) / (max_color - min_color)
    h *= 60
    if h < 0:
        h += 360
    return h, s, l


def hsl_to_rgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    r, g, b = 0, 0, 0
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
    return int(r), int(g), int(b)


def brighten(rgb, amount):
    r, g, b = rgb
    h, s, l = rgb_to_hsl(r, g, b)
    l += amount * (1 - l)
    l = min(1, l)
    nr, ng, nb = hsl_to_rgb(h, s, l)
    nr = min(255, max(0, nr))
    ng = min(255, max(0, ng))
    nb = min(255, max(0, nb))
    return (int(nr), int(ng), int(nb))


def darken(rgb, amount):
    r, g, b = rgb
    h, s, l = rgb_to_hsl(r, g, b)
    l *= (1 - amount)
    l = max(0, l)
    nr, ng, nb = hsl_to_rgb(h, s, l)
    nr = min(255, max(0, nr))
    ng = min(255, max(0, ng))
    nb = min(255, max(0, nb))
    return (int(nr), int(ng), int(nb))


def blend_colors(color_dict):
    total_intensity = sum(color_dict.values())
    if total_intensity == 0:
        return (0, 0, 0)

    total_r, total_g, total_b = 0, 0, 0
    for hex_color, intensity in color_dict.items():
        r, g, b = hex_to_rgb(hex_color)
        total_r += r * intensity
        total_g += g * intensity
        total_b += b * intensity

    avg_r = total_r / total_intensity
    avg_g = total_g / total_intensity
    avg_b = total_b / total_intensity

    return (int(avg_r), int(avg_g), int(avg_b))
