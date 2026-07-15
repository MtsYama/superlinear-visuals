# Space Group 矢量插图 · Stay Superlinear

7 张 space group 插图（对应 Circle 空间重构的 7 个分区）。真 SVG 矢量 · 可缩放 · 可编辑 · 参数化生成。

> 2026-07-15 定稿：**正式版 = 褪色 mono**（官方米底 + 官方墨 + 官方蓝降饱和）。另存七色备份与 v1 legacy，三套并存互不影响。

## 配色版本

| 套 | 状态 | 底 / 墨 / 强调 | 目录 |
|---|---|---|---|
| **✅ 褪色 mono** | **正式版（终选 2026-07-15）** | `#EEEBE0`（官方 icon 米底）/ `#1E1E1E`（Primary 1）/ `#7E97BD`（官方蓝 #4B96FF 降饱和） | `out-faded-mono/` |
| 褪色七色 | 备份 · 特殊场合备用 | 同底同墨 / 7 组各一 dusty 色 | `out-faded-family/` |
| v1 同族七色 | legacy · 旧嵌入链接专用，路径冻结 | `#F4F3F1` / `#1B1D21` / 7 组饱和色 | `out/`（tag `illustrations-v1`） |

选型理由与全过程见 4 列对比归档（内部 planning 目录）。要点：mono 品牌血缘最纯、加新空间零配色决策、Circle 里空间名永远在图旁所以颜色导航是冗余；淘汰过两稿（#EEEEEE 底艳蓝 mono、米底非褪色 #0E6EF4）。

## 文件

| 路径 | 是什么 |
|---|---|
| `build_illustrations.py` | **生成器**。`--palette` 切配色（family / faded-mono / faded-family / official-beige），motif/黑块开关/安全边距都在里面。 |
| `out*/` ×3 | 三套成品：`<slug>.svg`（源）+ `png/<slug>.png`（2x · 嵌入用） |
| `gallery.html` | **切换画廊**：按钮换套（默认显示正式版 mono）· 色块/底色联动 · 裁切安全线开关 · hash 直达 `#family` 等 |
| `compare.html` | 三列对比（工作文件 · 4 列决策版已归档） |
| `EMBED-LINKS.md` | **嵌入链接清单**（正式/备份/legacy 三套直链） |
| `gpt-prompts.md` | GPT 位图对比版 prompt（探索期产物） |

## 怎么改

1. **重刷某套**：`python build_illustrations.py --palette faded-mono`（默认 family=v1，v1 输出字节冻结勿动）。
2. **改造型**：改对应 `m_<slug>()` 坐标重跑——三套共用 motif，一改全套生效。
3. **直接改图**：任一 `out*/<slug>.svg` 拖进 Figma / Illustrator。
4. **PNG 重渲**：Chrome headless `--force-device-scale-factor=2 --default-background-color=00000000 --screenshot=... --window-size=640,640 <svg>`。

## 设计约定

- **无文字**（复用性/本地化）· **黑块统一**（正式/备份两套无大墨块；v1 保留原样）· **裁切安全**（主体在中心 480×480，抗 3:4 与 4:3 中心裁，画廊有校验线开关）· 超长超扁版留 `--wide` 占位待做。
- 链接稳定契约见仓库根 README：已发布路径永不改名删除。
