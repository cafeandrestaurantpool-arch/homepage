"""35サイトの一覧ページ(index.html)を生成する。 python3 _generator/index.py"""
import html, pathlib
from data import INDUSTRIES
from build import PAL, PHOTO

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
P1 = {"salon": ("HAIR ATELIER sora", "#5f7a8a", "#eef0f0"), "build": ("森下工務店", "#9a6a3a", "#1f3a2e"),
      "cafe": ("喫茶こもれび", "#e0ad45", "#22332a"), "pilates": ("Pilates Studio LINEA", "#6f8c79", "#f2f4ef"),
      "clinic": ("さくら台内科クリニック", "#17707c", "#eaf4f5"), "shop": ("器と暮らし つむぎ", "#2f5470", "#f5f5f2"),
      "corp": ("株式会社ネクスリンク", "#2a8fc9", "#0f1b2e")}
STYLES = [("01", "ナチュラル", "業種らしい配色の基本形"), ("02", "高級感", "暗色・明朝・全面写真"),
          ("03", "ポップ", "角丸カード・波形の区切り"), ("04", "ミニマル", "大きな文字・2カラム"), ("05", "和モダン", "縦書き・左サイドバー")]

def swatch(d, num):
    k = d["key"]
    if num == "01": n, a, b = P1[k]
    elif num == "02": n = d["names"]["luxe"][0]; b, a = PAL["luxe"][k]
    elif num == "03": n = d["names"]["pop"][0]; a, b = PAL["pop"][k]
    elif num == "04": n = d["names"]["minimal"][0]; a, b = PAL["minimal"][k], "#ffffff"
    else: n = d["names"]["wa"][0]; a, b = PAL["wa"][k], "#f4f2ec"
    return n, a, b

def build(artifact=False):
    rows = []
    for d in INDUSTRIES:
        cards = []
        for num, lab, _ in STYLES:
            n, a, b = swatch(d, num)
            p1, p2, _ = PHOTO[d["key"]]
            cards.append(f'''<a class="card" href="{d["key"]}/{num}.html">
<span class="thumb" style="--a:{a};--b:{b};--p1:{p1};--p2:{p2}"><i></i><i></i><i></i></span>
<span class="meta"><span class="no">{num}</span><span class="st">{lab}</span></span><span class="nm">{E(n)}</span></a>''')
        rows.append(f'<section class="ind"><h2>{E(d["label"])}<span>{d["key"]}/</span></h2><div class="cards">{"".join(cards)}</div></section>')
    legend = "".join(f'<li><b>{n}</b>{l}<span>{E(x)}</span></li>' for n, l, x in STYLES)
    head = '''<title>業種別ホームページ見本帳</title>
<meta name="claude:viewport-fit-sides" content="cover">''' if artifact else '''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>業種別ホームページ見本帳</title>'''
    body_open = "" if artifact else "</head><body>"
    tail = "" if artifact else "</body></html>"
    return f'''{head}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700&family=Jost:wght@400;600&display=swap">
<style>
/* Layout: 見出し＋凡例、業種ごとに5パターンのカードを横並び */
:root{{--bg:#f6f6f4;--fg:#1c1d20;--mute:#6c6e74;--line:#dedfdc;--card:#ffffff;--accent:#2f5bd3}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16171a;--fg:#ececea;--mute:#9a9ca2;--line:#2c2e33;--card:#1f2024;--accent:#8aa7ff;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#16171a;--fg:#ececea;--mute:#9a9ca2;--line:#2c2e33;--card:#1f2024;--accent:#8aa7ff;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:"Zen Kaku Gothic New",system-ui,sans-serif;line-height:1.7}}
.wrap{{max-width:1180px;margin:0 auto;padding-block:48px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
h1{{font-size:clamp(26px,4vw,38px);margin:0 0 6px;text-wrap:balance}}
.sub{{color:var(--mute);margin:0 0 24px;max-width:44em}}
.legend{{list-style:none;padding:0;margin:0 0 40px;display:flex;flex-wrap:wrap;gap:8px}}
.legend li{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px;font-size:13px;display:flex;gap:8px;align-items:baseline}}
.legend b{{font-family:"Jost",sans-serif;color:var(--accent)}}
.legend span{{color:var(--mute);font-size:12px}}
.ind{{padding-block:20px;border-top:1px solid var(--line)}}
.ind h2{{font-size:18px;margin:0 0 14px;display:flex;gap:10px;align-items:baseline}}
.ind h2 span{{font-family:"Jost",sans-serif;font-size:12px;font-weight:400;color:var(--mute)}}
.cards{{display:grid;gap:14px;grid-template-columns:repeat(5,minmax(0,1fr))}}
.card{{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;transition:border-color .15s,transform .15s}}
.card:hover{{border-color:var(--accent);transform:translateY(-2px)}}
.card:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.thumb{{display:grid;grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr;gap:4px;aspect-ratio:16/10;max-width:100%;border-radius:6px;overflow:hidden;background:var(--b);padding:6px}}
.thumb i:nth-child(1){{grid-row:span 2;background:linear-gradient(150deg,var(--p1),var(--p2));border-radius:3px}}
.thumb i:nth-child(2){{background:var(--a);border-radius:3px}}
.thumb i:nth-child(3){{background:color-mix(in srgb,var(--a) 35%,var(--b));border-radius:3px}}
.meta{{display:flex;gap:6px;align-items:baseline;font-size:12px}}
.no{{font-family:"Jost",sans-serif;font-weight:600;color:var(--accent)}}
.st{{font-weight:700}}
.nm{{font-size:12px;color:var(--mute);overflow-wrap:anywhere}}
.foot{{color:var(--mute);font-size:12px;margin-top:32px}}
@media (max-width:900px){{.cards{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
@media (max-width:520px){{.cards{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media (prefers-reduced-motion:reduce){{.card{{transition:none}}}}
</style>
{body_open}
<div class="wrap">
<h1>業種別ホームページ見本帳</h1>
<p class="sub">7業種 × 5パターン、計35サイト。店名・住所・電話番号はすべて架空です。気になるカードを開いて、デザインと構成を比べてください。</p>
<ul class="legend">{legend}</ul>
{"".join(rows)}
<p class="foot">写真枠はすべて仮のグラデーションです。納品時にクライアントの写真へ差し替えます。</p>
</div>
{tail}
'''

if __name__ == "__main__":
    (ROOT / "index.html").write_text(build())
    pathlib.Path(__file__).with_name("artifact_index.html").write_text(build(artifact=True))
    print("ok")
