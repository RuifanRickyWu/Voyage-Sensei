import requests

# 你的 Google API Key 和 Custom Search Engine ID (cx)
API_KEY = "AIzaSyCbWt8HLsCj3q2vzCQyJNWbjFRtoWkEAP0"
CX = "a19f3b2e14e6e436b"


def google_search(query, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,  # 搜索关键词
        "key": API_KEY,  # API Key
        "cx": CX,  # Custom Search Engine ID
        "num": num_results,  # 返回的搜索结果数
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("搜索失败:", response.json())
        return None


def parse_results(results):
    if not results or "items" not in results:
        return "没有找到相关结果。"

    output = []
    for item in results["items"]:
        print(item)
        title = item["title"]
        link = item["link"]
        snippet = item.get("snippet", "无摘要信息")
        output.append(f"**{title}**\n{snippet}\n[链接]({link})\n")

    return "\n".join(output)


# 示例: 进行搜索
query = "event for rogers center in feb 1 2025"
search_results = google_search(query, num_results=5)
print(parse_results(search_results))