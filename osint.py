import googlesearch as gs
import requests as req

def google(prompt, n):
    s = gs.search(prompt, stop=n)
    results = [_ for _ in s]
    return results
        
def eval_link(link):
    data = {}
    if not (link.startswith("http://") or link.startswith("https://")):
        link = "http://"+link

    response = req.get(link)
    data["Content-Type"] = response.headers["Content-Type"]
    content = response.content.decode(response.encoding or "UTF-8", errors="ignore").split(">")
    content = [_+">" for _ in content]
    
