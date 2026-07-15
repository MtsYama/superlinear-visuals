# Superlinear Visuals

山山（Mts Shu）自制的 **Superlinear Academy 视觉 / 品牌系统**归档。公开托管，供社区嵌入复用，同时留可编辑源文件。

> 不是所有 Superlinear 视觉内容都在这里 —— 这里收「我自己做的」那部分，作为**可公开引用的图床 + 源文件归档**。其它来源的物料后续再统一同步进来。

## 目录

| 子目录 | 内容 | 状态 |
|---|---|---|
| `space-illustrations/` | 7 个 space group 矢量插图（SVG 源 + PNG 成品 + 生成器） | ✅ v1 |
| `guidelines/` | Superlinear 社区 / 品牌 guideline 在线版（v2.2 · 网页优先，PDF 后补） | 🚧 规划中 |
| `certificates/` | 结业证书模板 / 导出 | 🚧 规划中 |
| `brand-assets/` | logo · 配色 · 字体 · banner 等共用视觉件 | 🚧 规划中 |

## 怎么拿嵌入链接（Embed link）

平台的「Embed link」框只吃**公开直链**，且只支持 **JPG / PNG / GIF（不吃 SVG）**。所以嵌入用 PNG 直链：

```
https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/<路径>.png
```

例（市政厅插图）：
```
https://raw.githubusercontent.com/MtsYama/superlinear-visuals/main/space-illustrations/out/png/townhall.png
```

复制 PNG URL → 贴进平台「Embed link」框 → Embed Image。换图只改这一处，不用每次本地上传。

- **PNG** = 用来嵌入（raster，平台支持）
- **SVG** = 可编辑源文件（拖进 Figma / Illustrator 改，或改脚本重刷）

## 加新内容

新建一个子目录丢进去 → `git add` → `git commit` → `git push`。PNG 推上去后自动获得公开直链。

## 各项目细节

见各子目录自己的 `README.md`。
