# -*- coding: utf-8 -*-
"""otium/index.html（旧版）を基準にした更新スクリプト。
  ・PAIN（Why we made it／休んでも、戻らない。）を
    WHY IT WORKS ＋ THE DAY に差し替え
  ・THE OBJECT の直後に「一日に、二度。」を追加
再実行できるよう、index.src.html（初回実行時に作られる原本）から毎回組み直す。
    python3 /Users/kou12/otium/build.py
"""
import os, io, base64, shutil

BASE = "/Users/kou12/otium"
SRC  = os.path.join(BASE, "index.src.html")
DST  = os.path.join(BASE, "index.html")
PH   = os.path.join(BASE, "photos")

if not os.path.exists(SRC):                 # 初回だけ原本を退避
    shutil.copy2(DST, SRC)

def b64(name):
    with open(os.path.join(PH, name), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

s = io.open(SRC, encoding="utf-8").read()

# ─────────────────────────────────────────────────────────
# 1. 追加する CSS（既存の変数・書体・アニメ規則のみを使う）
# ─────────────────────────────────────────────────────────
CSS_ADD = """
/* ══ WHY IT WORKS ══ */
.why{max-width:64rem;margin:0 auto}
.why__list{margin-top:clamp(2.4rem,5vh,3.4rem)}
.why__row{display:grid;grid-template-columns:2.2rem minmax(0,15rem) minmax(0,1fr);
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

/* ══ PAIR ══ */
.pair{margin-top:clamp(5rem,12vh,9rem)}
.pair__grid{display:grid;grid-template-columns:minmax(0,1fr) 1px minmax(0,1fr);
  gap:clamp(1.3rem,3.2vw,3rem);align-items:start}
.pair__hair{align-self:stretch;background:linear-gradient(180deg,
  transparent 0%,rgba(168,130,60,.55) 18%,rgba(168,130,60,.55) 82%,transparent 100%)}
.pair__side figure{aspect-ratio:16/9;overflow:hidden;background:#1c1613}
.pair__side figcaption{margin-top:1.2rem;font-size:.83rem;color:var(--smoke);letter-spacing:.1em}
.pair__side em{font-style:normal;font-family:var(--serif);color:var(--brass-lt);
  letter-spacing:.2em;margin-right:.85rem}
.pair__say{margin:clamp(3.6rem,9vh,7rem) auto 0;text-align:center}
.pair__say h2{font-size:clamp(1.62rem,4.4vw,3.35rem);line-height:1.62;color:#F6F2EA}
.pair__say small{display:block;font-size:.8rem;letter-spacing:.13em;
  color:var(--smoke);margin-top:clamp(1.8rem,4vh,2.6rem);line-height:2.1}

/* ══ TWICE A DAY ══ */
.tw{position:relative;display:grid;
  grid-template-columns:minmax(0,1fr) clamp(2rem,5vw,4rem) minmax(0,1fr);
  grid-template-rows:auto auto auto auto;
  row-gap:clamp(2rem,5vh,3.2rem);
  margin-top:clamp(2.8rem,6vh,4rem)}
.tw__bg{grid-column:3;grid-row:1/-1;background:var(--ink-2);
  margin:-1.6rem -1.4rem;z-index:0}
.tw__r1{grid-row:2}.tw__r2{grid-row:3}.tw__r3{grid-row:4}
.tw__head{position:relative;z-index:1;font-size:.82rem;letter-spacing:.34em;
  padding-bottom:.85rem;border-bottom:1px solid rgba(255,255,255,.1)}
.tw__head--day{grid-column:1;grid-row:1;color:var(--smoke)}
.tw__head--night{grid-column:3;grid-row:1;color:var(--brass)}
.tw__cell{position:relative;z-index:1}
.tw__cell--day{grid-column:1}
.tw__cell--night{grid-column:3}
.tw__cell--split{margin-top:clamp(.6rem,1.6vh,1.3rem)}
.tw__cell figure{aspect-ratio:16/9;overflow:hidden;background:#1c1613}
.tw__cap{margin-top:1.05rem;display:grid;grid-template-columns:2rem minmax(0,1fr);
  gap:.85rem;align-items:baseline}
.tw__n{font-family:var(--serif);font-weight:300;font-size:.92rem;letter-spacing:.16em;line-height:1}
.tw__cell--day .tw__n{color:var(--smoke)}
.tw__cell--night .tw__n{color:var(--brass)}
.tw__cap h3{font-size:.97rem;font-weight:500;line-height:1.8}
.tw__cell--day .tw__cap h3{color:#E6DED2}
.tw__cell--night .tw__cap h3{color:#F6F2EA}
.tw__cap p{font-size:.79rem;color:var(--smoke);margin-top:.28rem;line-height:1.95}

/* 真鍮のヘアライン：Ⅰ|Ⅳ を横に渡し、Ⅱ|Ⅴ から縦に分かれる */
.tw__join,.tw__drop{grid-column:2;z-index:1;background:var(--brass-lt);opacity:.72}
.tw__join{grid-row:2;align-self:center;width:100%;height:1px;
  transform:scaleX(0);transform-origin:center;
  transition:transform 1.3s cubic-bezier(.65,0,.35,1) .25s}
.tw__drop{grid-row:3/-1;justify-self:center;align-self:stretch;width:1px;
  transform:scaleY(0);transform-origin:top;
  transition:transform 1.2s cubic-bezier(.65,0,.35,1) 1.1s}
.tw__join.in{transform:scaleX(1)}
.tw__drop.in{transform:scaleY(1)}
@media (prefers-reduced-motion:reduce){
  .tw__join{transform:scaleX(1);transition:none}
  .tw__drop{transform:scaleY(1);transition:none}}
.tw__end{margin-top:clamp(2.6rem,6vh,4rem);text-align:center}
.tw__end p{font-size:clamp(.98rem,1.5vw,1.18rem);line-height:2.2;color:#E6DED2}
.tw__end b{font-weight:600;color:#F6F2EA}

/* ══ v1 追加分 responsive ══ */
@media (max-width:900px){
  .why__row{grid-template-columns:2rem minmax(0,1fr);row-gap:.4rem}
  .why__row p{grid-column:2}
  .pair__grid{grid-template-columns:1fr;gap:2.4rem}
  .pair__hair{height:1px;width:100%;background:linear-gradient(90deg,
    transparent,rgba(168,130,60,.55) 18%,rgba(168,130,60,.55) 82%,transparent)}
  .cut figure{aspect-ratio:4/3}
  .tw{grid-template-columns:1fr;grid-template-rows:none;row-gap:2.2rem}
  .tw__bg,.tw__join,.tw__drop{display:none}
  .tw__head,.tw__cell{grid-column:1;grid-row:auto}
  .tw__head--day{order:1}
  .tw__cell--day.tw__r1{order:2}
  .tw__cell--day.tw__r2{order:3}
  .tw__cell--day.tw__r3{order:4}
  .tw__head--night{order:5;margin-top:clamp(1.6rem,4vh,2.6rem)}
  .tw__cell--night.tw__r1{order:6}
  .tw__cell--night.tw__r2{order:7}
  .tw__cell--night.tw__r3{order:8}
  .tw__cell--split{margin-top:0}
}
"""

# ─────────────────────────────────────────────────────────
# 2. PAIN セクションを WHY IT WORKS ＋ THE DAY に差し替え
# ─────────────────────────────────────────────────────────
NEW_MIDDLE = u"""<!-- ══════ WHY IT WORKS ══════ -->
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

<!-- ══════ THE DAY ══════ -->
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="eyebrow rv">The day</div>
    <h2 class="rv d1" style="margin-top:1.8rem;color:#F6F2EA">ある平日の、四つの場面。</h2>

    <div class="day">
      <div class="cut rv"><figure><img src="%%P2%%" alt="会議室の手前の廊下。ケースを持っているが、まだ使っていない" loading="lazy"></figure>
        <div class="cut__cap"><div class="cut__n">Ⅱ</div>
          <div><h3>会議の前</h3><p>まだ、開けていない</p></div></div></div>

      <div class="cut rv"><figure><img src="%%P3%%" alt="非常階段の踊り場。嗅いでいる" loading="lazy"></figure>
        <div class="cut__cap"><div class="cut__n">Ⅲ</div>
          <div><h3>扉が閉まる</h3><p>閉めた側に、誰もいない</p></div></div></div>

      <div class="cut rv"><figure><img src="%%P4%%" alt="屋上。街を見ている" loading="lazy"></figure>
        <div class="cut__cap"><div class="cut__n">Ⅳ</div>
          <div><h3>屋上</h3><p>街のほうが、動いている</p></div></div></div>

      <div class="cut rv"><figure><img src="%%P5%%" alt="会議室の扉に手をかけている。ケースは閉じている" loading="lazy"></figure>
        <div class="cut__cap"><div class="cut__n">Ⅴ</div>
          <div><h3>戻る</h3><p>ケースは、閉じている</p></div></div></div>
    </div>

    <div class="pair">
      <div class="pair__grid">
        <div class="pair__side rv">
          <figure><img src="%%P1%%" alt="デスク。手が止まっている" loading="lazy"></figure>
          <figcaption><em>Before</em>手が止まっている</figcaption>
        </div>
        <div class="pair__hair rv d2"></div>
        <div class="pair__side rv d3">
          <figure><img src="%%P6%%" alt="デスク。手が動いている" loading="lazy"></figure>
          <figcaption><em>After</em>手が動いている</figcaption>
        </div>
      </div>

      <div class="pair__say rv d4">
        <h2>離れないと、<br>自分の判断が見えない。</h2>
        <small>同じ机、同じ光、同じ服。<br>違うのは、手だけ。</small>
      </div>
    </div>
  </div>
</section>

"""

start = s.index("<!-- ══════ PAIN ══════ -->")
end   = s.index("<!-- ══════ THE OBJECT ══════ -->")
s = s[:start] + NEW_MIDDLE + s[end:]

# ─────────────────────────────────────────────────────────
# 3. THE OBJECT の直後に「一日に、二度。」を挿入
# ─────────────────────────────────────────────────────────
TWICE = u"""<!-- ══════ TWICE A DAY ══════ -->
<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="eyebrow rv">Twice a day</div>
    <h2 class="rv d1" style="margin-top:1.8rem;color:#F6F2EA">一日に、二度。</h2>
    <p class="lede rv d2" style="margin-top:1.3rem">
      朝、一本挿して持ち出す。<br>
      同じ道具を、昼と夜に開ける。
    </p>

    <div class="tw">
      <div class="tw__bg" aria-hidden="true"></div>

      <div class="tw__head tw__head--day rv">昼</div>
      <div class="tw__head tw__head--night rv d1">夜</div>

      <div class="tw__join rv" aria-hidden="true"></div>
      <div class="tw__drop rv" aria-hidden="true"></div>

      <div class="tw__cell tw__cell--day tw__r1 rv">
        <figure><img src="%%N1%%" alt="非常階段。両手でキャップを引き抜くと、お香がついてくる" loading="lazy"></figure>
        <div class="tw__cap"><span class="tw__n">Ⅰ</span>
          <div><h3>開ける</h3><p>キャップを引き抜く。お香がついてくる</p></div></div>
      </div>
      <div class="tw__cell tw__cell--night tw__r1 rv d1">
        <figure><img src="%%N4%%" alt="夜の机。キャップを引き抜く" loading="lazy"></figure>
        <div class="tw__cap"><span class="tw__n">Ⅳ</span>
          <div><h3>開ける</h3><p>昼と、まったく同じ動作</p></div></div>
      </div>

      <div class="tw__cell tw__cell--day tw__cell--split tw__r2 rv">
        <figure><img src="%%N2%%" alt="非常階段。キャップごと鼻先へ運んでいる" loading="lazy"></figure>
        <div class="tw__cap"><span class="tw__n">Ⅱ</span>
          <div><h3>嗅ぐ</h3><p>火はつけない。ひと息だけ</p></div></div>
      </div>
      <div class="tw__cell tw__cell--night tw__cell--split tw__r2 rv d1">
        <figure><img src="%%N5%%" alt="夜の机。キャップを置いて、お香を立てる" loading="lazy"></figure>
        <div class="tw__cap"><span class="tw__n">Ⅴ</span>
          <div><h3>立てる</h3><p>キャップを置けば、香立てになる</p></div></div>
      </div>

      <div class="tw__cell tw__cell--day tw__r3 rv">
        <figure><img src="%%N3%%" alt="非常階段。キャップを本体に締め戻している" loading="lazy"></figure>
        <div class="tw__cap"><span class="tw__n">Ⅲ</span>
          <div><h3>閉じる</h3><p>戻して、締める。自分で終わらせる</p></div></div>
      </div>
      <div class="tw__cell tw__cell--night tw__r3 rv d1">
        <figure><img src="%%N6%%" alt="夜の机。火がつき、煙が上がっている" loading="lazy"></figure>
        <div class="tw__cap"><span class="tw__n">Ⅵ</span>
          <div><h3>焚く</h3><p>火をつけて、手を引く</p></div></div>
      </div>
    </div>

    <div class="tw__end rv">
      <p><b>同じ動作から始まって、行き先が分かれる。</b><br>
      昼は、自分で閉じる。夜は、火が終わらせる。</p>
    </div>
  </div>
</section>

"""

anchor = "<!-- ══════ SCENES ══════ -->"
s = s.replace(anchor, TWICE + anchor, 1)

# ─────────────────────────────────────────────────────────
# 4. CSS を FOOT の直前に足す
# ─────────────────────────────────────────────────────────
css_anchor = "/* ══ FOOT ══ */"
assert s.count(css_anchor) == 1, "CSS anchor not found"
s = s.replace(css_anchor, CSS_ADD + "\n" + css_anchor, 1)

# ─────────────────────────────────────────────────────────
# 5. 画像を base64 で埋め込む
# ─────────────────────────────────────────────────────────
for k, f in [("P1","p1.jpg"),("P2","p2.jpg"),("P3","p3.jpg"),
             ("P4","p4.jpg"),("P5","p5.jpg"),("P6","p6.jpg"),
             ("N1","n1.jpg"),("N2","n2.jpg"),("N3","n3.jpg"),
             ("N4","n4.jpg"),("N5","n5.jpg"),("N6","n6.jpg")]:
    s = s.replace("%%" + k + "%%", b64(f))

io.open(DST, "w", encoding="utf-8").write(s)
print("wrote", DST, os.path.getsize(DST)//1024, "KB")
