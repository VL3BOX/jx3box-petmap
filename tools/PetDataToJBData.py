import luadata, json

SRC_PATH = r"../source/zhcn_hd.jx3dat"
DST_PATH = r"../output/PetPOIs.json"
MAPS_PATH = r"../output/PetMaps.json"

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


with open(SRC_PATH, "r", encoding="gb2312") as fs:
    pets, pois = luadata.unserialize(fs.read()[7:], G=GLOBAL_IDENTIFIERS)
ret = {}
maps = {}
for pet in pets:
    subPOIs = []
    for poiInfo in [i for i in pois if i["nSerendipityID"] == pet["nID"]]:
        subPOIs.append({
            "WorkType": poiInfo.get("szType", ""),
            "ObjectType": poiInfo.get("dwType", 0),
            "ObjectID": poiInfo.get("dwID", 0),
            "MapID": poiInfo.get("dwMapID", 0),
            "Coordinates": [{ "x": i[0], "y": i[1], "z": i[2] } for i in poiInfo.get("aPosition", [])]
        })
        maps[poiInfo.get("dwMapID")] = True
    ret[pet["dwPet"]] = subPOIs

with open(DST_PATH, "w", encoding="utf-8") as fs:
    fs.write(json.dumps(ret, indent=4, ensure_ascii=False))
with open(MAPS_PATH, "w", encoding="utf-8") as fs:
    fs.write(json.dumps(list(maps.keys()), indent=4, ensure_ascii=False))
