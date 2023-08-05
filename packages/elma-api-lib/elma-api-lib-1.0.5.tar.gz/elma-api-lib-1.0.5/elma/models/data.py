import json
from typing import Optional


class Data:
    def __init__(self, items: [] = None, value: str = None) -> None:
        if items is None:
            items = []
        self.items = items
        self.value = value

    def __str__(self) -> str:
        return data_to_json_str(self) \
            .replace("\"null\"", "null") \
            .replace("\"[]\"", "[]") \
            .replace("{}", "null")

    def to_obj(self) -> dict:
        obj = {}
        for data_item in self.items:
            name = data_item.name
            if data_item.value is not None and str(data_item.value) != "null":
                obj[name] = data_item.value
            elif data_item.data is not None and str(data_item.data) != "null":
                obj[name] = data_item.data.to_obj()
            elif data_item.data_array is not None and str(data_item.data_array) != "[]":
                obj_array = []
                for data in data_item.data_array:
                    obj_array.append(data.to_obj())
                obj[name] = obj_array
            else:
                obj[name] = None
        return obj

    @staticmethod
    def from_json(json: dict):
        return dict_to_data(json)


class DataItem:
    def __init__(self, name: str = None, value: str = None, data: Data = None, data_array: [] = None) -> None:
        if data_array is None:
            data_array = []
        self.name = name
        self.value = value
        self.data = data
        self.data_array = data_array

    def __str__(self) -> str:
        return data_item_to_json_str(self) \
            .replace("\"null\"", "null") \
            .replace("\"[]\"", "[]") \
            .replace("{}", "null")

    @staticmethod
    def from_json(json: dict):
        return dict_to_data_item(json)


def data_item_to_dict(data_item: DataItem) -> Optional[dict]:
    result = {}
    if data_item is not None:
        transformed_data = data_to_dict(data_item.data)
        transformed_data_array = []
        for data in data_item.data_array:
            jd = data_to_dict(data)
            transformed_data_array.append(jd)
        if data_item.name is not None:
            result["Name"] = data_item.name
        else:
            result["Name"] = "null"
        if data_item.value is not None:
            result["Value"] = data_item.value
        else:
            result["Value"] = "null"
        if transformed_data is not None:
            result["Data"] = transformed_data
        else:
            result["Data"] = "null"
        if transformed_data_array is not None and len(transformed_data_array) > 0:
            result["DataArray"] = transformed_data_array
        else:
            result["DataArray"] = "[]"
    else:
        return None
    return result


def data_item_to_json_str(data_item: DataItem) -> str:
    return json.dumps(data_item_to_dict(data_item))


def data_to_dict(data: Data) -> dict:
    result = {}
    if data is not None:
        transformed_data_items = []
        for dataItem in data.items:
            jdi = data_item_to_dict(dataItem)
            transformed_data_items.append(jdi)
        if transformed_data_items is not None and len(transformed_data_items) > 0:
            result["Items"] = transformed_data_items
        if data.value is not None:
            result["Value"] = data.value
    return result


def data_to_json_str(data: Data) -> str:
    return json.dumps(data_to_dict(data))


def dict_to_data(json_data: dict) -> Data:
    result = Data()
    if json_data is not None:
        transformed_data_items = []
        for dataItem in json_data['Items']:
            jdi = dict_to_data_item(dataItem)
            transformed_data_items.append(jdi)
        if transformed_data_items is not None and len(transformed_data_items) > 0:
            result.items = transformed_data_items
        value = json_data['Value']
        if value is not None:
            result.value = value
    return result


def dict_to_data_item(json_item: dict) -> Optional[DataItem]:
    result = DataItem()
    if json_item is not None:
        transformed_data = dict_to_data(json_item['Data'])
        transformed_data_array = []
        for data in json_item['DataArray']:
            jd = dict_to_data(data)
            transformed_data_array.append(jd)
        name = json_item['Name']
        if name is not None:
            result.name = name
        value = json_item['Value']
        if value is not None:
            result.value = value
        if transformed_data is not None:
            result.data = transformed_data
        if transformed_data_array is not None and len(transformed_data_array) > 0:
            result.data_array = transformed_data_array
    else:
        return None
    return result
