import json

def createJson(n,t,target):
    dataset = []
    res = {}
    for i in range(0,len(n)):
        data = {
            'Num':n[i],
            'Time':t[i],
        }
        dataset.append(data)
    res["target"] = "Bus"
    res["data"] = dataset

    print()
    with open('data.json', 'w') as json_file:
        json.dump(res,json_file,indent=4)