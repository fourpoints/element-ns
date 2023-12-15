# element-ns
Namespaced variant of Python ElementTree's XML Element.

This lets you use `find`, `findtext`, `findall`, `iterfind` without having to specify namespaces, as they are inferred from the document.

`ElementNS` inherits from `ET.Element`, so the same constructor can be used. Alternatively `ElementNS.parse` and `ElementNS.fromstring` can be used to create a document. Note that this will insert a root node with the tag "Document", which is mainly for convenience, as the top element tag can be included in the path argument, which is often preferred. This behaviour can be disabled by returning `element_tree`.

`ElementNS` includes an additional attribute, `namespaces`, which includes the namespaces in the document.

This may be slower than using `ET.Element`, as this creates Python objects instead of using the C objects. It will also read through the file/string two times.


## From string

With `ET.Element`:

```py
xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<gml:FeatureCollection xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2">
    <xsi:element>content</xsi:element>
</gml:FeatureCollection>
"""

document = ET.fromstring(xml_string)
namespaces = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'gml': 'http://www.opengis.net/gml/3.2'}

text = document.find("xsi:element", namespaces).text
print(text)  # content

# Alternatively with explicit namespace:
text = document.find("{http://www.w3.org/2001/XMLSchema-instance}element").text
print(text)  # content
```

with `ElementNS`:

```py
xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<gml:FeatureCollection xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2">
    <xsi:element>content</xsi:element>
</gml:FeatureCollection>
"""

document = ElementNS.fromstring(xml_string)

text = document.find("gml:FeatureCollection/xsi:element").text
print(text)  # content
```

## From file/source

Given the filename `data.xml` containing

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gml:FeatureCollection xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml/3.2">
    <xsi:element>content</xsi:element>
</gml:FeatureCollection>
```

With `ET.Element`:

```py
document = ET.parse("data.xml")
namespaces = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 'gml': 'http://www.opengis.net/gml/3.2'}

text = document.find("xsi:element", namespaces).text
print(text)  # content

# Alternatively with explicit namespace:
text = document.find("{http://www.w3.org/2001/XMLSchema-instance}element").text
print(text)  # content
```

With `ElementNS`:

```py
document = ElementNS.parse("data.xml")

text = document.find("gml:FeatureCollection/xsi:element").text
print(text)  # content
```
