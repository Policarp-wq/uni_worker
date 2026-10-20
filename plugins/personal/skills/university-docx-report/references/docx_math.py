"""Native Word equations (OMML) from a small LaTeX subset.

Display formula structure mirrors math_formula_example.docx: a paragraph holding
m:oMathPara > m:oMath > m:eqArr > m:e with the formula, then " ", "#" and the
number in m:d, so Word right-aligns the number.

Supported: \\frac{a}{b}, ^ and _ (also together), \\sum_{..}^{..}{body}, \\text{..}
and \\mathrm{..} (upright), \\times \\cdot \\approx \\le \\ge \\ne \\pm \\to \\ldots,
\\% , ~ and "\\ " (space), round brackets as m:d, braces for grouping.
Cyrillic letters are set upright; Latin letters follow Word's math italics.
"""

import re

from lxml import etree

M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
SYMBOLS = {
    "times": "×", "cdot": "·", "approx": "≈", "le": "≤", "leq": "≤", "ge": "≥",
    "geq": "≥", "ne": "≠", "pm": "±", "to": "→", "ldots": "…", "%": "%",
}
CYRILLIC = re.compile(r"[А-Яа-яЁё]")


NSMAP = {"m": M, "w": W}


def m(tag, **attrs):
    element = etree.Element(f"{{{M}}}{tag}", nsmap=NSMAP)
    for key, value in attrs.items():
        element.set(f"{{{M}}}{key}", value)
    return element


def w(tag, **attrs):
    element = etree.Element(f"{{{W}}}{tag}", nsmap=NSMAP)
    for key, value in attrs.items():
        element.set(f"{{{W}}}{key}", value)
    return element


def sub(parent, element):
    parent.append(element)
    return element


class Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def peek(self):
        return self.text[self.pos] if self.pos < len(self.text) else ""

    def sequence(self, stop=""):
        nodes = []
        while self.pos < len(self.text) and self.peek() != stop:
            char = self.peek()
            if char.isspace():
                self.pos += 1
            elif char == "{":
                self.pos += 1
                inner = self.sequence("}")
                self.expect("}")
                nodes.append(("grp", inner))
            elif char == "(":
                self.pos += 1
                inner = self.sequence(")")
                self.expect(")")
                nodes.append(("d", inner))
            elif char in "^_":
                self.pos += 1
                nodes.append(self.script(char, nodes))
            elif char == "\\":
                nodes.extend(self.command())
            elif char == "~":
                self.pos += 1
                nodes.append(("c", " "))
            else:
                self.pos += 1
                nodes.append(("c", char))
        return nodes

    def expect(self, char):
        if self.peek() != char:
            raise ValueError(f"Ожидалось {char!r} в формуле: {self.text!r}")
        self.pos += 1

    def group(self):
        while self.peek().isspace():
            self.pos += 1
        if self.peek() == "{":
            self.pos += 1
            nodes = self.sequence("}")
            self.expect("}")
            return nodes
        if self.peek() == "\\":
            return self.command()
        char = self.peek()
        self.pos += 1
        return [("c", char)]

    def script(self, kind, nodes):
        if not nodes:
            raise ValueError(f"Индекс без основания в формуле: {self.text!r}")
        argument = self.group()
        base = nodes.pop()
        if kind == "_":
            if base[0] == "nary" and base[2] is None:
                return ("nary", base[1], argument, base[3], base[4])
            if base[0] == "sup":
                return ("subsup", base[1], argument, base[2])
            return ("sub", base, argument)
        if base[0] == "nary" and base[3] is None:
            return ("nary", base[1], base[2], argument, base[4])
        if base[0] == "sub":
            return ("subsup", base[1], base[2], argument)
        return ("sup", base, argument)

    def command(self):
        self.pos += 1
        if self.peek() in "% ,":
            char = self.peek()
            self.pos += 1
            return [("c", " " if char in " ," else char)]
        name = re.match(r"[A-Za-z]+", self.text[self.pos:])
        if not name:
            raise ValueError(f"Неизвестная команда в формуле: {self.text!r}")
        name = name.group()
        self.pos += len(name)
        if name == "frac":
            return [("frac", self.group(), self.group())]
        if name in ("text", "mathrm"):
            while self.peek().isspace():
                self.pos += 1
            self.expect("{")
            end = self.text.index("}", self.pos)
            value = self.text[self.pos:end]
            self.pos = end + 1
            return [("text", value)]
        if name == "sum":
            return [("nary", "∑", None, None, None)]
        if name in SYMBOLS:
            return [("c", SYMBOLS[name])]
        raise ValueError(f"Команда \\{name} не поддерживается: {self.text!r}")


def finish_nary(nodes):
    """Attach the next atom as the body of a sum."""
    result = []
    index = 0
    while index < len(nodes):
        node = nodes[index]
        if node[0] == "nary":
            body = [nodes[index + 1]] if index + 1 < len(nodes) else []
            result.append(("nary", node[1], node[2], node[3], body))
            index += 2
        else:
            result.append(node)
            index += 1
    return result


def run(text, upright=False):
    element = m("r")
    if upright:
        properties = sub(element, m("rPr"))
        sub(properties, m("sty", val="p"))
    font = sub(element, w("rPr"))
    sub(font, w("rFonts", ascii="Cambria Math", hAnsi="Cambria Math"))
    t = sub(element, m("t"))
    t.text = text
    if text != text.strip():
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return element


def ctrl(parent):
    properties = sub(parent, m("ctrlPr"))
    font = sub(properties, w("rPr"))
    sub(font, w("rFonts", ascii="Cambria Math", hAnsi="Cambria Math"))
    sub(font, w("i"))
    return properties


def emit(nodes, parent):
    nodes = finish_nary(nodes)
    buffer = ""
    upright = False

    def flush():
        nonlocal buffer
        if buffer:
            sub(parent, run(buffer, upright))
            buffer = ""

    for node in nodes:
        kind = node[0]
        if kind == "c":
            cyrillic = bool(CYRILLIC.match(node[1]))
            if buffer and cyrillic != upright:
                flush()
            upright = cyrillic
            buffer += node[1]
            continue
        flush()
        if kind == "text":
            sub(parent, run(node[1], upright=True))
        elif kind == "d":
            delimiter = sub(parent, m("d"))
            properties = sub(delimiter, m("dPr"))
            ctrl(properties)
            emit(node[1], sub(delimiter, m("e")))
        elif kind == "frac":
            fraction = sub(parent, m("f"))
            ctrl(sub(fraction, m("fPr")))
            emit(node[1], sub(fraction, m("num")))
            emit(node[2], sub(fraction, m("den")))
        elif kind == "grp":
            emit(node[1], parent)
        elif kind in ("sub", "sup"):
            tag = "sSub" if kind == "sub" else "sSup"
            element = sub(parent, m(tag))
            ctrl(sub(element, m(tag + "Pr")))
            emit([node[1]], sub(element, m("e")))
            emit(node[2], sub(element, m(kind)))
        elif kind == "subsup":
            element = sub(parent, m("sSubSup"))
            ctrl(sub(element, m("sSubSupPr")))
            emit([node[1]], sub(element, m("e")))
            emit(node[2], sub(element, m("sub")))
            emit(node[3], sub(element, m("sup")))
        elif kind == "nary":
            element = sub(parent, m("nary"))
            properties = sub(element, m("naryPr"))
            sub(properties, m("chr", val=node[1]))
            sub(properties, m("limLoc", val="undOvr"))
            ctrl(properties)
            emit(node[2] or [], sub(element, m("sub")))
            emit(node[3] or [], sub(element, m("sup")))
            emit(node[4] or [], sub(element, m("e")))
    flush()


def parse(latex):
    parser = Parser(latex)
    nodes = parser.sequence()
    if parser.pos != len(latex):
        raise ValueError(f"Лишняя скобка в формуле: {latex!r}")
    return nodes


def split_tag(latex):
    tag = re.search(r"\\tag\{([^}]*)\}\s*$", latex)
    if not tag:
        return latex.strip(), None
    return latex[:tag.start()].strip(), tag.group(1)


def inline_math(latex):
    """Return an m:oMath element for use inside a paragraph."""
    element = m("oMath")
    emit(parse(latex), element)
    return element


def display_math(latex):
    """Return m:oMathPara; a trailing \\tag{n} becomes the right-aligned number."""
    body, number = split_tag(latex)
    paragraph = m("oMathPara")
    math = sub(paragraph, m("oMath"))
    array = sub(math, m("eqArr"))
    properties = sub(array, m("eqArrPr"))
    sub(properties, m("maxDist", val="1"))
    ctrl(properties)
    cell = sub(array, m("e"))
    nodes = parse(body)
    if number is not None:
        nodes += [("c", " "), ("c", "#"), ("d", [("c", ch) for ch in number])]
    emit(nodes, cell)
    ctrl(cell)
    return paragraph


def math_text(element):
    """Concatenated visible text of an OMML element."""
    return "".join(element.xpath(".//m:t/text()", namespaces={"m": M}))


def plain(latex):
    body, number = split_tag(latex)
    element = display_math(latex) if number is not None else inline_math(body)
    return math_text(element)
