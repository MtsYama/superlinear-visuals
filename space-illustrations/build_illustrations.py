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

# ---------------------------------------------------------------- svg helpers
def rect(x, y, w, h, fill="none", stroke="none", sw=0, rx=0, op=1, extra=""):
    r = f' rx="{rx}"' if rx else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}" {extra}/>')

def circle(cx, cy, r, fill="none", stroke="none", sw=0, op=1):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')

def line(x1, y1, x2, y2, stroke=INK, sw=3, op=1, cap="round"):
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
    # 齿轮(右 · 小 · 坐台面)
    gx, gy, R = 420, 424, 20
    teeth = ""
    for ang in range(0, 360, 45):
        teeth += rect(gx-4, gy-R-7, 8, 11, fill=INK, extra=f'transform="rotate({ang} {gx} {gy})"')
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
    # 学位帽
    cap = poly([(378,300),(452,326),(378,352),(304,326)], fill=INK) + \
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

# ---------------------------------------------------------------- assemble
def build_svg(slug, accent, tint):
    open_g, defs, card = frame_open(accent, tint)
    motif = MOTIFS[slug](accent, tint)
    close_g = frame_close()
    return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">\n  '
            f'{defs}\n  {card}\n  {open_g}{motif}{close_g}\n</svg>\n')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wide", action="store_true", help="超长超扁版(预留)")
    args = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out")
    os.makedirs(out, exist_ok=True)
    cards = []
    for slug, cn, tier, accent, tint in GROUPS:
        svg = build_svg(slug, accent, tint)
        with open(os.path.join(out, f"{slug}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
        cards.append((slug, cn, tier, accent))
    # gallery
    overlay = ('<div class="crop-guide"><svg viewBox="0 0 100 100" preserveAspectRatio="none">'
               '<rect x="0" y="12.5" width="100" height="75" class="g43"/>'
               '<rect x="12.5" y="0" width="75" height="100" class="g34"/></svg></div>')
    tiles = ""
    for slug, cn, tier, accent in cards:
        art = open(os.path.join(out, slug+".svg"), encoding="utf-8").read()
        tiles += (f'<figure><div class="art">{art}{overlay}</div>'
                  f'<figcaption><span class="dot" style="background:{accent}"></span>'
                  f'<b>{cn}</b><small>{tier} · {slug}</small></figcaption></figure>\n')
    swatches = "".join(f'<span title="{cn} {a}" style="background:{a}"></span>' for _,cn,_,a,_ in GROUPS)
    html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stay Superlinear · Space Group 插图</title>
<style>
:root{{--bg:{GROUND};--ink:{INK};--soft:{INK_SOFT}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
 font-family:"Segoe UI",Manrope,system-ui,-apple-system,sans-serif;padding:48px}}
h1{{font-size:26px;font-weight:700;margin:0 0 6px}}
.sub{{color:var(--soft);font-size:16px;margin:0 0 8px}}
.pal{{display:flex;gap:8px;margin:18px 0 34px}}
.pal span{{width:34px;height:34px;border-radius:8px;border:1px solid rgba(0,0,0,.12)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:26px}}
figure{{margin:0;background:#fff;border:1px solid rgba(0,0,0,.10);border-radius:18px;
 overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.05)}}
.art{{position:relative}}
.art svg{{display:block;width:100%;height:auto}}
.crop-guide{{position:absolute;inset:0;display:none;pointer-events:none}}
.crop-guide svg{{width:100%;height:100%}}
.crop-guide rect{{fill:none;stroke-width:1.4;vector-effect:non-scaling-stroke;stroke-dasharray:5 5}}
.crop-guide .g43{{stroke:#D8564B}}
.crop-guide .g34{{stroke:#2F6FB0}}
body.guides .crop-guide{{display:block}}
.tog{{display:inline-flex;align-items:center;gap:8px;font-size:15px;color:var(--soft);
 margin:0 0 22px;cursor:pointer;user-select:none}}
.tog i{{font-style:normal;color:#D8564B}} .tog b{{font-weight:600;color:#2F6FB0}}
figcaption{{display:flex;align-items:center;gap:9px;padding:13px 16px;border-top:1px solid rgba(0,0,0,.08)}}
figcaption b{{font-size:16px}}
figcaption small{{color:var(--soft);font-size:13px;margin-left:auto}}
.dot{{width:11px;height:11px;border-radius:50%;flex:none}}
</style></head><body>
<h1>Stay Superlinear · Space Group 矢量插图</h1>
<p class="sub">7 组 · 1:1 · SVG（可改可缩放）· 同族配色 + 统一点纹 · 浅底极简</p>
<div class="pal">{swatches}</div>
<label class="tog"><input type="checkbox" id="tg"> 显示裁切安全线（<i>红 4:3</i> / <b>蓝 3:4</b> 中心裁切 · 关键元素应落在两框交叠的中心区内）</label>
<div class="grid">{tiles}</div>
<script>document.getElementById('tg').onchange=function(e){{document.body.classList.toggle('guides',e.target.checked)}}</script>
</body></html>"""
    with open(os.path.join(here, "gallery.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("done:", len(cards), "svg + gallery.html ->", out)

if __name__ == "__main__":
    main()
