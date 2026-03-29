---
name: auto-memory-sync
description: Auto memory synchronization and archival skill. Syncs chat history to daily memory files during heartbeats, deduplicates existing content, and archives memories older than 90 days. Activate during heartbeat checks when managing memory files.
---

# Auto Memory Sync

自动同步对话历史到每日记忆文件，并归档旧记忆。

## 工作流程

### 1. 心跳时同步（每日记忆）

当接收到心跳请求时：

1. **检查今日记忆文件** - `memory/YYYY-MM-DD.md`
2. **读取对话历史** - 使用 `sessions_history` 获取主会话历史
3. **去重处理** - 比较对话内容和已有记忆，避免重复
4. **追加新内容** - 将未记录的对话追加到今日记忆文件
5. **更新 MEMORY.md** - 保留重要的长期信息

### 2. 归档旧记忆（>90天）

每天执行一次：

1. **扫描 memory/ 目录** - 找出所有 `YYYY-MM-DD.md` 文件
2. **计算文件年龄** - 基于文件名中的日期
3. **创建归档目录** - `memory/archive/`（如果不存在）
4. **移动旧文件** - 将 >90 天的文件移到 `memory/archive/`
5. **更新索引** - 可选：维护 `memory/archive/index.md`

## 使用场景

- **Heartbeat 触发** - 自动执行同步和归档
- **手动同步** - 主动调用 `scripts/sync_memory.sh`
- **手动归档** - 主动调用 `scripts/archive_memory.sh`

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
- 显示同步摘要

### `scripts/archive_memory.sh`

归档 90 天以上的记忆：

```bash
./scripts/archive_memory.sh
```

功能：
- 扫描所有记忆文件
- 识别 >90 天的文件
- 移动到归档目录
- 显示归档摘要

## 配置

创建 `scripts/config.sh` 来自定义行为：

```bash
# 归档天数阈值（默认 90）
ARCHIVE_DAYS=90

# 同步的消息数量（默认 100）
SYNC_MESSAGE_LIMIT=100

# 归档目录（默认 memory/archive）
ARCHIVE_DIR="memory/archive"
```

## 注意事项

- **去重逻辑** - 使用消息时间戳和内容哈希去重
- **权限检查** - 确保对 `memory/` 目录有读写权限
- **备份建议** - 归档前建议手动备份重要记忆
- **文件命名** - 严格按照 `YYYY-MM-DD.md` 格式命名

## 示例输出

同步输出：
```
Auto Memory Sync
================
今日文件: memory/2026-03-29.md
获取消息数: 100
新增记录: 23
耗时: 1.2s
```

归档输出：
```
Auto Memory Archive
==================
扫描记忆文件: 95
归档阈值: 90 天
归档文件数: 5
归档目录: memory/archive/
耗时: 0.3s
```
