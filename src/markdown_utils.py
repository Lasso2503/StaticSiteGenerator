def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith('# '):
            return line.lstrip('# ')
    raise ValueError('No title was found')
