"""パターン2〜5（高級感・ポップ・ミニマル・和モダン）を業種データから生成する。
使い方: python3 _generator/build.py   （hp-samples/ 直下で実行）
"""
import html, pathlib, json
from data import INDUSTRIES

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape

FONTS = {
 "luxe": "family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Shippori+Mincho:wght@400;600&family=Zen+Kaku+Gothic+New:wght@400;500",
 "pop": "family=M+PLUS+Rounded+1c:wght@500;800&family=Zen+Maru+Gothic:wght@500;700",
 "minimal": "family=IBM+Plex+Sans+JP:wght@300;400;600&family=Jost:wght@300;500",
 "wa": "family=Zen+Old+Mincho:wght@500;700;900&family=Zen+Kaku+Gothic+New:wght@400;500",
}

PHOTO = {  # 写真枠の仮グラデーション（業種ごと）
 "salon": ("#c9d3d8", "#7f97a3", "#e6d9d1"), "build": ("#c9a77c", "#6b4a2b", "#b8c4b4"),
 "cafe": ("#a07a52", "#3b2a1c", "#d8c3a0"), "pilates": ("#d9cbb3", "#8fa595", "#efe6d6"),
 "clinic": ("#d6e8ec", "#7fb3bf", "#eef4f6"), "shop": ("#e7e2d8", "#6f7f8c", "#c3b9a6"),
 "corp": ("#9fb3cc", "#2c3e5c", "#d5dde8"),
}

PAL = {
 "luxe": {  # bg, accent
   "salon": ("#121014", "#c9a96e"), "build": ("#101311", "#bf9a6c"), "cafe": ("#140f0c", "#c99554"),
   "pilates": ("#12110f", "#cdb89c"), "clinic": ("#0e1215", "#a9c2cf"), "shop": ("#111111", "#c4aa7f"), "corp": ("#0b0f17", "#b3c3dc")},
 "pop": {  # main, sub
   "salon": ("#ff8fa3", "#ffd166"), "build": ("#f6a25b", "#6cc59a"), "cafe": ("#ffc44d", "#ff8c69"),
   "pilates": ("#7fd6b5", "#ffd36b"), "clinic": ("#6cc4f7", "#ffab91"), "shop": ("#f7a8c0", "#8fd3e8"), "corp": ("#5b9bff", "#ffcb47")},
 "minimal": {
   "salon": "#8a6f5c", "build": "#4b6b4f", "cafe": "#9a4f2b", "pilates": "#5f766a", "clinic": "#0b6e7a", "shop": "#2b4a6b", "corp": "#1f4fd1"},
 "wa": {
   "salon": "#8e3f52", "build": "#6b4f2a", "cafe": "#7a4528", "pilates": "#4f6e4c", "clinic": "#2c6675", "shop": "#26395b", "corp": "#a8382a"},
}

STYLE_LABEL = {"luxe": "高級感", "pop": "ポップ", "minimal": "ミニマル", "wa": "和モダン"}
NUM = {"luxe": "02", "pop": "03", "minimal": "04", "wa": "05"}

SEC_NAMES = {  # (id, EN, JA)
 "features": ("Concept", "私たちの特徴"),
 "services": {"salon": ("Menu", "メニュー"), "build": ("Service", "事業内容"), "cafe": ("Style", "楽しみ方"),
              "pilates": ("Class", "クラス紹介"), "clinic": ("Medical", "診療案内"), "shop": ("Service", "ショップについて"), "corp": ("Service", "事業内容")},
 "prices": ("Price", "料金"), "staff": ("Staff", "スタッフ"), "stats": ("Spec", "性能と実績"), "works": ("Works", "施工事例"),
 "flow": ("Flow", "家づくりの流れ"), "plans": ("Price", "料金プラン"), "hours": ("Hours", "診療時間"), "news": ("News", "お知らせ"),
 "products": ("Items", "商品一覧"), "guide": ("Guide", "ご利用ガイド"), "nums": ("Numbers", "数字で見る"), "timeline": ("History", "沿革"),
 "info": ("Information", "店舗情報"), "contact": ("Contact", "お問い合わせ"),
}
INFO_JA = {"build": "会社案内", "clinic": "アクセス", "corp": "会社概要", "pilates": "スタジオ情報"}


def ph(d, i, label=None, cls=""):
    a, b, c = PHOTO[d["key"]]
    grads = [f"linear-gradient(150deg,{a},{b})", f"linear-gradient(200deg,{c},{b})", f"linear-gradient(120deg,{c},{a})"]
    lab = label or d["photos"][i % len(d["photos"])]
    return f'<div class="ph {cls}" style="background:{grads[i % 3]}"><span>{E(lab)}（差し替え）</span></div>'


# ---------- 共通コンポーネント ----------
def price_groups(d):
    out = []
    for g, items in d["prices"]:
        lis = "".join(f'<li><span class="pn">{E(n)}{f"<small>{E(s)}</small>" if s else ""}</span><span class="dots"></span><span class="yen">{E(p)}</span></li>' for n, s, p in items)
        out.append(f'<div class="pgroup"><h3>{E(g)}</h3><ul class="plist">{lis}</ul></div>')
    return f'<div class="pgroups">{"".join(out)}</div><p class="note">表示価格はすべて税込です。</p>'

def plans(d):
    cards = "".join(f'<div class="plan{" pick" if i == 1 else ""}"><span class="pl-name">{E(n)}{"（人気）" if i == 1 else ""}</span><span class="pl-amt">{E(a)}</span><small>{E(s)}</small></div>' for i, (n, a, s) in enumerate(d["plans"]))
    t = d["trial"]
    return f'<div class="plans">{cards}</div><p class="note">{E(t[0])} {E(t[1])}／入会金 ¥11,000（体験当日のご入会で無料）。価格は税込です。</p>'

def staff(d):
    return '<div class="cards3">' + "".join(f'<div class="staff">{ph(d, i+1, "写真", "sq")}<h3>{E(n)}</h3><p class="role">{E(r)}</p><p>{E(x)}</p></div>' for i, (n, r, x) in enumerate(d["staff"])) + '</div>'

def stats(d):
    return '<div class="stats">' + "".join(f'<div class="stat"><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in d["stats"]) + '</div>'

def works(d):
    return '<div class="cards3">' + "".join(f'<div class="work">{ph(d, i, "写真")}<h3>{E(t)}</h3><p>{E(s)}</p></div>' for i, (t, s) in enumerate(d["works"])) + '</div>'

def flow(d):
    return '<ol class="flow">' + "".join(f'<li><b>{E(t)}</b><span>{E(s)}</span></li>' for t, s in d["flow"]) + '</ol>'

def hours(d):
    days = ["月", "火", "水", "木", "金", "土", "日祝"]
    head = "".join(f"<th>{x}</th>" for x in days)
    rows = ""
    for t, marks in d["hours"]["rows"]:
        tds = "".join(f'<td class="{"o" if m == "●" else "x"}">{m}</td>' for m in marks)
        rows += f"<tr><th>{t}</th>{tds}</tr>"
    return f'<div class="hours"><div class="tscroll"><table><thead><tr><th>診療時間</th>{head}</tr></thead><tbody>{rows}</tbody></table></div><p>{E(d["hours"]["note"])}<br>受付は診療終了の15分前までです。</p></div>'

def news(d):
    return '<ul class="news">' + "".join(f'<li><time>{E(a)}</time><span class="tag">{E(b)}</span><span>{E(c)}</span></li>' for a, b, c in d["news"]) + '</ul>'

def products(d):
    btns = "".join(f'<button type="button" class="fbtn" data-cat="{k}" aria-pressed="{"true" if k == "all" else "false"}">{E(v)}</button>' for k, v in d["cats"])
    return f'<div class="filters" role="group" aria-label="カテゴリで絞り込む">{btns}</div><div class="products" id="product-grid"></div>'

def nums(d):
    return '<div class="nums">' + "".join(f'<div><b>{E(v)}<small>{E(u)}</small></b><span>{E(l)}</span></div>' for v, u, l in d["nums"]) + '</div>'

def timeline(d):
    return '<ol class="tl">' + "".join(f'<li><time>{E(a)}</time><span>{E(b)}</span></li>' for a, b in d["timeline"]) + '</ol>'

def info(d):
    return '<div class="tscroll"><table class="tbl">' + "".join(f"<tr><th>{E(k)}</th><td>{E(v)}</td></tr>" for k, v in d["info"]) + '</table></div>'

def guide(d):
    return '<div class="cards4">' + "".join(f'<div class="gitem"><h3>{E(k)}</h3><p>{E(v)}</p></div>' for k, v in d["guide"]) + '</div>'

def form(d, pid):
    if d["key"] == "pilates":
        sel_label = "ご希望の時間帯"
    else:
        sel_label = "ご相談内容"
    opts = "".join(f"<option>{E(o)}</option>" for o in d.get("form_options", ["一般的なお問い合わせ"]))
    return f'''<form class="form" data-form>
<label for="{pid}-name">お名前<input id="{pid}-name" required></label>
<label for="{pid}-mail">メールアドレス<input id="{pid}-mail" type="email" required></label>
<label for="{pid}-kind">{sel_label}<select id="{pid}-kind">{opts}</select></label>
<label for="{pid}-msg">メッセージ<textarea id="{pid}-msg" rows="4"></textarea></label>
<div><button class="btn" type="submit">送信する</button></div>
<p class="form-msg" aria-live="polite"></p>
</form>'''

def features_list(d, style):
    if style == "luxe":  # 写真と文章を交互に
        return '<div class="zig">' + "".join(f'<div class="zrow">{ph(d, i)}<div class="ztxt"><span class="zno">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(s)}</p></div></div>' for i, (t, s) in enumerate(d["features"])) + '</div>'
    return '<div class="cards3 feats">' + "".join(f'<div class="feat"><span class="fico">{i+1}</span><h3>{E(t)}</h3><p>{E(s)}</p></div>' for i, (t, s) in enumerate(d["features"])) + '</div>'

def services_list(d):
    return '<div class="svcs">' + "".join(f'<div class="svc"><h3>{E(t)}</h3><p>{E(s)}</p></div>' for t, s in d["services"]) + '</div>'


def sections(d, style):
    """(id, en, ja, html) のリストを業種に応じて返す"""
    k = d["key"]; S = []
    def add(sid, body, name=None):
        en, ja = name or SEC_NAMES[sid]
        S.append((sid, en, ja, body))
    if k == "clinic":
        add("hours", hours(d)); add("news", news(d))
    add("features", features_list(d, style))
    sv = SEC_NAMES["services"][k]
    if "services" in d: add("services", services_list(d), sv)
    if k == "salon": add("prices", price_groups(d)); add("staff", staff(d))
    if k == "cafe": add("prices", price_groups(d), ("Menu", "メニュー"))
    if k == "build": add("stats", stats(d)); add("works", works(d)); add("flow", flow(d))
    if k == "pilates": add("plans", plans(d))
    if k == "shop": add("products", products(d))
    if k == "corp": add("nums", nums(d)); add("timeline", timeline(d))
    if k == "shop":
        add("guide", guide(d))
    else:
        add("info", info(d), ("Information", INFO_JA.get(k, "店舗情報")))
        add("contact", form(d, k[:2]), ("Contact", "体験レッスンのご予約" if k == "pilates" else "お問い合わせ"))
    return S

def nav_items(S):
    pick = [s for s in S if s[0] not in ("features",)][:5]
    return pick

def cart(d):
    return '<span class="cart">カート <b id="cart-n">0</b></span>' if d["key"] == "shop" else ""


SHOP_JS = """
  var items=%s, box=document.getElementById("product-grid"), n=0, cartEl=document.getElementById("cart-n"), toast=document.getElementById("toast"), tt;
  var grad=%s;
  function render(cat){
    box.innerHTML="";
    items.filter(function(i){return cat==="all"||i[3]===cat}).forEach(function(i,idx){
      var d=document.createElement("div"); d.className="prod";
      d.innerHTML='<div class="ph sq" style="background:'+grad[idx%%grad.length]+'"><span>写真</span></div><span class="meta">'+i[1]+'</span><h3>'+i[0]+'</h3><span class="yen">¥'+i[2].toLocaleString("ja-JP")+' <small>税込</small></span><button class="add" type="button">カートに入れる</button>';
      d.querySelector(".add").addEventListener("click",function(){
        n++; cartEl.textContent=n; toast.textContent="「"+i[0]+"」をカートに追加しました"; toast.hidden=false;
        clearTimeout(tt); tt=setTimeout(function(){toast.hidden=true},2200);
      });
      box.appendChild(d);
    });
  }
  document.querySelectorAll(".fbtn").forEach(function(b){b.addEventListener("click",function(){
    document.querySelectorAll(".fbtn").forEach(function(x){x.setAttribute("aria-pressed",x===b?"true":"false")});
    render(b.dataset.cat);
  })});
  render("all");
"""

def scripts(d):
    js = """
  document.querySelectorAll("[data-form]").forEach(function(f){
    f.addEventListener("submit",function(e){e.preventDefault();
      f.querySelector(".form-msg").textContent="これはサンプルのため、送信はされません（納品時に送信先を設定します）。";});
  });"""
    if d["key"] == "shop":
        a, b, c = PHOTO["shop"]
        g = [f"linear-gradient(150deg,{a},{b})", f"linear-gradient(200deg,{c},{b})", f"linear-gradient(120deg,{c},{a})", f"linear-gradient(170deg,#eee,{c})"]
        js += SHOP_JS % (json.dumps([list(p) for p in d["products"]], ensure_ascii=False), json.dumps(g))
    return "<script>\n(function(){" + js + "\n})();\n</script>"


def page(d, style, css, body):
    name, sub = d["names"][style]
    title = f"{name}｜{sub}"
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(d["tagline"][style])} {E(title)}（サンプルサイト・{STYLE_LABEL[style]}）">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[style]}&display=swap">
<style>
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;-webkit-text-size-adjust:100%}}
img{{max-width:100%}}
[hidden]{{display:none!important}}
a{{color:inherit}}
h1,h2,h3{{word-break:auto-phrase}}
:focus-visible{{outline:2px solid currentColor;outline-offset:3px}}
section[id]{{scroll-margin-top:72px}}
.wrap{{max-width:1080px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px))}}
.ph{{position:relative;width:100%;max-width:100%;aspect-ratio:4/3;display:flex;align-items:flex-end;padding:12px 14px;font-size:11px;letter-spacing:.06em;overflow:hidden}}
.ph.sq{{aspect-ratio:1}}
.ph span{{background:rgba(0,0,0,.38);color:#fff;padding:2px 8px;border-radius:3px}}
.tscroll{{overflow-x:auto}}
.tbl{{width:100%;border-collapse:collapse}}
.tbl th,.tbl td{{text-align:left;vertical-align:top;padding:14px 10px;border-bottom:1px solid var(--line)}}
.tbl th{{white-space:nowrap;width:9em;font-weight:600}}
.cards3{{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr))}}
.cards4{{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr))}}
.cards3>*,.cards4>*{{min-width:0}}
.svcs{{display:grid;gap:0 48px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))}}
.svc{{padding:22px 0;border-bottom:1px solid var(--line)}}
.svc h3,.feat h3,.gitem h3,.staff h3,.work h3{{margin:.2em 0 .3em}}
.svc p,.feat p,.gitem p,.staff p,.work p{{margin:0;font-size:.92em;opacity:.85}}
.staff .role{{font-size:12px;opacity:.65;margin:0 0 4px}}
.pgroups{{display:grid;gap:12px 56px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))}}
.plist{{list-style:none;margin:0;padding:0}}
.plist li{{display:flex;align-items:baseline;gap:10px;padding:11px 0;border-bottom:1px solid var(--line)}}
.plist .dots{{flex:1;min-width:16px;border-bottom:1px dotted var(--line);transform:translateY(-4px)}}
.plist small{{display:block;font-size:12px;opacity:.65}}
.yen{{font-variant-numeric:tabular-nums;white-space:nowrap;font-weight:600}}
.note{{font-size:12px;opacity:.65;margin-top:14px}}
.plans{{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr))}}
.plan{{display:flex;flex-direction:column;gap:4px;padding:26px 22px}}
.pl-amt{{font-size:30px;font-weight:600;font-variant-numeric:tabular-nums}}
.plan small{{font-size:12px;opacity:.7}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:1px;background:var(--line);border:1px solid var(--line)}}
.stat{{background:var(--bg);padding:24px 20px}}
.stat b{{display:block;font-size:32px;font-variant-numeric:tabular-nums;color:var(--accent);line-height:1.2}}
.stat span{{font-size:12px;opacity:.75}}
.flow{{list-style:none;margin:0;padding:0;counter-reset:f}}
.flow li{{counter-increment:f;display:grid;grid-template-columns:3.2em 1fr;column-gap:14px;padding:16px 0;border-bottom:1px solid var(--line)}}
.flow li::before{{content:counter(f,decimal-leading-zero);grid-row:span 2;color:var(--accent);font-size:22px;font-weight:700;line-height:1.3}}
.flow span{{font-size:.9em;opacity:.8}}
.hours table{{width:100%;border-collapse:collapse;text-align:center;font-size:14px}}
.hours th,.hours td{{padding:11px 4px;border-bottom:1px solid var(--line)}}
.hours td.o{{color:var(--accent);font-weight:700}} .hours td.x{{opacity:.35}}
.hours p{{font-size:13px;margin:12px 0 0}}
.news{{list-style:none;margin:0;padding:0}}
.news li{{display:grid;grid-template-columns:7.5em auto 1fr;gap:12px;align-items:baseline;padding:14px 0;border-bottom:1px solid var(--line)}}
.news time{{font-variant-numeric:tabular-nums;font-size:14px;opacity:.7}}
.tag{{font-size:11px;padding:2px 8px;white-space:nowrap;border:1px solid currentColor;border-radius:3px}}
.nums{{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr))}}
.nums b{{display:block;font-size:48px;line-height:1.1;font-variant-numeric:tabular-nums;font-weight:500}}
.nums b small{{font-size:16px;margin-left:4px}}
.nums span{{font-size:12px;opacity:.7}}
.tl{{list-style:none;margin:0;padding:0;border-left:2px solid var(--line)}}
.tl li{{position:relative;padding:0 0 22px 24px}}
.tl li::before{{content:"";position:absolute;left:-7px;top:8px;width:12px;height:12px;border-radius:50%;background:var(--accent)}}
.tl time{{display:block;font-weight:600;font-variant-numeric:tabular-nums}}
.filters{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:24px}}
.fbtn{{appearance:none;font:inherit;font-size:13px;padding:6px 16px;border:1px solid var(--line);background:transparent;color:var(--fg);cursor:pointer}}
.fbtn[aria-pressed="true"]{{background:var(--fg);color:var(--bg);border-color:var(--fg)}}
.products{{display:grid;gap:28px 20px;grid-template-columns:repeat(auto-fill,minmax(min(100%,200px),1fr))}}
.prod{{display:flex;flex-direction:column;gap:6px;min-width:0}}
.prod .meta{{font-size:11px;opacity:.6;letter-spacing:.06em}}
.prod h3{{font-size:14px;margin:0}}
.prod .yen small{{font-size:11px;opacity:.6;font-weight:400}}
.add{{appearance:none;font:inherit;font-size:13px;padding:9px;margin-top:auto;cursor:pointer;background:transparent;color:var(--fg);border:1px solid var(--fg)}}
.add:hover{{background:var(--fg);color:var(--bg)}}
.cart{{display:inline-flex;align-items:center;gap:8px;font-size:13px}}
.cart b{{background:var(--accent);color:var(--bg);border-radius:999px;min-width:22px;text-align:center;font-size:12px;padding:1px 6px}}
.toast{{position:fixed;left:50%;bottom:calc(20px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);background:#222;color:#fff;font-size:13px;padding:10px 18px;border-radius:999px;z-index:50;max-width:90vw}}
.form{{display:grid;gap:14px;max-width:560px}}
.form label{{display:grid;gap:5px;font-size:13px;font-weight:600}}
.form input,.form select,.form textarea{{font:inherit;font-weight:400;padding:12px;width:100%;border:1px solid var(--line);background:var(--field);color:var(--fg)}}
.form-msg{{font-size:13px;min-height:1.4em;color:var(--accent);font-weight:600}}
.btn{{display:inline-block;appearance:none;border:0;cursor:pointer;font:inherit;font-weight:600;font-size:14px;padding:14px 28px;text-decoration:none}}
.foot-note{{font-size:11px;opacity:.6}}
@media (max-width:760px){{.news li{{grid-template-columns:1fr auto}} .news li span:last-child{{grid-column:1/-1}}}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}} *{{animation:none!important;transition:none!important}}}}
{css}
</style>
</head>
<body class="{style}">
{body}
{'<div class="toast" id="toast" hidden></div>' if d["key"] == "shop" else ""}
{scripts(d)}
</body>
</html>
'''


# ================= パターン2：高級感（全面写真ヒーロー・交互レイアウト） =================
def luxe(d):
    bg, ac = PAL["luxe"][d["key"]]
    name, sub = d["names"]["luxe"]
    S = sections(d, "luxe")
    a, b, c = PHOTO[d["key"]]
    nav = "".join(f'<a href="#{s[0]}">{E(s[2])}</a>' for s in nav_items(S))
    secs = "".join(f'''<section id="{sid}" class="sec"><div class="wrap">
<div class="sh"><span class="en">{E(en)}</span><h2>{E(ja)}</h2></div>{body}</div></section>''' for sid, en, ja, body in S)
    ship = f'<div class="ship">{E(d["free_ship"])}</div>' if d["key"] == "shop" else ""
    body = f'''{ship}<header class="hdr"><div class="wrap">
<a class="logo" href="#top">{E(name)}<small>{E(sub)}</small></a>
<nav class="nav">{nav}</nav>{cart(d)}</div></header>
<section class="hero" id="top" style="--p1:{a};--p2:{b}">
<div class="hero-ph"><span>写真：メインビジュアル（差し替え）</span></div>
<div class="wrap hero-in"><p class="hero-sub">{E(sub)}</p><h1>{E(d["tagline"]["luxe"])}</h1><p class="lead">{E(d["lead"])}</p>
<a class="btn" href="#{"products" if d["key"]=="shop" else "contact"}">{E(d["cta"])}</a></div></section>
{secs}
<footer class="foot"><div class="wrap"><span class="flogo">{E(name)}</span><span class="foot-note">© {E(name)}　※架空の店舗・会社によるサンプルサイトです</span></div></footer>'''
    css = f'''
.luxe{{--bg:{bg};--fg:#ece7df;--accent:{ac};--line:rgba(236,231,223,.16);--field:rgba(255,255,255,.04);
 background:var(--bg);color:var(--fg);font-family:"Zen Kaku Gothic New",sans-serif;font-weight:400;line-height:1.9;font-size:15px;letter-spacing:.03em}}
.luxe h1,.luxe h2,.luxe h3{{font-family:"Shippori Mincho",serif;font-weight:600;text-wrap:balance;line-height:1.5}}
.ship{{text-align:center;font-size:12px;padding:7px 16px;color:var(--accent);border-bottom:1px solid var(--line)}}
.hdr{{position:absolute;left:0;right:0;z-index:5}}
.ship+.hdr{{top:36px}}
.hdr .wrap{{display:flex;align-items:center;justify-content:space-between;gap:12px 28px;flex-wrap:wrap;padding-block:22px}}
.logo{{font-family:"Cormorant Garamond","Shippori Mincho",serif;font-size:24px;font-weight:600;text-decoration:none;letter-spacing:.06em;line-height:1.2}}
.logo small{{display:block;font-family:"Zen Kaku Gothic New",sans-serif;font-size:10px;letter-spacing:.2em;opacity:.7}}
.nav{{display:flex;gap:6px 26px;flex-wrap:wrap;font-size:12px;letter-spacing:.14em}}
.nav a{{text-decoration:none;opacity:.8}} .nav a:hover{{opacity:1;color:var(--accent)}}
.hero{{position:relative;min-height:min(88vh,760px);display:flex;align-items:flex-end;overflow:hidden}}
.hero-ph{{position:absolute;inset:0;background:linear-gradient(160deg,var(--p1),var(--p2));display:flex;align-items:flex-start;justify-content:flex-end;padding:110px 18px 0}}
.hero-ph::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.15) 40%,var(--bg))}}
.hero-ph span{{position:relative;z-index:1;font-size:11px;background:rgba(0,0,0,.35);color:#fff;padding:2px 8px}}
.hero-in{{position:relative;z-index:2;padding-block:120px 72px;width:100%}}
.hero-sub{{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:20px;color:var(--accent);margin:0}}
.hero h1{{font-size:clamp(34px,6.4vw,68px);margin:.15em 0 .45em;max-width:12em}}
.lead{{max-width:34em;opacity:.85}}
.btn{{background:transparent;color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent);letter-spacing:.2em;font-weight:500;margin-top:18px}}
.btn:hover{{background:var(--accent);color:var(--bg)}}
.sec{{padding-block:96px}}
.sec+.sec{{border-top:1px solid var(--line)}}
.sh{{display:flex;flex-direction:column;align-items:center;text-align:center;margin-bottom:56px}}
.sh .en{{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:18px;color:var(--accent)}}
.sh h2{{font-size:clamp(22px,3.2vw,30px);margin:.1em 0 0;letter-spacing:.12em}}
.sh::after{{content:"";width:40px;height:1px;background:var(--accent);margin-top:20px}}
.zig{{display:grid;gap:64px}}
.zrow{{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}}
.zrow:nth-child(even) .ph{{order:2}}
.zno{{font-family:"Cormorant Garamond",serif;font-size:44px;color:var(--accent);line-height:1}}
.ztxt h3{{font-size:22px}}
.ztxt p{{opacity:.8}}
.svc h3{{font-size:18px}}
.svc h3::before{{content:"— ";color:var(--accent)}}
.pgroup h3{{font-family:"Cormorant Garamond",serif;font-size:24px;color:var(--accent);letter-spacing:.08em}}
.yen{{font-family:"Cormorant Garamond",serif;font-size:19px;font-weight:600}}
.plan{{border:1px solid var(--line)}}
.plan.pick{{border-color:var(--accent)}}
.pl-amt{{font-family:"Cormorant Garamond",serif;color:var(--accent);font-size:36px}}
.stat b,.nums b{{font-family:"Cormorant Garamond",serif;color:var(--accent)}}
.flow li::before{{font-family:"Cormorant Garamond",serif;font-size:28px;font-weight:500}}
.hours{{border:1px solid var(--line);padding:24px}}
.tag{{color:var(--accent)}}
.tl time{{font-family:"Cormorant Garamond",serif;font-size:20px;color:var(--accent)}}
.fbtn{{border-radius:0;letter-spacing:.1em}}
.fbtn[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:var(--bg)}}
.prod .yen{{font-size:18px}}
.add{{border-color:var(--line);letter-spacing:.1em}} .add:hover{{background:var(--accent);border-color:var(--accent);color:var(--bg)}}
.gitem{{border-top:1px solid var(--accent);padding-top:16px}}
.form{{margin:0 auto}}
.form input,.form select,.form textarea{{border-width:0 0 1px;padding-inline:0;background:transparent}}
.form select option{{background:var(--bg)}}
.form .btn{{width:100%}}
.foot{{border-top:1px solid var(--line)}}
.foot .wrap{{padding-block:44px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}}
.flogo{{font-family:"Cormorant Garamond","Shippori Mincho",serif;font-size:26px;letter-spacing:.08em}}
@media (max-width:760px){{.zrow{{grid-template-columns:1fr;gap:20px}} .zrow:nth-child(even) .ph{{order:0}} .sec{{padding-block:68px}} .hdr{{position:relative}} .ship+.hdr{{top:0}} .hero{{min-height:0}} .hero-in{{padding-block:80px 56px}}}}
'''
    return page(d, "luxe", css, body)


# ================= パターン3：ポップ（色ブロック・角丸カード・波形区切り） =================
WAVE = '<svg class="wave" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0,30 C240,70 480,-10 720,30 C960,70 1200,-10 1440,30 L1440,60 L0,60 Z"/></svg>'

def pop(d):
    m, s2 = PAL["pop"][d["key"]]
    name, sub = d["names"]["pop"]
    S = sections(d, "pop")
    nav = "".join(f'<a href="#{s[0]}">{E(s[2])}</a>' for s in nav_items(S)[:4])
    out = []
    for i, (sid, en, ja, body) in enumerate(S):
        tint = "t" if i % 2 == 0 else "w"
        out.append(f'''<section id="{sid}" class="sec {tint}">{WAVE}<div class="wrap">
<div class="sh"><span class="en">{E(en)}</span><h2>{E(ja)}</h2></div>{body}</div></section>''')
    ship = f'<div class="ship">{E(d["free_ship"])}</div>' if d["key"] == "shop" else ""
    target = "products" if d["key"] == "shop" else "contact"
    trial = f'<div class="bubble">{E(d["trial"][0])}<b>{E(d["trial"][1])}</b></div>' if d["key"] == "pilates" else ""
    body = f'''{ship}<header class="hdr"><div class="wrap">
<a class="logo" href="#top"><span class="dot"></span>{E(name)}</a>
<nav class="nav">{nav}</nav>{cart(d)}<a class="btn sm" href="#{target}">{E(d["cta"])}</a></div></header>
<section class="hero" id="top"><div class="wrap hero-in">
<div class="hero-txt"><p class="hero-sub">{E(sub)}</p><h1>{E(d["tagline"]["pop"])}</h1><p class="lead">{E(d["lead"])}</p>
<a class="btn" href="#{target}">{E(d["cta"])} →</a></div>
<div class="hero-vis"><div class="blob"></div>{ph(d, 0, None, "card")}{trial}</div></div></section>
{"".join(out)}
<footer class="foot"><div class="wrap"><a class="logo" href="#top"><span class="dot"></span>{E(name)}</a><span class="foot-note">© {E(name)}　※架空の店舗・会社によるサンプルサイトです</span></div></footer>
<a class="fixcta" href="#{target}">{E(d["cta"])}</a>'''
    css = f'''
.pop{{--bg:#fffdf8;--fg:#24233a;--accent:#24233a;--main:{m};--sub:{s2};--line:#ebe6dc;--field:#fff;--tint:color-mix(in srgb,var(--main) 16%,#fff);
 background:var(--bg);color:var(--fg);font-family:"Zen Maru Gothic",sans-serif;font-weight:500;line-height:1.85;font-size:15px}}
.pop h1,.pop h2,.pop h3,.logo,.btn,.en{{font-family:"M PLUS Rounded 1c","Zen Maru Gothic",sans-serif}}
.pop h1,.pop h2{{font-weight:800;text-wrap:balance;line-height:1.35}}
.pop h3{{font-weight:800}}
.ship{{background:var(--sub);text-align:center;font-size:13px;padding:7px 16px;font-weight:700}}
.hdr{{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:2px solid var(--fg)}}
.hdr .wrap{{display:flex;align-items:center;gap:10px 22px;flex-wrap:wrap;padding-block:12px}}
.logo{{font-weight:800;font-size:20px;text-decoration:none;display:flex;align-items:center;gap:8px;margin-right:auto}}
.dot{{width:22px;height:22px;border-radius:50%;background:var(--main);box-shadow:8px -6px 0 -4px var(--sub);flex:none}}
.nav{{display:flex;gap:4px 18px;flex-wrap:wrap;font-size:13px;font-weight:700}}
.nav a{{text-decoration:none}} .nav a:hover{{text-decoration:underline wavy var(--main)}}
.btn{{background:var(--fg);color:#fff;border-radius:999px;font-weight:800;box-shadow:0 4px 0 var(--main);transition:transform .15s,box-shadow .15s}}
.btn:hover{{transform:translateY(2px);box-shadow:0 2px 0 var(--main)}}
.btn.sm{{padding:9px 18px;font-size:13px}}
.hero{{background:var(--tint);overflow:hidden}}
.hero-in{{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:center;padding-block:48px 72px}}
.hero-sub{{display:inline-block;background:#fff;border:2px solid var(--fg);border-radius:999px;padding:2px 14px;font-size:13px;font-weight:700;margin:0}}
.hero h1{{font-size:clamp(32px,5.6vw,58px);margin:.35em 0 .4em}}
.lead{{max-width:30em}}
.hero-vis{{position:relative;padding:20px}}
.blob{{position:absolute;inset:0;background:var(--main);border-radius:42% 58% 63% 37% / 41% 44% 56% 59%}}
.ph.card{{position:relative;transform:rotate(-3deg);border:3px solid var(--fg);border-radius:24px;box-shadow:8px 8px 0 var(--fg)}}
.bubble{{position:absolute;right:0;bottom:6px;background:var(--sub);border:3px solid var(--fg);border-radius:999px;padding:8px 18px;font-weight:800;font-size:13px;transform:rotate(4deg)}}
.bubble b{{display:block;font-size:22px;line-height:1.1}}
.sec{{position:relative;padding-block:84px 76px}}
.sec.t{{background:var(--tint)}} .sec.w{{background:var(--bg)}}
.wave{{position:absolute;top:-1px;left:0;width:100%;height:36px;transform:scaleY(-1)}}
.sec.t .wave path{{fill:var(--bg)}} .sec.w .wave path{{fill:var(--tint)}}
.sh{{margin-bottom:36px}}
.sh .en{{display:inline-block;background:var(--main);border:2px solid var(--fg);border-radius:999px;padding:0 12px;font-size:12px;font-weight:800;transform:rotate(-2deg)}}
.sh h2{{font-size:clamp(26px,4vw,38px);margin:.25em 0 0}}
.feat{{background:#fff;border:2px solid var(--fg);border-radius:24px;padding:26px;box-shadow:5px 5px 0 var(--fg)}}
.fico{{display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:var(--sub);border:2px solid var(--fg);font-family:"M PLUS Rounded 1c",sans-serif;font-weight:800;font-size:20px}}
.feats .feat:nth-child(2) .fico{{background:var(--main)}}
.svcs{{gap:16px}}
.svc{{background:#fff;border:2px solid var(--fg);border-radius:20px;padding:20px 22px}}
.pgroup{{background:#fff;border:2px solid var(--fg);border-radius:24px;padding:8px 24px 16px}}
.pgroup h3{{display:inline-block;background:var(--sub);padding:0 10px;border-radius:8px}}
.plist li:last-child{{border-bottom:0}}
.plan{{background:#fff;border:2px solid var(--fg);border-radius:24px}}
.plan.pick{{background:var(--main);box-shadow:5px 5px 0 var(--fg)}}
.pl-amt{{font-family:"M PLUS Rounded 1c",sans-serif;font-weight:800}}
.staff .ph,.work .ph{{border:2px solid var(--fg);border-radius:20px}}
.stats{{background:var(--fg);border:2px solid var(--fg);border-radius:20px;overflow:hidden;gap:2px}}
.stat{{background:#fff}}
.stat b,.nums b{{font-family:"M PLUS Rounded 1c",sans-serif;font-weight:800;color:var(--fg)}}
.nums>div{{background:#fff;border:2px solid var(--fg);border-radius:20px;padding:20px}}
.flow li{{background:#fff;border:2px solid var(--fg);border-radius:16px;padding:14px 18px;margin-bottom:10px}}
.flow li::before{{color:var(--fg);background:var(--sub);border-radius:50%;width:42px;height:42px;display:grid;place-items:center;font-size:16px}}
.hours{{background:#fff;border:2px solid var(--fg);border-radius:20px;padding:20px}}
.hours td.o{{color:var(--fg)}}
.news li{{border-bottom:2px dashed var(--line)}}
.tag{{background:var(--sub);border-color:var(--fg)}}
.tl{{border-left:3px dashed var(--fg)}}
.tl li::before{{background:var(--main);border:2px solid var(--fg);left:-9px;width:16px;height:16px}}
.fbtn{{border:2px solid var(--fg);border-radius:999px;font-weight:700;background:#fff}}
.prod{{background:#fff;border:2px solid var(--fg);border-radius:20px;padding:12px}}
.prod .ph{{border-radius:12px}}
.add{{border:2px solid var(--fg);border-radius:999px;font-weight:700}}
.cart{{font-weight:700}}
.cart b{{background:var(--main);color:var(--fg)}}
.gitem{{background:#fff;border:2px solid var(--fg);border-radius:20px;padding:20px}}
.tbl{{background:#fff;border:2px solid var(--fg);border-radius:20px;border-collapse:separate;border-spacing:0;overflow:hidden}}
.tbl th,.tbl td{{padding:14px 18px}}
.tbl tr:last-child th,.tbl tr:last-child td{{border-bottom:0}}
.form{{background:#fff;border:2px solid var(--fg);border-radius:24px;padding:28px}}
.form input,.form select,.form textarea{{border:2px solid var(--line);border-radius:12px}}
.form-msg{{color:var(--fg)}}
.foot{{background:var(--fg);color:#fff}}
.foot .wrap{{padding-block:36px 96px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px}}
.fixcta{{display:none}}
@media (max-width:760px){{
 .hero-in{{grid-template-columns:1fr}} .nav{{display:none}} .hdr .btn.sm{{display:none}}
 .fixcta{{display:block;position:fixed;left:16px;right:16px;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:30;text-align:center;background:var(--main);color:var(--fg);border:2px solid var(--fg);border-radius:999px;padding:13px;font-weight:800;text-decoration:none;box-shadow:0 4px 0 var(--fg)}}
 .sec{{padding-block:64px 56px}}
}}
'''
    return page(d, "pop", css, body)


# ================= パターン4：ミニマル（大きな文字・2カラムの見出し／本文） =================
def minimal(d):
    ac = PAL["minimal"][d["key"]]
    name, sub = d["names"]["minimal"]
    S = sections(d, "minimal")
    nav = "".join(f'<a href="#{s[0]}">{E(s[1])}</a>' for s in nav_items(S))
    secs = "".join(f'''<section id="{sid}" class="sec"><div class="wrap row">
<div class="sh"><span class="idx">{i+1:02d}</span><span class="en">{E(en)}</span><h2>{E(ja)}</h2></div><div class="sb">{body}</div></div></section>''' for i, (sid, en, ja, body) in enumerate(S))
    ship = f'<div class="ship">{E(d["free_ship"])}</div>' if d["key"] == "shop" else ""
    target = "products" if d["key"] == "shop" else "contact"
    body = f'''{ship}<header class="hdr"><div class="wrap">
<a class="logo" href="#top">{E(name)}</a><nav class="nav">{nav}</nav>{cart(d)}</div></header>
<section class="hero" id="top"><div class="wrap">
<p class="hero-sub">{E(sub)}</p><h1>{E(d["tagline"]["minimal"])}</h1>
<div class="hero-row"><p class="lead">{E(d["lead"])}</p><a class="btn" href="#{target}">{E(d["cta"])}<span aria-hidden="true">→</span></a></div>
</div><div class="wrap">{ph(d, 0, "写真：メインビジュアル", "wide")}</div></section>
{secs}
<footer class="foot"><div class="wrap"><span>{E(name)}</span><span class="foot-note">© {E(name)}　※架空の店舗・会社によるサンプルサイトです</span></div></footer>'''
    css = f'''
.minimal{{--bg:#ffffff;--fg:#141414;--accent:{ac};--line:#e4e4e2;--field:#fafafa;
 background:var(--bg);color:var(--fg);font-family:"IBM Plex Sans JP",sans-serif;font-weight:400;line-height:1.9;font-size:15px}}
.minimal h1,.minimal h2,.minimal h3{{font-weight:600;text-wrap:balance;line-height:1.4}}
.ship{{font-size:12px;padding:8px 18px;border-bottom:1px solid var(--line);text-align:center}}
.hdr{{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.94);backdrop-filter:blur(8px)}}
.hdr .wrap{{display:flex;align-items:center;gap:10px 28px;flex-wrap:wrap;padding-block:18px}}
.logo{{font-family:"Jost","IBM Plex Sans JP",sans-serif;font-weight:500;font-size:18px;text-decoration:none;margin-right:auto;letter-spacing:.02em}}
.nav{{display:flex;gap:4px 22px;flex-wrap:wrap;font-family:"Jost",sans-serif;font-size:13px;font-weight:300;letter-spacing:.06em}}
.nav a{{text-decoration:none}} .nav a:hover{{color:var(--accent)}}
.hero .wrap:first-child{{padding-block:72px 40px}}
.hero-sub{{font-size:13px;color:var(--accent);margin:0;letter-spacing:.08em}}
.hero h1{{font-size:clamp(40px,8.4vw,104px);font-weight:300;letter-spacing:-.01em;line-height:1.15;margin:.15em 0 .5em}}
.hero-row{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}}
.lead{{max-width:30em;margin:0;color:#4a4a48}}
.btn{{background:var(--fg);color:#fff;font-weight:400;display:inline-flex;gap:14px;align-items:center;letter-spacing:.06em}}
.btn:hover{{background:var(--accent)}}
.ph.wide{{aspect-ratio:21/9}}
.sec{{padding-block:88px}}
.sec+.sec{{border-top:1px solid var(--line)}}
.row{{display:grid;grid-template-columns:220px 1fr;gap:40px}}
.row>*{{min-width:0}}
.sh{{display:flex;flex-direction:column;align-self:start;position:sticky;top:88px}}
.idx{{font-family:"Jost",sans-serif;font-weight:300;font-size:13px;color:var(--accent)}}
.en{{font-family:"Jost",sans-serif;font-size:13px;letter-spacing:.12em;text-transform:uppercase;opacity:.55}}
.sh h2{{font-size:22px;margin:.3em 0 0}}
.feat{{border-top:1px solid var(--fg);padding-top:16px}}
.fico{{font-family:"Jost",sans-serif;font-size:13px;color:var(--accent)}}
.pgroup h3{{font-family:"Jost",sans-serif;font-weight:500;font-size:14px;letter-spacing:.12em;color:var(--accent)}}
.plist .dots{{border:0}}
.yen{{font-weight:400;font-family:"Jost","IBM Plex Sans JP",sans-serif;font-size:17px}}
.plan{{border:1px solid var(--line)}}
.plan.pick{{border-color:var(--fg)}}
.pl-amt{{font-family:"Jost",sans-serif;font-weight:300;font-size:36px}}
.stat b,.nums b{{font-family:"Jost",sans-serif;font-weight:300}}
.nums b{{color:var(--fg)}}
.flow li::before{{font-family:"Jost",sans-serif;font-weight:300}}
.hours{{border-top:1px solid var(--fg)}}
.tl{{border-color:var(--fg);border-width:0 0 0 1px}}
.tl li::before{{width:7px;height:7px;left:-4px;top:11px;background:var(--fg)}}
.tl time{{font-family:"Jost",sans-serif;font-weight:500}}
.fbtn{{border-radius:0;font-family:"Jost","IBM Plex Sans JP",sans-serif}}
.prod .yen{{font-size:15px}}
.gitem{{border-top:1px solid var(--fg);padding-top:14px}}
.tbl th{{font-weight:400;opacity:.6}}
.form input,.form select,.form textarea{{border-radius:0}}
.form .btn{{justify-self:start}}
.foot .wrap{{padding-block:40px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;border-top:1px solid var(--fg);font-family:"Jost","IBM Plex Sans JP",sans-serif}}
@media (max-width:860px){{.row{{grid-template-columns:1fr;gap:20px}} .sh{{position:static}} .sec{{padding-block:60px}} .nav{{display:none}} .ph.wide{{aspect-ratio:4/3}}}}
'''
    return page(d, "minimal", css, body)


# ================= パターン5：和モダン（縦書き見出し・左サイドバー） =================
def wa(d):
    ac = PAL["wa"][d["key"]]
    name, sub = d["names"]["wa"]
    S = sections(d, "wa")
    nav = "".join(f'<a href="#{s[0]}">{E(s[2])}</a>' for s in nav_items(S))
    secs = "".join(f'''<section id="{sid}" class="sec"><div class="sh"><h2>{E(ja)}</h2><span class="en">{E(en)}</span></div><div class="sb">{body}</div></section>''' for sid, en, ja, body in S)
    ship = f'<div class="ship">{E(d["free_ship"])}</div>' if d["key"] == "shop" else ""
    target = "products" if d["key"] == "shop" else "contact"
    body = f'''<aside class="side"><a class="logo" href="#top"><span class="seal">{SEAL[d["key"]]}</span><span class="lname">{E(name)}</span></a>
<nav class="nav">{nav}</nav>{cart(d)}</aside>
<main class="main">{ship}
<section class="hero" id="top">
<div class="hero-ph" style="background:linear-gradient(150deg,{PHOTO[d["key"]][0]},{PHOTO[d["key"]][1]})"><span>写真：メインビジュアル（差し替え）</span></div>
<div class="hero-copy"><h1>{E(d["tagline"]["wa"])}</h1></div>
<div class="hero-foot"><p class="hero-sub">{E(sub)}</p><p class="lead">{E(d["lead"])}</p><a class="btn" href="#{target}">{E(d["cta"])}</a></div>
</section>
{secs}
<footer class="foot"><span>{E(name)}</span><span class="foot-note">© {E(name)}　※架空の店舗・会社によるサンプルサイトです</span></footer>
</main>'''
    css = f'''
.wa{{--bg:#f4f2ec;--fg:#1f2530;--accent:{ac};--indigo:#26395b;--line:#d9d4c7;--field:#fbfaf6;
 background:var(--bg);color:var(--fg);font-family:"Zen Kaku Gothic New",sans-serif;line-height:1.95;font-size:15px;letter-spacing:.04em;
 background-image:radial-gradient(rgba(31,37,48,.035) 1px,transparent 1px);background-size:4px 4px}}
.wa h1,.wa h2,.wa h3,.logo{{font-family:"Zen Old Mincho",serif;font-weight:700;line-height:1.5}}
.side{{position:fixed;inset:0 auto 0 0;width:120px;border-right:1px solid var(--line);display:flex;flex-direction:column;align-items:center;gap:28px;padding:28px 0 24px;padding-left:env(safe-area-inset-left,0px);background:var(--bg);z-index:20}}
.logo{{text-decoration:none;display:flex;flex-direction:column;align-items:center;gap:14px}}
.seal{{display:grid;place-items:center;width:44px;height:44px;background:var(--accent);color:#fff;font-size:22px;border-radius:4px}}
.lname{{writing-mode:vertical-rl;font-size:18px;letter-spacing:.2em}}
.nav{{writing-mode:vertical-rl;display:flex;gap:18px;font-size:13px;letter-spacing:.2em}}
.nav a{{text-decoration:none}} .nav a:hover{{color:var(--accent)}}
.cart{{writing-mode:horizontal-tb}}
.main{{margin-left:120px}}
.ship{{background:var(--indigo);color:#fff;font-size:12px;text-align:center;padding:7px 16px}}
.hero{{display:grid;grid-template-columns:1fr auto;grid-template-rows:auto auto;gap:0;padding:40px max(18px,env(safe-area-inset-right,0px)) 72px 40px;max-width:1120px}}
.hero-ph{{aspect-ratio:16/10;display:flex;align-items:flex-end;padding:12px 14px;font-size:11px}}
.hero-ph span{{background:rgba(0,0,0,.38);color:#fff;padding:2px 8px}}
.hero-copy{{grid-row:1/3;grid-column:2;padding-left:28px}}
.hero h1{{writing-mode:vertical-rl;font-size:clamp(30px,4.4vw,52px);font-weight:900;letter-spacing:.18em;margin:0;line-height:1.7}}
.hero-foot{{max-width:34em;padding-top:28px}}
.hero-sub{{font-family:"Zen Old Mincho",serif;color:var(--accent);margin:0;font-weight:700}}
.lead{{margin:.4em 0 1.4em}}
.btn{{background:var(--indigo);color:#fff;font-weight:500;letter-spacing:.2em;border-radius:2px}}
.btn:hover{{background:var(--accent)}}
.sec{{display:grid;grid-template-columns:72px 1fr;gap:36px;padding:72px max(18px,env(safe-area-inset-right,0px)) 72px 40px;max-width:1120px;border-top:1px solid var(--line)}}
.sec>*{{min-width:0}}
.sh{{display:flex;writing-mode:vertical-rl;gap:12px;align-items:center}}
.sh h2{{font-size:26px;letter-spacing:.25em;margin:0}}
.sh .en{{font-size:11px;letter-spacing:.2em;color:var(--accent);text-transform:uppercase;font-family:"Zen Kaku Gothic New",sans-serif}}
.zno,.fico{{font-family:"Zen Old Mincho",serif;color:var(--accent);font-size:28px;font-weight:900}}
.feat{{border-left:2px solid var(--accent);padding-left:18px}}
.svc h3::before{{content:"◆ ";color:var(--accent);font-size:.7em;vertical-align:.15em}}
.pgroup h3{{color:var(--accent)}}
.yen{{font-family:"Zen Old Mincho",serif;font-size:17px}}
.plan{{background:var(--field);border:1px solid var(--line)}}
.plan.pick{{background:var(--indigo);color:#fff;border-color:var(--indigo)}}
.pl-amt{{font-family:"Zen Old Mincho",serif;font-weight:900}}
.stat b,.nums b{{font-family:"Zen Old Mincho",serif;font-weight:900;color:var(--accent)}}
.flow li::before{{font-family:"Zen Old Mincho",serif;font-weight:900}}
.hours{{background:var(--field);border:1px solid var(--line);padding:20px}}
.tag{{color:var(--accent)}}
.tl li::before{{background:var(--accent);border-radius:0;transform:rotate(45deg);width:10px;height:10px;left:-6px}}
.tl time{{font-family:"Zen Old Mincho",serif}}
.fbtn{{border-radius:2px}}
.fbtn[aria-pressed="true"]{{background:var(--indigo);border-color:var(--indigo);color:#fff}}
.add:hover{{background:var(--indigo);border-color:var(--indigo);color:#fff}}
.gitem{{border-top:2px solid var(--indigo);padding-top:14px}}
.tbl th{{font-family:"Zen Old Mincho",serif}}
.form input,.form select,.form textarea{{border-radius:2px}}
.foot{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;padding:32px max(18px,env(safe-area-inset-right,0px)) 32px 40px;border-top:1px solid var(--line);font-family:"Zen Old Mincho",serif;max-width:1120px}}
@media (max-width:860px){{
 .side{{position:sticky;top:0;inset:auto;width:auto;flex-direction:row;justify-content:space-between;padding:10px max(18px,env(safe-area-inset-right,0px)) 10px max(18px,env(safe-area-inset-left,0px));border-right:0;border-bottom:1px solid var(--line)}}
 .logo{{flex-direction:row}} .lname{{writing-mode:horizontal-tb;font-size:16px;letter-spacing:.08em}} .seal{{width:34px;height:34px;font-size:17px}}
 .nav{{display:none}}
 .main{{margin-left:0}}
 .hero{{padding:24px max(18px,env(safe-area-inset-right,0px)) 56px max(18px,env(safe-area-inset-left,0px));gap:0}}
 .hero-copy{{padding-left:16px}}
 .hero h1{{font-size:26px}}
 .hero-foot{{grid-column:1/-1}}
 .sec{{grid-template-columns:1fr;gap:20px;padding:56px max(18px,env(safe-area-inset-right,0px)) 56px max(18px,env(safe-area-inset-left,0px))}}
 .sh{{writing-mode:horizontal-tb;align-items:baseline}} .sh h2{{font-size:22px;letter-spacing:.12em}}
 .foot{{padding-inline:max(18px,env(safe-area-inset-left,0px))}}
}}
'''
    return page(d, "wa", css, body)


SEAL = {"salon":"凛","build":"匠","cafe":"茶","pilates":"和","clinic":"陽","shop":"藍","corp":"結"}
BUILDERS = {"luxe": luxe, "pop": pop, "minimal": minimal, "wa": wa}

if __name__ == "__main__":
    for d in INDUSTRIES:
        for style, fn in BUILDERS.items():
            p = ROOT / d["key"] / f"{NUM[style]}.html"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(fn(d))
            print(p.relative_to(ROOT))
