const fs=require('fs');
const h=fs.readFileSync(process.argv[2],'utf8');
const src=h.split('/* calc-start */')[1].split('/* calc-end */')[0];
const marathonCalc=new Function(src+';return marathonCalc;')();
const O={threshold:1000,maxRate:10,cap:7000};
const R=a=>a.map(x=>typeof x==='number'?{amount:x}:x);
const cases=[
 ['0店舗（空）',[],{shops:0,rate:0,points:0,toNext:1}],
 ['0店舗（999円のみ）',[999],{shops:0,rate:0,points:0}],
 ['1店舗 ちょうど1,000円',[1000],{shops:1,rate:1,extraRate:0,points:0,taxless:909,normal:9}],
 ['1店舗 999円＋1,000円',[999,1000],{shops:1,rate:1,points:0}],
 ['2店舗 1,000円×2',[1000,1000],{shops:2,rate:2,taxless:1818,points:18}],
 ['3店舗 8,000/1,200/980(例)',[8000,1200,980],{shops:2,rate:2,taxless:8362,points:83}],
 ['8%行 1,080円',[{amount:1080,tax8:true},1100],{shops:2,taxless:2000,points:20}],
 ['10店舗 各11,000円（上限未満）',Array(10).fill(11000),{shops:10,rate:10,taxless:100000,rawPoints:9000,points:7000,capped:true,toNext:0}],
 ['10店舗 税抜77,700円（上限の手前）',Array(10).fill(8547),{shops:10,rate:10,taxless:77700,points:6993,capped:false}],
 ['11店舗→10倍止まり',Array(11).fill(1100),{shops:11,rate:10,extraRate:9,taxless:11000,points:990,toNext:0}],
 ['上限ちょうど 9倍分=7000 (税抜77,778)',[...Array(9).fill(1100),{amount:75656}],{rate:10,points:7000,capped:true}],
 ['上限超え 2店舗 税抜80万',[440000,440000],{shops:2,rawPoints:8000,points:7000,capped:true}],
 ['capTaxless 10店舗',Array(10).fill(1100),{capTaxless:77778}],
];
let fail=0;
for(const [name,rows,exp] of cases){
 const r=marathonCalc(R(rows),O);
 const bad=Object.entries(exp).filter(([k,v])=>r[k]!==v);
 if(bad.length)fail++;
 console.log(`| ${name} | shops=${r.shops} rate=${r.rate} 税抜=${r.taxless} 計算=${r.rawPoints} 表示=${r.points} 上限=${r.capped} 次=${r.toNext?r.nextRate+'倍':'-'} | ${bad.length?'NG '+JSON.stringify(bad):'OK'} |`);
}
console.log('FAIL',fail);
// 表示の確認（監査R2 軽1）：0店舗のとき「あと1店舗で1倍」と出さない
{
 const ok0=h.includes("if(r.shops===0)h+=")&&h.includes("else if(r.toNext)h+='➡️ あと<b>1店舗</b>");
 if(!ok0)fail++;
 console.log(`| 表示 0店舗のとき専用の案内（2店舗で2倍） | ${ok0?'OK':'NG'} |`);
}
console.log('FAIL(表示込み)',fail);
