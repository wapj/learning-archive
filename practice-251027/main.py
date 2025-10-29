import json


def read_data():
    with open("./news_metadata.json") as f:
        data = json.load(f)
        return data


if __name__ == "__main__":
    data: dict = read_data()
    for d in data:
        print(d)
