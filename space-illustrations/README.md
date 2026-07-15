# Space Group 矢量插图 · Stay Superlinear

一套 7 张 space group 插图（对应新 Circle 空间重构的 7 个分区）。真 SVG 矢量 · 可缩放 · 可编辑 · 参数化生成。

> 2026-07-15 建 · 1:1 版先做，超长超扁版预留。这是探索/对比稿，非定稿。

## 文件

| 路径 | 是什么 |
|---|---|
| `build_illustrations.py` | **生成器**（改这里，整套重刷）。配色/尺寸/每组 motif 都在里面。 |
| `out/*.svg` | 7 张 SVG 成品（townhall/plaza/club/venue/studio/courses/field）。 |
| `gallery.html` | 画廊预览（双击开，看全套 + 配色）。 |
| `gpt-prompts.md` | 拿去 GPT 出位图对比版的 7 段 prompt。 |

## 7 组 ↔ 分区 ↔ 配色

| slug | 中文 | 分区 | 强调色 |
|---|---|---|---|
| townhall | 市政厅 | 免费区 | `#3E6FB0` 蓝 |
| plaza | 广场 | 免费区 | `#2E9C8D` 青 |
| club | 俱乐部 | Stay Superlinear | `#7A5AA6` 紫 |
| venue | 会场 | Stay Superlinear | `#BE8C2C` 琥珀 |
| studio | 工作室 | Stay Superlinear | `#BE6438` 铜橙 |
| courses | 课程 | Academy | `#3A4C86` 靛 |
| field | 实验田 | Superlinear | `#79982F` 橄榄 |

共享：底 `#F4F3F1`、线 `#1B1D21`、统一点纹、柔光球、基线。7 色同族，成套。

## 怎么改（三种）

1. **换配色/尺寸**：改 `build_illustrations.py` 顶部 `GROUPS` / `GROUND` / `INK`，重跑 `python build_illustrations.py`。
2. **改某张造型**：改对应 `m_<slug>()` 函数里的坐标，重跑。
3. **直接改图**：`out/*.svg` 拖进 Figma / Illustrator 手动改（SVG 干净导入，图层可拆）。

## 后续超长超扁版（预留）

`build_illustrations.py` 已留 `--wide` 开关。要做时把画框 `W/H` 和各 motif 的布局参数改成横向长条（元素沿水平重排即可，因为是矢量，不用重画）。现在 `--wide` 是占位，需要时我补横版布局。

## 重跑 / 渲染

```bash
python build_illustrations.py            # 出 SVG + gallery.html
# 渲 PNG 预览（Windows Chrome）：
chrome --headless --screenshot=preview.png --window-size=1120,1560 gallery.html
```

## 说明

- 配色贴 Superlinear 极简气质（浅底、克制、几何），**未**套 MX_Studio 暗金。品牌真配色定了可一键替换 `GROUPS` 里的 hex。
- 插图**不含文字**（更好复用，也能当背景底纹）。标题在 `gallery.html` 里，不在图内。
- 兜底：真要背景纹理/pattern 版（山山 07-15 提的备选），点纹已在图里，可单独抽成 tileable pattern，需要时说一声。
