import requests
from requests.adapters import HTTPAdapter
from os import path
import os
import urllib3

urllib3.disable_warnings()

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))

save_path = path.join(os.environ['HOME'], 'Pictures')
dir_name = 'wallhaven'
save_dir = path.join(save_path, dir_name)
if not path.exists(save_dir):
    os.makedirs(save_dir)

save_path = save_path = os.path.join(save_path, dir_name)


def get_pictures(url: str) -> list:
    pic_urls = []
    response = session.get(url, timeout=(10, 10))
    if response.status_code == 200:
        js = response.json(encoding="utf-8")
        for p in js["data"]:
            print(p)
            pic_urls.append({"id": p["id"], "path": p["path"]})
    else:
        print("Get None, Code: {}".format(response.status_code))
    return pic_urls


if __name__ == "__main__":
    page = 1
    api_url = "https://wallhaven.cc/api/v1/search?apikey=OmD6tOzHlGge3MQzmxgKTnSBCpBq86gp&categories=111&purity=111&order=desc&sorting=toplist&topRange=1y&atleast=1920x1080&page={}"
    while True:
        url = api_url.format(page)
        pics = get_pictures(url)
        if not pics:
            break
        for pic in pics:
            pic_id = pic["id"]
            pic_url = pic["path"]
            parent_dir = os.path.join(save_path, pic_id[:2])
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            pic_response = session.get(pic_url)
            if pic_response.status_code == 200:
                pic_save_path = os.path.join(parent_dir, pic_id)
                with open(pic_save_path, "wb+") as f:
                    f.write(pic_response.content)
                    f.flush()
                    print("Download {} to {}".format(pic_url), pic_save_path)
        page += 1
