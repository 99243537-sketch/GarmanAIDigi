#!/usr/bin/env python3
"""
AIDigi 数据检查脚本
用法：python3 tools/check_data.py   （在仓库根目录运行）
检查 data/ 下每个 CSV 的列名、数值、日期和链接格式。全部通过时退出码为 0，否则为 1。
只用 Python 标准库，无需安装依赖。
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# 每个文件：必需列、数值列、不能为空的列、链接列
SCHEMA = {
    "ai_users.csv": {
        "cols": ["product", "company", "region", "metric", "users_m", "as_of", "basis", "source", "url"],
        "num": ["users_m"], "required": ["product", "users_m", "as_of", "source"], "url": "url",
    },
    "ai_growth.csv": {
        "cols": ["series", "date", "users_m", "source"],
        "num": ["users_m"], "required": ["series", "date", "users_m", "source"], "url": None,
    },
    "ai_funding.csv": {
        "cols": ["company", "country", "round", "amount_busd", "valuation_busd", "date", "basis", "source", "url"],
        "num": ["amount_busd", "valuation_busd"], "required": ["company", "valuation_busd", "date", "source"], "url": "url",
    },
    "ai_capex.csv": {
        "cols": ["company", "quarter", "capex_busd", "outlook", "date", "scope", "source", "url"],
        "num": ["capex_busd"], "required": ["company", "quarter", "capex_busd", "scope", "source"], "url": "url",
    },
    "ai_compute.csv": {
        "cols": ["model", "developer", "date", "flop", "confidence", "source", "url"],
        "num": ["flop"], "required": ["model", "flop", "source"], "url": "url",
    },
    "ai_marketcap.csv": {
        "cols": ["company", "ticker", "role", "cap_busd", "as_of", "source", "url"],
        "num": ["cap_busd"], "required": ["company", "cap_busd", "as_of", "source"], "url": "url",
    },
    "ai_adoption_global.csv": {
        "cols": ["source", "scope", "population", "period", "value_pct", "qualifier", "method", "url"],
        "num": ["value_pct"], "required": ["source", "scope", "population", "period", "value_pct", "method"], "url": "url",
        "pct": ["value_pct"],
    },
    "ai_adoption_country.csv": {
        "cols": ["economy", "source", "period", "value_pct", "prev_pct", "url"],
        "num": ["value_pct", "prev_pct"], "required": ["economy", "source", "period", "value_pct"], "url": "url",
        "pct": ["value_pct", "prev_pct"],
    },
}

errors = []


def err(f, line, msg):
    errors.append(f"{f} 第 {line} 行：{msg}")


for fname, sch in SCHEMA.items():
    path = os.path.join(DATA, fname)
    if not os.path.exists(path):
        errors.append(f"{fname}：文件不存在")
        continue
    raw = open(path, "rb").read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        errors.append(f"{fname}：不是 UTF-8 编码（Excel 保存时请选“CSV UTF-8”）")
        continue
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        errors.append(f"{fname}：文件为空")
        continue
    header = rows[0]
    if header != sch["cols"]:
        errors.append(f"{fname}：列名不对。应为 {','.join(sch['cols'])}，实际为 {','.join(header)}")
        continue
    if len(rows) < 2:
        errors.append(f"{fname}：没有数据行")
    for i, row in enumerate(rows[1:], start=2):
        if not any(c.strip() for c in row):
            continue
        if len(row) != len(header):
            err(fname, i, f"有 {len(row)} 列，应为 {len(header)} 列（检查是否多了逗号）")
            continue
        r = dict(zip(header, row))
        for c in sch["required"]:
            if not r[c].strip():
                err(fname, i, f"“{c}”不能为空")
        for c in sch["num"]:
            v = r[c].strip()
            if not v:
                continue
            try:
                x = float(v)
            except ValueError:
                err(fname, i, f"“{c}”应为数字，实际为“{v}”（不要带单位、逗号或百分号）")
                continue
            if x < 0:
                err(fname, i, f"“{c}”不能为负数")
            if c in sch.get("pct", []) and x > 100:
                err(fname, i, f"“{c}”是百分比，不能超过 100")
        u = sch["url"]
        if u and r[u].strip() and not re.match(r"^https://\S+$", r[u].strip()):
            err(fname, i, f"链接必须以 https:// 开头且不含空格：{r[u]}")
        for c in ("date", "as_of"):
            if c in r and r[c].strip() and not re.match(r"^\d{4}-\d{2}(-\d{2})?$", r[c].strip()):
                err(fname, i, f"“{c}”格式应为 YYYY-MM 或 YYYY-MM-DD，实际为“{r[c]}”")

# 各数据集的特定检查
try:
    rows = list(csv.DictReader(open(os.path.join(DATA, "ai_adoption_country.csv"), encoding="utf-8-sig")))
    for need in ("全球", "美国", "中国"):
        if not any(r["economy"] == need and r["source"] == "微软" for r in rows):
            errors.append(f"ai_adoption_country.csv：页面顶部数字需要一行 economy={need}、source=微软")
    rows = list(csv.DictReader(open(os.path.join(DATA, "ai_adoption_global.csv"), encoding="utf-8-sig")))
    if not any(r["source"] == "CNNIC" for r in rows):
        errors.append("ai_adoption_global.csv：页面中国卡片需要一行 source=CNNIC")
except Exception as e:  # 上面已报告的文件问题会导致这里读取失败
    errors.append(f"特定检查未能完成：{e}")

if errors:
    print("数据检查未通过：")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print(f"数据检查通过：{len(SCHEMA)} 个文件。")
