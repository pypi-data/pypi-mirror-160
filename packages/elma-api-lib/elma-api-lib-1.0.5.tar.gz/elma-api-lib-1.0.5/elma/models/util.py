import json

from elma.models.data import Data, DataItem


class JsonSerializable:
    class JsonData(dict):

        def __str__(self):
            return json.dumps(self)

    @staticmethod
    def from_json(obj: dict):
        return JsonSerializable()

    def to_json(self):
        return JsonSerializable.JsonData(self.__dict__)


class DataSerializable:
    def to_Data(self) -> Data:
        items = []
        for k, v in self.__dict__.items():
            data_item = DataItem()
            data_item.name = k
            data_item.data = Data()
            data_item.data_array = []
            data_item.value = "null"
            if v is None:
                data_item = None
            elif isinstance(v, DataItem):
                data_item = v
            elif isinstance(v, Data):
                data_item.data = v
            elif isinstance(v, DataSerializable):
                data_item.data = v.to_Data()
            elif isinstance(v, type([])):
                res = v
                for i in range(0, len(v)):
                    vi = v[i]
                    if isinstance(vi, DataSerializable):
                        res[i] = vi.to_Data()
                data_item.data_array = res
            else:
                data_item.value = v
            if data_item is not None:
                items.append(data_item)
        return Data(items=items)


class DataItemSerializable:
    def to_DataItem(self) -> DataItem:
        name = self.__class__.__name__
        value = None
        data = Data()
        data_array = []
        for k, v in self.__dict__.items():
            name = k
            if v is None:
                pass
            elif isinstance(v, Data):
                data = v
            elif isinstance(v, DataSerializable):
                data = v.to_Data()
            elif isinstance(v, type([])):
                res = v
                for i in range(0, len(v)):
                    vi = v[i]
                    if isinstance(vi, DataSerializable):
                        res[i] = vi.to_Data()
            else:
                value = v
            break
        return DataItem(name=name, value=value, data=data, data_array=data_array)


def init_class(o, cls):
    if o is None:
        return None
    elif isinstance(o, dict):
        return cls(**o)


def init_list(lst, cls):
    if lst is None:
        return []
    else:
        return [init_class(i, cls) for i in lst]


def init_data(d):
    if d is not None and isinstance(d, dict):
        return Data.from_json(d)
    else:
        return d
