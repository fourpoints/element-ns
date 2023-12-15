"""
Small patch to the ElementTree module to include namespaced elements.
"""
import xml.etree.ElementTree as ET
import io


### Namespaces

class Namespaces(dict):
    @classmethod
    def parse(cls, source):
        return cls(node for _e, node in ET.iterparse(source, events=['start-ns']))

    @classmethod
    def fromstring(cls, string):
        return cls.parse(io.StringIO(string))


### Namespaced Element Factory

class ElementFactory:
    def __init__(self, Element, namespaces):
        self.Element = Element
        self.namespaces = namespaces

    def __call__(self, tag, attrib):
        el = self.Element(tag, attrib)
        el.namespaces = self.namespaces
        return el


### Namespaced Element

class ElementNS(ET.Element):
    namespaces = None

    @classmethod
    def parse(cls, source):
        # Set up parser with namespaced element factory
        namespaces = Namespaces.parse(source)
        element_factory = ElementFactory(ElementNS, namespaces)
        tree_builder = ET.TreeBuilder(element_factory=element_factory)
        parser = ET.XMLParser(target=tree_builder)
        element_tree = ET.ElementTree()

        if hasattr(source, "seek"):
            source.seek(0)

        root = element_tree.parse(source, parser=parser)

        document = cls("Document", {})
        document.namespaces = namespaces
        document.append(root)

        return document

    @classmethod
    def fromstring(cls, string):
        return cls.parse(io.StringIO(string))

    # Patch methods to include namespaces
    # This breaks LSP, but can be modified to be substitutable
    def find(self, path):
        return super().find(path, self.namespaces)

    def findtext(self, path, default=None):
        return super().findtext(path, default, self.namespaces)

    def findall(self, path):
        return super().findall(path, self.namespaces)

    def iterfind(self, path):
        return super().iterfind(path, self.namespaces)
