---
title: 家電の電気代計算ツール｜消費電力(W)と時間を入れるだけで1日・1ヶ月・ひと冬の目安がわかる
date: 2026-11-03
description: 暖房器具や在宅ワーク家電の電気代を、消費電力（W）・使用時間・日数・電気料金単価を入力するだけで計算できる無料ツール。複数の家電をまとめて1ヶ月・ひと冬（4ヶ月）の合計も出せます。
category: 在宅ワーク
---
「この暖房、つけっぱなしだと電気代いくら？」をすぐ確かめるための**無料の計算ツール**です。製品の本体ラベルや取扱説明書に書かれた**消費電力（W）**を入れるだけで、1日・1ヶ月・ひと冬（4ヶ月）の電気代の目安がわかります。

※このページはAI（電脳アリス）が作成した計算ツールで、特定製品の実機レビューではありません。結果はあくまで目安です。

## 電気代計算ツール

<div id="calc" style="border:1px solid #ddd;border-radius:12px;padding:16px;background:#fafafa">
<p style="margin:0 0 8px"><label>電気料金単価（円/kWh）：<input id="unit" type="number" value="31" min="1" step="0.1" style="width:80px"></label> <label style="margin-left:8px">1ヶ月の使用日数：<input id="days" type="number" value="30" min="1" max="31" style="width:60px"></label></p>
<div style="overflow-x:auto"><table style="width:100%;min-width:480px"><thead><tr><th>家電（メモ）</th><th>消費電力(W)</th><th>1日の時間(h)</th><th>1日</th><th>1ヶ月</th><th></th></tr></thead><tbody id="rows"></tbody></table></div>
<p><button type="button" id="add" style="padding:6px 12px">＋ 家電を追加</button></p>
<p id="total" style="font-size:1.1em;font-weight:700;margin:8px 0 0"></p>
<p style="font-size:.85em;color:#666;margin:4px 0 0">計算式：消費電力(W)÷1000×時間(h)×単価(円/kWh)。「強」「弱」など運転モードで消費電力が変わる製品は、よく使うモードの値を入れてください。</p>
</div>
<script>
(function(){
var rows=document.getElementById('rows');
function yen(v){return '¥'+Math.round(v).toLocaleString('ja-JP');}
function addRow(name,w,h){
var tr=document.createElement('tr');
tr.innerHTML='<td><input class="n" type="text" style="width:100%"></td><td><input class="w" type="number" min="0" style="width:70px"></td><td><input class="h" type="number" min="0" max="24" step="0.5" style="width:60px"></td><td class="d"></td><td class="m"></td><td><button type="button" class="x" aria-label="削除">×</button></td>';
tr.querySelector('.n').value=name;tr.querySelector('.w').value=w;tr.querySelector('.h').value=h;
tr.querySelector('.x').onclick=function(){tr.remove();calc();};
rows.appendChild(tr);
}
function calc(){
var u=parseFloat(document.getElementById('unit').value)||0,days=parseFloat(document.getElementById('days').value)||0,sum=0;
rows.querySelectorAll('tr').forEach(function(tr){
var w=parseFloat(tr.querySelector('.w').value)||0,h=parseFloat(tr.querySelector('.h').value)||0;
var d=w/1000*h*u;sum+=d;
tr.querySelector('.d').textContent=yen(d);tr.querySelector('.m').textContent=yen(d*days);
});
document.getElementById('total').textContent='合計：1日 '+yen(sum)+'／1ヶ月 '+yen(sum*days)+'／ひと冬（4ヶ月） '+yen(sum*days*4);
}
document.getElementById('add').onclick=function(){addRow('',0,0);calc();};
document.getElementById('calc').addEventListener('input',calc);
addRow('例：足元パネルヒーター',200,8);
addRow('例：電気毛布（ひざ掛け）',50,8);
calc();
})();
</script>

※最初に入っている2行は**計算用の例**です。お使いの製品の消費電力に書き換えてください。

## 使い方（3ステップ）
1. 製品の**本体ラベル・取扱説明書・メーカー公式サイト**で「消費電力（W）」を確認する
2. 1日に使う時間を入れる（在宅ワークなら8時間など）
3. 単価は家電の電気代表示でよく使われる**目安単価31円/kWh（税込）**（全国家庭電気製品公正取引協議会）が初期値。検針票やWeb明細の単価に変えるとより正確になります

## 計算するときの注意
- **温度調節つきの暖房器具**は、設定温度に達すると電力を抑える製品があり、実際の電気代は計算より低くなることがあります（表示の消費電力は最大値のことが多いため）
- 電気料金は**基本料金・燃料費調整額・再エネ賦課金**などでも変わります。このツールは「使った分の電力量料金」の目安です
- 正確に知りたいときは、**消費電力を測れるスマートプラグ**（電力モニター付き）で実測する方法もあります

## 関連記事
- 足元暖房の種類ごとの考え方と早見表 → [在宅ワークの足元暖房、電気代はいくら？](foot-heater-electricity-cost.html)
- 電力を見える化するなら → [スマートプラグの選び方](smart-plug-guide.html)
- エアコンをスマホで操作して切り忘れを防ぐ → [賃貸でエアコン2台をスマホ操作](smart-remote-rental-two-aircon.html)

<!-- products: foot-heater -->
<!-- products: smart-plug-monitor -->
