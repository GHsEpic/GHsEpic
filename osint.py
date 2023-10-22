import requests as req

s = req.Session()

def post(url, data):
    try:
        response = s.post(url, data=data)
        if response.ok:
            return response
        else:
            response = s.get(url)
            if response.ok:
                return response
    except:
        return False

def tree(url, payload, depth, a=0):
    if a >= depth:
        return []
    
    response = post(url, payload)
    if type(response) != req.Response:
        return []
    content = response.content.decode(response.encoding or "UTF-8", errors="ignore")
    response = [_.split("'") for _ in content.split('"')]

    temp_list = []
    for temp in response:
        for _ in temp:
            temp_list.append(_)

    response = [_.replace(" ", "") for _ in temp_list]#[_.replace(" ", "").replace("<", "").replace(">", "").replace("!", "").replace(",", "").replace(";", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "") for _ in temp_list]

    temp_list = []
    for i, _ in enumerate(response):
        if "href" in _:
            #print(_)
            if response[i+1].startswith("http"):
                temp_list.append(response[i+1])
            else:
                _ = url.split("/")
                _ = "/".join(_[0:len(_)-1])
                temp_list.append(_+response[i+1])

    response = []
    for _ in temp_list:
        if (not "function" in _) and (_.startswith(r"http://") or _.startswith(r"https://")) and not (_.endswith(".js") or _.endswith(".css")):
            response.append(_)

    found_urls = [_ for _ in response]
    for i, url in enumerate(response):
        print(f"{'  '*a}|- Searching {i+1}/{len(response)}")
        result = tree(url, payload, depth, a+1)
        found_urls += result
    return found_urls

def eval_urls(urls, payload, keywords):
    data = {}
    for i, url in enumerate(urls):
        print(f"Scanning {i+1}/{len(urls)}")
        response = post(url, payload)
        if type(response) == req.Response:
            #print(response.content)
            content = response.content.decode(response.encoding or "UTF-8", errors="ignore").lower()
            for kw in keywords:
                if kw.lower() in content:
                    data[url] = True
                else:
                    data[url] = False
        else:
            data[url] = False
    return data

payload = {"username":"emmertf", "password":"---", "sesskey":"jwzfGWYzo1"}
a = tree("https://moodle.ewg-sha.de/moodle/login/index.php", payload, 2)
b = eval_urls(a, payload, ["bangert"])
