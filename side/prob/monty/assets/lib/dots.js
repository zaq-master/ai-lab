/* 1万個の点をcanvasに描く部品（決定的）。使い方：
 *   const g = document.getElementById("cv").getContext("2d");
 *   DOTS.draw(g, {x:90, y:500, size:900, n:10000, shown: 3200, color:(i)=> win[i] ? "#ffc928" : "#c9cde6", pop: t-tLand})
 * n 個を正方形に並べる（1万なら100×100）。shown 個目までを色付きで、残りは薄く描く。
 */
(function () {
  function draw(g, o) {
    const n = o.n || 10000, side = Math.ceil(Math.sqrt(n)), cell = o.size / side, r = Math.max(1, cell * 0.42);
    const shown = Math.max(0, Math.min(n, o.shown ?? n));
    g.save();
    for (let i = 0; i < n; i++) {
      const cx = o.x + (i % side + 0.5) * cell, cy = o.y + (Math.floor(i / side) + 0.5) * cell;
      g.fillStyle = i < shown ? o.color(i) : (o.empty || "rgba(201,205,230,.35)");
      if (cell >= 6) { g.beginPath(); g.arc(cx, cy, r, 0, 6.2832); g.fill(); } else g.fillRect(cx - r, cy - r, 2 * r, 2 * r);
    }
    g.restore();
  }
  // 並べ替え表示：色ごとにまとめて並べ直した図（割合が一目で分かる）。order はグループの並び
  function sorted(g, o) {
    const n = o.n || 10000, groups = o.groups; // groups: [{count, color}]
    let k = 0; const idx = [];
    for (const gr of groups) for (let j = 0; j < gr.count; j++) idx.push(gr.color);
    draw(g, { ...o, n, color: (i) => idx[i] || "#888" });
  }
  window.DOTS = { draw, sorted };
})();
