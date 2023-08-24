from common.exceptions import ApplicationError
from typing import Dict, TYPE_CHECKING
from enum import Enum as BuiltInEnum, EnumMeta
import inspect
import inflection

__codelist_enum_registry__: Dict[str, BuiltInEnum] = {}


def parse_entity_meta_from_enum_doc(origin_doc, enum_class) -> dict:
    '''要求的 doc 格式:
    """
    枚举类型的中文说明
    :枚举变量名 :枚举变量中文名(name) :枚举变量名(英文, 可选)
    """
    枚举变量名 = '枚举变量值(code)'
    '''
    lines = origin_doc.split("\n")
    field_map = {}
    entity = dict(
        id=inflection.underscore(enum_class.__name__),
        key=inflection.underscore(enum_class.__name__),
        name=inflection.titleize(enum_class.__name__),
        allow_custom=False,
    )
    entity_items = []
    desc = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            if line.startswith(":"):
                parts = line.split(":")
                if len(parts) < 3:
                    continue
                field_map[parts[1].strip()] = dict(
                    name=parts[2].strip(), name_en=parts[3].strip() if len(parts) > 3 else None
                )
            else:
                if i == 0 and line != "An enumeration.":
                    entity["name"] = line
                else:
                    desc.append(line)
    if desc:
        entity["desc"] = "\n".join(desc)
    for enum_item in enum_class:
        entity_item = dict(
            name=inflection.titleize(enum_item.name),
            code=enum_item.value,
            entity=inflection.underscore(enum_class.__name__),
        )
        if isinstance(enum_item.value, (int, float)):
            entity_item["value"] = enum_item.value
        field_doc_meta = field_map.get(enum_item.name)
        if field_doc_meta:
            entity_item["name"] = field_doc_meta["name"]
            entity_item["name_en"] = field_doc_meta.get("name_en", inflection.titleize(enum_item.name))
        entity_items.append(entity_item)
    entity["entity_items"] = entity_items
    return entity


class CodeListEnumMeta(EnumMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        if name in __codelist_enum_registry__:
            raise ApplicationError(
                f"""CodeListEnum类名 `{name}` 已被注册. CodeListEnum的类名要求全局唯一, 请更换一个类名, 或直接继承内建 Enum 类型;"""
            )
        super_new = super(CodeListEnumMeta, mcs).__new__
        # 从Enum注释中读取枚举选项的name等信息
        new_class = super_new(mcs, name, bases, namespace)
        if name != "CodeListEnum":
            origin_doc = inspect.getdoc(new_class)
            new_class.__entity__ = parse_entity_meta_from_enum_doc(origin_doc, new_class)
            __codelist_enum_registry__[name] = new_class
        return new_class


class CodeListEnum(BuiltInEnum, metaclass=CodeListEnumMeta):
    """可根据注释获取枚举项名称等meta信息的枚举类型"""

    if TYPE_CHECKING:
        __entity__: Dict

    @property
    def doc_name(self):
        for item in self.__entity__["entity_items"]:
            if item["code"] == self.value:
                return item["name"]
        return ""

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


class ServiceModeEnum(str, CodeListEnum):
    """ """

    API = "api"
    BEAT = "beat"
    WORKER = "worker"
    MONITOR = "monitor"
    SHELL = "shell"
