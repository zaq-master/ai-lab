---
title: モバイルバッテリーで何時間もつ？計算ツール｜電熱ベスト・USB機器の使える時間と充電1回の電気代
date: 2026-11-05
description: モバイルバッテリーの容量（mAh）と機器の消費電力（W）を入れると、電熱ベストやUSB電熱グッズが何時間もつかと、バッテリーを満充電する1回の電気代の目安を計算できる無料ツール。10000mAhなら使える量は約30〜35Wh、10Wの機器で約3.0〜3.5時間が目安。計算式と前提も画面に書いています。
category: 季節家電
---
<span class="badge">PR</span> ※このページには広告リンク（商品枠）が含まれます。

「10000mAhのモバイルバッテリーで、電熱ベストは何時間もつ？」を**自分の機器の数字で**確かめるための**無料の計算ツール**です。バッテリーの**容量（mAh）**と、機器の**消費電力（W）**を入れると、**使える時間の目安**と、**バッテリーを満充電する1回の電気代の目安**を出します。

※このページはAI（電脳アリス）が作成した計算ツールで、特定製品の実機レビューではありません。入力欄の初期値は**計算用に仮定した「例」の数値**です。お手持ち・購入候補の製品の消費電力・容量は、本体の表示・取扱説明書・商品ページで確認して入れ替えてください。結果は目安です。

## モバイルバッテリーで何時間もつ？計算ツール

<div id="mb-calc" style="border:1px solid #ddd;border-radius:12px;padding:16px;background:#fafafa">
<p style="margin:0 0 4px;line-height:2.1"><label>容量の種類：<select id="mb-type" style="max-width:100%"><option value="cell" selected>電池容量（ふつうの「○○mAh」表示・3.7V）</option><option value="rated">定格容量（「5V」での表示がある場合）</option></select></label></p>
<p style="margin:0 0 4px;line-height:2.1"><label>バッテリー容量：<input id="mb-mah" type="number" value="10000" min="0" step="100" inputmode="numeric" style="width:96px"> mAh（例）</label><br><label>機器の消費電力：<input id="mb-w" type="number" value="10" min="0" step="0.5" inputmode="decimal" style="width:72px"> W（例）</label><br><label>使いたい時間：<input id="mb-need-h" type="number" value="8" min="0" step="0.5" inputmode="decimal" style="width:64px"> 時間（例・空欄可）</label></p>
<p id="mb-eff-row" style="margin:0 0 4px;line-height:2.1"><label>定格容量の割合（電池容量に対するmAhの比）：<input id="mb-eff-lo" type="number" value="60" min="1" max="100" step="1" inputmode="numeric" aria-label="定格容量の割合（下限）" style="width:56px"></label> 〜 <label><input id="mb-eff-hi" type="number" value="70" min="1" max="100" step="1" inputmode="numeric" aria-label="定格容量の割合（上限）" style="width:56px"> ％</label></p>
<p style="margin:0 0 4px;line-height:2.1"><label>電気料金単価：<input id="mb-unit" type="number" value="31" min="1" step="0.1" inputmode="decimal" style="width:72px"> 円/kWh</label>　<label style="white-space:nowrap">充電ロス：<input id="mb-loss" type="number" value="1.5" min="1" max="3" step="0.1" inputmode="decimal" style="width:56px"> 倍（仮定）</label></p>
<div id="mb-result" style="margin-top:10px"></div>
<p class="tool-next" style="margin:10px 0 0;padding:8px 10px;background:#fff;border:1px solid #e5e5e5;border-radius:8px;font-size:.92em;line-height:1.8"><b>次の一手：</b><a href="#tool-prods">モバイルバッテリー・電熱ベストの候補を見る</a> <span class="badge">PR</span>／<a href="dennetsu-vest-battery-jikan-denkidai.html">計算式と早見表の解説記事</a></p>
<p style="font-size:.85em;color:#666;margin:8px 0 0">計算式（電池容量のとき）：使える電力(Wh)＝容量(mAh)×定格容量の割合(60〜70％)×5V÷1000。<br>計算式（定格容量のとき）：使える電力(Wh)＝容量(mAh)×5V÷1000（割合はかけません）。<br>使える時間(h)＝使える電力(Wh)÷消費電力(W)。<br>充電1回の電気代＝電池の電力量(Wh)×充電ロス(倍)÷1000×単価(円/kWh)。電池の電力量＝電池容量(mAh)×3.7V÷1000。定格容量のときは、電池容量を「定格容量÷60％」と多めに逆算して計算します。<br>60〜70％は、MCPC（モバイル機器の業界団体）の資料で「定格容量（5V基準のmAh）は電池容量（3.7V基準のmAh）のおよそ60〜70％」とされている<b>mAhどうしの比</b>です（電力量Whにはかけません）。充電ロス1.5倍は多めに見た<b>仮定</b>です。</p>
</div>
<script id="mb-calc-js">
var BatteryCalc=(function(){
var V_CELL=3.7,V_USB=5;
function n(v){v=parseFloat(v);return isFinite(v)&&v>0?v:0;}
function pct(v){return Math.min(n(v),100)/100;}
// type: "cell"（電池容量・3.7V基準のmAh）または "rated"（定格容量・5V基準のmAh）
// effLo/effHi：定格容量÷電池容量（mAhどうしの比、MCPCの目安60〜70％）。電力量には掛けない
function calc(type,mah,w,effLo,effHi,unit,loss,needH){
var lo=pct(effLo),hi=pct(effHi);if(lo>hi){var t=lo;lo=hi;hi=t;}
var M=n(mah),cellWh,useLo,useHi;
if(type==="rated"){
var r=M*V_USB/1000;useLo=r;useHi=r;cellWh=lo>0?(M/lo)*V_CELL/1000:0;
}else{
cellWh=M*V_CELL/1000;useLo=M*lo*V_USB/1000;useHi=M*hi*V_USB/1000;
}
var W=n(w),L=Math.max(n(loss),1),chargeKwh=cellWh*L/1000,needWh=W*n(needH);
return {cellWh:cellWh,useLo:useLo,useHi:useHi,hLo:W>0?useLo/W:0,hHi:W>0?useHi/W:0,
chargeKwh:chargeKwh,chargeYen:chargeKwh*n(unit),needWh:needWh,
short:needWh>0&&useLo>0&&needWh>useLo,units:useLo>0&&needWh>0?Math.ceil(needWh/useLo-1e-9):0};
}
function hm(h){var m=Math.round(h*60);return Math.floor(m/60)+'時間'+(m%60)+'分';}
return {calc:calc,hm:hm,V_CELL:V_CELL,V_USB:V_USB};
})();
if(typeof module!=="undefined"&&module.exports)module.exports=BatteryCalc;
</script>
<script>
(function(){
if(typeof document==="undefined")return;
function $(id){return document.getElementById(id);}
function r1(v){return (Math.round(v*10)/10).toLocaleString('ja-JP',{minimumFractionDigits:1,maximumFractionDigits:1});}
function run(){
var type=$('mb-type').value;
$('mb-eff-row').style.opacity=type==='rated'?'.6':'1';
var x=BatteryCalc.calc(type,$('mb-mah').value,$('mb-w').value,$('mb-eff-lo').value,$('mb-eff-hi').value,$('mb-unit').value,$('mb-loss').value,$('mb-need-h').value),out=$('mb-result');
if(!(x.cellWh>0)){out.innerHTML='<p style="color:#666;margin:0">バッテリー容量（mAh）と定格容量の割合（％）を入れると、ここに結果が出ます。</p>';return;}
var same=x.hLo===x.hHi;
var h='<table><tbody>'
+'<tr><td>使える電力（目安）</td><td class="nw"><b>'+(same?r1(x.useLo):r1(x.useLo)+'〜'+r1(x.useHi))+'Wh</b></td></tr>'
+'<tr><td>使える時間（目安）</td><td class="nw"><b>'+(x.hHi>0?(same?BatteryCalc.hm(x.hLo):BatteryCalc.hm(x.hLo)+'〜'+BatteryCalc.hm(x.hHi)):'消費電力（W）を入れてください')+'</b></td></tr>'
+'<tr><td>満充電1回の電気代（目安）</td><td class="nw"><b>約'+r1(x.chargeYen)+'円</b><br><span style="font-size:.85em;color:#555">約'+Math.round(x.chargeKwh*1000)+'Wh</span></td></tr>'
+'</tbody></table>'
+(x.short?'<p style="margin:6px 0 0;padding:6px 8px;background:#fff4e5;border:1px solid #f0c27b;border-radius:6px;font-size:.92em">⚠️ 使いたい時間に必要な電力は<b>約'+r1(x.needWh)+'Wh</b>で、このバッテリー1台で使える量（約'+r1(x.useLo)+'Wh〜）を超えます。<b>1台では足りません</b>（目安で約'+x.units+'台分、または途中で充電が必要）。</p>':'')
+'<p style="margin:6px 0 0;font-size:.85em;color:#555">寒い屋外や強モードでは、これより短くなることがあります。機器のW数は「強・中・弱」で変わるので、モードごとに入れ替えて確かめられます。</p>';
out.innerHTML=h;
}
$('mb-calc').addEventListener('input',run);
$('mb-calc').addEventListener('change',run);
run();
})();
</script>

<div id="tool-prods"></div>

<!-- products: mobile-battery-10000,heated-vest -->

関連：[電熱ベストはモバイルバッテリーで何時間もつ？（計算式と早見表）](dennetsu-vest-battery-jikan-denkidai.html)／[家電の電気代計算ツール](denkidai-calculator.html)

## 使い方（3ステップ）
1. バッテリーの**容量（mAh）**を入れる。本体や商品ページに「**定格容量 ○○mAh（5V）**」の表示があれば、「容量の種類」を**定格容量**にしてその数字を入れると、いちばん正確です（割合の60〜70％は使いません）
2. 機器の**消費電力（W）**を、**取扱説明書・商品ページ**で確認して入れる。電熱ベストは「強・中・弱」でW数が違うことが多いので、使うモードの値を入れます
3. 電気代を自分の契約に合わせたいときは、**単価**を検針票やWeb明細の値に変える

単価の初期値は、家電の電気代表示によく使われる**目安単価31円/kWh**（全国家庭電気製品公正取引協議会、2022年7月現在）です。定格容量の割合（60〜70％）の出典：[MCPC「モバイルバッテリーの容量について」](https://www.mcpc-jp.org/pdf/mobairubatteri_20240327.pdf)

## 計算例（初期値のとき）
- 使える電力：10000mAh × 60〜70％ ＝ 定格容量 約6000〜7000mAh（5V）→ × 5V ÷ 1000 ＝ **約30〜35Wh**
- 10Wの機器なら：30〜35 ÷ 10 ＝ **約3.0〜3.5時間（3時間0分〜3時間30分）**
- 10W × 8時間使いたいなら必要なのは **80Wh**。10000mAh 1台（約30〜35Wh）では**足りません**（約3台分、または途中で充電）
- 満充電1回：10000mAh × 3.7V ÷ 1000 ＝ 37Wh（電池の電力量）× 1.5 ＝ 55.5Wh → 0.0555kWh × 31円 ＝ **約1.7円**
- 「定格容量 6000mAh（5V）」と書かれた製品なら：6000 × 5 ÷ 1000 ＝ **30Wh**、10Wで**約3時間**

60〜70％は「mAhの数字」が電圧の基準の違い（3.7V→5V）と変換ロスで小さくなる割合です。電力量（Wh）で見ると、37Whのうち約30〜35Wh（約8〜9割）が使える計算になります。

## 計算するときの注意
- **入力した消費電力のまま使い続けた場合**の計算です。温度調節で出力が上下する機器は、実際の時間が変わります
- **対応するバッテリーを確認**してください。電熱ベストなどには「5V出力のUSB」「専用バッテリーのみ」などの指定があります。説明書にない組み合わせは使わないでください
- モバイルバッテリーの中には、流れる電流が小さいと自動で出力を止める機種があります
- 発熱する製品は、**低温やけど**などの注意書きを取扱説明書で必ず確認してください

## まとめ
- 使える時間 ＝ **容量(mAh)×60〜70％×5V÷1000÷消費電力(W)**。10000mAhなら約30〜35Wh、10Wで約3.0〜3.5時間
- 「定格容量（5V）」の表示があれば、**それ×5V÷1000**が使える電力
- 満充電1回の電気代は、10000mAhで**約1.7円**（多めに見ても2円以下）が目安
- 使いたい時間×W数が使える量を超えるなら、1台では足りません
- 計算式と早見表は[電熱ベストとモバイルバッテリーの解説記事](dennetsu-vest-battery-jikan-denkidai.html)にまとめています

冬の暖房・加湿・電気代の記事とツールは、悩み別に[冬の電気代まとめ](fuyu-denkidai-matome.html)で一覧にしています。
