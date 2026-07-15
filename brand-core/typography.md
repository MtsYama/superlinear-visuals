# Superlinear Academy · 字体规范

> 权威来源：Brand Guidelines **V2.0**（2026-03）Typography 页 · 抽取 2026-07-15 · v2.2 建设用。

## 字族

| 用途 | 字体 | 说明 |
|---|---|---|
| **Logo + 标题/副标题** | **Albert Sans** | 官方 logo 字体（Regular + SemiBold）· **不可替换 / 不可改动字形**。本地源文件见下。 |
| **正文 / 长文阅读** | **Inter** | 段落、说明、长文 |
| **中文** | **思源黑体**（Noto Sans SC / Source Han Sans）推荐 · fallback 微软雅黑 Microsoft YaHei | 中英混排时中文配 Albert Sans 或 Inter |

## 字体源文件

- `AlbertSans[wght].ttf`（可变字重）当前在 `cert-issuance/templates/fonts/`。
- 建议 v2.2 时把它做成**单一源** `brand-core/fonts/AlbertSans[wght].ttf`，证书系统与网页 guideline 都引用同一份（避免多副本漂移）。Albert Sans 与 Inter 均为 OFL 开源字体，可随库分发 / 网页 @font-face。

## 网页 v2.2 加载建议

- Albert Sans / Inter：Google Fonts 或自托管 `@font-face`（OFL 允许）。
- 中文：思源黑体自托管或系统 fallback 链 `"Source Han Sans SC","Noto Sans SC","Microsoft YaHei",sans-serif`。
- 遵守全局 A11y 底线：正文 ≥ 18px（目标 20px）· 小字 ≥ 14px。
