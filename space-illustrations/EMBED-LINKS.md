# Space Group 插图 · 嵌入链接清单

仓库：<https://github.com/MtsYama/superlinear-visuals>

**用法**：复制 **PNG 链接** → 平台「Embed link」框粘贴 → Embed Image。
（Embed link 框只支持 JPG/PNG/GIF，**不吃 SVG**；SVG 是可编辑源文件。）

四套统一命名（受根 README 链接稳定契约保护）：

| 套 | 身份 | 底色 | 目录 |
|---|---|---|---|
| **✅ mono** | **正式版（2026-07-15 终选）· 新嵌入一律用它** | `#F4F3F1` 中性暖灰 | `out-mono/` |
| seven | 备份（七色）· 特殊场合备用 | `#F4F3F1` | `out-seven/` |
| vivid | 对照存档 · 官方 icon 米底原蓝，仅展示不嵌入 | `#EEEBE0` | `out-vivid/` |
| v1 | 旧版 · 已复制出去的旧链接专用，永久保留 | `#F4F3F1` | `out/`（特例名 · tag `illustrations-v1`） |

---

## ✅ 正式版 mono（新嵌入用这套）

配色：浅灰底 `#F4F3F1` · 官方墨 `#1E1E1E`（Primary 1）· 官方蓝降饱和 `#7E97BD`（源自 `#4B96FF`）

| 空间 | PNG 直链（raw · 复制即用） |
|---|---|
| 市政厅 | `https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/png/townhall.png` |
| 广场 | `https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/png/plaza.png` |
| 俱乐部 | `https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/png/club.png` |
| 会场 | `https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/png/venue.png` |
| 工作室 | `https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/png/studio.png` |
| 课程 | `https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/png/courses.png` |
| 实验田 | `https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/png/field.png` |

Pages 版（CDN 更稳）：把域名段换成 `https://mtsyama.github.io/superlinear-visuals/`，路径不变。

### 📱 mono 横版 wide（responsive campaign · 2026-07-15 加）

**用在会被叠印文字的横卡位**（手机 app 空间导航卡等）：16:9 · 2560×1440 · 主体右上、左侧+底部留白给 Circle 叠字 · 抗 1.5:1~2:1 中心裁。1:1 方版仍是 base，用在方形位。

前缀：`https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-mono/wide/png/`

### 📐 mono banner 版（2.8:1 · Circle Directory 官方推荐比例 · 2026-07-16 加）

840×300 设计 · 1680×600 PNG · 主体右置左半留叠字区。**备选**：仅当实测 app 卡片为扁长条时用（当前观测卡片 ≈1.63:1 → wide 版为准）。
前缀：`.../main/space-illustrations/out-mono/banner/png/`，7 个 slug 同上。

| 空间 | 横版 PNG 直链 |
|---|---|
| 市政厅 | `…/out-mono/wide/png/townhall.png` |
| 广场 | `…/out-mono/wide/png/plaza.png` |
| 俱乐部 | `…/out-mono/wide/png/club.png` |
| 会场 | `…/out-mono/wide/png/venue.png` |
| 工作室 | `…/out-mono/wide/png/studio.png` |
| 课程 | `…/out-mono/wide/png/courses.png` |
| 实验田 | `…/out-mono/wide/png/field.png` |

## seven · 备份（特殊场合）

前缀 `.../main/space-illustrations/out-seven/png/`，7 个 slug 同上。7 组各一 dusty 色（townhall `#6E8CAE` / plaza `#6D9E96` / club `#9284AE` / venue `#C0A36E` / studio `#C08A6B` / courses `#7A85A8` / field `#99A566`）。

## vivid · 对照（不出嵌入链接）

仅 SVG（`out-vivid/*.svg`），在画廊/对比里展示用。

## v1 · 旧版（旧链接专用 · 不用于新嵌入）

前缀 `.../main/space-illustrations/out/png/`。已复制出去的链接全指这套，永久有效；tag 快照 `illustrations-v1`。

## 画廊 / 源文件

- 切换画廊（默认 mono · 4 按钮换套 · 裁切安全线开关）：
  `https://mtsyama.github.io/superlinear-visuals/space-illustrations/gallery.html`
  hash 直达：`#mono` / `#seven` / `#vivid` / `#v1`
- SVG 源：各套目录 `<slug>.svg` · 重生成：`python build_illustrations.py --palette mono|seven|vivid`（默认 v1）
