# AIDigi · 全球 AI 行业公开数据与估算

AIDigi 汇总主流 AI 模型与应用的公开数据和第三方估算，帮助学习者了解 AI 行业的大致轮廓。**不构成投资建议。**

页面包含六个板块：

| 板块 | 内容 | 主要来源 |
|---|---|---|
| 全球 AI 应用普及率 | 全球与主要经济体使用生成式 AI 的人口比例，五项调查口径对照 | 微软 AI 扩散报告、CNNIC、OECD、Eurostat、Google / Ipsos |
| 用户规模 | 主流 AI 助手的周活 / 月活，ChatGPT 与 Gemini 增长轨迹 | 公司公布、QuestMobile、Sensor Tower |
| 融资与估值 | 头部 AI 公司最近一轮融资额与融资后估值 | 公司公告、媒体报道 |
| 算力投入 | 四大科技公司季度资本开支、知名模型训练算力 | 公司财报、Epoch AI |
| 上市公司市值 | AI 产业链主要上市公司市值快照 | 财经媒体 |
| 怎么读这些数字 | 口径说明与常见误读 | — |

每个数字都标注了日期、出处，以及是“公司公布”还是“第三方估算”。

## 目录结构

```
index.html            页面（唯一的 HTML 文件）
assets/theme.css      配色、字号等样式变量（自动适配深色模式）
assets/data-loader.js 读取 data/ 下的 CSV 并交给页面绘制
data/*.csv            全部数据，UTF-8 编码
vendor/d3.v7.min.js   图表库 D3.js 7.9.0（已内置，不依赖外部 CDN）
部署说明.md            给网站管理员的部署说明
数据维护说明.md        每月更新数据的流程与规则（Eddy 执行）
tools/check_data.py   数据格式检查脚本，改完 CSV 后运行
CLAUDE.md             给 AI 助手读的项目背景
maintenance/log.md    数据维护日志
```

## 本地预览

页面要通过网页服务器打开（直接双击 `index.html` 会因浏览器安全限制读不到数据）：

```bash
cd GarmanAIDigi
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000
```

## 更新数据

定期维护的节奏、数据源和核验规则见 `数据维护说明.md`。

数据全部在 `data/` 目录的 CSV 文件里，用 Excel、WPS 或任意文本编辑器修改即可，**不需要改代码**。

| 文件 | 内容 | 数值单位 |
|---|---|---|
| `ai_users.csv` | 各产品最新用户数 | `users_m`：百万人 |
| `ai_growth.csv` | ChatGPT、Gemini 历次公布的用户数 | `users_m`：百万人 |
| `ai_funding.csv` | 融资额与融资后估值 | `amount_busd`、`valuation_busd`：十亿美元 |
| `ai_capex.csv` | 季度资本开支 | `capex_busd`：十亿美元 |
| `ai_compute.csv` | 模型训练算力 | `flop`：科学计数法，如 `2.1e25` |
| `ai_marketcap.csv` | 上市公司市值 | `cap_busd`：十亿美元 |
| `ai_adoption_global.csv` | 各项普及率调查的总体数字 | `value_pct`：百分比，如 `18.8`；`qualifier`：可选限定词，如“超” |
| `ai_adoption_country.csv` | 各经济体普及率（`source` 列为“微软”或“OECD”） | `value_pct`、`prev_pct`（上一期，可空）：百分比 |

修改规则：

- **不要改第一行的列名**，页面靠列名找数据。
- 新增一行即可在图表和表格里多出一项；`url` 列填出处网址。
- 用 Excel 保存时选择“CSV UTF-8（逗号分隔）”，否则中文会乱码。
- 改完数据后运行 `python3 tools/check_data.py`，显示“数据检查通过”才能发布。
- 同步修改 `index.html` 页脚里的核验日期。

## 数据说明与授权

- 模型训练算力来自 [Epoch AI](https://epoch.ai/data/ai-models)，采用 CC BY 4.0 授权，转载需注明出处（页脚已注明）。
- 其余数据为人工整理自公开报道与公司披露，出处见各 CSV 的 `source`、`url` 列。
- D3.js 采用 ISC 许可证，见 `vendor/d3-LICENSE.txt`。
