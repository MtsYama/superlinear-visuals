# Superlinear Visuals

山山（Mts Shu）自制的 **Superlinear Academy 视觉 / 品牌系统**归档。公开托管，供社区嵌入复用，同时留可编辑源文件。

> 不是所有 Superlinear 视觉内容都在这里 —— 这里收「我自己做的」那部分，作为**可公开引用的图床 + 源文件归档**。其它来源的物料后续再统一同步进来。

## 目录

| 子目录 | 内容 | 状态 |
|---|---|---|
| `space-illustrations/` | 7 个 space group 矢量插图（SVG 源 + PNG 成品 + 生成器 + 嵌入链接清单） | ✅ v1（tag `illustrations-v1`） |
| `brand-core/` | 官方品牌 token（配色 palette / 字体 typography） | ✅ 初版 |
| `guidelines/` | Superlinear 社区 / 品牌 guideline 在线版（v2.2 · 网页优先，PDF 后补） | 🚧 占位 |
| `certificates/` | 结业证书视觉资产 | 🚧 占位 |
| `brand-assets/` | logo · banner · 头图等共用视觉件 | 🚧 占位 |

## 🔒 链接稳定契约（本库硬规则）

已经被复制出去、嵌进平台的链接**永远不能断**。因此：

1. **已发布路径永不改名、永不删除**。`space-illustrations/out/png/*.png` 这类已被引用的路径是冻结的；新内容只**新增**文件/目录，不动旧路径。
2. **分支就叫 `main`，库名不改，库不转私有**——这三样任何一个变了，所有 raw 链接全断。
3. **原地修订 vs 换版**：小修（错位、瑕疵）允许原地覆盖同名 PNG——所有嵌入处自动显示新图（这是图床的优点）；**大改版**（例如换成官方品牌配色）出**新文件名或新目录**（如 `out/png-v2/`），旧文件原样保留。
4. **要永久冻结某个版本**：用 tag 链接代替 `main`。tag 指向的内容永不再变：
   ```
   https://raw.githubusercontent.com/MtsYama/superlinear-visuals/illustrations-v1/space-illustrations/out/png/townhall.png
   ```
   `main` 链接 = 始终最新；tag 链接 = 永久快照。两种都长期有效，按需选。

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
