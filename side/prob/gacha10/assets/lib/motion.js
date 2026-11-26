/* 動きの部品集（HyperFrames の renderAt(t) から呼ぶ。すべて時刻だけで決まる＝決定的。Math.random は使わない）
 * 使い方：<script src="../pachi3d/lib/motion.js"></script> のあと window.M.xxx
 * 解説は side/pachi3d/VIDEO_KNOWLEDGE.md
 *
 * 一部の関数は次の MIT ライセンスのコードを参考に書き直したもの：
 *   - mg-styles-15  Copyright (c) 2026 Vincentwei1021  https://github.com/Vincentwei1021/mg-styles-15
 *     （wob, bez, roll, typed, hash, slap, camera の fly/drift, springTo）
 *   - ClaudeAnimationBase  Copyright (c) JohnHeibel  https://github.com/JohnHeibel/ClaudeAnimationBase
 *     （smooth, easeIn/Out, backOut, spring, ring, pulse, shakeXY, kf）
 *
 * MIT License: Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 * and associated documentation files (the "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following
 * conditions: The above copyright notice and this permission notice shall be included in all copies or
 * substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
(function () {
  const FPS = 30;
  const clamp = (x, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
  const lerp = (a, b, u) => a + (b - a) * u;
  const prog = (t, t0, d) => clamp((t - t0) / d);                 // 0→1 の進み具合
  const frac = (x) => x - Math.floor(x);

  // ---- イージング ----
  const smooth = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
  const easeOut = (x) => 1 - Math.pow(1 - clamp(x), 3);            // 出現・到着
  const easeIn = (x) => Math.pow(clamp(x), 3);                     // 退場
  const easeInOut = (x) => { x = clamp(x); return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const expoOut = (x) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * clamp(x)));
  const backOut = (x, s = 1.7) => { x = clamp(x); return 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); };
  // CSS の cubic-bezier と同じ指定ができるイージング
  function bez(x1, y1, x2, y2) {
    return (u) => {
      if (u <= 0) return 0; if (u >= 1) return 1; let t = u;
      for (let i = 0; i < 8; i++) {
        const cx = 3 * x1 * t * (1 - t) ** 2 + 3 * x2 * t * t * (1 - t) + t ** 3 - u;
        const d = 3 * x1 * (1 - t) ** 2 + 6 * (x2 - x1) * t * (1 - t) + 3 * (1 - x2) * t * t;
        if (Math.abs(d) < 1e-6) break; t = clamp(t - cx / d);
      }
      return 3 * y1 * t * (1 - t) ** 2 + 3 * y2 * t * t * (1 - t) + t ** 3;
    };
  }
  const flyEase = bez(0.62, 0, 0.22, 1);                             // カメラ移動：ゆっくり出て、さっと着く
  const popEase = bez(0.34, 1.56, 0.64, 1);                          // 跳ね返り

  // ---- 揺れ・バネ ----
  const spring = (t, t0, k = 6, w = 18) => (t < t0 ? 0 : Math.exp(-k * (t - t0)) * Math.sin(w * (t - t0)));  // 出来事の後の減衰ゆれ（0中心）
  const ring = (t, evs, k, w) => evs.reduce((s, e) => s + spring(t, e, k, w), 0);
  const wob = (dt, f = 5, k = 11) => (dt < 0 ? 0 : Math.exp(-k * dt) * Math.cos(2 * Math.PI * f * dt));       // 着地後の揺れ（1から減衰）
  // 0→1 へ行き過ぎて戻るバネ（z=減衰比, w=固有角速度）。花字の出現：z=.517,w=22 で 5コマ目に約1.15倍
  function springTo(dt, z = 0.517, w = 22) {
    if (dt <= 0) return 0; const wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w * dt) * (Math.cos(wd * dt) + (z * w / wd) * Math.sin(wd * dt));
  }
  const pulse = (t, beat, off = 0, k = 6) => Math.exp(-frac((t - off) / beat) * k);  // 拍ちょうどで1、その後減衰

  // ---- 決定的な乱数 ----
  function hash(...a) {
    let h = 2166136261 >>> 0;
    for (const v of a) { h ^= (Math.floor(v * 1000) * 2654435761) >>> 0; h = Math.imul(h ^ (h >>> 15), 2246822507) >>> 0; h = Math.imul(h ^ (h >>> 13), 3266489909) >>> 0; h ^= h >>> 16; }
    return (h >>> 0) / 4294967296;
  }
  const frameOf = (t) => Math.floor(t * FPS + 0.5);
  // 画面の揺れ（px）。fps ごとに決まった値
  const shakeXY = (t, amt) => { const f = frameOf(t); return [(hash(f, 1.7) - 0.5) * 2 * amt, (hash(f, 2.3) - 0.5) * 2 * amt]; };

  // ---- キーフレーム補間：keys=[[t,値],...]（値は数か配列） ----
  function kf(t, keys, e = smooth) {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [ta, va] = keys[i - 1], [tb, vb] = keys[i];
      if (t <= tb) { const u = e((t - ta) / (tb - ta)); return Array.isArray(va) ? va.map((v, j) => lerp(v, vb[j], u)) : lerp(va, vb, u); }
    }
    return keys[keys.length - 1][1];
  }

  // ---- 文字 ----
  // 数字ルーレット：t0 から n コマはでたらめ（桁数・記号は保つ）、その後に本当の値
  function roll(t, t0, final, id = 0, n = 5) {
    if (t < t0) return null; const f = frameOf(t) - frameOf(t0); if (f >= n) return final;
    let s = ""; for (let i = 0; i < final.length; i++) { const c = final[i]; s += /[0-9]/.test(c) ? "0123456789"[Math.floor(hash(id, i, f + 7) * 10)] : c; }
    return s;
  }
  const typed = (t, t0, str, cps = 30) => (t < t0 ? "" : str.slice(0, Math.floor((t - t0) * cps + 1e-6)));
  // 0から数え上げ（fmt で書式）
  const countUp = (t, t0, d, value, fmt = (v) => Math.round(v).toLocaleString()) => fmt(value * easeOut(prog(t, t0, d)));

  // ---- ステッカーの貼り付け：大きく傾いた状態から dur 秒で着地 → 揺れが収まる ----
  function slap(t, land, dur = 0.2, amp = 0.3) {
    const p = (t - (land - dur)) / dur;
    if (p < 0) return { o: 0, s: 1 + amp, r: 6, lift: 1 };
    if (p < 1) { const L = 1 - p * p; return { o: clamp(p * 5), s: 1 + amp * L, r: 6 * L, lift: L }; }
    const w = wob(t - land, 4.5, 10); return { o: 1, s: 1 - 0.035 * w, r: -0.8 * w, lift: 0 };
  }
  const stickerShadow = (lift) => `drop-shadow(0 ${6 + 34 * lift}px ${10 + 34 * lift}px rgba(22,34,46,${0.26 - 0.08 * lift}))`;

  // ---- 表情の切り替えを演技にする（PNG差し替え用）。change=表情が変わる時刻, amt=感情の大きさ ----
  function faceAct(t, change, amt = 0.3) {
    const d = t - change;
    const pre = d < 0 && d > -0.1 ? 1 + d / 0.1 : 0;                // 0.1秒前から少しつぶれる
    const take = d >= 0 ? spring(t, change, 7, 16) : 0;             // 変わった直後に伸びてバネで戻る
    return { sx: 1 + 0.04 * pre - 0.04 * amt * take, sy: 1 - 0.05 * pre + 0.07 * amt * take };
  }

  // ---- カメラ：CAM=[{t,x,y,z,move:'fly'|'drift'}...]（世界座標）。W,H=画面 ----
  function camera(t, CAM) {
    if (t <= CAM[0].t) return CAM[0];
    for (let i = 1; i < CAM.length; i++) {
      const a = CAM[i - 1], b = CAM[i]; if (t > b.t) continue;
      const u = (t - a.t) / (b.t - a.t), e = b.move === "fly" ? flyEase(u) : -(Math.cos(Math.PI * u) - 1) / 2;
      const arc = b.move === "fly" ? Math.sin(Math.PI * e) * 0.12 : 0;   // 移動の途中で少し引く
      return { x: lerp(a.x, b.x, e), y: lerp(a.y, b.y, e), z: Math.exp(lerp(Math.log(a.z), Math.log(b.z), e)) * (1 - arc) };
    }
    return CAM[CAM.length - 1];
  }
  const camMatrix = (C, W = 1080, H = 1920, jx = 0, jy = 0) => `matrix(${C.z},0,0,${C.z},${W / 2 - C.x * C.z + jx},${H / 2 - C.y * C.z + jy})`;

  window.M = { FPS, clamp, lerp, prog, frac, smooth, easeOut, easeIn, easeInOut, expoOut, backOut, bez, flyEase, popEase,
    spring, ring, wob, springTo, pulse, hash, frameOf, shakeXY, kf, roll, typed, countUp, slap, stickerShadow, faceAct, camera, camMatrix };
})();
