import json


def load_json_config():
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
        except IndexError:
            try:
                sl.append([{"title": data[i].split(";")[1], "file": data[i].split(";")[0]},
                           {"title": data[i + 1].split(";")[1], "file": data[i + 1].split(";")[0]}
                           ])
            except IndexError:
                sl.append(sl.append([{"title": data[i].split(";")[1], "file": data[i].split(";")[0]}, ]))
    print(sl)
    while None in sl:
        del sl[-1]
    print(sl)
    file_out.write(json.dumps(sl, ensure_ascii=False))
    file_out.close()


if __name__ == "__main__":
    load_json_config()
