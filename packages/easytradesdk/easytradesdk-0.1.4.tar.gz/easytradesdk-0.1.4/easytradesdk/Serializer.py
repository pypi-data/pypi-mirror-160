import abc
import decimal
import json
from datetime import datetime, date


class DefaultJsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        return o.__dict__


class DeserializableObject(metaclass=abc.ABCMeta):

    def getObjectMapper(self):
        return {}


def objectToJson(obj):
    """
        python 对象转 json 字符串
        :param obj:
        :return:
    """
    if obj is not None:
        return json.dumps(obj, cls=DefaultJsonEncoder)
    return None


def jsonToObject(jsonStr, objClass):
    """
        json 反序列化 python object, objClass 需要继承 DeserializableObject
        :param jsonStr:
        :param objClass:
        :return: objClass 不继承 DeserializableObject 则返回 dict 类型，否则返回 objClass 类型
    """
    if jsonStr:
        dictData = json.loads(jsonStr, parse_float=decimal.Decimal)
        if not issubclass(objClass, DeserializableObject):
            return dictData
        obj = objClass()
        __setAttrFromDict(obj, dictData)
        return __dictToObject0(obj)
    return None


def jsonToDict(jsonStr):
    """
        json 字符串转 python dict
        :param jsonStr:
        :return:
    """
    if jsonStr:
        return json.loads(jsonStr)
    return None


def jsonArrayToObjectList(jsonStr, objClass):
    """
        json 字符串转 python object list
        :param jsonStr:
        :param objClass:
        :return: 如果 objClass 未继承 DeserializableObject, 则默认返回 dict list
    """
    if jsonStr:
        _list = []
        _dataList = json.loads(jsonStr)
        if not isinstance(_dataList, list):
            raise Exception("json string is not json array format")
        return dictListToObjectList(_dataList, objClass)
    return []


def dictToObject(dictData, objClass):
    """
        python dict 转 python object
        :param dictData:
        :param objClass:
        :return:如果 objClass
    """
    if objClass is None or dictData is None:
        return None

    if not isinstance(dictData, dict):
        raise Exception("type of dictData is not dict")

    if not issubclass(objClass, DeserializableObject):
        return dictData

    obj = objClass()
    __setAttrFromDict(obj, dictData)
    return __dictToObject0(obj)


def dictListToObjectList(dictList, objClass):
    """
        python dict list 转 object list
        :param dictList:
        :param objClass:
        :return:
    """
    if dictList is None:
        return None

    if len(dictList) == 0:
        return []

    if not isinstance(dictList, list):
        raise Exception("type of dictList is not list")

    _list = []
    for dictData in dictList:
        _list.append(dictToObject(dictData, objClass))
    return _list


def __dictToObject0(obj):
    if isinstance(obj, list):
        for _data in obj:
            if isinstance(_data, DeserializableObject):
                __dictToObject00(_data)

    elif isinstance(obj, DeserializableObject):
        __dictToObject00(obj)
    return obj


def __dictToObject00(obj):
    _dict_data = obj.__dict__
    _object_mapper = obj.getObjectMapper()

    for _p, _class in _object_mapper.items():

        _p_name = None
        _data = None
        _className = obj.__class__.__name__
        _private_key = "_" + _className + _p

        if _p in _dict_data:
            _p_name = _p
            _data = _dict_data[_p]
        elif _private_key in _dict_data:
            _p_name = _private_key
            _data = _dict_data[_private_key]

        if _data is None:
            continue

        if _class == dict:

            if isinstance(_data, str):
                try:
                    _data = json.loads(_data, parse_float=decimal.Decimal)
                except Exception as e:
                    print(e)

            if isinstance(_data, dict):
                setattr(obj, _p_name, _data)
                continue

            if isinstance(_data, list):
                _list = []
                for _d in _data:
                    if isinstance(_d, dict):
                        _list.append(_d)
                setattr(obj, _p_name, _list)
                continue

        if _class == decimal.Decimal:
            if isinstance(_data, str):
                setattr(obj, _p_name, decimal.Decimal(_data))
                continue

        if _class == datetime:
            if isinstance(_data, str):
                setattr(obj, _p_name, datetime.strptime(_data, "%Y-%m-%d %H:%M:%S"))
                continue

        if _class == date:
            if isinstance(_data, str):
                setattr(obj, _p_name, datetime.strptime(_data, "%Y-%m-%d").date())
                continue

        if not issubclass(_class, DeserializableObject):
            continue

        if isinstance(_data, str):
            try:
                _data = json.loads(_data, parse_float=decimal.Decimal)
            except Exception as e:
                print(e)

        if isinstance(_data, dict):
            __dictToObject0(__resolveDict(obj, _p_name, _class, _data))

        elif isinstance(_data, list):
            __dictToObject0(__resolveDictList(obj, _p_name, _class, _data))
        else:
            _o = _class()
            setattr(obj, _p_name, _o)
            __dictToObject0(_o)


def __resolveDict(obj, p_name, _class, dict_data):
    _o = _class()
    __setAttrFromDict(_o, dict_data)
    setattr(obj, p_name, _o)
    return _o


def __resolveDictList(obj, p_name, _class, dict_list):
    _l = []
    for _d in dict_list:
        _o = _class()
        if isinstance(_d, dict):
            __setAttrFromDict(_o, _d)
        _l.append(_o)
    setattr(obj, p_name, _l)
    return _l


def __setAttrFromDict(obj, dict_data):
    for _k, _v in dict_data.items():
        setattr(obj, _k, _v)
