# Internet Slang - 网络黑话翻译

## 功能介绍

实时翻译和理解网络黑话、流行语和缩写，支持从互联网自动更新词库。

## 核心功能

### 基础功能

1. **翻译网络黑话**
   - 自动识别并翻译流行网络用语
   - 支持缩写、梗、代称的即时解释
   - 提供背景和使用场景

2. **在线实时更新词库**
   - 从互联网搜索最新黑话（每周/每月新词）
   - 支持多个来源：微博、知乎、B站、抖音
   - 智能去重，避免重复添加

3. **词库管理**
   - 查看当前词库
   - 手动添加新词
   - 批量导入词汇

## 使用方法

### 翻译黑话

在对话中提到的网络黑话会自动翻译，例如：

- "yyds" → "永远的神"
- "摸鱼" → "工作中偷懒、不务正业"
- "内卷" → "过度竞争、恶性竞争"

### 在线更新词库

**从互联网搜索最新黑话：**

```bash
cd /Users/yiminglu/.openclaw/workspace/repos/yiming-skills/internet-slang
python update_slang.py search-online
```

**批量添加搜索结果到词库：**

```bash
python update_slang.py batch-add
```

**直接同步（搜索+添加）：**

```bash
python update_slang.py sync-online
```

**查看词库状态：**

```bash
python update_slang.py status
```

**手动添加词汇：**

```bash
python update_slang.py add --term "新词" --desc "解释"
```

## 数据来源

### 1. GitHub 开源项目
- **GitHub**: shadowings-zy/internet-industry-terms-generator
  - 已提取 106 个职场黑话术语
  - 涵盖互联网企业常用词汇

### 2. 互联网平台
在线更新从以下平台提取词汇：

- **微博热搜**: 最新流行话题和热词
- **知乎热榜**: 知识社区热门讨论
- **B站弹幕**: 视频评论区高频词汇
- **抖音流行语**: 短视频平台热梗

## 词库结构

词库保存在 `data/slang-dict.json`，支持：

```json
{
  "词汇": {
    "desc": "解释",
    "source": "来源",
    "date": "添加日期",
    "usage": "使用场景"
  }
}
```

## 调度更新

### 手动更新

```bash
python update_slang.py sync-online
```

### 自动更新（建议）

在 OpenClaw heartbeat 或 cron 中添加每周更新：

```bash
# 每周一凌晨 2 点更新
0 2 * * 1 cd /path/to/internet-slang && python update_slang.py sync-online
```

## 注意事项

1. **网络连接**: 在线更新需要网络访问权限
2. **数据质量**: 搜索结果需要人工审核后批量添加
3. **去重机制**: 自动过滤重复词汇
4. **词库备份**: 每次更新会自动备份旧词库

## 示例输出

```
$ python update_slang.py search-online

🔍 搜索关键词: 最新黑话 2026流行语
✅ 找到 12 个候选词汇
📝 保存到: data/new-terms.json

⚠️  请先检查搜索结果，再运行:
   python update_slang.py batch-add
```

```
$ python update_slang.py sync-online

🔍 搜索互联网词汇...
📥 下载新词汇: 15 个
🧹 去重后: 12 个
✅ 成功添加 12 个新词
💾 词库备份: slang-dict-backup-20260328.json
```

## 扩展功能

### 自定义搜索关键词

编辑 `update_slang.py` 中的 `SEARCH_KEYWORDS` 列表：

```python
SEARCH_KEYWORDS = [
    "最新黑话",
    "2026流行语",
    "网络热词",
    "职场黑话",
    "你的关键词"
]
```

### 添加自定义来源

在 `update_slang.py` 的 `fetch_from_platform()` 函数中添加新的平台逻辑。
