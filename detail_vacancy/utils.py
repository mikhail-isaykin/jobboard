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

