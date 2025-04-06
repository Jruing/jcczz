# encoding:utf8
import requests

hero_response =requests.get("https://game.gtimg.cn/images/lol/act/jkzlk/js//1/1.0.0-S1/chess.js")
print(hero_response.json())
with open("hero.json", "w",encoding="utf8") as f:
    f.write(hero_response.text)



zhiye_response = requests.get("https://game.gtimg.cn/images/lol/act/jkzlk/js//1/1.0.0-S1/job.js")
print(zhiye_response)
with open("zhiye.json", "w",encoding="utf8") as f:
    f.write(zhiye_response.text)


tezhi_response = requests.get("https://game.gtimg.cn/images/lol/act/jkzlk/js//1/1.0.0-S1/race.js")
print(tezhi_response)
with open("tezhi.json", "w",encoding="utf8") as f:
    f.write(tezhi_response.text)