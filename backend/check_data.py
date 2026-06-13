import httpx, json

r1 = httpx.get("http://127.0.0.1:8000/api/v1/dashboard/summary")
print("仪表盘:", json.dumps(r1.json(), ensure_ascii=False, indent=2))

r2 = httpx.get("http://127.0.0.1:8000/api/v1/news")
news = r2.json()
print(f"\n新闻: {len(news)} 条")
for n in news[:5]:
    print(f"  [{n['source']}] {n['title'][:60]}")
    if n.get("summary"):
        print(f"         摘要: {n['summary'][:80]}")
