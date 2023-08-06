import pmg

LATEX_ESCAPE = {
    '\\': "\\backslash",
    '&': '\\&',
    '%': '\\%',
    '$': '\\$',
    '#': '\\#',
    '_': '\\_',
    '{': '\\{',
    '}': '\\}',
    '~': '\\textasciitilde',
    '^': '\\textasciicircum',
    '\n': ' \\newline '
}

def escape(s):
    return pmg.mass_replace(s, LATEX_ESCAPE)
