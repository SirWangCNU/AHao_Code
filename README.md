# Ahaocode

Ahaocode 是一个运行在终端里的 AI 编程助手。它基于 Python 和 Textual 构建，支持多模型 Provider、交互式 TUI、非交互式命令执行、权限模式、MCP 工具接入、项目记忆、会话恢复、子 Agent、团队协作和远程浏览器 UI。

项目当前版本：`0.2.0`

## 功能特性

- 终端交互式 AI 编程助手，启动命令为 `ahaocode`
- 类 Claude Code 的启动欢迎界面
- 支持 Anthropic、OpenAI、OpenAI-compatible Provider
- 支持 `default`、`acceptEdits`、`plan`、`bypassPermissions` 权限模式
- 支持 `-p` 非交互式单次 Prompt 执行
- 支持 `stream-json` NDJSON 事件流输出
- 支持 MCP Server 配置和工具注册
- 支持项目级和用户级指令文件
- 支持会话保存、恢复、清理和压缩
- 支持记忆系统和上下文管理
- 支持子 Agent、后台任务和 Team 协作模式
- 支持文件读取、写入、编辑、搜索、diff、命令执行等开发工具
- 支持远程模式，通过浏览器访问本地 WebSocket UI

## 环境要求

- Python `>=3.11`
- Windows、macOS 或 Linux 终端环境
- 推荐使用虚拟环境
- 可选：`uv`，用于更快的依赖安装和运行

主要依赖：

- `textual`
- `anthropic`
- `openai`
- `pyyaml`
- `pydantic`
- `mcp`
- `httpx`
- `websockets`

## 快速启动

如果项目目录里已经有 `.venv`：

```powershell
cd D:\GitHubProgram\AHaoCode
.\.venv\Scripts\Activate.ps1
ahaocode
```

也可以不激活虚拟环境，直接运行：

```powershell
.\.venv\Scripts\ahaocode.exe
```

或者使用 Python 模块方式：

```powershell
.\.venv\Scripts\python.exe -m ahaocode
```

## 安装依赖

### 使用 uv

```powershell
uv sync
uv run ahaocode
```

如果系统提示找不到 `uv`，需要先安装 `uv`，或者改用下面的 pip 方式。

### 使用 pip

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .
ahaocode
```

## 配置文件

Ahaocode 默认从以下位置读取配置，后面的配置会覆盖前面的配置：

```text
~/.ahaocode/config.yaml
./.ahaocode/config.yaml
./.ahaocode/config.local.yaml
```

如果没有配置文件，会提示：

```text
No config file found. Expected .ahaocode/config.yaml in project or ~/.ahaocode/config.yaml
```

可以参考 `.ahaocode/config.yaml.example` 创建配置：

```yaml
providers:
  - name: anthropic-official
    protocol: anthropic
    base_url: https://api.anthropic.com
    api_key: "your-api-key-here"
    model: claude-sonnet-4-20250514
    thinking: true

permission_mode: default

mcp_servers:
  - name: context7
    command: npx
    args: ["-y", "@upstash/context7-mcp"]

enable_coordinator_mode: false
```

也可以通过环境变量提供 API Key：

```powershell
$env:ANTHROPIC_API_KEY="your-anthropic-key"
$env:OPENAI_API_KEY="your-openai-key"
```

## Provider 配置

### Anthropic

```yaml
providers:
  - name: anthropic
    protocol: anthropic
    base_url: https://api.anthropic.com
    api_key: "${ANTHROPIC_API_KEY}"
    model: claude-sonnet-4-20250514
    thinking: true
```

### OpenAI

```yaml
providers:
  - name: openai
    protocol: openai
    base_url: https://api.openai.com/v1
    api_key: "${OPENAI_API_KEY}"
    model: gpt-4o
```

### OpenAI-compatible

```yaml
providers:
  - name: custom
    protocol: openai-compat
    base_url: https://example.com/v1
    api_key: "${OPENAI_API_KEY}"
    model: your-model-name
```

## CLI 用法

查看帮助：

```powershell
ahaocode --help
```

交互式启动：

```powershell
ahaocode
```

指定权限模式：

```powershell
ahaocode --mode plan
ahaocode --mode acceptEdits
ahaocode --mode bypassPermissions
```

非交互式执行：

```powershell
ahaocode -p "帮我解释这个项目的结构"
```

输出 JSON 事件流：

```powershell
ahaocode -p "运行测试并总结结果" --output-format stream-json
```

启动远程模式：

```powershell
ahaocode --remote
```

远程模式会启动 WebSocket 服务，默认监听：

```text
0.0.0.0:18888
```

浏览器访问：

```text
http://localhost:18888
```

## 权限模式

| 模式 | 说明 |
| --- | --- |
| `default` | 默认模式，敏感操作会按规则检查 |
| `acceptEdits` | 自动接受编辑类操作 |
| `plan` | 计划模式，优先产出实施方案 |
| `bypassPermissions` | 跳过权限确认，适合受信环境，需谨慎使用 |

项目级权限规则文件位置：

```text
.ahaocode/permissions.yaml
.ahaocode/permissions.local.yaml
```

用户级权限规则文件位置：

```text
~/.ahaocode/permissions.yaml
```

## 指令文件

Ahaocode 会自动读取项目和用户指令文件，用于补充系统上下文。

读取顺序：

```text
~/.ahaocode/AHAOCODE.md
~/.ahaocode/AGENTS.md
项目路径中的 AHAOCODE.md
项目路径中的 AGENTS.md
.ahaocode/INSTRUCTIONS.md
AHAOCODE.local.md
```

当前项目的主指令文件是：

```text
AHAOCODE.md
```

## 常用内置能力

Ahaocode 内置了一组开发工具，供 Agent 在对话中调用：

- `ReadFile`：读取文件
- `WriteFile`：写入文件
- `EditFile`：编辑文件
- `Glob`：按通配符搜索文件
- `Grep`：按文本搜索代码
- `Bash`：执行 shell 命令
- `ToolSearch`：搜索可用工具
- `Agent`：启动子 Agent
- `TeamCreate` / `TeamDelete`：管理团队协作

具体工具是否可用取决于权限模式、配置和当前运行环境。

## MCP Server

可以在 `.ahaocode/config.yaml` 里配置 MCP Server：

```yaml
mcp_servers:
  - name: context7
    command: npx
    args: ["-y", "@upstash/context7-mcp"]
```

HTTP MCP 示例：

```yaml
mcp_servers:
  - name: my-http-mcp
    url: https://example.com/mcp
    headers:
      Authorization: "Bearer ${MY_TOKEN}"
```

启动后，Ahaocode 会连接 MCP Server 并注册可用工具。

## 项目结构

```text
AHaoCode/
├── ahaocode/                 # 主源码包
│   ├── __main__.py           # CLI 入口
│   ├── app.py                # Textual TUI 应用
│   ├── agent.py              # Agent 主循环
│   ├── client.py             # 模型客户端
│   ├── config.py             # 配置加载和合并
│   ├── conversation.py       # 会话消息结构
│   ├── commands/             # 斜杠命令系统
│   ├── context/              # 上下文管理
│   ├── hooks/                # Hook 系统
│   ├── mcp/                  # MCP 客户端和工具包装
│   ├── memory/               # 记忆和会话系统
│   ├── permissions/          # 权限检查
│   ├── skills/               # Skill 加载和执行
│   ├── teams/                # Team 协作能力
│   ├── tools/                # 内置工具
│   └── worktree/             # Git worktree 支持
├── tests/                    # 测试用例
├── AHAOCODE.md               # 项目指令文件
├── pyproject.toml            # Python 项目配置
├── uv.lock                   # uv 锁文件
└── README.md                 # 项目说明文档
```

## 开发

安装为 editable 模式：

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

运行重点测试：

```powershell
pytest tests/test_ahaocode_branding.py tests/test_agent.py tests/test_commands.py tests/test_skills.py tests/test_worktree.py
```

运行全部测试：

```powershell
pytest
```

在当前 Windows 环境中，部分测试可能依赖 Unix 命令或进程行为，例如 `sleep`、`rm`、临时目录锁检测等，需要根据平台做兼容处理。

## GitHub 仓库

当前远程仓库：

```text
git@github.com:SirWangCNU/AHao_Code.git
```

推送到 `master`：

```powershell
git add .
git commit -m "Update project"
git push origin master
```

## 常见问题

### PowerShell 提示找不到 uv

说明系统没有安装 `uv`，或者 `uv` 没加入 PATH。可以改用：

```powershell
.\.venv\Scripts\ahaocode.exe
```

也可以安装 `uv` 后重新打开 PowerShell。

### PowerShell 无法执行 Activate.ps1

临时放开当前终端的执行策略：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 找不到配置文件

创建项目配置：

```powershell
mkdir .ahaocode
copy .ahaocode\config.yaml.example .ahaocode\config.yaml
```

然后填入 Provider 的 `api_key`、`base_url` 和 `model`。


```powershell
ahaocode
```

### 如何确认当前安装正常

```powershell
ahaocode --help
python -m ahaocode --help
```

两者都能输出帮助信息时，说明入口可用。

## 许可证

当前仓库暂未声明许可证。公开视频或发布前，建议补充 `LICENSE` 文件。
