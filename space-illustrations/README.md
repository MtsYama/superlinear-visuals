# Space Group 矢量插图 · Stay Superlinear

7 张 space group 插图（对应 Circle 空间重构的 7 个分区）。真 SVG 矢量 · 可缩放 · 可编辑 · 参数化生成。

> 2026-07-15 定稿：**正式版 = mono**（浅灰底 + 官方墨 + 官方蓝降饱和）。四套统一命名，并存互不影响。

## 四套配色（统一命名）

| 套 | 身份 | 底 / 墨 / 强调 | 目录 |
|---|---|---|---|
| **✅ mono** | **正式版（终选 2026-07-15）** | `#F4F3F1` 中性暖灰 / `#1E1E1E`（Primary 1）/ `#7E97BD`（官方蓝 #4B96FF 降饱和） | `out-mono/` |
| seven | 备份 · 特殊场合备用 | 同底同墨 / 7 组各一 dusty 色 | `out-seven/` |
| vivid | 对照存档 · 平时不用 | `#EEEBE0`（官方 icon 米底 Icon_Azure_HaveBgd）/ 同墨 / 官方蓝原样 `#0E6EF4` | `out-vivid/` |
| v1 | 旧版 · 旧嵌入链接专用，路径冻结 | `#F4F3F1` / `#1B1D21` / 7 组饱和色 | `out/`（特例名 · tag `illustrations-v1`） |

要点：mono 品牌血缘最纯、加新空间零配色决策；底色用中性暖灰而非米色（奶油米底已是 AI 风指纹，且 `#F4F3F1` 更接近官方 Primary 2 `#EEEEEE`）；官方米底保留在 vivid 对照版。完整决策过程见 4 列对比归档（内部 planning 目录）。

## 文件

| 路径 | 是什么 |
|---|---|
| `build_illustrations.py` | **生成器**。`--palette` 切配色（v1 / mono / seven / vivid），motif/黑块开关/安全边距都在里面。 |
| `out*/` ×4 | 四套成品：`<slug>.svg`（源）；mono/seven/v1 另有 `png/<slug>.png`（2x · 嵌入用），vivid 仅 SVG。**mono 另有 `wide/`（16:9 横版 · 叠字卡位用 · 主体右上留字区）** |
| `gallery.html` | **切换画廊**：4 按钮换套（默认 ✅ mono）· 色块/底色联动 · 裁切安全线开关 · hash 直达 `#mono` 等 |
| `compare.html` | 4 列对比（本地工作文件 · 不入库） |
| `EMBED-LINKS.md` | **嵌入链接清单**（四套直链与身份） |
| `gpt-prompts.md` | GPT 位图对比版 prompt（探索期产物） |

## 怎么改

1. **重刷某套**：`python build_illustrations.py --palette mono`（默认 v1；v1 输出字节冻结勿动）。
2. **改造型**：改对应 `m_<slug>()` 坐标重跑——四套共用 motif，一改全套生效。
3. **直接改图**：任一 `out*/<slug>.svg` 拖进 Figma / Illustrator。
4. **PNG 重渲**：Chrome headless `--force-device-scale-factor=2 --default-background-color=00000000 --screenshot=... --window-size=640,640 <svg>`。

## 设计约定

- **无文字** · **黑块统一**（mono/seven/vivid 无大墨块；v1 保留原样）· **裁切安全**（主体在中心 480×480，抗 3:4 与 4:3 中心裁，画廊有校验线开关）· 横版=`--wide`（16:9 · 2560×1440 · 抗 1.5~2:1 裁 · 手机 app 卡位实测调校 2026-07-15）。
- 链接稳定契约见仓库根 README：已发布路径永不改名删除（2026-07-15 定名 mono/seven/vivid 后即冻结）。
