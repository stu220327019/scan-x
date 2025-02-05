def sizeof_fmt(num, suffix='B'):
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(num) < 1024:
            return f'{num:.2f}'.rstrip('0').rstrip('.') + f' {unit}{suffix}'
        num /= 1024
    return f'{num:.1f} Y{suffix}'
