#!/usr/bin/env python3
"""
Internet Slang Updater - 网络黑话词库更新工具

功能：
1. 从互联网搜索最新黑话和流行语
2. 从多个平台提取词汇（微博、知乎、B站、抖音）
3. 智能去重，避免重复添加
4. 批量管理和更新词库
"""

import json
import os
import sys
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

# 配置
DATA_DIR = Path(__file__).parent / "data"
SLANG_DICT_FILE = DATA_DIR / "slang-dict.json"
NEW_TERMS_FILE = DATA_DIR / "new-terms.json"
BACKUP_DIR = DATA_DIR / "backups"

# 搜索关键词配置
SEARCH_KEYWORDS = [
    "最新黑话",
    "2026流行语",
    "网络热词",
    "职场黑话",
    "网络流行语大全",
    "年轻人黑话",
]

# 平台关键词映射
PLATFORM_KEYWORDS = {
    "微博": ["微博热搜", "微博热词", "微博黑话"],
    "知乎": ["知乎热榜", "知乎流行语", "知乎黑话"],
    "B站": ["B站弹幕", "B站梗", "B站黑话", "bilibili流行语"],
    "抖音": ["抖音热梗", "抖音黑话", "抖音流行语"],
}

class SlangUpdater:
    """黑话词库更新器"""

    def __init__(self):
        self.ensure_dirs()
        self.slang_dict = self.load_slang_dict()

    def ensure_dirs(self):
        """确保目录存在"""
        DATA_DIR.mkdir(exist_ok=True)
        BACKUP_DIR.mkdir(exist_ok=True)

    def load_slang_dict(self) -> Dict:
        """加载词库"""
        if SLANG_DICT_FILE.exists():
            with open(SLANG_DICT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_slang_dict(self):
        """保存词库"""
        with open(SLANG_DICT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.slang_dict, f, ensure_ascii=False, indent=2)
        print(f"💾 词库已保存: {SLANG_DICT_FILE}")

    def backup_slang_dict(self):
        """备份词库"""
        if not SLANG_DICT_FILE.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"slang-dict-backup-{timestamp}.json"

        with open(SLANG_DICT_FILE, 'r', encoding='utf-8') as f:
            backup_data = f.read()

        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(backup_data)

        print(f"💾 词库已备份: {backup_file.name}")

    def search_online(self) -> Dict:
        """从互联网搜索最新黑话"""
        print("🔍 开始搜索互联网词汇...")
        print(f"📋 搜索关键词: {', '.join(SEARCH_KEYWORDS[:3])}...")

        all_terms = {}

        # 使用 OpenClaw web_search 工具
        for keyword in SEARCH_KEYWORDS[:4]:  # 限制搜索次数，避免超时
            print(f"  🔎 搜索: {keyword}")
            terms = self._search_keyword(keyword)
            all_terms.update(terms)

        print(f"\n✅ 共找到 {len(all_terms)} 个候选词汇")
        return all_terms

    def _search_keyword(self, keyword: str) -> Dict:
        """搜索单个关键词"""
        terms = {}

        try:
            # 尝试使用 web_search 工具（通过 subprocess 调用 OpenClaw）
            # 注意：这需要 OpenClaw 的 web_search 功能可用
            cmd = f'cd /Users/yiminglu/.openclaw/workspace && openclaw run "from openclaw import tools; import json; result = tools.web_search(query=\\\"{keyword}\\\", count=5); print(json.dumps(result))"'
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # 从搜索结果中提取词汇
                extracted = self._extract_terms_from_search(result.stdout, keyword)
                terms.update(extracted)
                print(f"    ✓ 提取 {len(extracted)} 个词汇")
            else:
                print(f"    ✗ 搜索失败: {keyword}")
                # 如果搜索失败，使用模拟数据
                terms = self._get_mock_terms(keyword)
                print(f"    📦 使用模拟数据: {len(terms)} 个词汇")

        except subprocess.TimeoutExpired:
            print(f"    ⏱️ 搜索超时: {keyword}")
        except Exception as e:
            print(f"    ⚠️ 搜索错误: {e}")
            # 降级到模拟数据
            terms = self._get_mock_terms(keyword)

        return terms

    def _get_mock_terms(self, keyword: str) -> Dict:
        """获取模拟数据（用于测试）"""
        mock_terms = {
            "最新黑话": {
                "尊嘟假嘟": {"desc": "真的假的", "usage": "口语表达"},
                "家人们": {"desc": "对网友的亲昵称呼", "usage": "口语表达"},
                "摆烂": {"desc": "彻底放弃，不想努力", "usage": "态度表达"},
            },
            "2026流行语": {
                "显眼包": {"desc": "爱出风头、引人注目的人", "usage": "人物描述"},
                "哈基米": {"desc": "可爱的小猫咪", "usage": "昵称"},
                "泰酷辣": {"desc": "太酷了", "usage": "口语表达"},
            },
            "网络热词": {
                "挖野菜": {"desc": "恋爱脑，不顾一切爱一个人", "usage": "情感状态"},
                "科目三": {"desc": "网络爆火舞蹈", "usage": "网络热梗"},
                "特种兵旅游": {"desc": "高强度、快节奏的旅游方式", "usage": "生活方式"},
            },
            "职场黑话": {
                "颗粒度": {"desc": "精细程度、细节", "usage": "职场术语"},
                "对齐": {"desc": "统一认识、沟通确认", "usage": "职场术语"},
                "抓手": {"desc": "切入点、突破口", "usage": "职场术语"},
            },
        }

        result = {}
        for key, terms_dict in mock_terms.items():
            if key in keyword or keyword in key:
                for term, info in terms_dict.items():
                    result[term] = {
                        "desc": info["desc"],
                        "source": f"模拟-{keyword}",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "usage": info["usage"]
                    }
        return result

    def _extract_terms_from_search(self, search_output: str, source: str) -> Dict:
        """从搜索结果中提取术语"""
        terms = {}

        # 常见的黑话模式
        patterns = [
            r'["\'"「「]([^\s\"\']+?)["\'"」」]\s*[：::=]\s*([^\n]+)',
            r'([^\s\"\']+?)\s*[→➤👉]\s*([^\n]+)',
            r'([A-Za-z0-9]{2,6})\s*[：:]=\s*([^\n]+)',
        ]

        lines = search_output.split('\n')
        for line in lines:
            line = line.strip()
            if not line or len(line) < 3:
                continue

            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    term = match.group(1).strip()
                    desc = match.group(2).strip()

                    if len(term) < 2 or len(desc) < 2:
                        continue

                    # 清理描述
                    desc = re.sub(r'[^\w\s\u4e00-\u9fff]', '', desc)
                    desc = desc[:100]  # 限制长度

                    if term not in terms:
                        terms[term] = {
                            "desc": desc,
                            "source": f"网络搜索-{source}",
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "usage": "通用"
                        }
                        break

        return terms

    def fetch_from_platform(self, platform: str) -> Dict:
        """从指定平台提取词汇"""
        print(f"📱 从 {platform} 提取词汇...")

        if platform not in PLATFORM_KEYWORDS:
            print(f"⚠️ 不支持的平台: {platform}")
            return {}

        keywords = PLATFORM_KEYWORDS[platform]
        terms = {}

        for keyword in keywords[:2]:  # 限制每个平台的搜索次数
            print(f"  🔎 搜索: {keyword}")
            platform_terms = self._search_keyword(keyword)
            terms.update(platform_terms)

        print(f"  ✅ 从 {platform} 提取 {len(terms)} 个词汇")
        return terms

    def deduplicate_terms(self, new_terms: Dict) -> Tuple[Dict, int]:
        """去重"""
        existing_terms = set(self.slang_dict.keys())
        filtered_terms = {}
        duplicate_count = 0

        for term, info in new_terms.items():
            if term in existing_terms:
                duplicate_count += 1
                continue

            # 检查近似重复（简单版本）
            is_duplicate = False
            for existing in existing_terms:
                if term.lower() == existing.lower():
                    is_duplicate = True
                    duplicate_count += 1
                    break

            if not is_duplicate:
                filtered_terms[term] = info

        return filtered_terms, duplicate_count

    def save_new_terms(self, terms: Dict):
        """保存新词汇到临时文件"""
        with open(NEW_TERMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(terms, f, ensure_ascii=False, indent=2)
        print(f"📝 新词汇已保存: {NEW_TERMS_FILE}")

    def load_new_terms(self) -> Dict:
        """加载待添加的新词汇"""
        if NEW_TERMS_FILE.exists():
            with open(NEW_TERMS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def batch_add(self):
        """批量添加新词汇"""
        new_terms = self.load_new_terms()

        if not new_terms:
            print("⚠️ 没有找到待添加的新词汇")
            print("💡 先运行: python update_slang.py search-online")
            return

        self.backup_slang_dict()

        filtered_terms, duplicate_count = self.deduplicate_terms(new_terms)

        if not filtered_terms:
            print("⚠️ 所有词汇都已存在于词库中")
            return

        # 合并到词库
        self.slang_dict.update(filtered_terms)
        self.save_slang_dict()

        print(f"\n✅ 批量添加完成:")
        print(f"   📥 读取: {len(new_terms)} 个")
        print(f"   🧹 去重: {duplicate_count} 个")
        print(f"   ➕ 新增: {len(filtered_terms)} 个")

        # 清理临时文件
        NEW_TERMS_FILE.unlink(missing_ok=True)

    def sync_online(self):
        """在线同步（搜索+添加）"""
        print("🚀 开始在线同步...\n")

        # 搜索
        new_terms = self.search_online()

        if not new_terms:
            print("\n⚠️ 未找到新词汇")
            return

        # 保存并去重
        filtered_terms, duplicate_count = self.deduplicate_terms(new_terms)

        if not filtered_terms:
            print("\n⚠️ 所有词汇都已存在于词库中")
            return

        # 备份
        self.backup_slang_dict()

        # 添加到词库
        self.slang_dict.update(filtered_terms)
        self.save_slang_dict()

        print(f"\n✅ 在线同步完成:")
        print(f"   📥 搜索: {len(new_terms)} 个")
        print(f"   🧹 去重: {duplicate_count} 个")
        print(f"   ➕ 新增: {len(filtered_terms)} 个")

    def add_term(self, term: str, desc: str, source: str = "手动添加"):
        """添加单个词汇"""
        if term in self.slang_dict:
            print(f"⚠️ 词汇已存在: {term}")
            print(f"   当前解释: {self.slang_dict[term]['desc']}")
            return False

        self.slang_dict[term] = {
            "desc": desc,
            "source": source,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "usage": "通用"
        }

        self.save_slang_dict()
        print(f"✅ 已添加: {term} → {desc}")
        return True

    def show_status(self):
        """显示词库状态"""
        print("📊 词库状态:\n")
        print(f"   📁 词库文件: {SLANG_DICT_FILE}")
        print(f"   📚 词汇数量: {len(self.slang_dict)}")

        if NEW_TERMS_FILE.exists():
            new_terms = self.load_new_terms()
            print(f"   📝 待添加: {len(new_terms)} 个")

        # 统计来源
        sources = {}
        for term, info in self.slang_dict.items():
            source = info.get('source', '未知')
            sources[source] = sources.get(source, 0) + 1

        if sources:
            print(f"\n   📋 来源统计:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
                print(f"      • {source}: {count} 个")

    def list_terms(self, limit: int = 20):
        """列出词汇"""
        print(f"📚 最新添加的词汇 (最多 {limit} 个):\n")

        terms_sorted = sorted(
            self.slang_dict.items(),
            key=lambda x: x[1].get('date', ''),
            reverse=True
        )[:limit]

        for term, info in terms_sorted:
            desc = info.get('desc', '无解释')
            source = info.get('source', '未知')
            print(f"   • {term}: {desc}")
            print(f"     (来源: {source})")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("📘 Internet Slang Updater\n")
        print("用法:")
        print("  python update_slang.py search-online     # 从互联网搜索新词")
        print("  python update_slang.py batch-add         # 批量添加搜索结果")
        print("  python update_slang.py sync-online       # 在线同步（搜索+添加）")
        print("  python update_slang.py add --term TERM --desc DESC  # 添加词汇")
        print("  python update_slang.py status             # 查看词库状态")
        print("  python update_slang.py list               # 列出词汇")
        return

    updater = SlangUpdater()
    command = sys.argv[1]

    if command == "search-online":
        terms = updater.search_online()
        if terms:
            updater.save_new_terms(terms)
            print(f"\n💡 下一步: python update_slang.py batch-add")
            print(f"   或: python update_slang.py sync-online")

    elif command == "batch-add":
        updater.batch_add()

    elif command == "sync-online":
        updater.sync_online()

    elif command == "add":
        if len(sys.argv) < 6:
            print("❌ 缺少参数")
            print("用法: python update_slang.py add --term TERM --desc DESC")
            return

        term = None
        desc = None

        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--term" and i + 1 < len(sys.argv):
                term = sys.argv[i + 1]
            elif sys.argv[i] == "--desc" and i + 1 < len(sys.argv):
                desc = sys.argv[i + 1]

        if not term or not desc:
            print("❌ 缺少参数")
            return

        updater.add_term(term, desc)

    elif command == "status":
        updater.show_status()

    elif command == "list":
        limit = 20
        if len(sys.argv) > 2:
            try:
                limit = int(sys.argv[2])
            except ValueError:
                pass
        updater.list_terms(limit)

    else:
        print(f"❌ 未知命令: {command}")
        print("运行不带参数查看帮助")


if __name__ == "__main__":
    main()
