import httpx
from bs4 import BeautifulSoup

client = httpx.Client(timeout=15, follow_redirects=True)
r = client.get("https://www.yntw.com/", headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, "lxml")

# 找所有带链接的标题
for tag in ["article", "div", "li", "section"]:
    items = soup.find_all(tag, class_=True)
    if items:
        classes = set()
        for item in items:
            for c in item.get("class", []):
                classes.add(c)
        if classes:
            print(f"[{tag}] classes: {classes}")

# 直接找标题链接
print("\n=== 所有 h2/h3 a 前10个 ===")
for i, a in enumerate(soup.select("h2 a, h3 a")):
    if i >= 10:
        break
    text = a.get_text(strip=True)
    href = a.get("href", "")
    parent_class = " ".join(a.parent.get("class", []))
    print(f"  [{parent_class}] {text[:60]} -> {href}")

print("\n=== 纯文本链接 (含/2026/) 前10个 ===")
count = 0
for a in soup.find_all("a", href=True):
    if "/2026/" in a["href"]:
        text = a.get_text(strip=True)
        if len(text) > 5:
            print(f"  {text[:60]} -> {a['href']}")
            count += 1
            if count >= 10:
                break

client.close()
