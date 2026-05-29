import urllib.request, json, re

req = urllib.request.Request(
    "https://api.juejin.cn/content_api/v1/article/query_list",
    data=json.dumps({"user_id":"1227480633975166","sort_type":2,"cursor":"0"}).encode(),
    headers={"Content-Type":"application/json"})

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())

arts = data.get("data", [])
lines = []
for a in arts:
    i = a["article_info"]
    lines.append(f"- [{i['title']}](https://juejin.cn/post/{i['article_id']})")

content = "\n".join(lines) if lines else "*No articles*"
marker_start = "<!-- BLOG-POST-LIST:START -->"
marker_end = "<!-- BLOG-POST-LIST:END -->"
result = marker_start + "\n" + content + "\n" + marker_end

with open("README.md") as f:
    readme = f.read()

new_readme = re.sub(
    marker_start + ".*?" + marker_end,
    result, readme, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(new_readme)

print(f"OK: {len(arts)} articles updated")
