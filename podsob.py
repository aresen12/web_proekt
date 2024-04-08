import json

file = open('config.csv', encoding='utf-8')
data = file.readlines()[1:]
print(data)
file.close()
sl = []
file_out = open("config.json", encoding='utf-8', mode="w")
for i in range(0, len(data), 3):
    try:
        sl.append([{"title": data[i + 1].split(";")[1], "file": data[i + 1].split(";")[0]},
               {"title": data[i].split(";")[1], "file": data[i].split(";")[0]},
               {"title": data[i + 2].split(";")[1], "file": data[i + 2].split(";")[0]}])
    except Exception:
        pass
file_out.write(json.dumps(sl, ensure_ascii=False))
file_out.close()
