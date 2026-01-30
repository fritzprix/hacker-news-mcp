# Hacker News MCP Server

이 프로젝트는 Python의 **FastMCP** 라이브러리를 사용하여 구현된 [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/spec) 서버입니다. LLM 에이전트가 Hacker News API와 상호작용하여 데이터를 검색하고 분석할 수 있도록 설계되었습니다.

## 특징

- **Hacker News API 연동:** 실시간으로 인기 게시물, 사용자 정보 및 댓글을 조회할 수 있는 도구를 제공합니다.
- **FastMCP 기반:** 빠르고 효율적인 Python MCP 서버 구현을 제공합니다.

## 설치 및 실행

### 1. 의존성 설치

프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 필요한 의존성을 설치합니다.

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. 서버 실행

다음 명령어로 MCP 서버를 실행합니다.

\`\`\`bash
python server.py
\`\`\`

서버가 실행되면, 클라이언트 (예: LibrAgent)는 `stdio` 또는 `http` 전송 방식을 통해 이 서버에 연결하여 Hacker News 관련 작업을 수행할 수 있습니다.

## 사용 가능한 도구 (LLM 에이전트용)

서버가 제공하는 구체적인 도구 목록은 연결된 LLM 에이전트 환경에서 확인할 수 있습니다. 일반적으로 다음과 같은 도구들이 포함됩니다.

- `get_top_stories`: 현재 인기 있는 기사 목록을 가져옵니다.
- `get_item_details`: 특정 ID의 기사, 댓글, 또는 사용자 정보를 가져옵니다.
- `get_user_info`: 특정 사용자의 프로필 정보를 가져옵니다.

## 정리된 파일 목록

- \`.gitignore\`: Git 버전 관리에서 제외할 파일 목록
- \`requirements.txt\`: Python 의존성 목록 (\`fastmcp\`, \`httpx\`)
- \`server.py\`: MCP 서버의 메인 구현 파일
- \`README.md\`: 이 문서 (프로젝트 개요 및 사용법)
