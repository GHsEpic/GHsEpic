import googlesearch as gs
import requests as req

def google(prompt, n):
	s = gs.search(prompt, stop=n)
	results = [_ for _ in s]
	return results
        
def eval_link(link, keywords):
	data = {}
	if not (link.startswith("http://") or link.startswith("https://")):
		link = "http://"+link

	response = req.get(link)
	data["Content-Type"] = response.headers["Content-Type"]
	content = response.content.decode(response.encoding or "UTF-8", errors="ignore").replace(" ", "").split("\n")

	data["found_keywords"] = {}
	important = []
	for _ in content:
		for kw in keywords:
			data["found_keywords"][kw] = []
			if kw.lower() in _.lower():
				data["found_keywords"][kw].append(_)
				important.append(_)
	
	data["found_links"] = []
	for _ in important:
		if "href=" in _:
			_ = _.split("'")
			for i, . in enumerate(_):
				if "href=" in .:
					link_index = i+1
					break
		data["found_links"].append(_[link_index])

	return data
