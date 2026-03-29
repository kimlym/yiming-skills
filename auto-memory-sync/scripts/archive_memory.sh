#!/bin/bash

# Auto Memory Archive Script
# 归档 90 天以上的记忆文件

set -e

# 配置
WORKSPACE="/Users/yiminglu/.openclaw/workspace"
MEMORY_DIR="${WORKSPACE}/memory"
ARCHIVE_DIR="${MEMORY_DIR}/archive"
ARCHIVE_DAYS=90

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Auto Memory Archive"
echo "=================="
echo ""

# 创建归档目录
if [ ! -d "$ARCHIVE_DIR" ]; then
    echo -e "${BLUE}创建归档目录${NC}: $ARCHIVE_DIR"
    mkdir -p "$ARCHIVE_DIR"
fi

# 获取截止日期
ARCHIVE_DATE=$(date -v-${ARCHIVE_DAYS}d +%Y%m%d 2>/dev/null || date -d "-${ARCHIVE_DAYS} days" +%Y%m%d)

echo "归档阈值: $ARCHIVE_DAYS 天（${ARCHIVE_DATE} 之前）"
echo ""

# 扫描记忆文件
count=0
archived=0

for file in "$MEMORY_DIR"/*.md; do
    # 跳过 README、MEMORY.md 等非日期文件
    basename=$(basename "$file")
    if [[ ! $basename =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.md$ ]]; then
        continue
    fi

    count=$((count + 1))

    # 提取日期并转换为 YYYYMMDD 格式
    file_date=$(basename "$file" .md | tr -d '-')
    file_date_num=${file_date//-/}

    # 比较日期
    if [ "$file_date_num" -lt "$ARCHIVE_DATE" ]; then
        echo -e "${YELLOW}归档${NC}: $basename"
        mv "$file" "$ARCHIVE_DIR/"
        archived=$((archived + 1))
    fi
done

echo ""
echo -e "${GREEN}扫描完成${NC}"
echo "扫描文件数: $count"
echo "归档文件数: $archived"
echo "归档目录: $ARCHIVE_DIR/"
