from math import ceil


def render_stars_html(rating, max_stars=5):
    rating = min(rating, max_stars)
    if not rating:
        return '\n'.join(['<i class="bi bi-star text-warning"></i>'] * max_stars)
    full_count = int(rating)
    html = '\n'.join(['<i class="bi bi-star-fill text-warning"></i>'] * full_count)
    if (diff := rating - full_count):
        if diff >= 0.5:
            html += '\n<i class="bi bi-star-half text-warning"></i>'
        else:
            html += '\n<i class="bi bi-star text-warning"></i>'
    if (diff := max_stars - ceil(rating)):
        html += '\n' + '\n'.join(['<i class="bi bi-star text-warning"></i>'] * diff)
    return html


def years_declension(experience_from):
    if not experience_from or experience_from == 0:
        return 'Без опыта работы'
    elif 11 <= (experience_from % 100) <= 14:
        return f'{experience_from} лет'
    elif experience_from % 10 == 1:
        return '1 год'
    elif experience_from % 10 in (2, 3, 4):
        return f'{experience_from} года'
    else:
        return f'{experience_from} лет'


def split_lines(text):
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]
