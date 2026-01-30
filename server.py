import httpx
import asyncio
from typing import Dict, Any, List

BASE_URL = "https://hacker-news.firebaseio.com/v0"

class HackerNewsClient:
    def __init__(self):
        self.client = httpx.AsyncClient(base_url=BASE_URL, timeout=10.0)

    async def get_item(self, item_id: int) -> Dict[str, Any]:
        url = f"/item/{item_id}.json"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # print(f"HTTP error for item {item_id}: {e}")
            return {}
        except Exception as e:
            # print(f"An error occurred while fetching item {item_id}: {e}")
            return {}

    async def recursive_download(self, item_id: int, max_depth: int, current_depth: int = 0) -> Dict[str, Any]:
        if current_depth > max_depth:
            return {"error": "Max depth reached", "id": item_id}

        item = await self.get_item(item_id)
        if not item or item.get('deleted') or item.get('dead'):
            return {}

        if 'kids' in item:
            child_tasks = []
            for kid_id in item['kids']:
                task = self.recursive_download(kid_id, max_depth, current_depth + 1)
                child_tasks.append(task)
            
            item['comments'] = await asyncio.gather(*child_tasks)
            del item['kids']
            
        return item

    async def get_top_stories(self, count: int = 10, max_depth: int = 1) -> List[Dict[str, Any]]:
        print(f"Fetching top {count} stories...")
        try:
            response = await self.client.get("/topstories.json")
            response.raise_for_status()
            top_story_ids = response.json()[:count]
        except Exception as e:
            print(f"Error fetching top stories: {e}")
            return []

        download_tasks = [
            self.recursive_download(story_id, max_depth)
            for story_id in top_story_ids
        ]

        results = await asyncio.gather(*download_tasks)
        
        return [res for res in results if res]

# FastMCP 관련 코드 추가
import json
from fastmcp.server import server

# 클라이언트 인스턴스는 한 번만 생성하여 재사용합니다.
hn_client = HackerNewsClient()

@server.Tool
async def download_hacker_news_stories(
    count: int = 10,
    max_comment_depth: int = 1,
    export_file_path: str = "hacker_news_data.json"
) -> str:
    """
    Recursively downloads the latest Hacker News stories and their comments, saving the result to a JSON file.

    Args:
        count: The number of top stories to download (max 50).
        max_comment_depth: The maximum recursive depth for downloading comments (0 for no comments).
        export_file_path: The file path to save the downloaded JSON data.
    
    Returns:
        A message containing the saved file path and the number of downloaded stories.
    """
    # count와 depth의 유효성 검사
    count = max(1, min(50, count))
    max_comment_depth = max(0, min(5, max_comment_depth))

    print(f"Starting download of {count} stories with depth {max_comment_depth}...")
    
    # 핵심 로직 호출
    results = await hn_client.get_top_stories(count=count, max_depth=max_comment_depth)
    
    # 결과를 JSON 파일로 저장
    try:
        # 파일은 workspace root 기준이므로 상대 경로를 사용합니다.
        # 이 서버는 'hacker-news-mcp' 디렉토리에서 실행될 예정입니다.
        with open(export_file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
        return f"Successfully downloaded {len(results)} stories (depth={max_comment_depth}) and saved to '{export_file_path}'"
    except Exception as e:
        return f"Error saving data to file: {e}"

# FastMCP 서버 시작
if __name__ == "__main__":
    server.start_server()

