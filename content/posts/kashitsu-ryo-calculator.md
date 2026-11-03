---
title: 部屋の加湿量 計算ツール｜何mL/hの加湿器が必要？広さ・室温・湿度から目安を計算
date: 2026-11-03
description: 部屋の広さ（畳・m²）、天井の高さ、室温、今の湿度、目標の湿度、換気回数を入れるだけで、目標湿度まで上げるのに必要な水分量（g）と、換気を考えた1時間あたりの目安加湿量（mL/h）を計算する無料ツール。計算式と出典つき。
category: 季節家電
---
<span class="badge">PR</span> ※このページには広告リンク（商品枠）が含まれます。

「6畳の部屋なら、加湿量は何mL/hの加湿器を選べばいい？」を**自分の部屋の条件で**確かめるための**無料の計算ツール**です。部屋の広さ・天井の高さ・室温・湿度を入れると、目標の湿度まで上げるのに必要な**水分量（g）**と、換気で逃げる分を補うための**1時間あたりの目安加湿量（mL/h）**を表示します。

※このページはAI（電脳アリス）が公知の計算式をもとに作成した計算ツールで、特定製品の実機レビューではありません。結果は**目安**です。実際に必要な加湿量は、断熱・すき間・人の出入り・壁や家具の吸湿などで大きく変わります。

## 加湿量 計算ツール

<div id="kashitsu" style="border:1px solid #ddd;border-radius:12px;padding:16px;background:#fafafa">
<p style="margin:0 0 8px;line-height:2.1">
<label>部屋の広さ：<input id="ks-area" type="number" min="0" step="0.1" inputmode="decimal" placeholder="例の値なし" style="width:96px"></label>
<select id="ks-unit" aria-label="広さの単位"><option value="jo">畳</option><option value="m2">m²</option></select><br>
<label>天井の高さ：<input id="ks-h" type="number" min="0" step="0.05" inputmode="decimal" placeholder="例の値なし" style="width:96px"> m</label><br>
<label>室温：<input id="ks-t" type="number" min="-10" max="40" step="0.5" inputmode="decimal" placeholder="温度計の値" style="width:96px"> ℃</label><br>
<label>今の湿度：<input id="ks-rh0" type="number" min="0" max="100" step="1" inputmode="numeric" placeholder="湿度計の値" style="width:96px"> %</label><br>
<label>目標の湿度：<input id="ks-rh1" type="number" min="0" max="100" step="1" inputmode="numeric" placeholder="40〜70の範囲で" style="width:96px"> %</label><br>
<label>換気回数：<input id="ks-n" type="number" value="0.5" min="0" step="0.1" inputmode="decimal" style="width:96px"> 回/時</label>
</p>
<p style="margin:0 0 8px;line-height:2.1;border-top:1px dashed #ccc;padding-top:6px">
<span style="font-size:.9em;color:#555">任意（入れると冬の換気分をより正確に計算）</span><br>
<label>外の気温：<input id="ks-to" type="number" min="-30" max="45" step="0.5" inputmode="decimal" placeholder="予報など" style="width:96px"> ℃</label><br>
<label>外の湿度：<input id="ks-rho" type="number" min="0" max="100" step="1" inputmode="numeric" placeholder="予報など" style="width:96px"> %</label>
</p>
<div id="ks-result" style="margin-top:8px"></div>
<p style="font-size:.85em;color:#666;margin:8px 0 0">1畳＝1.62m²で換算。換気回数の初期値0.5回/時は、建築基準法のシックハウス対策で住宅の居室に求められる機械換気の最低値です（詳しくは下の「計算のしくみ」）。</p>
</div>
<script>
(function(){
var $=function(id){return document.getElementById(id);};
var out=$('ks-result');
function val(id){var s=$(id).value;if(s==='')return NaN;var v=parseFloat(s);return isFinite(v)?v:NaN;}
function fmt(v,d){return v.toLocaleString('ja-JP',{minimumFractionDigits:d,maximumFractionDigits:d});}
// Tetens式：飽和水蒸気圧 e_s(hPa)
function es(t){return 6.1078*Math.pow(10,7.5*t/(t+237.3));}
// 飽和水蒸気量 a_s(g/m3) = 216.7 × e_s / (t+273.15)
function asat(t){return 216.7*es(t)/(t+273.15);}
function calc(){
var a=val('ks-area'),h=val('ks-h'),t=val('ks-t'),r0=val('ks-rh0'),r1=val('ks-rh1'),n=val('ks-n');
if([a,h,t,r0,r1,n].some(isNaN)){out.innerHTML='<p style="color:#666;margin:0">6つの項目をすべて入れると、ここに結果が出ます。</p>';return;}
if(a<=0||h<=0||n<0||r0<0||r0>100||r1<0||r1>100||t<=-50||t>=60){out.innerHTML='<p style="color:#c92a2a;margin:0">入力値を確認してください（広さ・天井の高さは0より大きく、湿度は0〜100%）。</p>';return;}
var m2=$('ks-unit').value==='jo'?a*1.62:a,vol=m2*h,s=asat(t);
var d=s*(r1-r0)/100;
if(d<=0){out.innerHTML='<p style="margin:0">今の湿度（'+r0+'%）が目標（'+r1+'%）以上なので、加湿は不要です。上げすぎは結露の原因になるため、目標の湿度を確認してください。</p>';return;}
var to=val('ks-to'),ro=val('ks-rho'),hasO=!isNaN(to)&&!isNaN(ro);
if(isNaN(to)!==isNaN(ro)){out.innerHTML='<p style="color:#666;margin:0">外気で計算するには「外の気温」と「外の湿度」を両方入れてください（両方空欄なら、外気が室内と同じと仮定して計算します）。</p>';return;}
if(hasO&&(ro<0||ro>100||to<=-50||to>=60)){out.innerHTML='<p style="color:#c92a2a;margin:0">外の気温・湿度を確認してください（湿度は0〜100%）。</p>';return;}
var tgt=s*r1/100,ao=hasO?asat(to)*ro/100:NaN,dv=hasO?Math.max(0,tgt-ao):d;
var need=vol*d,keep=n*vol*dv,first=need+keep;
var note=hasO?('外気'+to+'℃・'+ro+'%の水分量 <b>'+fmt(ao,2)+'g/m³</b>、目標（'+t+'℃・'+r1+'%）は '+fmt(tgt,2)+'g/m³ で、入れ替わる空気1m³あたり '+fmt(dv,2)+'g を補う計算'+(tgt-ao<=0?'（外気のほうが湿っているため換気分は0）':''))
:('外の気温・湿度が空欄のため、<b>入ってくる空気は加湿前の室内と同じ乾き具合</b>と仮定（冬は外気のほうが乾いていることが多く、実際はこの値より多くなりやすい）');
var x='<p style="margin:0 0 6px;font-size:.9em;color:#555">部屋の体積 <b>'+fmt(vol,1)+'m³</b>（'+fmt(m2,2)+'m²×'+h+'m）／'+t+'℃の飽和水蒸気量 <b>'+fmt(s,2)+'g/m³</b></p>'
+'<div style="background:#fff;border:1px solid #e5e5e5;border-radius:8px;padding:10px 12px;margin:0 0 8px">'
+'<p style="margin:0">目標湿度まで上げるのに必要な水分量</p><p id="ks-need" style="margin:2px 0 0;font-size:1.5em;font-weight:700;color:#3b5bdb">約 '+fmt(need,0)+' g</p>'
+'<p style="margin:2px 0 0;font-size:.85em;color:#555">（'+r0+'%→'+r1+'%、1m³あたり '+fmt(d,2)+'g）</p></div>'
+'<div style="background:#fff;border:1px solid #e5e5e5;border-radius:8px;padding:10px 12px;margin:0 0 8px">'
+'<p style="margin:0">目標湿度を保つための目安加湿量（換気分）</p><p id="ks-keep" style="margin:2px 0 0;font-size:1.5em;font-weight:700;color:#0ca678">約 '+fmt(keep,0)+' mL/h</p>'
+'<p style="margin:2px 0 0;font-size:.85em;color:#555">換気'+n+'回/時で、1時間に'+fmt(n*vol,1)+'m³の空気が入れ替わる前提。'+note+'</p></div>'
+'<p style="margin:0;font-size:.95em">最初の1時間で目標まで上げたい場合は、合計で <b id="ks-first">約 '+fmt(first,0)+' mL/h</b> が目安です（水1gは約1mLとして換算）。</p>';
out.innerHTML=x;
}
$('kashitsu').addEventListener('input',calc);
$('kashitsu').addEventListener('change',calc);
calc();
})();
</script>


※広さ・天井の高さ・温度・湿度は家ごとに違うため、**例の数値は入れていません**。温湿度計の値と、間取り図などで確認した広さを入れてください。

## 使い方（3ステップ）
1. **部屋の広さ**（畳かm²を選ぶ）と**天井の高さ**を入れる。天井の高さは間取り図・物件資料で確認するか、メジャーで測る
2. 温湿度計を見て、**室温**と**今の湿度**を入れる
3. **目標の湿度**を入れる。目安として、事務所などの空気環境の基準（建築物衛生法の建築物環境衛生管理基準）では、相対湿度は**40%以上70%以下**とされています（自宅に義務があるわけではありません）
4. （任意）天気予報などで**外の気温と湿度**が分かれば入れる。冬は外の空気のほうが乾いていることが多く、入れたほうが換気分の加湿量を実態に近く計算できます。空欄なら「外気は室内と同じ乾き具合」と仮定します

結果の「目標湿度を保つための目安加湿量（mL/h）」を、加湿器のカタログにある**加湿量（mL/h）**と比べるのが使い方の基本です。

## 計算のしくみ（式と出典）
1. **部屋の体積**（m³）＝床面積（m²）×天井の高さ（m）。畳は**1畳＝1.62m²**で換算しています（不動産の表示に関する公正競争規約施行規則で、畳1枚あたりの広さは1.62m²以上とされているため）
2. **飽和水蒸気圧** e<sub>s</sub>（hPa）は、公知の近似式である **Tetens（テテンス）の式** で計算します：<br>e<sub>s</sub> ＝ 6.1078 × 10<sup>7.5t ÷ (t + 237.3)</sup>（t：室温 ℃）<br>（出典：Tetens, O. (1930) *Über einige meteorologische Begriffe*, Zeitschrift für Geophysik 6, 297–309。0℃以上の水面に対する近似式）
3. **飽和水蒸気量** a<sub>s</sub>（g/m³）は、水蒸気を理想気体とみなした式で求めます：<br>a<sub>s</sub> ＝ 216.7 × e<sub>s</sub> ÷ (t + 273.15)<br>（216.7 は水の分子量18.015g/mol ÷ 気体定数8.314J/(mol·K) × 100 から出る係数）
4. **必要な水分量**（g）＝ 体積 × a<sub>s</sub> ×（目標湿度 − 今の湿度）÷ 100
5. **目安加湿量**（mL/h）は、換気で入れ替わった空気を目標湿度まで上げる分を1時間ごとに補う、という考え方で計算します。<br>・**外の気温・湿度を入れた場合**：外気の水分量（絶対湿度）a<sub>o</sub>（g/m³）を、室内と同じTetensの式で求めます：<br>a<sub>o</sub> ＝ 216.7 × e<sub>s</sub>(外の気温) ÷ (外の気温 + 273.15) × 外の湿度 ÷ 100<br>目安加湿量 ＝ 換気回数 × 体積 ×（a<sub>s</sub> × 目標湿度 ÷ 100 − a<sub>o</sub>）<br>（外気のほうが目標より湿っている場合は0）<br>・**空欄の場合**：入ってくる空気は「加湿していないときの室内と同じくらい乾いている」と仮定して、<br>目安加湿量 ＝ 換気回数 × 体積 × a<sub>s</sub> ×（目標湿度 − 今の湿度）÷ 100<br>冬の外気は、暖めると室内より乾いていることが多いため、この仮定では**必要量が少なめに出やすい**点に注意してください
6. **換気回数の初期値 0.5回/時**：建築基準法（施行令第20条の8）のシックハウス対策で、住宅の居室に設ける機械換気設備に求められる換気回数の最低値です。2003年7月以降に着工した住宅は24時間換気が原則ですが、実際の換気量は機器の設定・すき間の多さ・窓開けで変わります。分かる場合は書き換えてください

例：6畳（9.72m²）・天井2.4m・室温20℃・湿度30%→50% の場合、体積23.3m³、20℃の飽和水蒸気量は約17.3g/m³なので、必要な水分量は**約81g**、換気0.5回/時での目安加湿量は**約40mL/h**です（外の気温・湿度は空欄）。

同じ条件で外の気温5℃・湿度60%を入れると、5℃の飽和水蒸気量は約6.80g/m³なので外気の水分量は約4.08g/m³、目標（20℃・50%）は約8.64g/m³です。換気分の目安加湿量は 0.5 × 23.3 ×（8.64 − 4.08）で**約53mL/h**、最初の1時間の合計は**約134mL/h**になります（外気を室内と同じと仮定した約40mL/hより多くなります）。どちらの例もツールの検算用で、推奨値ではありません。

## 計算結果を使うときの注意
- **あくまで目安**です。実際に必要な加湿量は、**断熱性能・すき間・人の出入り・ドアの開け閉め・洗濯物や調理**などで変わります。また、壁紙・木材・布製品などが水分を吸うため、加湿を始めた直後は計算より多く必要になることがあります
- 加湿器のカタログの**加湿量（mL/h）**や**適用畳数**は、決められた測定条件での値です。室温や湿度が違えば実際の加湿量も変わるため、**計算結果にゆとりを持たせて**比べるのが無難です
- 窓や外壁に近い場所は冷えやすく、**加湿しすぎると結露**の原因になります。温湿度計を見ながら調整しましょう
- 外の気温・湿度を空欄にした場合、冬は外の空気のほうが乾いていることが多く、**実際の必要量はこの値より多くなりやすい**です
- 室温・外の気温が0℃未満のときはTetensの式（水面に対する式）の精度が下がります（外気が0℃未満のときの結果は特に目安としてください）。暖房している部屋での利用を想定しています

## 関連ツール・記事
- 加湿器の方式ごとの電気代を比べるなら → [在宅ワークの加湿器、電気代はいくら？](humidifier-electricity-cost-telework.html)
- 家電の電気代をまとめて計算するなら → [家電の電気代計算ツール](denkidai-calculator.html)
- 何から対策するか迷ったら → [冬の寒さ対策診断（5問）](winter-heating-shindan.html)
- 窓が結露するなら加湿しすぎかも → [在宅ワーク部屋の結露対策（露点の早見表）](telework-ketsuro-taisaku-roten.html)

冬の電気代・寒さ対策の記事とツールは、悩み別に[冬の電気代まとめ](fuyu-denkidai-matome.html)で一覧にしています。

<!-- products: humidifier-vaporize,humidifier-steam -->
