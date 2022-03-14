import codecs, pandas, luadata, os, json
from re import sub
from multiprocessing.sharedctypes import Value

SRC_PATH = "D:\\Download\\宠物奇遇_new.txt"
POS_PATH = "D:\\Download\\宠物奇遇_new_pos.txt"
DST_PATH = "D:\\Download\\PetOutput.json"
GLOBAL_IDENTIFIERS = {
    "ITEM_TABLE_TYPE": { 
        "ATTRIB": 1,
        "OTHER": 5,
        "CUST_WEAPON": 6,
        "CUST_ARMOR": 7,
        "CUST_TRINKET": 8,
        "SET": 9,
    },

    "TARGET": {
        "NO_TARGET": 1,
        "COORDINATION": 2,
        "NPC": 3,
        "PLAYER": 4,
        "DOODAD": 5,
        "ITEM": 6,
    }
}

def ProcessGlobal(path):
    keys = path.split('.')
    current = GLOBAL_IDENTIFIERS
    for key in keys:
        if key in current:
            current = current[key]
        else:
            return None
    return current

# 解析数组
def ProcessArray(value):
    return luadata.unserialize(value, G=GLOBAL_IDENTIFIERS)

# 解析物品数组
def ProcessItemArray(value):
    return [{"type": i[0], "id": int(i[1])} for i in luadata.unserialize(value, G=GLOBAL_IDENTIFIERS)]

# 解析坐标数组
def ProcessCoordinateArray(value):
    return [{"x": i[0], "y": i[1], "z": i[2]} for i in luadata.unserialize(value, G=GLOBAL_IDENTIFIERS)]

# 通过路径向字典插入一个数据，不存在则创建
def InsertDictByPath(obj, path, value):
    # Nested array is not supported!
    if len(path) == 0:
        raise ValueError("Empty path")
    if path.startswith("$."):
        path = path[2:]
    pathComponents = path.split(".")
    currentItem = obj
    for i in range(len(pathComponents)):
        currentKey = pathComponents[i]
        if currentKey == "":
            raise ValueError("Empty key")
        if i == len(pathComponents) - 1:
            currentItem[currentKey] = value
        else:
            if currentKey not in currentItem:
                currentItem[currentKey] = dict()
            currentItem = currentItem[currentKey]
            if not isinstance(currentItem, dict):
                raise ValueError("Item exists and isn't a dict")

# 从一行记录生成一个数据
def ProcessRow(headers, values):
    subItem = {}
    for i in range(len(values)):
        path = headers[i][1]
        type = headers[i][0]
        value = values[i]
        if path.startswith('Unnamed') or type.startswith('Unnamed'):
            continue
        if not pandas.notna(value):
            continue
        if type == "number":
            value = int(value)
        elif type == "string":
            value = str(value)
        elif type == "strings" or type == "numbers":
            value = ProcessArray(value)
        elif type == "items":
            value = ProcessItemArray(value)
        elif type == "coordinates":
            value = ProcessCoordinateArray(value)
        elif type == "global":
            value = ProcessGlobal(value)
        else:
            raise ValueError("Unknown column type")
        InsertDictByPath(subItem, path, value)
    return len(subItem) > 0 and subItem or None

def LoadPOIData():
    ret = {}
    for _, row in pandas.read_csv(POS_PATH, sep='\t', encoding="gb2312", skiprows=1, header=[0, 1]).iterrows():
        subItem = ProcessRow(row.index, row.values)
        if subItem:
            key = subItem["ID"]
            if key not in ret:
                ret[key] = []
            ret[key].append(subItem)
    return ret

def LoadItemData():
    ret = []
    for _, row in pandas.read_csv(SRC_PATH, sep='\t', encoding="gb2312", skiprows=2, header=[0, 1]).iterrows():
        subItem = ProcessRow(row.index, row.values)
        if subItem:
            ret.append(subItem)
    return ret

def Main():
    pois = LoadPOIData()
    items = LoadItemData()
    for item in items:
        if item["ID"] in pois:
            item["POIs"] = pois[item["ID"]]
    with open(DST_PATH, "w", encoding="gb2312") as fs:
        fs.write(json.dumps(items, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    Main()
