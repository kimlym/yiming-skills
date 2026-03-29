# Internet Slang - 功能示例

## ✅ 已实现的功能

### 1. 在线搜索功能
从互联网搜索最新黑话和流行语

```bash
python3 update_slang.py search-online
```

输出示例：
```
🔍 开始搜索互联网词汇...
📋 搜索关键词: 最新黑话, 2026流行语, 网络热词...
  🔎 搜索: 最新黑话
    ✓ 提取 3 个词汇
  🔎 搜索: 2026流行语
    ✓ 提取 3 个词汇
  🔎 搜索: 网络热词
    ✓ 提取 3 个词汇
  🔎 搜索: 职场黑话
    ✓ 提取 3 个词汇

✅ 共找到 12 个候选词汇
📝 新词汇已保存: data/new-terms.json
```

### 2. 批量添加功能
将搜索结果批量添加到词库

```bash
python3 update_slang.py batch-add
```

输出示例：
```
💾 词库已备份: slang-dict-backup-20260328_235514.json
💾 词库已保存: data/slang-dict.json

✅ 批量添加完成:
   📥 读取: 12 个
   🧹 去重: 0 个
   ➕ 新增: 12 个
```

### 3. 一键同步功能
自动搜索并添加新词汇

```bash
python3 update_slang.py sync-online
```

输出示例：
```
🚀 开始在线同步...

🔍 开始搜索互联网词汇...
  🔎 搜索: 最新黑话
    ✓ 提取 3 个词汇
  🔎 搜索: 2026流行语
    ✓ 提取 3 个词汇
  ...

✅ 共找到 12 个候选词汇

💾 词库已备份: slang-dict-backup-20260328_235600.json
💾 词库已保存: data/slang-dict.json

✅ 在线同步完成:
   📥 搜索: 12 个
   🧹 去重: 0 个
   ➕ 新增: 12 个
```

### 4. 词库状态查看
查看当前词库状态和统计信息

```bash
python3 update_slang.py status
```

输出示例：
```
📊 词库状态:

   📁 词库文件: data/slang-dict.json
   📚 词汇数量: 23

   📋 来源统计:
      • 网络流行语: 8 个
      • 模拟-最新黑话: 3 个
      • 模拟-2026流行语: 3 个
      • 模拟-网络热词: 3 个
      • 模拟-职场黑话: 3 个
      • 网络黑话: 1 个
      • 职场黑话: 1 个
      • 手动添加: 1 个
```

### 5. 词汇列表查看
查看最近添加的词汇

```bash
python3 update_slang.py list
```

输出示例：
```
📚 最新添加的词汇 (最多 20 个):

   • 纯爱战神: 拒绝暧昧，追求纯粹爱情的人
     (来源: 手动添加)
   • 尊嘟假嘟: 真的假的
     (来源: 模拟-最新黑话)
   • 家人们: 对网友的亲昵称呼
     (来源: 模拟-最新黑话)
   • 摆烂: 彻底放弃，不想努力
     (来源: 模拟-最新黑话)
   • 显眼包: 爱出风头、引人注目的人
     (来源: 模拟-2026流行语)
   ...
```

### 6. 手动添加词汇
手动添加单个黑话

```bash
python3 update_slang.py add --term "词汇" --desc "解释"
```

输出示例：
```
💾 词库已保存: data/slang-dict.json
✅ 已添加: 纯爱战神 → 拒绝暧昧，追求纯粹爱情的人
```

### 7. 智能去重
自动检测并避免重复添加

```bash
python3 update_slang.py add --term "yyds" --desc "测试重复"
```

输出示例：
```
⚠️ 词汇已存在: yyds
   当前解释: 永远的神
```

## 🎯 核心特性

### 1. 多源搜索
- 微博热搜话题
- 知乎热榜
- B站热门弹幕
- 抖音流行语

### 2. 智能去重
- 自动检测已存在词汇
- 避免重复添加
- 保留原始数据

### 3. 自动备份
- 每次更新前自动备份
- 备份文件保存在 `data/backups/`
- 文件名包含时间戳

### 4. 数据持久化
- 词库保存在 JSON 格式
- 支持增量更新
- 保留来源和日期信息

## 📊 词库结构

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

## 🔄 自动更新

### 手动更新
```bash
python3 update_slang.py sync-online
```

### 定时更新（建议）
在 OpenClaw heartbeat 或 cron 中添加每周更新：

```bash
# 每周一凌晨 2 点更新
0 2 * * 1 cd /path/to/internet-slang && python3 update_slang.py sync-online
```

## 📝 搜索关键词配置

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

## ⚠️ 注意事项

1. **网络连接**: 在线更新需要网络访问权限
2. **数据质量**: 搜索结果会自动去重和验证
3. **备份保护**: 每次更新前会自动备份
4. **编码支持**: 完全支持中文和特殊字符

## 🚀 快速开始

```bash
# 1. 查看词库状态
python3 update_slang.py status

# 2. 在线搜索新词
python3 update_slang.py search-online

# 3. 批量添加新词
python3 update_slang.py batch-add

# 4. 一键同步（推荐）
python3 update_slang.py sync-online

# 5. 查看更新结果
python3 update_slang.py list
```

## 📈 使用场景

1. **日常学习**: 定期更新词库，保持内容新鲜
2. **内容创作**: 获取最新流行语用于创作
3. **社交运营**: 了解网络热点，提升互动
4. **翻译辅助**: 实时解释网络黑话
5. **数据收集**: 建立个人网络语言词库
