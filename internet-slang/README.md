# Internet Slang - 网络黑话翻译与词库管理

## 🎯 简介

实时翻译和理解网络黑话、流行语和缩写，支持从互联网自动更新词库。

## ✨ 功能特点

- **实时翻译**: 自动识别并解释网络黑话
- **在线更新**: 从互联网搜索最新流行语
- **多源支持**: 微博、知乎、B站、抖音等平台
- **智能去重**: 自动避免重复添加
- **自动备份**: 每次更新前备份词库

## 📖 使用文档

详细使用说明请查看：

- **[SKILL.md](SKILL.md)** - 技能使用指南
- **[EXAMPLES.md](EXAMPLES.md)** - 功能示例和输出

## 🚀 快速开始

### 1. 查看词库状态
```bash
cd /Users/yiminglu/.openclaw/workspace/repos/yiming-skills/internet-slang
python3 update_slang.py status
```

### 2. 在线搜索新词
```bash
python3 update_slang.py search-online
```

### 3. 批量添加新词
```bash
python3 update_slang.py batch-add
```

### 4. 一键同步（推荐）
```bash
python3 update_slang.py sync-online
```

### 5. 查看词汇列表
```bash
python3 update_slang.py list
```

## 📋 命令列表

| 命令 | 说明 |
|------|------|
| `status` | 查看词库状态 |
| `list` | 列出词汇（最多20个） |
| `search-online` | 从互联网搜索新词 |
| `batch-add` | 批量添加搜索结果 |
| `sync-online` | 在线同步（搜索+添加） |
| `add --term TERM --desc DESC` | 手动添加词汇 |

## 📊 词库结构

词库保存在 `data/slang-dict.json`：

```json
{
  "yyds": {
    "desc": "永远的神",
    "source": "网络黑话",
    "date": "2024-01-01",
    "usage": "表示极度崇拜或赞赏"
  }
}
```

## 🔄 自动更新

### 手动更新
```bash
python3 update_slang.py sync-online
```

### 定时更新（建议）
在 OpenClaw heartbeat 或 cron 中配置每周更新：

```bash
# 每周一凌晨 2 点更新
0 2 * * 1 cd /path/to/internet-slang && python3 update_slang.py sync-online
```

## 📁 目录结构

```
internet-slang/
├── SKILL.md              # 技能使用指南
├── README.md             # 项目说明
├── EXAMPLES.md           # 功能示例
├── update_slang.py       # 更新脚本
├── data/
│   ├── slang-dict.json   # 主词库
│   ├── new-terms.json    # 待添加词汇（临时）
│   └── backups/          # 备份目录
```

## ⚙️ 配置

编辑 `update_slang.py` 可自定义：

### 搜索关键词
```python
SEARCH_KEYWORDS = [
    "最新黑话",
    "2026流行语",
    "网络热词",
    "职场黑话",
]
```

### 平台关键词
```python
PLATFORM_KEYWORDS = {
    "微博": ["微博热搜", "微博热词"],
    "知乎": ["知乎热榜", "知乎流行语"],
    "B站": ["B站弹幕", "B站梗"],
    "抖音": ["抖音热梗", "抖音黑话"],
}
```

## 🔧 技术细节

### 工作流程

1. **搜索阶段**:
   - 使用配置的关键词搜索互联网
   - 从搜索结果中提取术语和解释
   - 保存到临时文件 `data/new-terms.json`

2. **去重阶段**:
   - 加载现有词库
   - 检测重复和近似重复
   - 过滤已存在词汇

3. **添加阶段**:
   - 备份当前词库
   - 合并新词汇到词库
   - 保存更新后的词库

### 数据来源

- **网络搜索**: 使用 OpenClaw web_search 工具
- **模拟数据**: 当搜索失败时降级使用预设数据
- **手动添加**: 支持用户手动补充

## ⚠️ 注意事项

1. **网络连接**: 在线更新需要网络访问权限
2. **数据质量**: 搜索结果会自动去重和验证
3. **备份保护**: 每次更新前会自动备份
4. **编码支持**: 完全支持中文和特殊字符

## 📈 使用场景

1. **日常学习**: 定期更新词库，保持内容新鲜
2. **内容创作**: 获取最新流行语用于创作
3. **社交运营**: 了解网络热点，提升互动
4. **翻译辅助**: 实时解释网络黑话
5. **数据收集**: 建立个人网络语言词库

## 🔗 相关链接

- [OpenClaw 文档](https://github.com/openclaw-ai/openclaw)
- [Web Search 工具](https://github.com/openclaw-ai/openclaw#web-search)

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

---

Made with ❤️ by OpenClaw
