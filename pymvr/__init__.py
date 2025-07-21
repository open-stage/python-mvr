from typing import List, Union
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
import zipfile
import sys
import uuid as py_uuid
from .value import Matrix, Color  # type: ignore
from enum import Enum

__version__ = "1.0.0-dev0"


def _find_root(pkg: "zipfile.ZipFile") -> "ElementTree.Element":
    """Given a GDTF zip archive, find the GeneralSceneDescription of the
    corresponding GeneralSceneDescription.xml file."""

    with pkg.open("GeneralSceneDescription.xml", "r") as f:
        description_str = f.read().decode("utf-8")
        if description_str[-1] == "\x00":  # this should not happen, but...
            description_str = description_str[:-1]
    return ElementTree.fromstring(description_str)


class GeneralSceneDescription:
    def __init__(self, path=None):
        if path is not None:
            self._package = zipfile.ZipFile(path, "r")
        if self._package is not None:
            self._root = _find_root(self._package)
        if self._root is not None:
            self._read_xml()

    def _read_xml(self):
        self.version_major: str = self._root.get("verMajor", "")
        self.version_minor: str = self._root.get("verMinor", "")
        self.provider: str = self._root.get("provider", "")
        self.providerVersion: str = self._root.get("providerVersion", "")

        scene = self._root.find("Scene")
        if scene is not None:
            self.scene = Scene(xml_node=scene)

        user_data = self._root.find("UserData")

        if user_data is not None:
            self.user_data = UserData(xml_node=user_data)


class GeneralSceneDescriptionWriter:
    """Creates MVR zip archive with packed GeneralSceneDescription xml and other files"""

    # Currently, MVR creation is manual, outside of the library.
    # The to_xml() often takes a parent and then creates a ElementTree.SubElement.
    # For complete, automatic conversion of an mvr object to xml, we need to adjust all the to_xml methods

    def __init__(self):
        self.version_major: str = "1"
        self.version_minor: str = "6"
        self.provider: str = "pymvr"
        self.providerVersion: str = __version__
        self.files_list: List[str] = []
        self.xml_root = ElementTree.Element(
            "GeneralSceneDescription", verMajor=self.version_major, verMinor=self.version_minor, provider=self.provider, providerVersion=self.providerVersion
        )

    def write_mvr(self, path=None):
        if path is not None:
            if sys.version_info >= (3, 9):
                ElementTree.indent(self.xml_root, space="    ", level=0)
            xmlstr = ElementTree.tostring(self.xml_root, encoding="unicode", xml_declaration=True)
            with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
                z.writestr("GeneralSceneDescription.xml", xmlstr)
                for file_path, file_name in self.files_list:
                    try:
                        z.write(file_path, arcname=file_name)
                    except Exception:
                        print(f"File does not exist {file_path}")


class BaseNode:
    def __init__(self, xml_node: "Element" = None):
        if xml_node is not None:
            self._read_xml(xml_node)

    def _read_xml(self, xml_node: "Element"):
        pass


class ContainerNode(BaseNode):
    def __init__(self, children=None, xml_node: "Element" = None, *args, **kwargs):
        if children is None:
            children = []
        self.children = children
        super().__init__(xml_node, *args, **kwargs)

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, item):
        return self.children[item]

    def append(self, child):
        self.children.append(child)

    def extend(self, children_list):
        self.children.extend(children_list)

    def insert(self, index, child):
        self.children.insert(index, child)

    def remove(self, child):
        self.children.remove(child)

    def pop(self, index=-1):
        return self.children.pop(index)

    def clear(self):
        self.children.clear()

    def __len__(self):
        return len(self.children)

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, type(self).__name__)
        for child in self.children:
            element.append(child.to_xml())
        return element


class Protocols(ContainerNode):
    def _read_xml(self, xml_node: "Element"):
        self.children = [Protocol(xml_node=i) for i in xml_node.findall("Protocol")]


class Alignments(ContainerNode):
    def _read_xml(self, xml_node: "Element"):
        self.children = [Alignment(xml_node=i) for i in xml_node.findall("Alignment")]


class CustomCommands(ContainerNode):
    def _read_xml(self, xml_node: "Element"):
        self.children = [CustomCommand(xml_node=i) for i in xml_node.findall("CustomCommand")]


class Overwrites(ContainerNode):
    def _read_xml(self, xml_node: "Element"):
        self.children = [Overwrite(xml_node=i) for i in xml_node.findall("Overwrite")]


class Connections(ContainerNode):
    def _read_xml(self, xml_node: "Element"):
        self.children = [Connection(xml_node=i) for i in xml_node.findall("Connection")]


class Mappings(ContainerNode):
    def _read_xml(self, xml_node: "Element"):
        self.children = [Mapping(xml_node=i) for i in xml_node.findall("Mapping")]


class Scene(BaseNode):
    def __init__(
        self,
        layers: "Layers" = None,
        aux_data: "AUXData" = None,
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.layers = layers
        self.aux_data = aux_data
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.layers = Layers(xml_node=xml_node.find("Layers"))

        aux_data_collect = xml_node.find("AUXData")

        if aux_data_collect is not None:
            self.aux_data = AUXData(xml_node=aux_data_collect)
        else:
            self.aux_data = None

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, "Scene")
        if self.layers:
            self.layers.to_xml(element)
        if self.aux_data:
            self.aux_data.to_xml(element)
        return element


class Layers(BaseNode):
    def __init__(
        self,
        layers: List["Layer"] = [],
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.layers = layers
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.layers = [Layer(xml_node=i) for i in xml_node.findall("Layer")]

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, "Layers")
        for layer in self.layers:
            element.append(layer.to_xml())
        return element

    def __iter__(self):
        return iter(self.layers)

    def __getitem__(self, item):
        return self.layers[item]

    def append(self, layer: "Layer"):
        self.layers.append(layer)

    def extend(self, layers: List["Layer"]):
        self.layers.extend(layers)

    def insert(self, index: int, layer: "Layer"):
        self.layers.insert(index, layer)

    def remove(self, layer: "Layer"):
        self.layers.remove(layer)

    def pop(self, index: int = -1):
        return self.layers.pop(index)

    def clear(self):
        self.layers.clear()

    def __len__(self):
        return len(self.layers)


class UserData(BaseNode):
    def __init__(
        self,
        data: List["Data"] = [],
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.data = data
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.data = [Data(xml_node=i) for i in xml_node.findall("Data")]

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, type(self).__name__)
        for _data in self.data:
            element.append(_data.to_xml())
        return element


class ScaleHandelingEnum(Enum):
    SCALE_KEEP_RATIO = "ScaleKeepRatio"
    SCALE_IGNORE_RATIO = "ScaleIgnoreRatio"
    KEEP_SIZE_CENTER = "KeepSizeCenter"


class ScaleHandeling(BaseNode):
    def __init__(
        self,
        value: ScaleHandelingEnum = ScaleHandelingEnum.SCALE_KEEP_RATIO,
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.value = value
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        if xml_node.text:
            try:
                self.value = ScaleHandelingEnum(xml_node.text)
            except ValueError:
                self.value = ScaleHandelingEnum.SCALE_KEEP_RATIO
        else:
            self.value = ScaleHandelingEnum.SCALE_KEEP_RATIO

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, "ScaleHandeling")
        element.text = self.value.value
        return element


class Network(BaseNode):
    def __init__(
        self,
        geometry: str = "",
        ipv4: Union[str, None] = None,
        subnetmask: Union[str, None] = None,
        ipv6: Union[str, None] = None,
        dhcp: bool = False,
        hostname: Union[str, None] = None,
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.geometry = geometry
        self.ipv4 = ipv4
        self.subnetmask = subnetmask
        self.ipv6 = ipv6
        self.dhcp = dhcp
        self.hostname = hostname
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.geometry = xml_node.attrib.get("geometry", "")
        self.ipv4 = xml_node.attrib.get("ipv4")
        self.subnetmask = xml_node.attrib.get("subnetmask")
        self.ipv6 = xml_node.attrib.get("ipv6")
        self.dhcp = xml_node.attrib.get("dhcp", "false").lower() in ("true", "1", "on")
        self.hostname = xml_node.attrib.get("hostname")

    def to_xml(self, parent: Element):
        attributes = {"geometry": self.geometry}
        if self.ipv4:
            attributes["ipv4"] = self.ipv4
        if self.subnetmask:
            attributes["subnetmask"] = self.subnetmask
        if self.ipv6:
            attributes["ipv6"] = self.ipv6
        if self.dhcp:
            attributes["dhcp"] = "true"
        if self.hostname:
            attributes["hostname"] = self.hostname
        element = ElementTree.SubElement(parent, "Network", **attributes)
        return element


class Addresses(BaseNode):
    def __init__(
        self,
        address: List["Address"] = [],
        network: List["Network"] = [],
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.address = address if address is not None else []
        self.network = network if network is not None else []
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.address = [Address(xml_node=i) for i in xml_node.findall("Address")]
        self.network = [Network(xml_node=i) for i in xml_node.findall("Network")]

    def to_xml(self, parent: Element):
        if not self.address and not self.network:
            return None
        element = ElementTree.SubElement(parent, "Addresses")
        for dmx_address in self.address:
            dmx_address.to_xml(element)
        for network_address in self.network:
            network_address.to_xml(element)
        return element

    def __len__(self):
        return len(self.address) + len(self.network)


class BaseChildNode(BaseNode):
    def __init__(
        self,
        name: Union[str, None] = None,
        uuid: Union[str, None] = None,
        gdtf_spec: Union[str, None] = None,
        gdtf_mode: Union[str, None] = None,
        matrix: Matrix = Matrix(0),
        classing: Union[str, None] = None,
        fixture_id: Union[str, None] = None,
        fixture_id_numeric: int = 0,
        unit_number: int = 0,
        custom_id: int = 0,
        custom_id_type: int = 0,
        cast_shadow: bool = False,
        addresses: "Addresses" = None,
        alignments: "Alignments" = None,
        custom_commands: "CustomCommands" = None,
        overwrites: "Overwrites" = None,
        connections: "Connections" = None,
        child_list: Union["ChildList", None] = None,
        multipatch: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.name = name
        if uuid is None:
            uuid = str(py_uuid.uuid4())
        self.uuid = uuid
        self.gdtf_spec = gdtf_spec
        self.gdtf_mode = gdtf_mode
        self.matrix = matrix
        self.classing = classing
        self.fixture_id = fixture_id
        self.fixture_id_numeric = fixture_id_numeric
        self.unit_number = unit_number
        self.custom_id = custom_id
        self.custom_id_type = custom_id_type
        self.cast_shadow = cast_shadow
        self.addresses = addresses if addresses is not None else Addresses()
        self.alignments = alignments if alignments is not None else Alignments()
        self.custom_commands = custom_commands if custom_commands is not None else CustomCommands()
        self.overwrites = overwrites if overwrites is not None else Overwrites()
        self.connections = connections if connections is not None else Connections()
        self.child_list = child_list
        self.multipatch = multipatch
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.name = xml_node.attrib.get("name")
        self.uuid = xml_node.attrib.get("uuid")
        self.multipatch = xml_node.attrib.get("multipatch")
        _gdtf_spec = xml_node.find("GDTFSpec")
        if _gdtf_spec is not None:
            self.gdtf_spec = _gdtf_spec.text
            if self.gdtf_spec is not None:
                self.gdtf_spec = self.gdtf_spec.encode("utf-8").decode("cp437")  # IBM PC encoding
            if self.gdtf_spec is not None and len(self.gdtf_spec) > 5:
                if self.gdtf_spec[-5:].lower() != ".gdtf":
                    self.gdtf_spec = f"{self.gdtf_spec}.gdtf"
        if xml_node.find("GDTFMode") is not None:
            self.gdtf_mode = xml_node.find("GDTFMode").text
        if xml_node.find("Matrix") is not None:
            self.matrix = Matrix(str_repr=xml_node.find("Matrix").text)
        if xml_node.find("FixtureID") is not None:
            self.fixture_id = xml_node.find("FixtureID").text

        if xml_node.find("FixtureIDNumeric") is not None:
            self.fixture_id_numeric = int(xml_node.find("FixtureIDNumeric").text)
        if xml_node.find("UnitNumber") is not None:
            self.unit_number = int(xml_node.find("UnitNumber").text)

        if xml_node.find("CustomId") is not None:
            self.custom_id = int(xml_node.find("CustomId").text or 0)

        if xml_node.find("CustomIdType") is not None:
            self.custom_id_type = int(xml_node.find("CustomIdType").text or 0)

        if xml_node.find("CastShadow") is not None:
            text_value = (xml_node.find("CastShadow").text or "false").lower()
            self.cast_shadow = text_value in ("true", "1")

        addresses_node = xml_node.find("Addresses")
        if addresses_node is not None:
            self.addresses = Addresses(xml_node=addresses_node)
        else:
            self.addresses = Addresses()

        if xml_node.find("Alignments"):
            self.alignments = Alignments(xml_node=xml_node.find("Alignments"))
        if xml_node.find("Connections"):
            self.connections = Connections(xml_node=xml_node.find("Connections"))
        if xml_node.find("CustomCommands") is not None:
            self.custom_commands = CustomCommands(xml_node=xml_node.find("CustomCommands"))
        if xml_node.find("Overwrites"):
            self.overwrites = Overwrites(xml_node=xml_node.find("Overwrites"))
        if xml_node.find("Classing") is not None:
            self.classing = xml_node.find("Classing").text

        self.child_list = ChildList(xml_node=xml_node.find("ChildList"))

    def __str__(self):
        return f"{self.name}"

    def to_xml(self, element: Element):
        Matrix(self.matrix.matrix).to_xml(element)
        if self.classing:
            ElementTree.SubElement(element, "Classing").text = self.classing
        if self.gdtf_spec:
            ElementTree.SubElement(element, "GDTFSpec").text = self.gdtf_spec
        if self.gdtf_mode:
            ElementTree.SubElement(element, "GDTFMode").text = self.gdtf_mode
        if self.cast_shadow:
            ElementTree.SubElement(element, "CastShadow").text = "true"

        if self.addresses:
            self.addresses.to_xml(element)

        if self.alignments:
            self.alignments.to_xml(element)

        if self.custom_commands:
            self.custom_commands.to_xml(element)

        if self.overwrites:
            self.overwrites.to_xml(element)

        if self.connections:
            self.connections.to_xml(element)

        ElementTree.SubElement(element, "FixtureID").text = str(self.fixture_id) or "0"
        ElementTree.SubElement(element, "FixtureIDNumeric").text = str(self.fixture_id_numeric)
        if self.unit_number is not None:
            ElementTree.SubElement(element, "UnitNumber").text = str(self.unit_number)
        if self.custom_id_type is not None:
            ElementTree.SubElement(element, "CustomIdType").text = str(self.custom_id_type)
        if self.custom_id is not None:
            ElementTree.SubElement(element, "CustomId").text = str(self.custom_id)

        if self.child_list:
            self.child_list.to_xml(element)


class BaseChildNodeExtended(BaseChildNode):
    def __init__(
        self,
        geometries: "Geometries" = None,
        child_list: Union["ChildList", None] = None,
        *args,
        **kwargs,
    ):
        self.geometries = geometries
        self.child_list = child_list
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        super()._read_xml(xml_node)
        if xml_node.find("Geometries") is not None:
            self.geometries = Geometries(xml_node=xml_node.find("Geometries"))

        self.child_list = ChildList(xml_node=xml_node.find("ChildList"))

    def __str__(self):
        return f"{self.name}"

    def to_xml(self, element: Element):
        super().to_xml(element)
        if self.geometries:
            self.geometries.to_xml(element)


class Data(BaseNode):
    def __init__(
        self,
        provider: str = "",
        ver: str = "1",
        *args,
        **kwargs,
    ):
        self.provider = provider
        self.ver = ver
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.provider = xml_node.attrib.get("provider")
        self.ver = xml_node.attrib.get("ver")

    def __str__(self):
        return f"{self.provider} {self.ver}"

    def to_xml(self):
        attributes = {"name": self.name, "uuid": self.uuid}
        return ElementTree.Element(type(self).__name__, provider=self.provider, ver=self.ver)


class AUXData(BaseNode):
    def __init__(
        self,
        classes: List["Class"] = [],
        symdefs: List["Symdef"] = [],
        positions: List["Position"] = [],
        mapping_definitions: List["MappingDefinition"] = [],
        *args,
        **kwargs,
    ):
        self.classes = classes
        self.symdefs = symdefs
        self.positions = positions
        self.mapping_definitions = mapping_definitions
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.classes = [Class(xml_node=i) for i in xml_node.findall("Class")]
        self.symdefs = [Symdef(xml_node=i) for i in xml_node.findall("Symdef")]
        self.positions = [Position(xml_node=i) for i in xml_node.findall("Position")]
        self.mapping_definitions = [MappingDefinition(xml_node=i) for i in xml_node.findall("MappingDefinition")]

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, type(self).__name__)
        for _class in self.classes:
            element.append(_class.to_xml())
        for symdef in self.symdefs:
            element.append(symdef.to_xml())
        for position in self.positions:
            element.append(position.to_xml())
        for mapping_definition in self.mapping_definitions:
            element.append(mapping_definition.to_xml())
        return element


class MappingDefinition(BaseNode):
    def __init__(
        self,
        name: Union[str, None] = None,
        uuid: Union[str, None] = None,
        size_x: int = 0,
        size_y: int = 0,
        source=None,
        scale_handling: "ScaleHandeling" = None,
        *args,
        **kwargs,
    ):
        self.name = name
        self.uuid = uuid
        self.size_x = size_x
        self.size_y = size_y
        self.source = source
        self.scale_handling = scale_handling if scale_handling is not None else ScaleHandeling()
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.name = xml_node.attrib.get("name")
        self.uuid = xml_node.attrib.get("uuid")
        # TODO handle missing data...
        self.size_x = int(xml_node.find("SizeX").text)
        self.size_y = int(xml_node.find("SizeY").text)
        source_node = xml_node.find("Source")
        if source_node is not None:
            self.source = Source(xml_node=source_node)
        scale_handling_node = xml_node.find("ScaleHandeling")
        if scale_handling_node is not None:
            self.scale_handling = ScaleHandeling(xml_node=scale_handling_node)

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, name=self.name, uuid=self.uuid)
        ElementTree.SubElement(element, "SizeX").text = str(self.size_x)
        ElementTree.SubElement(element, "SizeY").text = str(self.size_y)
        if self.scale_handling:
            self.scale_handling.to_xml(element)
        # TODO source
        return element


class Fixture(BaseChildNode):
    def __init__(
        self,
        focus: Union[str, None] = None,
        color: Union["Color", str, None] = Color(),
        dmx_invert_pan: bool = False,
        dmx_invert_tilt: bool = False,
        position: Union[str, None] = None,
        function_: Union[str, None] = None,
        child_position: Union[str, None] = None,
        protocols: "Protocols" = None,
        mappings: "Mappings" = None,
        gobo: Union["Gobo", None] = None,
        unit_number: int = 0,
        *args,
        **kwargs,
    ):
        self.focus = focus
        self.color = color
        self.dmx_invert_pan = dmx_invert_pan
        self.dmx_invert_tilt = dmx_invert_tilt
        self.position = position
        self.function_ = function_
        self.child_position = child_position
        self.protocols = protocols if protocols is not None else Protocols()
        self.mappings = mappings if mappings is not None else Mappings()
        self.gobo = gobo
        self.unit_number = unit_number
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        super()._read_xml(xml_node)

        if xml_node.find("Focus") is not None:
            self.focus = xml_node.find("Focus").text

        if xml_node.find("Color") is not None:
            self.color = Color(str_repr=xml_node.find("Color").text)

        if xml_node.find("DMXInvertPan") is not None:
            text_value = (xml_node.find("DMXInvertPan").text or "false").lower()
            self.dmx_invert_pan = text_value in ("true", "1")

        if xml_node.find("DMXInvertTilt") is not None:
            text_value = (xml_node.find("DMXInvertTilt").text or "false").lower()
            self.dmx_invert_tilt = text_value in ("true", "1")

        if xml_node.find("Position") is not None:
            self.position = xml_node.find("Position").text

        if xml_node.find("Function") is not None:
            self.function_ = xml_node.find("Function").text

        if xml_node.find("ChildPosition") is not None:
            self.child_position = xml_node.find("ChildPosition").text

        if xml_node.find("Protocols"):
            self.protocols = Protocols(xml_node=xml_node.find("Protocols"))
        if xml_node.find("Mappings") is not None:
            self.mappings = Mappings(xml_node=xml_node.find("Mappings"))
        if xml_node.find("Gobo") is not None:
            self.gobo = Gobo(xml_node=xml_node.find("Gobo"))
        if xml_node.find("UnitNumber") is not None:
            self.unit_number = int(xml_node.find("UnitNumber").text)

    def to_xml(self):
        attributes = {"name": self.name, "uuid": self.uuid}
        if self.multipatch:
            attributes["multipatch"] = self.multipatch
        element = ElementTree.Element(type(self).__name__, **attributes)
        super().to_xml(element)

        if self.focus:
            ElementTree.SubElement(element, "Focus").text = self.focus
        if self.dmx_invert_pan:
            ElementTree.SubElement(element, "DMXInvertPan").text = "true"
        if self.dmx_invert_tilt:
            ElementTree.SubElement(element, "DMXInvertTilt").text = "true"
        if self.position:
            ElementTree.SubElement(element, "Position").text = self.position
        if self.function_:
            ElementTree.SubElement(element, "Function").text = self.function_
        if self.child_position:
            ElementTree.SubElement(element, "ChildPosition").text = self.child_position

        if len(self.protocols) > 0:
            self.protocols.to_xml(element)

        if isinstance(self.color, Color):
            self.color.to_xml(element)
        elif self.color:
            Color(str_repr=self.color).to_xml(element)

        if len(self.mappings) > 0:
            self.mappings.to_xml(element)
        if self.gobo:
            element.append(self.gobo.to_xml())

        ElementTree.SubElement(element, "UnitNumber").text = str(self.unit_number)

        return element

    def __str__(self):
        return f"{self.name}"


class GroupObject(BaseNode):
    def __init__(
        self,
        name: Union[str, None] = None,
        uuid: Union[str, None] = None,
        classing: Union[str, None] = None,
        child_list: Union["ChildList", None] = None,
        matrix: Matrix = Matrix(0),
        *args,
        **kwargs,
    ):
        self.name = name
        self.uuid = uuid
        self.classing = classing
        self.child_list = child_list
        self.matrix = matrix

        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.name = xml_node.attrib.get("name")
        self.uuid = xml_node.attrib.get("uuid")
        if xml_node.find("Classing") is not None:
            self.classing = xml_node.find("Classing").text
        self.child_list = ChildList(xml_node=xml_node.find("ChildList"))
        if xml_node.find("Matrix") is not None:
            self.matrix = Matrix(str_repr=xml_node.find("Matrix").text)

    def __str__(self):
        return f"{self.name}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, name=self.name, uuid=self.uuid)
        Matrix(self.matrix.matrix).to_xml(parent=element)
        if self.classing:
            ElementTree.SubElement(element, "Classing").text = self.classing
        if self.child_list:
            self.child_list.to_xml(parent=element)
        return element


class ChildList(BaseNode):
    def __init__(
        self,
        scene_objects: List["SceneObject"] = [],
        group_objects: List["GroupObject"] = [],
        focus_points: List["FocusPoint"] = [],
        fixtures: List["Fixture"] = [],
        supports: List["Support"] = [],
        trusses: List["Truss"] = [],
        video_screens: List["VideoScreen"] = [],
        projectors: List["Projector"] = [],
        *args,
        **kwargs,
    ):
        if scene_objects is not None:
            self.scene_objects = scene_objects
        else:
            self.scene_objects = []

        if group_objects is not None:
            self.group_objects = group_objects
        else:
            self.group_objects = []

        if focus_points is not None:
            self.focus_points = focus_points
        else:
            self.focus_points = []

        if fixtures is not None:
            self.fixtures = fixtures
        else:
            self.fixtures = []

        if supports is not None:
            self.supports = supports
        else:
            self.supports = []

        if trusses is not None:
            self.trusses = trusses
        else:
            self.trusses = []

        if video_screens is not None:
            self.video_screens = video_screens
        else:
            self.video_screens = []

        if projectors is not None:
            self.projectors = projectors
        else:
            self.projectors = []

        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.scene_objects = [SceneObject(xml_node=i) for i in xml_node.findall("SceneObject")]

        self.group_objects = [GroupObject(xml_node=i) for i in xml_node.findall("GroupObject")]

        self.focus_points = [FocusPoint(xml_node=i) for i in xml_node.findall("FocusPoint")]

        self.fixtures = [Fixture(xml_node=i) for i in xml_node.findall("Fixture")]

        self.supports = [Support(xml_node=i) for i in xml_node.findall("Support")]
        self.trusses = [Truss(xml_node=i) for i in xml_node.findall("Truss")]

        self.video_screens = [VideoScreen(xml_node=i) for i in xml_node.findall("VideoScreen")]

        self.projectors = [Projector(xml_node=i) for i in xml_node.findall("Projector")]

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, type(self).__name__)
        for fixture in self.fixtures:
            element.append(fixture.to_xml())
        for focus_point in self.focus_points:
            element.append(focus_point.to_xml())
        for group_object in self.group_objects:
            element.append(group_object.to_xml())
        for scene_object in self.scene_objects:
            element.append(scene_object.to_xml())
        for support in self.supports:
            element.append(support.to_xml())
        for truss in self.trusses:
            element.append(truss.to_xml())
        for video_screen in self.video_screens:
            element.append(video_screen.to_xml())
        for projector in self.projectors:
            element.append(projector.to_xml())
        return element


class Layer(BaseNode):
    def __init__(
        self,
        name: str = "",
        uuid: Union[str, None] = None,
        matrix: Matrix = Matrix(0),
        child_list: Union["ChildList", None] = None,
        *args,
        **kwargs,
    ):
        self.name = name
        if uuid is None:
            uuid = str(py_uuid.uuid4())
        self.uuid = uuid
        self.child_list = child_list
        self.matrix = matrix

        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.name = xml_node.attrib.get("name", "")
        self.uuid = xml_node.attrib.get("uuid")

        self.child_list = ChildList(xml_node=xml_node.find("ChildList"))
        if xml_node.find("Matrix") is not None:
            self.matrix = Matrix(str_repr=xml_node.find("Matrix").text)

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, name=self.name, uuid=self.uuid)
        Matrix(self.matrix.matrix).to_xml(parent=element)
        if self.child_list:
            self.child_list.to_xml(parent=element)
        return element

    def __str__(self):
        return f"{self.name}"


class Address(BaseNode):
    def __init__(
        self,
        dmx_break: int = 0,
        universe: int = 1,
        address: int = 1,
        *args,
        **kwargs,
    ):
        self.dmx_break = dmx_break
        self.address = address
        self.universe = universe
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.dmx_break = int(xml_node.attrib.get("break", 0))
        raw_address = xml_node.text or "1"
        if raw_address == "0":
            raw_address = "1"
        if "." in raw_address:
            universe, address = raw_address.split(".")
            self.universe = int(universe) if (int(universe)) > 0 else 1
            self.address = int(address) if int(address) > 0 else 1
            return
        self.universe = (int(raw_address) - 1) // 512 + 1
        self.address = (int(raw_address) - 1) % 512 + 1

    def __repr__(self):
        return f"B: {self.dmx_break}, U: {self.universe}, A: {self.address}"

    def __str__(self):
        return f"B: {self.dmx_break}, U: {self.universe}, A: {self.address}"

    def to_xml(self, addresses):
        # universes are always from 1 in MVR
        if self.universe == 0:
            self.universe = 1

        universes = 512 * (self.universe - 1)

        raw_address = self.address + universes
        address = ElementTree.SubElement(addresses, "Address", attrib={"break": str(self.dmx_break)})
        address.text = str(raw_address)


class Class(BaseNode):
    def __init__(
        self,
        uuid: Union[str, None] = None,
        name: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.uuid = uuid
        self.name = name
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.name = xml_node.attrib.get("name")
        self.uuid = xml_node.attrib.get("uuid")

    def __str__(self):
        return f"{self.name}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, name=self.name, uuid=self.uuid)
        return element


class Position(BaseNode):
    def __init__(
        self,
        uuid: Union[str, None] = None,
        name: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.uuid = uuid
        self.name = name
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.name = xml_node.attrib.get("name")
        self.uuid = xml_node.attrib.get("uuid")

    def __str__(self):
        return f"{self.name}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, name=self.name, uuid=self.uuid)
        return element


class Symdef(BaseNode):
    def __init__(
        self,
        uuid: Union[str, None] = None,
        name: Union[str, None] = None,
        geometry3d: List["Geometry3D"] = [],
        symbol: List["Symbol"] = [],
        *args,
        **kwargs,
    ):
        self.uuid = uuid
        self.name = name
        self.geometry3d = geometry3d
        self.symbol = symbol
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.name = xml_node.attrib.get("name")
        self.uuid = xml_node.attrib.get("uuid")

        child_list = xml_node.find("ChildList")
        if child_list is not None:
            self.symbol = [Symbol(xml_node=i) for i in child_list.findall("Symbol")]
            _geometry3d = [Geometry3D(xml_node=i) for i in child_list.findall("Geometry3D")]
        else:
            self.symbol = []
            _geometry3d = []

        # sometimes the list of geometry3d is full of duplicates, eliminate them here
        self.geometry3d = list(set(_geometry3d))

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, name=self.name, uuid=self.uuid)
        for geo in self.geometry3d:
            element.append(geo.to_xml())
        for sym in self.symbol:
            element.append(sym.to_xml())
        return element


class Geometry3D(BaseNode):
    def __init__(
        self,
        file_name: Union[str, None] = None,
        matrix: Matrix = Matrix(0),
        *args,
        **kwargs,
    ):
        self.file_name = file_name
        self.matrix = matrix
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.file_name = xml_node.attrib.get("fileName", "").encode("utf-8").decode("cp437")
        if xml_node.find("Matrix") is not None:
            self.matrix = Matrix(str_repr=xml_node.find("Matrix").text)

    def __str__(self):
        return f"{self.file_name} {self.matrix}"

    def __repr__(self):
        return f"{self.file_name} {self.matrix}"

    def __eq__(self, other):
        return self.file_name == other.file_name and self.matrix == other.matrix

    def __ne__(self, other):
        return self.file_name != other.file_name or self.matrix != other.matrix

    def __hash__(self):
        return hash((self.file_name, str(self.matrix)))

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, fileName=self.file_name)
        Matrix(self.matrix.matrix).to_xml(parent=element)
        return element


class Symbol(BaseNode):
    def __init__(
        self,
        uuid: Union[str, None] = None,
        symdef: Union[str, None] = None,
        matrix: Matrix = Matrix(0),
        *args,
        **kwargs,
    ):
        self.uuid = uuid
        self.symdef = symdef
        self.matrix = matrix
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.uuid = xml_node.attrib.get("uuid")
        self.symdef = xml_node.attrib.get("symdef")
        if xml_node.find("Matrix") is not None:
            self.matrix = Matrix(str_repr=xml_node.find("Matrix").text)

    def __str__(self):
        return f"{self.uuid}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, uuid=self.uuid, symdef=self.symdef)
        Matrix(self.matrix.matrix).to_xml(parent=element)
        return element


class Geometries(BaseNode):
    def __init__(
        self,
        geometry3d: List["Geometry3D"] = [],
        symbol: List["Symbol"] = [],
        *args,
        **kwargs,
    ):
        self.geometry3d = geometry3d
        self.symbol = symbol
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.symbol = [Symbol(xml_node=i) for i in xml_node.findall("Symbol")]
        self.geometry3d = [Geometry3D(xml_node=i) for i in xml_node.findall("Geometry3D")]

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, type(self).__name__)
        for geo in self.geometry3d:
            element.append(geo.to_xml())
        for sym in self.symbol:
            element.append(sym.to_xml())
        return element


class FocusPoint(BaseNode):
    def __init__(
        self,
        uuid: Union[str, None] = None,
        name: Union[str, None] = None,
        matrix: Matrix = Matrix(0),
        classing: Union[str, None] = None,
        geometries: "Geometries" = None,
        *args,
        **kwargs,
    ):
        self.name = name
        self.uuid = uuid
        self.matrix = matrix
        self.classing = classing
        if geometries is None:
            geometries = Geometries()
        self.geometries = geometries

        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.uuid = xml_node.attrib.get("uuid")
        self.name = xml_node.attrib.get("name")
        if xml_node.find("Matrix") is not None:
            self.matrix = Matrix(str_repr=xml_node.find("Matrix").text)
        if xml_node.find("Classing") is not None:
            self.classing = xml_node.find("Classing").text
        if xml_node.find("Geometries") is not None:
            self.geometries = Geometries(xml_node=xml_node.find("Geometries"))

    def __str__(self):
        return f"{self.name}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, name=self.name, uuid=self.uuid)
        Matrix(self.matrix.matrix).to_xml(parent=element)
        if self.classing:
            ElementTree.SubElement(element, "Classing").text = self.classing
        self.geometries.to_xml(parent=element)
        return element


class SceneObject(BaseChildNodeExtended):
    pass


class Truss(BaseChildNodeExtended):
    def __init__(
        self,
        position: Union[str, None] = None,
        function_: Union[str, None] = None,
        child_position: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.position = position
        self.function_ = function_
        self.child_position = child_position
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        super()._read_xml(xml_node)
        if xml_node.find("Position") is not None:
            self.position = xml_node.find("Position").text
        if xml_node.find("Function") is not None:
            self.function_ = xml_node.find("Function").text
        if xml_node.find("ChildPosition") is not None:
            self.child_position = xml_node.find("ChildPosition").text

    def to_xml(self):
        attributes = {"name": self.name, "uuid": self.uuid}
        if self.multipatch:
            attributes["multipatch"] = self.multipatch
        element = ElementTree.Element(type(self).__name__, **attributes)
        super().to_xml(element)
        if self.position:
            ElementTree.SubElement(element, "Position").text = self.position
        if self.function_:
            ElementTree.SubElement(element, "Function").text = self.function_
        if self.child_position:
            ElementTree.SubElement(element, "ChildPosition").text = self.child_position
        return element


class Support(BaseChildNodeExtended):
    def __init__(
        self,
        chain_length: float = 0,
        position: Union[str, None] = None,
        function_: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.chain_length = chain_length
        self.position = position
        self.function_ = function_
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        super()._read_xml(xml_node)
        chain_length_node = xml_node.find("ChainLength")
        if chain_length_node is not None:
            self.chain_length = float(chain_length_node.text or 0)

        position_node = xml_node.find("Position")
        if position_node is not None:
            self.position = position_node.text

        function_node = xml_node.find("Function")
        if function_node is not None:
            self.function_ = function_node.text

    def to_xml(self):
        attributes = {"name": self.name, "uuid": self.uuid}
        if self.multipatch:
            attributes["multipatch"] = self.multipatch
        element = ElementTree.Element(type(self).__name__, **attributes)
        super().to_xml(element)

        if self.position:
            ElementTree.SubElement(element, "Position").text = self.position

        if self.function_:
            ElementTree.SubElement(element, "Function").text = self.function_

        ElementTree.SubElement(element, "ChainLength").text = str(self.chain_length)

        return element


class VideoScreen(BaseChildNodeExtended):
    def __init__(
        self,
        sources: "Sources" = None,
        function_: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.sources = sources
        self.function_ = function_
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        super()._read_xml(xml_node)
        if xml_node.find("Sources") is not None:
            self.sources = Sources(xml_node=xml_node.find("Sources"))
        if xml_node.find("Function") is not None:
            self.function_ = xml_node.find("Function").text

    def to_xml(self):
        attributes = {"name": self.name, "uuid": self.uuid}
        if self.multipatch:
            attributes["multipatch"] = self.multipatch
        element = ElementTree.Element(type(self).__name__, **attributes)
        super().to_xml(element)

        if self.sources:
            self.sources.to_xml(element)
        if self.function_:
            ElementTree.SubElement(element, "Function").text = self.function_

        return element


class Projector(BaseChildNodeExtended):
    def __init__(
        self,
        projections: "Projections" = None,
        *args,
        **kwargs,
    ):
        self.projections = projections
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        super()._read_xml(xml_node)
        if xml_node.find("Projections") is not None:
            self.projections = Projections(xml_node=xml_node.find("Projections"))

    def to_xml(self):
        attributes = {"name": self.name, "uuid": self.uuid}
        if self.multipatch:
            attributes["multipatch"] = self.multipatch
        element = ElementTree.Element(type(self).__name__, **attributes)
        super().to_xml(element)

        if self.projections:
            self.projections.to_xml(element)

        return element


class Protocol(BaseNode):
    def __init__(
        self,
        geometry: Union[str, None] = "NetworkInOut_1",
        name: Union[str, None] = None,
        type_: Union[str, None] = None,
        version: Union[str, None] = None,
        transmission: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.geometry = geometry
        self.name = name
        self.type = type_
        self.version = version
        self.transmission = transmission
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.geometry = xml_node.attrib.get("geometry")
        self.name = xml_node.attrib.get("name")
        self.type = xml_node.attrib.get("type")
        self.version = xml_node.attrib.get("version")
        self.transmission = xml_node.attrib.get("transmission")

    def __str__(self):
        return f"{self.name}"

    def to_xml(self):
        attributes = {}
        if self.geometry:
            attributes["geometry"] = self.geometry
        if self.name:
            attributes["name"] = self.name
        if self.type:
            attributes["type"] = self.type
        if self.version:
            attributes["version"] = self.version
        if self.transmission:
            attributes["transmission"] = self.transmission
        element = ElementTree.Element(type(self).__name__, **attributes)
        return element


class Alignment(BaseNode):
    def __init__(
        self,
        geometry: Union[str, None] = "Beam",
        up: Union[str, None] = "0,0,1",
        direction: Union[str, None] = "0,0,-1",
        *args,
        **kwargs,
    ):
        self.geometry = geometry
        self.up = up
        self.direction = direction
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.geometry = xml_node.attrib.get("geometry")
        self.up = xml_node.attrib.get("up", "0,0,1")
        self.direction = xml_node.attrib.get("direction", "0,0,-1")

    def __str__(self):
        return f"{self.geometry}"

    def to_xml(self):
        attributes = {}
        if self.geometry:
            attributes["geometry"] = self.geometry
        if self.up:
            attributes["up"] = self.up
        if self.direction:
            attributes["direction"] = self.direction
        element = ElementTree.Element(type(self).__name__, **attributes)
        return element


class Overwrite(BaseNode):
    def __init__(
        self,
        universal: Union[str, None] = None,
        target: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.universal = universal
        self.target = target
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.universal = xml_node.attrib.get("universal")
        self.target = xml_node.attrib.get("target")

    def __str__(self):
        return f"{self.universal} {self.target}"

    def to_xml(self):
        attributes = {"universal": self.universal}
        if self.target:
            attributes["target"] = self.target
        element = ElementTree.Element(type(self).__name__, **attributes)
        return element


class Connection(BaseNode):
    def __init__(
        self,
        own: Union[str, None] = None,
        other: Union[str, None] = None,
        to_object: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.own = own
        self.other = other
        self.to_object = to_object
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.own = xml_node.attrib.get("own")
        self.other = xml_node.attrib.get("other")
        self.to_object = xml_node.attrib.get("toObject")

    def __str__(self):
        return f"{self.own} {self.other}"

    def to_xml(self):
        element = ElementTree.Element(
            type(self).__name__,
            own=self.own,
            other=self.other,
            toObject=self.to_object,
        )
        return element


class Mapping(BaseNode):
    def __init__(
        self,
        link_def: Union[str, None] = None,
        ux: Union[int, None] = None,
        uy: Union[int, None] = None,
        ox: Union[int, None] = None,
        oy: Union[int, None] = None,
        rz: Union[float, None] = None,
        *args,
        **kwargs,
    ):
        self.link_def = link_def
        self.ux = ux
        self.uy = uy
        self.ox = ox
        self.oy = oy
        self.rz = rz
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.link_def = xml_node.attrib.get("linkedDef")
        ux_node = xml_node.find("ux")
        if ux_node is not None:
            self.ux = int(ux_node.text)
        uy_node = xml_node.find("uy")
        if uy_node is not None:
            self.uy = int(uy_node.text)
        ox_node = xml_node.find("ox")
        if ox_node is not None:
            self.ox = int(ox_node.text)
        oy_node = xml_node.find("oy")
        if oy_node is not None:
            self.oy = int(oy_node.text)
        rz_node = xml_node.find("rz")
        if rz_node is not None:
            self.rz = float(rz_node.text)

    def __str__(self):
        return f"{self.link_def}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, linkedDef=self.link_def)
        if self.ux is not None:
            ElementTree.SubElement(element, "ux").text = str(self.ux)
        if self.uy is not None:
            ElementTree.SubElement(element, "uy").text = str(self.uy)
        if self.ox is not None:
            ElementTree.SubElement(element, "ox").text = str(self.ox)
        if self.oy is not None:
            ElementTree.SubElement(element, "oy").text = str(self.oy)
        if self.rz is not None:
            ElementTree.SubElement(element, "rz").text = str(self.rz)
        return element


class Gobo(BaseNode):
    def __init__(
        self,
        rotation: Union[str, float, None] = None,
        filename: Union[str, None] = None,
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.rotation = rotation
        self.filename = filename
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.rotation = float(xml_node.attrib.get("rotation", 0))
        self.filename = xml_node.text

    def __str__(self):
        return f"{self.filename} {self.rotation}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__, rotation=str(self.rotation))
        element.text = self.filename
        return element


class CustomCommand(BaseNode):
    # TODO: split more: <CustomCommand>Body_Pan,f 50</CustomCommand>
    def __init__(
        self,
        custom_command: Union[str, None] = None,
        *args,
        **kwargs,
    ):
        self.custom_command = custom_command
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.custom_command = xml_node.text

    def __str__(self):
        return f"{self.custom_command}"

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__)
        element.text = self.custom_command
        return element


class Projection(BaseNode):
    def __init__(
        self,
        source: "Source" = None,
        scale_handling: "ScaleHandeling" = None,
        *args,
        **kwargs,
    ):
        self.source = source
        self.scale_handling = scale_handling if scale_handling is not None else ScaleHandeling()
        super().__init__(*args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        if xml_node.find("Source") is not None:
            self.source = Source(xml_node=xml_node.find("Source"))
        scale_handling_node = xml_node.find("ScaleHandeling")
        if scale_handling_node is not None:
            self.scale_handling = ScaleHandeling(xml_node=scale_handling_node)

    def to_xml(self):
        element = ElementTree.Element(type(self).__name__)
        if self.source:
            element.append(self.source.to_xml())
        if self.scale_handling:
            self.scale_handling.to_xml(element)
        return element


class Projections(BaseNode):
    def __init__(
        self,
        projections: List["Projection"] = [],
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.projections = projections
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.projections = [Projection(xml_node=i) for i in xml_node.findall("Projection")]

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, type(self).__name__)
        for projection in self.projections:
            element.append(projection.to_xml())
        return element


class Source(BaseNode):
    def __init__(
        self,
        linked_geometry: Union[str, None] = None,
        type_: Union[str, None] = None,
        value: Union[str, None] = None,
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.linked_geometry = linked_geometry
        self.type_ = type_
        self.value = value
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.linked_geometry = xml_node.attrib.get("linkedGeometry")
        self.type_ = xml_node.attrib.get("type")
        self.value = xml_node.text

    def __str__(self):
        return f"{self.linked_geometry} {self.type_}"

    def to_xml(self):
        attributes = {}
        if self.linked_geometry:
            attributes["linkedGeometry"] = self.linked_geometry
        if self.type_:
            attributes["type"] = self.type_
        element = ElementTree.Element(type(self).__name__, **attributes)
        element.text = self.value
        return element


class Sources(BaseNode):
    def __init__(
        self,
        sources: List["Source"] = [],
        xml_node: "Element" = None,
        *args,
        **kwargs,
    ):
        self.sources = sources
        super().__init__(xml_node, *args, **kwargs)

    def _read_xml(self, xml_node: "Element"):
        self.sources = [Source(xml_node=i) for i in xml_node.findall("Source")]

    def to_xml(self, parent: Element):
        element = ElementTree.SubElement(parent, type(self).__name__)
        for source in self.sources:
            element.append(source.to_xml())
        return element
