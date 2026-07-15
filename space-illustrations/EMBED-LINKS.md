# Space Group 插图 · 嵌入链接清单

仓库：<https://github.com/MtsYama/superlinear-visuals>

**用法**：复制 **PNG 链接** → 平台「Embed link」框粘贴 → Embed Image。
（Embed link 框只支持 JPG/PNG/GIF，**不吃 SVG**；SVG 是可编辑源文件。）

三套并存（受根 README 链接稳定契约保护，路径永不改名删除）：

| 套 | 状态 | 目录 |
|---|---|---|
| **✅ 褪色 mono** | **正式版（2026-07-15 终选）· 新用途一律用它** | `out-faded-mono/` |
| 褪色七色 | 备份 · 特殊场合备用，平时不用 | `out-faded-family/` |
| v1 同族七色 | legacy · 已复制出去的旧链接靠它活着，永久保留 | `out/` |
| 官方非褪色 | 对照存档 · 仅画廊/对比里展示，不出嵌入链接 | `out-official-beige/` |

raw = 推送后即用；Pages = CDN 更稳。永久钉死某版本：URL 里 `main` 换成 tag（v1 有 `illustrations-v1`）。

---

## ✅ 正式版 · 褪色 mono（新嵌入用这套）

前缀：`https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-faded-mono/png/`
（Pages 版把域名换成 `https://mtsyama.github.io/superlinear-visuals/space-illustrations/out-faded-mono/png/`）

| 组 | PNG 直链（raw） |
|---|---|
| 市政厅 townhall | `…/out-faded-mono/png/townhall.png` |
| 广场 plaza | `…/out-faded-mono/png/plaza.png` |
| 俱乐部 club | `…/out-faded-mono/png/club.png` |
| 会场 venue | `…/out-faded-mono/png/venue.png` |
| 工作室 studio | `…/out-faded-mono/png/studio.png` |
| 课程 courses | `…/out-faded-mono/png/courses.png` |
| 实验田 field | `…/out-faded-mono/png/field.png` |

完整示例（市政厅）：
```
https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-faded-mono/png/townhall.png
```

配色：官方米底 `#EEEBE0`（Icon_Azure_HaveBgd 同款）· 官方墨 `#1E1E1E` · 官方蓝降饱和 `#7E97BD`。

## 备份 · 褪色七色（特殊场合备用）

前缀：`https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out-faded-family/png/`
文件名同上 7 个 slug。7 组各一 dusty 色（townhall `#6E8CAE` / plaza `#6D9E96` / club `#9284AE` / venue `#C0A36E` / studio `#C08A6B` / courses `#7A85A8` / field `#99A566`），底墨与正式版相同。

## Legacy · v1 同族七色（旧链接专用 · 不用于新嵌入）

前缀：`https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out/png/`
已复制出去的链接全部指这套，按链接契约永久有效。永久快照 tag：`illustrations-v1`。

## 画廊 / 源文件

- 切换画廊（默认显示正式版 mono · 按钮换套 · 含裁切安全线开关）：
  `https://mtsyama.github.io/superlinear-visuals/space-illustrations/gallery.html`
  hash 直达：`gallery.html#family` / `#faded-family` / `#faded-mono`
- SVG 源：各套目录下 `<slug>.svg`（拖进 Figma/Illustrator 可编辑）
- 重生成：`python build_illustrations.py [--palette faded-mono|faded-family|official-beige]`
