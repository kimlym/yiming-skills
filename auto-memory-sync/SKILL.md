---
name: auto-memory-sync
description: Auto memory synchronization and archival skill. Syncs chat history to daily memory files during heartbeats, deduplicates existing content, and archives memories older than 90 days. Activate during heartbeat checks when managing memory files. Requires manual configuration in HEARTBEAT.md.
---

# Auto Memory Sync

自动同步对话历史到每日记忆文件，并归档旧记忆。

## ⚠️ 手动配置要求（重要）

此技能需要在 `HEARTBEAT.md` 中手动配置才能自动工作。请编辑 `/Users/yiminglu/.openclaw/workspace/HEARTBEAT.md`，添加记忆同步和归档的任务描述。

**配置步骤：**
1. 编辑 `HEARTBEAT.md`
2. 复制以下内容到文件中：
```markdown
## Memory Sync (Daily)
- 检查今日记忆文件 `memory/YYYY-MM-DD.md`
- 获取主会话历史（最近 100 条消息）
- 去重后追加新内容到今日记忆文件

## Memory Archive (Daily)
- 每天执行一次（检查 `memory/.last-archive`）
- 扫描并归档 >90 天的记忆文件到 `memory/archive/`
```
3. 保存文件，OpenClaw 会在下次心跳时自动执行

## 工作流程

### 1. 心跳时同步（每日记忆）

当接收到心跳请求时：

1. **检查今日记忆文件** - `memory/YYYY-MM-DD.md`
   - 如果不存在则创建
   - 格式：`# 2026-03-29 日记\n\n## 对话记录\n\n...`

2. **读取对话历史** - 使用 `sessions_history` 获取主会话历史
   - 参数：`sessionKey="main"`, `limit=100`
   - 返回：最近 100 条消息（用户和 AI 的对话）

3. **去重处理** - 比较对话内容和已有记忆
   - **策略 1（推荐）**：基于消息时间戳去重
   - **策略 2**：基于消息内容哈希去重（适合没有时间戳的情况）
   - 只追加不在已有内容中的消息

4. **追加新内容** - 将未记录的对话追加到今日记忆文件
   - 格式：`### HH:MM - User/AI\n\n消息内容\n\n`
   - 保留 Markdown 格式

5. **可选摘要** - 对重要的对话片段生成摘要添加到 `MEMORY.md`
   - 只添加：决策、重要事件、学习内容、待办事项

### 2. 归档旧记忆（>90天）

每天执行一次（检查 `memory/.last-archive` 时间戳）：

1. **检查归档时间** - 读取 `memory/.last-archive`
   - 如果今天已归档，跳过
   - 否则继续执行归档

2. **扫描 memory/ 目录** - 找出所有 `YYYY-MM-DD.md` 文件
   - 跳过：`MEMORY.md`, `archive/` 目录, 非日期格式的文件
   - 匹配模式：`^[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$`

3. **计算文件年龄** - 基于文件名中的日期
   - 将 `YYYY-MM-DD` 转换为可比较的日期格式
   - 计算与当前日期的天数差

4. **创建归档目录** - `memory/archive/`（如果不存在）
   - 保持原始文件名

5. **移动旧文件** - 将 >90 天的文件移到 `memory/archive/`
   - 使用 `mv` 命令（而不是复制，节省空间）

6. **更新归档时间戳** - 写入当前日期到 `memory/.last-archive`
   - 格式：`YYYY-MM-DD`

7. **生成归档报告** - 显示归档文件数量和统计信息
   - 格式：`归档 5 个文件到 memory/archive/（2026-03-29）`

## 使用场景

- **Heartbeat 触发**（自动）- OpenClaw 定期发送心跳时自动执行
- **手动同步** - 主动调用 `scripts/sync_memory.sh`
- **手动归档** - 主动调用 `scripts/archive_memory.sh`
- **调试模式** - 在脚本中设置 `DEBUG=1` 查看详细日志

## 脚本说明

### `scripts/sync_memory.sh`

同步今日对话到记忆文件：

```bash
./scripts/sync_memory.sh
```

功能：
- 读取今日记忆文件（如果存在）
- 获取主会话历史（最近 100 条消息）
- 去重后追加新内容
- 显示同步摘要（新增记录数、耗时）

**输出示例：**
```
Auto Memory Sync
================
今日文件: memory/2026-03-29.md
获取消息数: 100
新增记录: 23
耗时: 1.2s
```

### `scripts/archive_memory.sh`

归档 90 天以上的记忆：

```bash
./scripts/archive_memory.sh
```

功能：
- 扫描所有记忆文件
- 识别 >90 天的文件
- 移动到归档目录
- 显示归档摘要（归档文件数、耗时）

**输出示例：**
```
Auto Memory Archive
==================
归档阈值: 90 天（2025-12-29 之前）
扫描文件数: 95
归档文件数: 5
归档目录: memory/archive/
耗时: 0.3s
```

## 配置

创建 `scripts/config.sh` 来自定义行为：

```bash
# 归档天数阈值（默认 90）
ARCHIVE_DAYS=90

# 同步的消息数量（默认 100）
SYNC_MESSAGE_LIMIT=100

# 归档目录（默认 memory/archive）
ARCHIVE_DIR="memory/archive"

# 工作目录（默认 ~/.openclaw/workspace）
WORKSPACE="/Users/yiminglu/.openclaw/workspace"

# 主会话 key（默认 main）
MAIN_SESSION_KEY="main"

# 调试模式（0=关闭，1=开启）
DEBUG=0
```

使用配置：
```bash
source scripts/config.sh
./scripts/sync_memory.sh
```

## 性能优化建议

1. **去重策略** - 使用时间戳去重比内容哈希快 10 倍以上
2. **消息限制** - 同步时限制为最近 100 条消息，避免处理过多历史
3. **归档频率** - 每天只检查一次，使用时间戳避免重复扫描
4. **文件移动** - 使用 `mv` 而不是 `cp` 节省磁盘 I/O
5. **批量操作** - 可以考虑批量处理多个文件，减少系统调用

## 错误处理

脚本包含以下错误处理：

- 目录不存在时自动创建
- 文件权限问题会显示错误并退出
- Git 仓库配置错误会提示用户
- 空文件或空目录会优雅处理

**调试提示**：
```bash
# 启用调试模式
DEBUG=1 ./scripts/sync_memory.sh
```

## 测试建议

测试技能是否正常工作：

1. **手动同步测试**
```bash
cd /Users/yiminglu/.openclaw/workspace/skills/auto-memory-sync
./scripts/sync_memory.sh
```
检查 `memory/2026-03-29.md` 是否有新内容

2. **手动归档测试**
```bash
./scripts/archive_memory.sh
```
检查 `memory/archive/` 目录是否有文件

3. **Heartbeat 测试**
- 向 OpenClaw 发送心跳请求
- 观察是否有同步和归档日志

4. **去重测试**
- 多次运行同步脚本
- 确认文件内容不会重复追加

## 注意事项

- **去重逻辑** - 使用消息时间戳和内容哈希去重
- **权限检查** - 确保对 `memory/` 目录有读写权限
- **备份建议** - 归档前建议手动备份重要记忆
- **文件命名** - 严格按照 `YYYY-MM-DD.md` 格式命名
- **HEARTBEAT.md 配置** - 必须手动配置才能自动工作（见上方说明）

## 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 同步失败 | 会话 key 错误 | 检查 `MAIN_SESSION_KEY` 配置 |
| 归档失败 | 权限不足 | 检查 `memory/` 目录权限 |
| 内容重复 | 去重逻辑错误 | 启用 `DEBUG=1` 查看日志 |
| 归档不执行 | 时间戳问题 | 删除 `memory/.last-archive` 重试 |

## 高级用法

### 自定义去重逻辑

在 `scripts/sync_memory.sh` 中添加自定义去重函数：

```bash
custom_deduplicate() {
    local new_content="$1"
    local existing_file="$2"

    # 你的去重逻辑
    # 例如：只保留包含特定关键词的消息
    echo "$new_content"" | grep -i "重要\|决策\|学习"
}
```

### 生成摘要

在同步后调用 AI 生成摘要：

```bash
# 提取今日重要对话
important=$(grep -A 5 "重要" memory/2026-03-29.md)

# 调用 AI 生成摘要（需要集成）
echo "生成摘要: $important" > memory/2026-03-29-summary.md
```

### 监控和告警

添加监控脚本，检测记忆文件异常：

```bash
# 检查今日文件是否为空
if [ ! -s "memory/$(date +%Y-%m-%d).md" ]; then
    echo "警告：今日记忆文件为空"
fi
```
