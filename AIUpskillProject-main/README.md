# AI Upskill Project

**Multi-agent news aggregation system with MCP integration**
A production-ready AI agent pipeline that fetches, filters, summarizes, and writes AI/ML news newsletters.

## Features

- 🚀 **Async News Fetching** from multiple sources (HackerNews, RSS)
- 🤖 **AI-Powered Filtering** via LiteLLM (default: Claude Haiku 4.5; swap providers via env var)
- 🔧 **MCP Integration** with reusable tools
- 📝 **Multi-Agent Pipeline** (Filter → Summarize → Write)
- 💾 **SQLite Database** for article storage
- 📊 **Evaluation Framework** for quality measurement
- ✅ **60%+ Test Coverage**

## Quick Start

### Prerequisites

- Python 3.11+
- One LLM provider API key (Anthropic recommended; OpenAI, Gemini, or any other [LiteLLM-supported provider](https://docs.litellm.ai/docs/providers) also works)

### Tech stack
Python 3.11+ with async/await throughout
aiohttp for concurrent HTTP, feedparser for RSS
LiteLLM as the LLM provider abstraction — default model is claude-haiku-4-5-20251001, swap to any LiteLLM-supported provider by changing one env var
MCP (Model Context Protocol) for tool integration in Milestone 4
SQLite for the database server in Milestone 4
pytest + pytest-asyncio for tests
ruff for formatting and linting


### Architecture

┌─────────────────────────────────────────────┐
│         News Sources                         │
│  HackerNews | RSS Feeds | GitHub Trending   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
        ┌──────────────────┐
        │ Fetch Orchestrator│
        │   (Milestone 1)   │
        └──────────┬────────┘
                   │
                   ▼
            ┌──────────┐
            │ Database │ ← MCP Server
            │ (SQLite) │
            └──────────┘
                   │
                   ▼
        ┌──────────────────┐
        │  FilterAgent      │
        │   (LLM + Tools)   │
        └──────────┬────────┘
                   │
                   ▼
        ┌──────────────────┐
        │ SummarizerAgent   │
        │  (+ SearchSkill)  │
        └──────────┬────────┘
                   │
                   ▼
        ┌──────────────────┐
        │  WriterAgent      │
        │   (Newsletter)    │
        └──────────┬────────┘
                   │
                   ▼
           📄 Newsletter.md

### Project Structure

AIUpskillProject/
├── src/
│   ├── agents/          # AI agents
│   │   ├── base_agent.py
│   │   ├── news_filter_agent.py
│   │   ├── summarizer_agent.py
│   │   └── writer_agent.py
│   ├── fetchers/        # News fetchers
│   ├── mcp_servers/     # MCP servers
│   │   ├── database_server.py
│   │   └── simple_client.py
│   ├── skills/          # Reusable skills
│   │   └── search_skill.py
│   ├── tools/           # LLM-callable tools (calculator, web_search)
│   ├── evaluation/      # Evaluation framework
│   └── complete_pipeline.py
├── tests/               # Test suite
├── data/
│   ├── articles/        # Fetched articles
│   ├── context/         # Agent outputs
│   ├── output/          # Final newsletter
│   └── evaluation/      # Evaluation data
└── docs/                # Documentation


# Run the complete pipeline
python src/complete_pipeline.py

 Output will be in:
 - data/output/newsletter.md (final newsletter)
- data/context/ (intermediate outputs)
- data/news_agent.db (article database)

# Milestone Completed

✅ Milestone 0: Setup
✅ Milestone 1: Async News Fetcher
✅ Milestone 2: SOLID Refactoring
✅ Milestone 3: First Agent with Tools
✅ Milestone 4: MCP-Powered Pipeline
✅ Milestone 5: Evaluation & Documentation

# Evaluation Metrics
Accuracy: 85%+
Precision: 90%+
Recall: 80%+
F1 Score: 0.850+
See: data/evaluation/evaluation_report.md

# Running Tests

Run all tests-
pytest tests/ -v

Run with coverage-
pytest tests/ --cov=src --cov-report=term-missing

Target: 60%+ coverage ✅

# Adding New Sources
Create fetcher in src/fetchers/
Inherit from BaseFetcher
Implement fetch_articles() and get_source_name()
Register in FetchOrchestrator

# Adding New MCP Tools
Add tool schema to MCP server
Implement tool function
Register in @server.call_tool()
Test with MCP client

# License
MIT

# Acknowledgments

---

### **Step 2: Architecture Documentation (45 min)**

**File:** `docs/architecture.md`

```markdown
# Architecture Documentation

## System Overview

Multi-agent AI system for news aggregation and newsletter generation.

## Design Principles

1. **SOLID Principles**
   - Single Responsibility: Each agent has one job
   - Open/Closed: Easy to add new sources/agents
   - Dependency Inversion: Agents depend on abstractions

2. **Design Patterns**
   - Template Method: BaseAgent
   - Factory: FetcherFactory
   - Strategy: Rate limiting
   - Observer: Pipeline coordination

3. **Async-First**
   - All I/O is async
   - Concurrent fetching
   - Non-blocking operations

## Component Details

### 1. Fetchers (Milestone 1)

**Purpose:** Fetch articles from external sources

**Sources:**
- HackerNews API
- RSS feeds

**Key Features:**
- Async concurrent fetching
- Rate limiting (10 concurrent max)
- Error handling
- Markdown output

### 2. Agents (Milestones 3-4)

**BaseAgent:**
- Template Method pattern
- Consistent lifecycle: load → process → save
- LLM integration
- Tool support

**NewsFilterAgent:**
- Filters AI/ML relevant articles
- Uses the configured LLM (via LiteLLM) for classification
- Returns relevance scores
- JSON output parsing

**SummarizerAgent:**
- Groups articles by topic
- Generates topic summaries
- Can use SearchSkill for context

**WriterAgent:**
- Writes engaging newsletter
- Professional tone
- Structured format

### 3. MCP Integration (Milestone 4)

**Database MCP Server:**
- Provides 3 tools: query, search, get_sources
- SQLite backend
- Stdio transport

**SearchSkill:**
- High-level abstraction over MCP
- Combines database search
- Reusable across agents

### 4. Pipeline Orchestration

**Flow:**

External APIs ↓
Fetchers (async) ↓
Markdown Files + Database ↓
FilterAgent (LLM via LiteLLM) ↓
Filtered Markdown ↓
SummarizerAgent (LLM + SearchSkill) ↓
Summary Markdown ↓
WriterAgent (LLM) ↓
Newsletter Markdown


## Technology Choices

**Why Python?**
- Excellent async support
- Rich AI/ML ecosystem
- Easy to learn and maintain

**Why LiteLLM + Claude Haiku 4.5?**
- LiteLLM lets us swap providers via env var — no code changes
- Claude Haiku is cheap (~$1.50 for the whole curriculum at typical usage)
- Anthropic's $5 trial credit covers it without paying
- Solid function-calling and JSON output support
- Aligns with Blend's broader Claude tooling

**Why SQLite?**
- No server required
- Perfect for local development
- Easy to deploy

**Why MCP?**
- Industry standard emerging
- Tool reusability
- LLM-agnostic

**Why Markdown?**
- Human-readable
- Git-friendly
- Easy to debug
- Flexible format

## Performance

**Metrics:**
- Fetch 30 articles: ~2-3 seconds
- Filter 30 articles: ~30-45 seconds
- Complete pipeline: ~2-3 minutes

**Bottlenecks:**
- LLM API calls (rate limited)
- Network I/O

**Optimizations:**
- Concurrent fetching
- Rate limiting
- Caching (future)

## Security

**API Keys:**
- Stored in .env (not committed)
- Loaded at runtime
- Never logged

**Input Validation:**
- URL validation
- SQL injection prevention (parameterized queries)
- LLM output parsing (safe JSON)

**Rate Limiting:**
- Prevents API abuse
- Semaphore-based
- Configurable

## Future Enhancements

1. **More Sources**
   - Twitter API
   - Reddit
   - Research papers (arXiv)

2. **Better Evaluation**
   - Larger golden dataset
   - A/B testing framework
   - Human feedback loop

3. **Deployment**
   - Docker container
   - Scheduled runs (cron)
   - Web interface

4. **Advanced Features**
   - Semantic search
   - Personalization
   - Multi-language support

# Scheduling
Edit crontab-
crontab -e

 Add line to run daily at 9 AM-
0 9 * * * cd /path/to/project && /path/to/venv/bin/python src/complete_pipeline.py

# Configuration
Environment Variables:

LITELLM_MODEL - Required (default: claude-haiku-4-5-20251001)
ANTHROPIC_API_KEY (or OPENAI_API_KEY / GEMINI_API_KEY / etc.) - Required, must match the provider in LITELLM_MODEL
ENVIRONMENT - development/production
LOG_LEVEL - INFO/DEBUG

# Monitoring
check logs
-Application logs
tail -f logs/app.log

-Error logs
tail -f logs/error.log

# Troubleshooting
API rate limits:
- Reduce fetch frequency
- Increase delays between calls

Out of disk space:
- Clean old articles
- Reduce retention period

LLM errors:
- Check API key
- Verify internet connection
- Check API quotas
