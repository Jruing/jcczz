# encoding:utf-8
# 处理羁绊
import pathlib
import json

# 数据处理
class DataBatch:
    def __init__(self):
        zhiye_path = pathlib.Path()
        self.zhiye_json = zhiye_path.absolute().joinpath("data").joinpath("zhiye.json")
        tezhi_path = pathlib.Path()
        self.tezhi_json = tezhi_path.absolute().joinpath("data").joinpath("tezhi.json")
        hero_path = pathlib.Path()
        self.hero_json = hero_path.absolute().joinpath("data").joinpath("hero.json")
        self.zhiye_list = []
        self.tezhi_list=[]
        self.hero_list = []
        self.zhiye_data(self.zhiye_json)
        self.tezhi_data(self.tezhi_json)
        self.hero_data(self.hero_json)

    # 职业数据解析
    def zhiye_data(self,zhiye_json_path):
        zhiye_json = []
        with open(zhiye_json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            zhiye = json.loads(content)['data']
            for k, v in zhiye.items():
                zhiye_json.append({"id": v['id'], "name": v["name"]})
        unique_data = [dict(t) for t in {tuple(d.items()) for d in zhiye_json}]
        self.zhiye_list = [{i["name"]: i["id"]} for i in unique_data]

    # 特质数据解析
    def tezhi_data(self, tezhi_json_path):
        tezhi_json = []
        with open(tezhi_json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            jiban = json.loads(content)['data']
            for k,v in jiban.items():
                tezhi_json.append({"id":v['id'],"name":v["name"]})
        unique_data = [dict(t) for t in {tuple(d.items()) for d in tezhi_json}]
        self.tezhi_list = [ {i["name"]:i["id"]} for i in unique_data]

    # 英雄数据解析
    def hero_data(self, hero_json_path):
        # 处理英雄
        with open(hero_json_path, 'r', encoding='utf-8') as f:
            content = f.read()
            hero = json.loads(content)['data']
            for k,v in hero.items():
                tezhi,zhiye = [],[]
                if "|" in v["class"]:
                    d = v["class"].split("|")
                    for i in d:
                        tezhi.append(int(i))
                else:
                    tezhi.append(int(v["class"]))

                if "|" in v["species"]:
                    d = v["species"].split("|")
                    for i in d:
                        zhiye.append(int(i))
                else:
                    zhiye.append(int(v["species"]))

                self.hero_list.append({"id":v['id'],"name":v["name"],"zhiye":list(set(tezhi)),"tezhi":list(set(zhiye)),"price":int(v["price"])})

    # 封装数据
    def save_data(self):
        # 特质+职业+费用组成key
        result = {}
        for i in self.tezhi_list:
            for j in self.zhiye_list:
                for k in range(1,6):
                    key = f"{list(i.values())[0]}_{list(j.values())[0]}_{k}"
                    result[key] = []
        for k,v in result.items():
            tezhi,zhiye,price = k.split("_")
            for h in self.hero_list:
                if int(tezhi) in h["tezhi"] and int(zhiye) in h["zhiye"] and int(price) == h["price"]:
                    result[k].append(h["name"])
        result["226_0_5"] = []
        for h in self.hero_list:
            if h['name'] in ("索拉卡","费德提克","厄加特","奇亚娜","丽桑卓","贝蕾亚","慧","卑尔维斯","米利欧","娑娜"):
                result["226_0_5"].append(h["name"])
        result_copy = result.copy()
        for key,value in result_copy.items():
            if value:
                result[key] = list(set(value))
            else:
                result.pop(key)
        return result
# if __name__ == '__main__':
#     a = DataBatch()
#     print(a.tezhi_list)
#     print(a.zhiye_list)
#     print(a.hero_list)
#     print(a.save_data())