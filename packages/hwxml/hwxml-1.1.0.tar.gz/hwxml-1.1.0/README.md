# hwxml
Parse Happy Wheels XML Leveldata!

Available via pip:

    pip install --user hwxml

# Usage:
    import hwxml
    xml = open("xml.txt", "r").read()
    parsed = hwxml.parse(xml)

    shapes = parsed.shapes
    print(shapes[0].coordinates)
