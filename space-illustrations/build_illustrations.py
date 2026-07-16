#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stay Superlinear · Space Group 矢量插图生成器
================================================
一套共享画框 + 配色 + 纹理，7 个 space group 各一个 motif。
改配色/尺寸/motif 后重跑即整套刷新。1:1 版现做；wide(超长超扁)版预留 MODE 开关。

用法:
    python build_illustrations.py            # 出 1:1 方形版
    python build_illustrations.py --wide     # 出超长超扁版(预留 · 目前 = 方形版拉伸占位)

产物: out/<slug>.svg  ×7  +  gallery.html
"""
import argparse, os, math

# ---------------------------------------------------------------- palette
GROUND   = "#F4F3F1"   # 浅底 · 微暖中性 (可换成 Superlinear 品牌白)
INK      = "#1B1D21"   # 主线/主字
INK_SOFT = "#585C63"   # 次级线
WHITE    = "#FFFFFF"

# 7 组 · (slug, 中文名, 分区, 强调色, 强调浅色) —— 同族饱和度/明度，成套
GROUPS = [
    ("townhall", "市政厅",  "免费区",           "#3E6FB0", "#CBD9EC"),  # civic blue
    ("plaza",    "广场",    "免费区",           "#2E9C8D", "#C3E2DC"),  # public teal
    ("club",     "俱乐部",  "Stay Superlinear", "#7A5AA6", "#DACFEA"),  # member plum
    ("venue",    "会场",    "Stay Superlinear", "#BE8C2C", "#ECDBB0"),  # stage amber
    ("studio",   "工作室",  "Stay Superlinear", "#BE6438", "#ECCEBE"),  # craft copper
    ("courses",  "课程",    "Academy",          "#3A4C86", "#CCD3E9"),  # scholar indigo
    ("field",    "实验田",  "Superlinear",      "#79982F", "#DCE7BE"),  # growth olive
]

W = H = 640
CARD = dict(x=24, y=24, w=592, h=592, rx=30)
BASE = 486         # 平台基线 y
SHOW_ORB = False   # 右上角柔光球 · 默认关(它在角上, 3:4/4:3 裁切易被切成残角)
SAFE = 80          # 安全边距(px·640 基) · 关键元素留在中心 480×480, 兼容 3:4 与 4:3 中心裁切
BLOCK = "ink"      # 大墨色块: "ink"=v1 原样(课程帽板/工作室齿轮 实心墨) · "soft"=统一去黑块
                   # 山山 2026-07-15: 全套要么都有黑块锚点要么都无 · 实验版统一走 soft(无)

# ---------------------------------------------------------------- palettes
# family       = v1 · 7 组同族审美色(上面 GROUPS) —— 已发布, 路径+视觉冻结(链接契约)
# faded-family = 褪色七色 · 手工感: 暖纸底 + 官方墨 #1E1E1E + v1 七色统一降饱和(dusty)
# faded-mono   = 褪色 mono: 同底同墨 + 官方蓝 #4B96FF 保色相降饱和 → #7E97BD 统一点睛
#                (兼顾官方色卡: 墨=Primary1 原样, 蓝=官方蓝 hue 219° 的褪色派生)
# (2026-07-15 曾试过 official=原样 #0E6EF4 艳蓝 mono, 山山毙 → 已删)
PALETTES = {
    "v1": dict(
        ground="#F4F3F1", ink="#1B1D21", ink_soft="#585C63",
        groups=GROUPS, outdir="out", gallery="gallery.html",
        title="Stay Superlinear · Space Group 矢量插图",
        sub="7 组 · 1:1 · SVG（可改可缩放）· 同族配色 + 统一点纹 · 浅底极简"),
    "seven": dict(
        ground="#F4F3F1", ink="#1E1E1E", ink_soft="#6B675F",
        groups=[
            ("townhall", "市政厅",  "免费区",           "#6E8CAE", "#DDE3EA"),
            ("plaza",    "广场",    "免费区",           "#6D9E96", "#D9E4E1"),
            ("club",     "俱乐部",  "Stay Superlinear", "#9284AE", "#E1DDE9"),
            ("venue",    "会场",    "Stay Superlinear", "#C0A36E", "#EBE3D1"),
            ("studio",   "工作室",  "Stay Superlinear", "#C08A6B", "#EBDCD0"),
            ("courses",  "课程",    "Academy",          "#7A85A8", "#DCDFE8"),
            ("field",    "实验田",  "Superlinear",      "#99A566", "#E3E6CF"),
        ],
        block="soft", outdir="out-seven", gallery="gallery-faded-family.html",
        title="Space Group 插图 · seven（备份 · 七色）",
        sub="浅灰底 #F4F3F1（同 v1·中性暖灰）· 官方墨 #1E1E1E · 七色降饱和 dusty · seven=备份"),
    "mono": dict(
        ground="#F4F3F1", ink="#1E1E1E", ink_soft="#6B675F",
        groups=[(s, cn, tier, "#7E97BD", "#DCE2EC") for s, cn, tier, _, _ in GROUPS],
        block="soft", outdir="out-mono", gallery="gallery-faded-mono.html",
        title="Space Group 插图 · mono（✅ 正式 · 单蓝）",
        sub="浅灰底 #F4F3F1（同 v1·中性暖灰）· 官方墨 #1E1E1E · 官方蓝降饱和 #7E97BD 点睛 · ✅ mono=正式(终选 2026-07-15)"),
    "vivid": dict(
        ground="#EEEBE0", ink="#1E1E1E", ink_soft="#6B675F",
        groups=[(s, cn, tier, "#0E6EF4", "#D2E5FF") for s, cn, tier, _, _ in GROUPS],
        block="soft", outdir="out-vivid", gallery="gallery-official-beige.html",
        title="Space Group 插图 · vivid（对照 · 官方米底原蓝）",
        sub="官方米底 #EEEBE0（Icon_Azure_HaveBgd 同款）· 官方墨 #1E1E1E · 官方蓝原样 #0E6EF4 · vivid=对照存档"),
}

# ---------------------------------------------------------------- svg helpers
def rect(x, y, w, h, fill="none", stroke="none", sw=0, rx=0, op=1, extra=""):
    r = f' rx="{rx}"' if rx else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}" {extra}/>')

def circle(cx, cy, r, fill="none", stroke="none", sw=0, op=1):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')

def line(x1, y1, x2, y2, stroke=None, sw=3, op=1, cap="round"):
    stroke = INK if stroke is None else stroke  # 运行时取全局 INK · 配合 --palette 切换
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}" opacity="{op}" stroke-linecap="{cap}"/>')

def poly(pts, fill="none", stroke="none", sw=0, op=1):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" opacity="{op}" stroke-linejoin="round"/>')

def path(d, fill="none", stroke="none", sw=0, op=1, cap="round"):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'opacity="{op}" stroke-linecap="{cap}" stroke-linejoin="round"/>')

def group(*parts):
    return "\n    ".join(p for p in parts if p)

# ---------------------------------------------------------------- shared frame
def frame_open(accent, tint):
    dots = (f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1.5" fill="{accent}" opacity="0.13"/></pattern>')
    defs = (f'<defs><clipPath id="card"><rect x="{CARD["x"]}" y="{CARD["y"]}" '
            f'width="{CARD["w"]}" height="{CARD["h"]}" rx="{CARD["rx"]}"/></clipPath>{dots}</defs>')
    card = rect(**CARD, fill=GROUND)
    tex  = rect(CARD["x"], CARD["y"], CARD["w"], CARD["h"], fill="url(#dots)")
    # 顶部柔光 orb (默认关 · 见 SHOW_ORB)
    orb = ""
    if SHOW_ORB:
        orb = (circle(500, 150, 46, fill=tint) +
               circle(500, 150, 46, stroke=accent, sw=1.5, op=0.5))
    # 平台: 一条基线 + 柔影
    plat = (rect(70, BASE, 500, 12, fill=INK, op=0.06, rx=6) +
            line(78, BASE, 562, BASE, stroke=INK, sw=2, op=0.85))
    return f'<g clip-path="url(#card)">\n    {tex}\n    {orb}\n    {plat}\n    ', defs, card

def frame_close():
    border = rect(**CARD, fill="none", stroke=INK, sw=1.5, op=0.14)
    return f'\n  </g>\n  {border}'

# ---------------------------------------------------------------- motifs
def m_townhall(a, t):
    """市政厅 · 古典门厅: 山花 + 柱廊 + 台阶 + 徽记 · 官方/入口"""
    cols = ""
    for cx in (214, 268, 322, 376, 430):
        cols += rect(cx-13, 322, 26, 150, fill=WHITE, stroke=INK, sw=2) + \
                rect(cx-17, 316, 34, 8, fill=t, stroke=INK, sw=2) + \
                line(cx, 330, cx, 466, stroke=INK, sw=1.2, op=0.35)
    steps = (rect(176, 472, 292, 12, fill=t, stroke=INK, sw=2) +
             rect(158, 484, 328, 12, fill=WHITE, stroke=INK, sw=2))
    entab = rect(190, 296, 264, 22, fill=WHITE, stroke=INK, sw=2)
    ped   = poly([(180,296),(322,214),(464,296)], fill=t, stroke=INK, sw=2.5)
    emb   = circle(322, 262, 17, fill=a) + circle(322,262,17,stroke=INK,sw=2)
    flag  = line(322,214,322,188,stroke=INK,sw=2.5) + poly([(322,190),(352,198),(322,206)],fill=a,stroke=INK,sw=1.5)
    return group(ped, emb, flag, entab, cols, steps)

def m_plaza(a, t):
    """广场 · 中心喷泉 + 彩旗 bunting + 铺地环 · 公开交流/展示"""
    string = path("M 150 300 Q 322 346 494 300", stroke=INK, sw=1.6, op=0.65)
    pts = [(150,300),(207,316),(264,328),(322,333),(380,328),(437,316),(494,300)]
    flags = ""
    for i,(fx,fy) in enumerate(pts):
        col = a if i % 2 == 0 else t
        flags += poly([(fx-11,fy),(fx+11,fy),(fx,fy+20)], fill=col, stroke=INK, sw=1.3)
    basin = rect(250, 452, 144, 26, fill=t, stroke=INK, sw=2, rx=13)
    stem  = rect(316, 404, 12, 50, fill=WHITE, stroke=INK, sw=2)
    bowl  = rect(288, 396, 68, 16, fill=t, stroke=INK, sw=2, rx=8)
    fin   = circle(322, 390, 7, fill=a, stroke=INK, sw=2)
    waterL = path("M 316 400 Q 292 426 300 450", stroke=a, sw=2, op=0.7)
    waterR = path("M 328 400 Q 352 426 344 450", stroke=a, sw=2, op=0.7)
    drops  = circle(300, 452, 3, fill=a, op=0.8) + circle(344, 452, 3, fill=a, op=0.8) + circle(322, 384, 3.2, fill=a)
    return group(string, flags, basin, stem, bowl, fin, waterL, waterR, drops)

def m_club(a, t):
    """俱乐部 · 单椅 + 双人沙发(不对称) + 偏心几 + 吊灯 · 会员深聊"""
    # 吊灯: 挪到偏左、悬在茶几上方(不居中)
    lamp = (line(300, 150, 300, 206, stroke=INK, sw=2) +
            poly([(280,206),(320,206),(311,234),(289,234)], fill=t, stroke=INK, sw=2) +
            circle(300, 240, 5, fill=a))
    # 左: 单扶手椅(朝右 · 较小)
    left = (rect(150, 374, 18, 80, fill=t, stroke=INK, sw=2, rx=9) +       # 靠背
            rect(168, 390, 12, 42, fill=a, op=0.28) +                       # 靠垫
            rect(162, 430, 58, 20, fill=WHITE, stroke=INK, sw=2, rx=8) +    # 座
            rect(210, 410, 15, 40, fill=t, stroke=INK, sw=2, rx=7) +        # 内扶手
            line(170, 450, 170, 470, stroke=INK, sw=2) + line(216, 450, 216, 470, stroke=INK, sw=2))
    # 右: 双人沙发(朝左 · 更宽更矮 · 制造不对称)
    sofa = (rect(360, 396, 130, 42, fill=t, stroke=INK, sw=2, rx=12) +      # 靠背/体
            rect(368, 428, 116, 26, fill=WHITE, stroke=INK, sw=2, rx=10) +  # 坐垫排
            line(426, 430, 426, 452, stroke=INK, sw=1.6, op=0.5) +          # 中缝
            rect(352, 414, 16, 40, fill=t, stroke=INK, sw=2, rx=7) +        # 左扶手
            rect(484, 414, 16, 40, fill=t, stroke=INK, sw=2, rx=7) +        # 右扶手
            line(366, 454, 366, 470, stroke=INK, sw=2) + line(486, 454, 486, 470, stroke=INK, sw=2))
    # 茶几: 偏左(靠单椅这侧 · 不居中)
    table = (rect(268, 440, 50, 12, fill=t, stroke=INK, sw=2, rx=6) +
             line(276, 452, 276, 470, stroke=INK, sw=2) + line(310, 452, 310, 470, stroke=INK, sw=2) +
             circle(293, 430, 7, fill=a, stroke=INK, sw=2))                 # 小杯
    return group(left, sofa, table, lamp)

def m_venue(a, t):
    """会场 · 舞台幕布 + 屏幕 + 座位 + 聚光 · 大师课/回放"""
    beam = poly([(322,196),(230,300),(414,300)], fill=t, op=0.55)
    screen = rect(214, 300, 216, 118, fill=WHITE, stroke=INK, sw=2.5, rx=6)
    play = poly([(310,338),(310,380),(346,359)], fill=a)
    curtain = ""
    for i, cx in enumerate(range(196, 449, 42)):
        curtain += path(f"M {cx} 300 q 10 40 0 80", stroke=INK, sw=1.4, op=0.4)
    top = rect(196, 288, 252, 14, fill=t, stroke=INK, sw=2, rx=4)
    spot = circle(322, 190, 12, fill=a, stroke=INK, sw=2)
    seats = ""
    for row, y in enumerate((440, 468)):
        for cx in range(238, 421, 36):
            off = 0 if row == 0 else 18
            seats += rect(cx-14+off, y, 26, 14, fill=t, stroke=INK, sw=1.6, rx=5)
    return group(spot, beam, top, screen, curtain, play, seats)

def m_studio(a, t):
    """工作室 · 加宽工作台 · 灯泡/烧瓶/齿轮同置台面 · 大小成节奏 · 工具/共创"""
    bench = (rect(150, 452, 340, 16, fill=t, stroke=INK, sw=2, rx=5) +
             line(184, 468, 184, 486, stroke=INK, sw=2) + line(456, 468, 456, 486, stroke=INK, sw=2))
    # 灯泡(左 · 中号 · 坐台面)
    bx = 224
    bulb = (circle(bx, 404, 26, fill=WHITE, stroke=INK, sw=2.5) +
            circle(bx, 404, 26, fill=a, op=0.16) +
            path(f"M {bx-9} 400 q 9 11 18 0", stroke=a, sw=2) +
            rect(bx-10, 430, 20, 22, fill=t, stroke=INK, sw=2) +
            line(bx-10, 437, bx+10, 437, stroke=INK, sw=1.2, op=0.5) +
            line(bx-10, 444, bx+10, 444, stroke=INK, sw=1.2, op=0.5))
    rays = ""
    for ang in (-90, -52, -128):
        r = math.radians(ang)
        rays += line(bx+34*math.cos(r), 404+34*math.sin(r), bx+50*math.cos(r), 404+50*math.sin(r),
                     stroke=a, sw=2, op=0.6)
    # 烧瓶(中 · hero · 最高 · 坐台面)
    fx = 322
    flask = (path(f"M {fx-14} 356 L {fx-14} 388 L {fx-32} 442 Q {fx-36} 452 {fx-22} 452 "
                  f"L {fx+22} 452 Q {fx+36} 452 {fx+32} 442 L {fx+14} 388 L {fx+14} 356 Z",
                  fill=t, stroke=INK, sw=2.5) +
             rect(fx-18, 348, 36, 10, fill=WHITE, stroke=INK, sw=2) +
             path(f"M {fx-27} 428 Q {fx} 434 {fx+27} 428", stroke=a, sw=3) +
             circle(fx-10, 438, 3.4, fill=a) + circle(fx+9, 434, 2.6, fill=a))
    # 齿轮(右 · 小 · 坐台面) · 齿: ink 模式=实心墨(v1 原样) / soft 模式=白填充+墨描边(去黑块)
    gx, gy, R = 420, 424, 20
    tf, ts, tsw = (INK, "none", 0) if BLOCK == "ink" else (WHITE, INK, 2)
    teeth = ""
    for ang in range(0, 360, 45):
        teeth += rect(gx-4, gy-R-7, 8, 11, fill=tf, stroke=ts, sw=tsw,
                      extra=f'transform="rotate({ang} {gx} {gy})"')
    gear = teeth + circle(gx, gy, R, fill=WHITE, stroke=INK, sw=2.5) + circle(gx, gy, 7, fill=a)
    return group(bench, rays, bulb, flask, gear)

def m_courses(a, t):
    """课程 · 书堆 + 学位帽 + 翻开的书 · 结构化学习"""
    books = ""
    ys = [(300, 452, "t"), (280, 448, "w"), (306, 436, "a")]
    stack = [(452, 300, t), (448, 280, WHITE), (436, 306, t)]
    b = ""
    b += rect(300, 452, 150, 20, fill=t, stroke=INK, sw=2, rx=3)
    b += rect(288, 434, 150, 20, fill=WHITE, stroke=INK, sw=2, rx=3)
    b += rect(310, 416, 150, 20, fill=a, op=0.85, stroke=INK, sw=2, rx=3)
    for by in (462, 444, 426):
        b += line(316, by, 316, by, stroke=INK, sw=0)  # noop keep
    # 翻开的书 (扇形双页 + 书脊)
    ob = path("M 250 434 C 226 427 208 431 196 444 L 202 474 C 216 462 236 460 250 467 Z",
              fill=WHITE, stroke=INK, sw=2.2) + \
         path("M 250 434 C 274 427 292 431 304 444 L 298 474 C 284 462 264 460 250 467 Z",
              fill=t, stroke=INK, sw=2.2) + \
         line(250, 434, 250, 467, stroke=INK, sw=1.6)
    for i in range(1, 4):
        ob += line(212, 446+i*4, 240, 444+i*4, stroke=INK, sw=1, op=0.3)
        ob += line(260, 444+i*4, 288, 446+i*4, stroke=INK, sw=1, op=0.3)
    # 学位帽 · 帽板: ink 模式=实心墨(v1 原样) / soft 模式=强调色填充+墨描边(去黑块)
    if BLOCK == "ink":
        board = poly([(378,300),(452,326),(378,352),(304,326)], fill=INK)
    else:
        board = poly([(378,300),(452,326),(378,352),(304,326)], fill=a, stroke=INK, sw=2.2)
    cap = board + \
          poly([(340,342),(340,372),(378,384),(416,372),(416,342)], fill=t, stroke=INK, sw=2) + \
          line(452, 326, 452, 366, stroke=INK, sw=2) + circle(452, 372, 6, fill=a)
    return group(ob, b, cap)

def m_field(a, t):
    """实验田 · 未定型的试验苗床(虚线) + 单株破土 + 念头上升成火花 · 边缘探索(去字面化)"""
    # 试验苗床: 透视椭圆 + 虚线边(未定型/试验中, 不是实心农田)
    bed = (f'<ellipse cx="322" cy="478" rx="112" ry="28" fill="{t}" opacity="0.42"/>'
           f'<ellipse cx="322" cy="478" rx="112" ry="28" fill="none" stroke="{a}" '
           f'stroke-width="2" stroke-dasharray="5 9" opacity="0.7"/>')
    # 单株幼苗破土(中心 · 笃定)
    x, base, hgt = 322, 470, 108
    stem = line(x, base, x, base - hgt, stroke=INK, sw=2.6)
    ly = base - hgt + 12
    leaves = (path(f"M {x} {ly} q -28 -6 -32 -30 q 26 2 32 24", fill=t, stroke=INK, sw=1.8) +
              path(f"M {x} {ly+8} q 28 -6 32 -30 q -26 2 -32 24", fill=t, stroke=INK, sw=1.8))
    bud = circle(x, base - hgt, 5, fill=a)
    # 念头/种子上升 (散点 · 疏密不匀)
    rise = ""
    for dx, dy, r in [(-58,4,3),(-44,-30,2.4),(-30,-58,2),(52,-6,3),(40,-38,2.4),(64,-30,2)]:
        rise += circle(x + dx, base - 44 + dy, r, fill=a, op=0.7)
    # 顶端化成小火花(可能性)
    spark = ""
    for sx, sy in [(x - 54, base - 108), (x + 60, base - 98)]:
        spark += line(sx-7, sy, sx+7, sy, stroke=a, sw=2) + line(sx, sy-7, sx, sy+7, stroke=a, sw=2)
    # 虚线上升轨迹(未定型的生长方向)
    traj = (f'<path d="M {x} {base-hgt} q 22 -20 44 -14" fill="none" stroke="{a}" '
            f'stroke-width="1.6" stroke-dasharray="3 6" opacity="0.55"/>')
    return group(bed, traj, stem, leaves, bud, rise, spark)

MOTIFS = dict(townhall=m_townhall, plaza=m_plaza, club=m_club, venue=m_venue,
              studio=m_studio, courses=m_courses, field=m_field)

# ---------------------------------------------------------------- wide (16:9 横版)
# 2026-07-15 手机 app 实测: Circle 空间导航卡 ≈1.63:1, 名称+描述叠印在图的左侧+下部。
# 横版构图: 主体右置(中心 x=920/1280 ≈72%W) · 左 52% + 底 28% 留白给叠字 ·
# 全出血无卡框(裁切不露边) · 抗 1.5:1~2:1 中心裁。1:1 方版保留为 base。
WIDE_W, WIDE_H = 1280, 720
WIDE_S  = 1.25                    # 三调(山山 mock): 不压字前提下的最大号(主体顶到 y30)
WIDE_TX = 640.0 - 322 * WIDE_S    # 主体水平完全居中(50%W · 山山 mock 定稿方向)
WIDE_TY = 450.0 - 486 * WIDE_S    # 基线 486→450 · 平台线贴文字带上沿(带从 62%H≈y446 起)

# banner (2.8:1 · Circle Directory 官方推荐 840×300 · 2026-07-16)
# 仅当实测 app 卡片为扁长条时用; 当前观测卡片 ≈1.63:1 → wide 版为准, banner 是备选。
# 构图: 主体缩 0.6 置右(63%W) · 基线 y250 · 左下留叠字区。
BANNER_W, BANNER_H = 840, 300
BANNER_S  = 0.6
BANNER_TX = 529.2 - 322 * BANNER_S
BANNER_TY = 250.0 - 486 * BANNER_S

def build_banner_svg(slug, accent, tint):
    dots = (f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1.5" fill="{accent}" opacity="0.13"/></pattern>')
    ground = rect(0, 0, BANNER_W, BANNER_H, fill=GROUND)
    tex    = rect(0, 0, BANNER_W, BANNER_H, fill="url(#dots)")
    plat   = (rect(379, 250, 300, 10, fill=INK, op=0.06, rx=5) +
              line(387, 250, 671, 250, stroke=INK, sw=2, op=0.85))
    motif  = MOTIFS[slug](accent, tint)
    return (f'<svg viewBox="0 0 {BANNER_W} {BANNER_H}" width="{BANNER_W}" height="{BANNER_H}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f'<defs>{dots}</defs>\n  {ground}\n  {tex}\n  {plat}\n'
            f'  <g transform="translate({BANNER_TX:.1f},{BANNER_TY:.1f}) scale({BANNER_S})">\n    {motif}\n  </g>\n</svg>\n')

def build_wide_svg(slug, accent, tint):
    dots = (f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1.5" fill="{accent}" opacity="0.13"/></pattern>')
    ground = rect(0, 0, WIDE_W, WIDE_H, fill=GROUND)
    tex    = rect(0, 0, WIDE_W, WIDE_H, fill="url(#dots)")
    plat   = (rect(405, 450, 470, 12, fill=INK, op=0.06, rx=6) +
              line(413, 450, 867, 450, stroke=INK, sw=2, op=0.85))
    motif  = MOTIFS[slug](accent, tint)
    return (f'<svg viewBox="0 0 {WIDE_W} {WIDE_H}" width="{WIDE_W}" height="{WIDE_H}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n'
            f'<defs>{dots}</defs>\n  {ground}\n  {tex}\n  {plat}\n'
            f'  <g transform="translate({WIDE_TX:.1f},{WIDE_TY:.1f}) scale({WIDE_S})">\n    {motif}\n  </g>\n</svg>\n')

# ---------------------------------------------------------------- assemble
def build_svg(slug, accent, tint):
    open_g, defs, card = frame_open(accent, tint)
    motif = MOTIFS[slug](accent, tint)
    close_g = frame_close()
    return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n  '
            f'{defs}\n  {card}\n  {open_g}{motif}{close_g}\n</svg>\n')

COMPARE_SETS = [
    ("out",       "v1 · 旧版 · 灰底七色（旧嵌入链接专用）"),
    ("out-vivid", "vivid · 对照 · 官方米底原蓝 #0E6EF4"),
    ("out-mono",  "✅ mono · 正式 · 灰底单蓝 #7E97BD（终选）"),
    ("out-seven", "seven · 备份 · 灰底七色 dusty"),
]

def maybe_compare(here):
    """COMPARE_SETS 里已生成的变体 ≥2 时输出 compare.html 多列对照。
    用 <img> 引外部 SVG(不内联), 避免多套 SVG 的 clipPath/pattern id 冲突。"""
    avail = [(d, lab) for d, lab in COMPARE_SETS
             if all(os.path.exists(os.path.join(here, d, f"{slug}.svg"))
                    for slug, *_ in GROUPS)]
    if len(avail) < 2:
        return
    cols = len(avail)
    rows = ""
    for slug, cn, tier, _, _ in GROUPS:
        cells = "".join(
            f'<figure><img src="{d}/{slug}.svg" alt="{cn} {lab}">'
            f'<figcaption>{lab}</figcaption></figure>' for d, lab in avail)
        rows += (f'<section><h2>{cn} <small>{tier} · {slug}</small></h2>'
                 f'<div class="pair">{cells}</div></section>\n')
    fullset = ""
    for d, lab in avail:
        imgs = "".join(f'<img src="{d}/{s}.svg" alt="{cn}" title="{cn}">' for s, cn, *_ in GROUPS)
        fullset += (f'<section class="full"><h2>{lab}</h2>'
                    f'<div class="row7">{imgs}</div></section>\n')
    if fullset:
        fullset = '<h1 class="fullhead">整套效果（每排一套 · 7 张连看）</h1>\n' + fullset
    heads = " · ".join(lab for _, lab in avail)
    # 终选块: 褪色 mono = 终选(山山 2026-07-15) · 判词表含四方案定论
    rec = f"""<aside class="rec">
<h3>✅ 终选：mono · 正式版（山山 2026-07-15 定）</h3>
<ul>
<li><b>为什么 mono 成立</b>：Circle 里头图永远和空间名并排出现，文字才是导航——七个图形本身（门厅/喷泉/沙发/舞台/工作台/书堆/嫩芽）已足够分辨。「颜色导航」是此前推荐七色的核心理由，经复核在真实场景里不成立。</li>
<li><b>品牌血缘 + 避开 AI 滥用米底</b>：底改用 <code>#F4F3F1</code> 中性暖灰（山山 2026-07-15 定——奶油米底已是 AI 风指纹，且它比米色更接近官方 Primary 2 <code>#EEEEEE</code>）；墨 = Primary 1 <code>#1E1E1E</code> 原样；蓝 = 官方 <code>#4B96FF</code> 保色相降饱和 <code>#7E97BD</code>。官方米底 <code>#EEEBE0</code> 留在 vivid 对照版。</li>
<li><b>可扩展性</b>：space 结构还会变；mono 加任意新空间都是同一套底+墨+蓝，零新配色决策；七色方案每加一区都要扩色彩家族。</li>
<li><b>底色定调</b>：中性暖灰不抢戏、不赶奶油风潮；蓝只点睛；黑块已按统一原则全部去除。</li>
</ul>
<table><tr><th>方案</th><th>一句话判词</th></tr>
<tr><td>v1 · 旧版（灰底七色）</td><td>现行上库版：已复制的嵌入链接正在用它，按链接契约永久保留、不删不改；新用途不再选它。</td></tr>
<tr><td>vivid · 对照（官方米底原蓝 · 平时不用）</td><td>#0E6EF4 在暖纸上过艳、锚点抢主体，不选用；留列做对照。</td></tr>
<tr><td><b>✅ mono · 正式（灰底单蓝 · 终选）</b></td><td><b>官方血缘 + 可扩展 + 克制耐看，定为正式版。</b></td></tr>
<tr><td>seven · 备份（灰底七色）</td><td>曾获推荐；「颜色导航」理由复核后不成立，转为备选存档。</td></tr>
</table>
</aside>"""
    html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>插图配色对比 · {cols} 版</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#FAFAF9;color:#1B1D21;
 font-family:"Segoe UI",Manrope,system-ui,sans-serif;padding:44px}}
h1{{font-size:24px;margin:0 0 4px}}
.sub{{color:#585C63;font-size:15px;margin:0 0 26px}}
.rec{{border:1.5px solid #C0A36E;background:#FDFBF6;border-radius:14px;
 padding:20px 24px;margin:0 0 36px;max-width:{cols*480}px}}
.rec h3{{margin:0 0 14px;font-size:17px}}
.fullhead{{font-size:22px;margin:14px 0 18px}}
.full{{margin:0 0 24px}}
.full h2{{font-size:15px;color:#585C63;font-weight:600;margin:0 0 8px}}
.row7{{display:grid;grid-template-columns:repeat(7,1fr);gap:10px;max-width:{cols*480}px}}
.row7 img{{width:100%;height:auto;border-radius:10px;border:1px solid rgba(0,0,0,.10);background:#fff}}
.rec ul{{margin:0 0 14px;padding-left:20px;font-size:14.5px;line-height:1.65}}
.rec li{{margin:0 0 6px}}
.rec code{{background:rgba(0,0,0,.05);padding:1px 5px;border-radius:4px;font-size:13px}}
.rec table{{border-collapse:collapse;font-size:14px}}
.rec th,.rec td{{border:1px solid rgba(0,0,0,.12);padding:7px 12px;text-align:left}}
.rec th{{background:rgba(0,0,0,.04)}}
section{{margin:0 0 34px}}
h2{{font-size:18px;margin:0 0 10px}} h2 small{{color:#585C63;font-weight:400;font-size:13px}}
.pair{{display:grid;grid-template-columns:repeat({cols},1fr);gap:20px;max-width:{cols*480}px}}
figure{{margin:0;background:#fff;border:1px solid rgba(0,0,0,.10);border-radius:14px;overflow:hidden}}
figure img{{display:block;width:100%;height:auto}}
figcaption{{padding:9px 14px;font-size:13.5px;color:#585C63;border-top:1px solid rgba(0,0,0,.08)}}
</style></head><body>
<h1>配色对比（左→右）</h1>
<p class="sub">{heads}</p>
{rec}
{rows}
{fullset}
</body></html>"""
    with open(os.path.join(here, "compare.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"compare.html updated ({cols} columns: {', '.join(d for d, _ in avail)})")

GALLERY_TEMPLATE = """<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stay Superlinear · Space Group 矢量插图</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#F4F3F1;color:#1B1D21;
 font-family:"Segoe UI",Manrope,system-ui,-apple-system,sans-serif;padding:48px;transition:background .25s}
h1{font-size:26px;font-weight:700;margin:0 0 6px}
.sub{color:#585C63;font-size:16px;margin:0 0 14px}
.btns{display:flex;gap:10px;margin:0 0 14px;flex-wrap:wrap}
.btns button{font:600 14.5px/1 "Segoe UI",sans-serif;padding:9px 16px;border-radius:999px;
 border:1.5px solid rgba(0,0,0,.25);background:#fff;color:#1B1D21;cursor:pointer}
.btns button.on{background:#1B1D21;color:#fff;border-color:#1B1D21}
.pal{display:flex;gap:8px;margin:0 0 26px}
.pal span{width:34px;height:34px;border-radius:8px;border:1px solid rgba(0,0,0,.12)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:26px}
figure{margin:0;background:#fff;border:1px solid rgba(0,0,0,.10);border-radius:18px;
 overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.art{position:relative}
.art img{display:block;width:100%;height:auto}
.crop-guide{position:absolute;inset:0;display:none;pointer-events:none}
.crop-guide svg{width:100%;height:100%}
.crop-guide rect{fill:none;stroke-width:1.4;vector-effect:non-scaling-stroke;stroke-dasharray:5 5}
.crop-guide .g43{stroke:#D8564B}
.crop-guide .g34{stroke:#2F6FB0}
body.guides .crop-guide{display:block}
.tog{display:inline-flex;align-items:center;gap:8px;font-size:15px;color:#585C63;
 margin:0 0 22px;cursor:pointer;user-select:none}
.tog i{font-style:normal;color:#D8564B} .tog b{font-weight:600;color:#2F6FB0}
figcaption{display:flex;align-items:center;gap:9px;padding:13px 16px;border-top:1px solid rgba(0,0,0,.08)}
figcaption b{font-size:16px}
figcaption small{color:#585C63;font-size:13px;margin-left:auto}
.dot{width:11px;height:11px;border-radius:50%;flex:none}
</style></head><body>
<h1>Stay Superlinear · Space Group 矢量插图</h1>
<p class="sub" id="sub"></p>
<div class="btns" id="btns">__BTNS__</div>
<div class="pal" id="pal"></div>
<label class="tog"><input type="checkbox" id="tg"> 显示裁切安全线（<i>红 4:3</i> / <b>蓝 3:4</b> 中心裁切 · 关键元素应落在两框交叠的中心区内）</label>
<div class="grid">__TILES__</div>
<script>
const PALS = __PALS__;
function setPal(k){
  const p = PALS[k]; if(!p) return;
  document.querySelectorAll('img.tile').forEach(im => { im.src = p.dir + '/' + im.dataset.slug + '.svg'; });
  document.querySelectorAll('.dot').forEach(d => { d.style.background = p.accents[d.dataset.slug]; });
  document.getElementById('sub').textContent = p.sub;
  document.getElementById('pal').innerHTML = Object.entries(p.accents)
    .map(([s,a]) => '<span title="'+s+' '+a+'" style="background:'+a+'"></span>').join('');
  document.body.style.background = p.ground;
  document.querySelectorAll('#btns button').forEach(b => b.classList.toggle('on', b.dataset.key===k));
  try { history.replaceState(null,'','#'+k); } catch(e) {}
}
document.querySelectorAll('#btns button').forEach(b => b.onclick = () => setPal(b.dataset.key));
document.getElementById('tg').onchange = e => document.body.classList.toggle('guides', e.target.checked);
const init = location.hash.slice(1);
setPal(PALS[init] ? init : (PALS['mono'] ? 'mono' : 'v1'));
</script>
</body></html>
"""

def build_gallery(here):
    """gallery.html = 配色 button 切换画廊(山山 2026-07-15 提议)。
    <img> 引各 outdir 的 SVG · 切换只换 src · 色块/副标题/圆点/页底色联动 · 裁切安全线开关保留。
    默认 v1(family) · URL hash 指定初始配色(如 gallery.html#faded-mono)。终选后删多余 outdir 即自动缩按钮。"""
    import json
    order = [("mono", "✅ mono · 正式"), ("seven", "seven · 备份"),
             ("vivid", "vivid · 对照"), ("v1", "v1 · 旧版")]
    pals = {}
    for key, btn in order:
        pal = PALETTES.get(key)
        if not pal:
            continue
        d = pal["outdir"]
        if not all(os.path.exists(os.path.join(here, d, f"{s}.svg")) for s, *_ in GROUPS):
            continue
        pals[key] = dict(btn=btn, dir=d, sub=pal["sub"], ground=pal["ground"],
                         accents={s: a for s, _, _, a, _ in pal["groups"]})
    if "v1" not in pals:
        return
    overlay = ('<div class="crop-guide"><svg viewBox="0 0 100 100" preserveAspectRatio="none">'
               '<rect x="0" y="12.5" width="100" height="75" class="g43"/>'
               '<rect x="12.5" y="0" width="75" height="100" class="g34"/></svg></div>')
    tiles = ""
    for slug, cn, tier, _, _ in GROUPS:
        tiles += ('<figure><div class="art">'
                  f'<img class="tile" data-slug="{slug}" src="out/{slug}.svg" alt="{cn}">{overlay}</div>'
                  f'<figcaption><span class="dot" data-slug="{slug}"></span>'
                  f'<b>{cn}</b><small>{tier} · {slug}</small></figcaption></figure>\n')
    btns = "".join(f'<button data-key="{k}">{v["btn"]}</button>' for k, v in pals.items())
    html = (GALLERY_TEMPLATE
            .replace("__PALS__", json.dumps(pals, ensure_ascii=False))
            .replace("__TILES__", tiles)
            .replace("__BTNS__", btns))
    with open(os.path.join(here, "gallery.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("gallery.html updated (switcher:", ", ".join(pals), ")")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wide", action="store_true", help="横版 16:9(1280x720) · 主体右置 · 左/下留叠字区 · 出 <outdir>/wide/")
    ap.add_argument("--banner", action="store_true", help="banner 2.8:1(840x300 · Circle Directory 官方推荐) · 出 <outdir>/banner/")
    ap.add_argument("--palette", choices=list(PALETTES), default="v1",
                    help="v1=旧版(默认·路径冻结) · mono=正式 · seven=备份 · vivid=对照")
    args = ap.parse_args()
    pal = PALETTES[args.palette]
    global GROUND, INK, INK_SOFT, BLOCK
    GROUND, INK, INK_SOFT = pal["ground"], pal["ink"], pal["ink_soft"]
    BLOCK = pal.get("block", "ink")
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, pal["outdir"])
    os.makedirs(out, exist_ok=True)
    if args.wide:  # 横版模式: 只出 16:9 到 <outdir>/wide/, 不动方版/画廊
        wout = os.path.join(out, "wide")
        os.makedirs(wout, exist_ok=True)
        for slug, cn, tier, accent, tint in pal["groups"]:
            with open(os.path.join(wout, f"{slug}.svg"), "w", encoding="utf-8") as f:
                f.write(build_wide_svg(slug, accent, tint))
        print("wide:", len(pal["groups"]), "svg ->", wout)
        return
    if args.banner:  # banner 模式: 只出 2.8:1 到 <outdir>/banner/
        bout = os.path.join(out, "banner")
        os.makedirs(bout, exist_ok=True)
        for slug, cn, tier, accent, tint in pal["groups"]:
            with open(os.path.join(bout, f"{slug}.svg"), "w", encoding="utf-8") as f:
                f.write(build_banner_svg(slug, accent, tint))
        print("banner:", len(pal["groups"]), "svg ->", bout)
        return
    cards = []
    for slug, cn, tier, accent, tint in pal["groups"]:
        svg = build_svg(slug, accent, tint)
        with open(os.path.join(out, f"{slug}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        cards.append((slug, cn, tier, accent))
    build_gallery(here)
    print("done:", len(cards), "svg ->", out)
    maybe_compare(here)

if __name__ == "__main__":
    main()
