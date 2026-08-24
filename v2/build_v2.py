# -*- coding: utf-8 -*-
"""Otium LP v2 builder.
新6枚は PHOTO_DIR にファイルが揃えば自動で base64 埋め込み、無ければプレースホルダ。
再実行すれば /Users/kou12/otium/v2/index.html が作り直される。
"""
import re, io, os, base64, glob, sys

SRC   = "/Users/kou12/otium/index.html"
DST   = "/Users/kou12/otium/v2/index.html"
PHOTO_DIR = "/Users/kou12/otium/photos"   # p1.jpg … p6.jpg （拡張子は何でも可）

src = io.open(SRC, encoding="utf-8").read()

# ── 1. 現行LPから流用する写真を alt で取り出す ──────────────────
pat = re.compile(r'<img\s+src="data:image/([a-z+]+);base64,([A-Za-z0-9+/=]+)"\s+alt="([^"]*)"')
bank = {m.group(3): (m.group(1), m.group(2)) for m in pat.finditer(src)}

def keep(alt):
    ext, b64 = bank[alt]
    return 'data:image/%s;base64,%s' % (ext, b64)

# ── 2. 新6枚 ────────────────────────────────────────────────
MIME = {'.jpg':'jpeg', '.jpeg':'jpeg', '.png':'png', '.webp':'webp'}
def new_photo(n):
    for f in sorted(glob.glob(os.path.join(PHOTO_DIR, "p%d.*" % n))):
        ext = MIME.get(os.path.splitext(f)[1].lower())
        if ext:
            return 'data:image/%s;base64,%s' % (ext, base64.b64encode(open(f,'rb').read()).decode())
    return None

SHOTS = {
 1: ("デスク。手はキーボードに置かれたまま、視線は窓の外", "Ⅰ 渦の中／デスク"),
 2: ("会議室の手前の廊下。ケースを持っているが、まだ使っていない", "Ⅱ 廊下"),
 3: ("非常階段の踊り場。扉が閉まった直後。嗅いでいる", "Ⅲ 非常階段"),
 4: ("屋上。日中。街を見ている", "Ⅳ 屋上"),
 5: ("会議室の扉に手をかけている。ケースはベルトに下がって閉じている", "Ⅴ 戻る"),
 6: ("デスク。1と同じ構図・同じ光。手が動いている", "Ⅵ デスク（1の対）"),
}

def P(n, alt, cls=""):
    """新写真スロット。ファイルが無ければプレースホルダを返す。"""
    d = new_photo(n)
    c = (' class="%s"' % cls) if cls else ''
    if d:
        return '<img%s src="%s" alt="%s">' % (c, d, alt)
    label, head = SHOTS[n][0], SHOTS[n][1]
    return ('<div class="ph"><span>写真 %d ／ %s<br><b>%s</b><br>'
            'photos/p%d.jpg を置いて再ビルド</span></div>' % (n, head, label, n))

MISSING = [n for n in range(1,7) if not new_photo(n)]

CSS_ADD = """
/* ══ PAIN（文字のみ） ══ */
.painx{max-width:64rem;margin:0 auto}
.painx__list{margin-top:clamp(2.4rem,5vh,3.4rem)}
.painx__row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);
  gap:clamp(.6rem,3vw,3rem);padding:1.7rem 0;
  border-top:1px solid rgba(0,0,0,.1);align-items:baseline}
.painx__row:last-of-type{border-bottom:1px solid rgba(0,0,0,.1)}
.painx__row h3{font-size:clamp(.98rem,1.4vw,1.08rem);font-weight:600;line-height:1.75}
.painx__row p{font-size:.86rem;color:#6B5C4B;line-height:1.95}
.painx__end{margin-top:clamp(2.6rem,6vh,4rem);padding-top:2.1rem;
  border-top:1px solid rgba(168,130,60,.45);max-width:42rem}
.painx__end p{font-size:clamp(.98rem,1.45vw,1.16rem);line-height:2.2}
.painx__end b{font-weight:600}

/* ══ WHY ══ */
.why{max-width:64rem;margin:0 auto}
.why__list{margin-top:clamp(2.4rem,5vh,3.4rem)}
.why__row{display:grid;grid-template-columns:2.2rem minmax(0,14rem) minmax(0,1fr);
  gap:clamp(.9rem,3vw,2.4rem);padding:1.75rem 0;
  border-top:1px solid rgba(168,130,60,.24);align-items:baseline}
.why__row:last-child{border-bottom:1px solid rgba(168,130,60,.24)}
.why__n{font-family:var(--serif);font-size:1.45rem;color:var(--brass);line-height:1}
.why__row h3{font-size:1.02rem;font-weight:500;color:#F6F2EA}
.why__row p{font-size:.88rem;color:var(--smoke-lt);line-height:2}
.why__blank{display:inline-block;width:4.4rem;height:1px;background:var(--brass);opacity:.55}
.why__row--res p{color:#E8E0D4;font-size:clamp(.95rem,1.3vw,1.06rem)}

/* ══ THE DAY ══ */
.day{margin-top:clamp(3rem,6vh,4.4rem);display:grid;gap:clamp(2.8rem,7vh,5.5rem)}
.cut figure{aspect-ratio:16/9;overflow:hidden;background:#1c1613}
.cut__cap{margin-top:1.15rem;display:grid;grid-template-columns:2.8rem minmax(0,1fr);
  gap:1rem;align-items:baseline;max-width:44rem}
.cut__n{font-family:var(--serif);font-size:.95rem;letter-spacing:.16em;color:var(--brass)}
.cut__cap h3{font-size:.99rem;font-weight:500;color:#E6DED2;line-height:1.8}
.cut__cap p{font-size:.8rem;color:var(--smoke);margin-top:.3rem;line-height:1.95}

/* ══ PAIR — 見せ場 ══ */
.pair{padding:clamp(6.5rem,15vh,12rem) var(--pad)}
.pair__grid{max-width:82rem;margin:0 auto;
  display:grid;grid-template-columns:minmax(0,1fr) 1px minmax(0,1fr);
  gap:clamp(1.3rem,3.2vw,3rem);align-items:start}
.pair__hair{align-self:stretch;background:linear-gradient(180deg,
  transparent 0%,rgba(168,130,60,.55) 18%,rgba(168,130,60,.55) 82%,transparent 100%)}
.pair__side figure{aspect-ratio:16/9;overflow:hidden;background:#1c1613}
.pair__side figcaption{margin-top:1.2rem;font-size:.83rem;color:var(--smoke);letter-spacing:.1em}
.pair__side em{font-style:normal;font-family:var(--serif);color:var(--brass-lt);
  letter-spacing:.2em;margin-right:.85rem}
.pair__say{max-width:82rem;margin:clamp(3.6rem,9vh,7rem) auto 0;text-align:center}
.pair__say h2{font-size:clamp(1.62rem,4.4vw,3.35rem);line-height:1.62;color:#F6F2EA}
.pair__say small{display:block;font-size:.8rem;letter-spacing:.13em;
  color:var(--smoke);margin-top:clamp(1.8rem,4vh,2.6rem);line-height:2.1}

/* ══ 未配置写真のプレースホルダ ══ */
.ph{width:100%;height:100%;min-height:12rem;
  background:repeating-linear-gradient(45deg,#1c1613,#1c1613 14px,#221a15 14px,#221a15 28px);
  border:1px solid rgba(168,130,60,.35);
  display:flex;align-items:center;justify-content:center;text-align:center;padding:1.4rem}
.ph span{font-family:var(--jp);font-size:.76rem;color:var(--brass-lt);
  letter-spacing:.12em;line-height:2.1}
.ph b{font-weight:500;color:#E6DED2}

/* ══ v2 responsive ══ */
@media (max-width:900px){
  .painx__row{grid-template-columns:1fr;gap:.4rem}
  .why__row{grid-template-columns:2rem minmax(0,1fr);row-gap:.4rem}
  .why__row p{grid-column:2}
  .pair__grid{grid-template-columns:1fr;gap:2.4rem}
  .pair__hair{height:1px;width:100%;background:linear-gradient(90deg,
    transparent,rgba(168,130,60,.55) 18%,rgba(168,130,60,.55) 82%,transparent)}
  .cut figure{aspect-ratio:4/3}
}
"""

HTML = u"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow, noarchive, noimageindex">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>Otium — 離れないと、自分の判断が見えない。</title>
<meta property="og:title" content="Otium">
<meta property="og:description" content="離れないと、自分の判断が見えない。">
<meta property="og:type" content="website">
<meta name="theme-color" content="#17120E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300&family=Shippori+Mincho:wght@400;500;600&display=swap" rel="stylesheet">
%%STYLE%%
</head>
<body>

<!-- ══════ Ⅰ. HERO ══════ -->
<header class="hero">
  <div class="hero__bg">%%P1_HERO%%</div>
  <div class="hero__in">
    <div class="hero__copy">
      <div class="mark rv">OTIUM</div>
      <h1 class="rv d1">この選択で、<br>あっているのか。</h1>
      <div class="hero__hair rv d2"></div>
      <div class="hero__sub rv d3">
        <p>確かめる手段がないまま、決め続けている。<br>
        古代ローマの言葉、Otium（オティウム）から。</p>
      </div>
    </div>
  </div>
  <div class="scroll"><span></span>SCROLL</div>
</header>

<!-- ══════ Ⅱ. THE PAIN ══════ -->
<section class="band band--paper">
  <div class="wrap painx">
    <div class="eyebrow rv">The pain</div>
    <h2 class="rv d1" style="margin-top:1.8rem">誰も、答えを持っていない。</h2>

    <div class="painx__list">
      <div class="painx__row rv d1">
        <h3>周りが全員、利害関係者</h3>
        <p>立場のない相手がいない。素の判断が、返ってこない</p>
      </div>
      <div class="painx__row rv d2">
        <h3>正解がない</h3>
        <p>自ら道を切り拓く以上、答えを持っている人がいない</p>
      </div>
      <div class="painx__row rv d3">
        <h3>一人で決め続けている</h3>
        <p>確かめられないまま、次の判断が来る</p>
      </div>
    </div>

    <div class="painx__end rv d3">
      <p>確かめられないから、量で埋めようとする。<br>
      <b>休まなくなるのは、原因ではなく、結果だった。</b></p>
    </div>
  </div>
</section>

<!-- ══════ Ⅲ. THE WORD ══════ -->
<section class="band">
  <div class="wrap word">
    <div>
      <div class="eyebrow rv">The word</div>
      <div class="word__lat rv d1" style="margin-top:2.2rem">Otium</div>
      <div class="word__yomi rv d2">オティウム ／ ラテン語</div>
    </div>
    <div>
      <p class="word__def rv d1">仕事や公務から<u>離れ</u>、<br>
      <u>思索</u>・芸術・学問に浸る、<br>充実した自由な時間。</p>
      <div class="word__note rv d2">
        <p class="lede">日本語には、これにあたる言葉がなかった。<br>
        休むことを、怠けることとしか呼べない国で、<br>
        この時間には、二千年前から名前があった。</p>
      </div>
    </div>
  </div>
</section>

<!-- ══════ Ⅳ. NEGOTIUM ══════ -->
<section class="neg">
  <div class="eyebrow rv" style="justify-content:center">The opposite</div>

  <div class="eq rv d1">
    <span class="term"><b>nec</b><em>否定</em></span>
    <i>+</i>
    <span class="term"><b class="strike" id="strike">otium</b><em>余暇</em></span>
  </div>

  <div class="neg__res rv d3">
    <div class="arrow">↓</div>
    <p>negotium</p>
    <small>仕事</small>
  </div>

  <div class="neg__say rv d4">
    <p>ラテン語では、「仕事」が「余暇の否定形」として定義されていた。<br>
    <b style="font-weight:600;color:#F6F2EA">余暇が先で、仕事が後だった。</b></p>
    <cite>そして二千年前、セネカは「これは怠惰ではない」と弁明し続けている。</cite>
  </div>
</section>

<!-- ══════ Ⅴ. WHY ══════ -->
<section class="band">
  <div class="wrap why">
    <div class="eyebrow rv">Why it works</div>
    <h2 class="rv d1" style="margin-top:1.8rem;color:#F6F2EA">答えは、定義の中にあった。</h2>

    <div class="why__list">
      <div class="why__row rv d1">
        <div class="why__n">Ⅰ</div>
        <h3>仕事から離れる</h3>
        <p>判断の渦から、一度出る</p>
      </div>
      <div class="why__row rv d2">
        <div class="why__n">Ⅱ</div>
        <h3>思索・芸術・学問に浸る</h3>
        <p>自分以外の視点に、触れる</p>
      </div>
      <div class="why__row why__row--res rv d3">
        <div class="why__n">Ⅲ</div>
        <h3><span class="why__blank"></span></h3>
        <p>自分の判断を、別の位置から見られる</p>
      </div>
    </div>
  </div>
</section>

<!-- ══════ Ⅵ. THE DAY ══════ -->
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="eyebrow rv">The day</div>
    <h2 class="rv d1" style="margin-top:1.8rem;color:#F6F2EA">ある平日の、四つの場面。</h2>

    <div class="day">
      <div class="cut rv"><figure>%%P2%%</figure>
        <div class="cut__cap"><div class="cut__n">Ⅱ</div>
          <div><h3>会議の前</h3><p>まだ、開けていない</p></div></div></div>

      <div class="cut rv"><figure>%%P3%%</figure>
        <div class="cut__cap"><div class="cut__n">Ⅲ</div>
          <div><h3>扉が閉まる</h3><p>閉めた側に、誰もいない</p></div></div></div>

      <div class="cut rv"><figure>%%P4%%</figure>
        <div class="cut__cap"><div class="cut__n">Ⅳ</div>
          <div><h3>屋上</h3><p>街のほうが、動いている</p></div></div></div>

      <div class="cut rv"><figure>%%P5%%</figure>
        <div class="cut__cap"><div class="cut__n">Ⅴ</div>
          <div><h3>戻る</h3><p>ケースは、閉じている</p></div></div></div>
    </div>
  </div>
</section>

<!-- ══════ Ⅶ. ★ THE PAIR ══════ -->
<section class="pair">
  <div class="pair__grid">
    <div class="pair__side rv">
      <figure>%%P1%%</figure>
      <figcaption><em>Before</em>手が止まっている</figcaption>
    </div>
    <div class="pair__hair rv d2"></div>
    <div class="pair__side rv d3">
      <figure>%%P6%%</figure>
      <figcaption><em>After</em>手が動いている</figcaption>
    </div>
  </div>

  <div class="pair__say rv d4">
    <h2>離れないと、<br>自分の判断が見えない。</h2>
    <small>同じ机、同じ光、同じ服。<br>違うのは、手だけ。</small>
  </div>
</section>

<!-- ══════ Ⅷ. THE OBJECT ══════ -->
<section class="band">
  <div class="wrap obj">
    <div class="obj__img rv"><img src="%%CASE%%" alt="ウォルナットと真鍮のケース"></div>
    <div>
      <div class="eyebrow rv d1">The object</div>
      <h2 class="rv d1" style="margin-top:1.8rem;color:#F6F2EA">持ち歩ける、Otium。</h2>
      <p class="lede rv d2" style="margin-top:1.3rem">
        木のケースに、お香を一本。<br>
        香水と違い、常には香らない。迷っている、その瞬間にだけ。
      </p>
      <div class="steps">
        <div class="step rv d2"><div class="step__n">Ⅰ</div>
          <div><h3>開ける</h3><p>ポケットから出して、真鍮の蓋をひねる</p></div></div>
        <div class="step rv d3"><div class="step__n">Ⅱ</div>
          <div><h3>嗅ぐ</h3><p>ひと息。目を閉じても、閉じなくてもいい</p></div></div>
        <div class="step rv d4"><div class="step__n">Ⅲ</div>
          <div><h3>閉じる</h3><p>終わりを、自分で決めなくていい</p></div></div>
      </div>
      <p class="obj__foot rv d4">
        数秒では、思索に浸る時間にはならない。<br>
        できるのは、走り続けている思考を、一瞬止めることだけ。<br><br>
        Otium そのものではなく、Otium へ向かうための道具として。
      </p>
    </div>
  </div>
</section>

<!-- ══════ Ⅸ. CARRY ══════ -->
<section class="band" style="padding-top:0">
  <div class="wrap carry">
    <figure class="rv"><img src="%%CARRY1%%" alt="ベルトループに掛ける"></figure>
    <figure class="rv d1"><img src="%%CARRY2%%" alt="首から下げる"></figure>
    <figure class="rv d2"><img src="%%CARRY3%%" alt="鞄に掛ける"></figure>
    <div class="carry__say">
      <div>
        <div class="eyebrow rv">Carry</div>
        <h2 class="rv d1" style="margin-top:1.6rem;color:#F6F2EA">身につけても、<br>しまってもいい。</h2>
      </div>
      <p class="lede rv d2">
        鍵と、イヤホンと、Otium。<br>
        持ち歩くのが当たり前のものとして、日常の並びに入る。<br>
        見せても、隠しても、どちらでもいい。
      </p>
    </div>
  </div>
</section>

<!-- ══════ Ⅹ. THE SCENT ══════ -->
<section class="band band--paper">
  <div class="wrap scent">
    <div>
      <div class="eyebrow rv">The scent</div>
      <h2 class="rv d1" style="margin-top:1.8rem">香りに、背景を。</h2>
      <p class="lede rv d2" style="margin-top:1.3rem">
        どこの、誰が作った、何の香りか。<br>
        それを知っていることが、嗅いだときに戻ってくる。
      </p>
    </div>
    <dl class="scent__list">
      <div class="rv d1"><dt>素材</dt><dd>日本の伝統的な香木と、その産地のもの</dd></div>
      <div class="rv d2"><dt>強さ</dt><dd>人に気づかれない濃度。まとわりつかせない</dd></div>
      <div class="rv d3"><dt>選び方</dt><dd>その場では選ばない。持ち出す前に、一本だけ</dd></div>
      <div class="rv d4"><dt>ケース</dt><dd>ウォルナットと真鍮。使うほど、色が変わる</dd></div>
    </dl>
  </div>
</section>

<!-- ══════ Ⅺ. CLOSE ══════ -->
<section class="close">
  <div class="close__bg"><img src="%%CLOSE%%" alt="夕方の街を歩く"></div>
  <div class="close__in">
    <div class="eyebrow rv">Otium</div>
    <h2 class="rv d1" style="margin-top:2rem"><span class="lat">Otium</span> を持てない人が、<br>持てるようになる。</h2>
    <p class="lede rv d3" style="margin-top:2.4rem;max-width:32rem">
      休息は、生産性の対極ではなく、その源にある。<br>
      そう思えて初めて、人はその時間を自分に許せる。
    </p>
    <div class="cta rv d4">
      <p class="cta__lead">いま、日本中の Otium を探して、書いています。</p>
      <a class="btn" href="https://note.com/kosei_mohri" target="_blank" rel="noopener noreferrer">記録を読む<span aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

<!-- ══════ Ⅻ. WRITING ══════ -->
<section class="band" id="writing">
  <div class="wrap writing">
    <div>
      <div class="eyebrow rv">Writing</div>
      <h2 class="rv d1" style="margin-top:1.8rem;color:#F6F2EA">記録を、note に。</h2>
      <p class="lede rv d2" style="margin-top:1.3rem">
        休むことに名前がなかった国で、<br>
        それでも離れられている人は、何をしているのか。
      </p>
      <a class="btn rv d3 writing__all" href="https://note.com/kosei_mohri"
         target="_blank" rel="noopener noreferrer">
        note ですべて読む<span aria-hidden="true">→</span></a>
    </div>

    <div class="notes rv d2">
      <a class="note-item" href="https://note.com/kosei_mohri/n/n05efaf5c9aee"
         target="_blank" rel="noopener noreferrer">
        <div class="note-item__meta">2026.08.23 <i>note</i></div>
        <h3>「休んだのに疲れが取れない」のはなぜか<br>─ 二千年前の哲学者も同じ悩みを抱えていた</h3>
        <p>日曜、ちゃんと休んだはずだった。予定は入れなかった。それなりに寝た。
        なのに月曜の朝、何も回復していない。──　これが「休みが足りない」問題ではないとしたら。</p>
        <div class="note-item__go">読む<span aria-hidden="true">→</span></div>
      </a>
    </div>
  </div>
</section>

<footer>
  <div class="foot">
    <div class="foot__mark">OTIUM</div>
    <small>毛利 康聖 ／ Kosei Mohri　·　<a href="https://note.com/kosei_mohri" target="_blank" rel="noopener noreferrer" style="color:var(--smoke-lt);text-decoration:none;border-bottom:1px solid rgba(201,162,94,.45);padding-bottom:.12rem">note</a><br>
      本ページはコンセプト検討用のイメージです。掲載写真はすべてイメージです。</small>
  </div>
</footer>

<script>
(function(){
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    });
  },{threshold:.14, rootMargin:'0px 0px -6% 0px'});
  document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });

  var st = document.getElementById('strike');
  if(st){
    var io2 = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ st.classList.add('in'); io2.unobserve(st); }});
    },{threshold:.6});
    io2.observe(st);
  }
})();
</script>
</body>
</html>
"""

# ── 3. スタイル：現行の <style> をそのまま流用し、v2 分を足す ──────
style = src[src.index("<style>"): src.index("</style>")]
# 定義文の下線（--brass）を word__def 用に追加
style += """
.word__def u{text-decoration:none;background-image:linear-gradient(var(--brass-lt),var(--brass-lt));
  background-repeat:no-repeat;background-position:0 100%;background-size:0 1px;
  padding-bottom:.18em;transition:background-size 1.3s cubic-bezier(.65,0,.35,1) .5s}
.rv.in .word__def u,.word__def.in u{background-size:100% 1px}
.word__def.rv.in u{background-size:100% 1px}
@media (prefers-reduced-motion:reduce){.word__def u{background-size:100% 1px;transition:none}}
""" + CSS_ADD + "</style>"

out = (HTML
  .replace("%%STYLE%%", style)
  .replace("%%P1_HERO%%", P(1, "デスクで手が止まっている"))
  .replace("%%P1%%",  P(1, "デスク。手が止まっている"))
  .replace("%%P2%%",  P(2, "廊下。まだ開けていない"))
  .replace("%%P3%%",  P(3, "非常階段。嗅いでいる"))
  .replace("%%P4%%",  P(4, "屋上。街を見ている"))
  .replace("%%P5%%",  P(5, "会議室の扉に手をかける"))
  .replace("%%P6%%",  P(6, "デスク。手が動いている"))
  .replace("%%CASE%%",   keep("ウォルナットと真鍮のケース"))
  .replace("%%CARRY1%%", keep("ベルトループに掛ける"))
  .replace("%%CARRY2%%", keep("首から下げる"))
  .replace("%%CARRY3%%", keep("鞄に掛ける"))
  .replace("%%CLOSE%%",  keep("夕方の街を歩く"))
)

os.makedirs(os.path.dirname(DST), exist_ok=True)
io.open(DST, "w", encoding="utf-8").write(out)
print("wrote", DST, os.path.getsize(DST)//1024, "KB")
print("未配置の写真:", MISSING if MISSING else "なし（6枚すべて埋め込み済み）")
