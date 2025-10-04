# LangChain と LangGraph による RAG・AI エージェント［実践］入門

https://github.com/GenerativeAgents/agent-book をベースに AI Agent の学習を目的とした repo

## setup

```bash
pyenv local 3.12

uv sync --all-groups

uv run python main.py
```

```bash
pyenv local 3.12

uv sync --all-groups

uv run python -m documentation_agent.main --task "スマートフォン向けの健康管理アプリを開発したい"
```