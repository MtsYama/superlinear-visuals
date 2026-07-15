# GPT 生图 prompts · Space Group 插图（对比用）

> 用途：拿去 ChatGPT（GPT Image / DALL·E）出一套**位图**版，跟我这套 SVG 矢量版对比效果。
> 用法：**一条一个**复制整段发给 GPT，一次出一张（要成套一致，就每张都带同一段风格前缀——下面每条都已内嵌）。
> 英文 prompt（图像模型英文效果更好）。想要中文我也可以出一版。
> 一致性提示：出图时告诉 GPT「keep the same style, palette, and framing across all seven」，或把已出的第一张贴回去让它对齐。

**共用配色（想让 GPT 贴我这套就把 hex 保留）**：底 `#F4F3F1`、线 `#1B1D21`；各组强调色见每条末尾。

---

### 1 · 市政厅 Town Hall（免费区 · 强调 `#3E6FB0`）
```
Flat vector editorial illustration, minimal and clean, 1:1 square. A small neoclassical civic hall: a triangular pediment resting on a row of slender columns, wide steps, a tiny pennant flag on top and a round emblem in the pediment — a symbol of an official welcome desk / town hall. Thin consistent dark outlines (#1B1D21), limited palette, one soft accent color #3E6FB0 with a paler tint, warm light-grey background #F4F3F1 with a very subtle dotted paper texture, a small pale circle like a sun in the top-right, object centered on a thin horizon line, generous negative space. No text, no people, no gradients, no glow.
```

### 2 · 广场 Plaza（免费区 · 强调 `#2E9C8D`）
```
Flat vector editorial illustration, minimal and clean, 1:1 square. An open public square with a small tiered stone fountain in the center (basin, stem, upper bowl, gentle water arcs), a string of festive triangular bunting flags arching across the top, faint concentric paving rings on the ground — a lively public gathering space. Thin consistent dark outlines (#1B1D21), limited palette, one soft accent color #2E9C8D with a paler tint, warm light-grey background #F4F3F1 with a very subtle dotted paper texture, a small pale circle like a sun in the top-right, centered on a thin horizon line, generous negative space. No text, no people, no gradients, no glow.
```

### 3 · 俱乐部 Club（Stay Superlinear · 强调 `#7A5AA6`）
```
Flat vector editorial illustration, minimal and clean, 1:1 square. Two cozy armchairs facing each other with a small round side table and a single cup between them, and one pendant lamp hanging above — an intimate members' lounge for deep conversation. Thin consistent dark outlines (#1B1D21), limited palette, one soft accent color #7A5AA6 with a paler tint, warm light-grey background #F4F3F1 with a very subtle dotted paper texture, a small pale circle like a sun in the top-right, furniture resting on a thin horizon line, generous negative space. No text, no people, no gradients, no glow.
```

### 4 · 会场 Venue（Stay Superlinear · 强调 `#BE8C2C`）
```
Flat vector editorial illustration, minimal and clean, 1:1 square. A small auditorium stage: a screen showing a simple play/triangle icon, a soft spotlight beam coming from above, a stage valance across the top, and a few rows of tidy seats in front — a masterclass venue and replay hall. Thin consistent dark outlines (#1B1D21), limited palette, one soft accent color #BE8C2C with a paler tint, warm light-grey background #F4F3F1 with a very subtle dotted paper texture, a small pale circle like a sun in the top-right, centered on a thin horizon line, generous negative space. No text, no people, no gradients, no glow.
```

### 5 · 工作室 Studio（Stay Superlinear · 强调 `#BE6438`）
```
Flat vector editorial illustration, minimal and clean, 1:1 square. A maker's workbench holding a glowing light bulb, a chemistry flask with a little liquid, and a single gear — a workshop of tools and co-creation. Thin consistent dark outlines (#1B1D21), limited palette, one soft accent color #BE6438 with a paler tint, warm light-grey background #F4F3F1 with a very subtle dotted paper texture, a small pale circle like a sun in the top-right, objects resting on a thin bench line, generous negative space. No text, no people, no gradients, no glow.
```

### 6 · 课程 Courses（Academy · 强调 `#3A4C86`）
```
Flat vector editorial illustration, minimal and clean, 1:1 square. A neat stack of books with a graduation cap resting on top, and an open fanned book beside it — structured, sequential learning. Thin consistent dark outlines (#1B1D21), limited palette, one soft accent color #3A4C86 with a paler tint, warm light-grey background #F4F3F1 with a very subtle dotted paper texture, a small pale circle like a sun in the top-right, resting on a thin horizon line, generous negative space. No text, no people, no gradients, no glow.
```

### 7 · 实验田 Field（Superlinear · 强调 `#79982F`）
```
Flat vector editorial illustration, minimal and clean, 1:1 square. Three young seedlings sprouting from gentle soil mounds on an open plot of soft farmland — an experimental field of new, unfinished ideas. Thin consistent dark outlines (#1B1D21), limited palette, one soft accent color #79982F with a paler tint, warm light-grey background #F4F3F1 with a very subtle dotted paper texture, a small pale circle like a sun in the top-right, seedlings on a thin ground line, generous negative space. No text, no people, no gradients, no glow.
```

---

## 对比时看什么

| 维度 | 我的 SVG 版 | GPT 位图版 |
|---|---|---|
| 矢量/可缩放 | ✅ 无损，任意尺寸（含后面超长超扁版） | ❌ 位图，放大糊 |
| 可编辑 | ✅ 拖进 Figma/AI 改，或改脚本重刷 | ❌ 改不了，只能重新生成 |
| 成套一致 | ✅ 同框同色同纹，天生一致 | ⚠️ 需反复调，容易每张风格漂 |
| 质感/丰富度 | 克制、几何、干净 | 可能更有"绘感"、更暖或更花 |
| 出图速度 | 改脚本秒出 | 一张张等 |

→ 看你要的是「干净可维护的系统件」还是「更有插画味的单张」。也可以两者取长：拿 GPT 的方向感，让我用 SVG 复刻成可维护版。
