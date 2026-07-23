/* =====================================================================
   Players to Study — interactive hexagonal node cloud
   - Hover (fine pointer) balloons a node; tap toggles it on touch.
   - The active photo shoves its neighbours out of the way (each neighbour
     gets a --px/--py push vector), and its paired text circle slides out
     toward the stage centre so both read as an overlapping "duo".
   - One active at a time. Fast, Apple-smooth (CSS transitions do the motion;
     JS only sets targets, so wild mouse-dragging stays coherent).
   ===================================================================== */
(function () {
  "use strict";

  var stage = document.querySelector(".players-stage");
  if (!stage) return;

  var nodes = Array.prototype.slice.call(stage.querySelectorAll(".pnode"));
  var canHover = window.matchMedia &&
    window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* a hidden probe to resolve the clamp()-based size tokens to pixels */
  var probe = document.createElement("div");
  probe.style.cssText = "position:absolute;visibility:hidden;height:0;top:0;left:0;";
  stage.appendChild(probe);
  function tokenPx(name) {
    probe.style.width = "var(" + name + ")";
    return parseFloat(getComputedStyle(probe).width) || 0;
  }

  var geom = [];        // {cx, cy} resting centre of each node, in stage px
  var baseR = 0, bigR = 0, cardR = 0, sw = 0, sh = 0;
  var current = -1;

  function measure() {
    var r = stage.getBoundingClientRect();
    sw = r.width; sh = r.height;
    baseR = tokenPx("--base") / 2;
    bigR  = tokenPx("--big")  / 2;
    cardR = tokenPx("--card") / 2;
    geom = nodes.map(function (n) {
      var xf = parseFloat(getComputedStyle(n).getPropertyValue("--x")) / 100;
      var yf = parseFloat(getComputedStyle(n).getPropertyValue("--y")) / 100;
      return { cx: xf * sw, cy: yf * sh };
    });
  }

  function clearPushes() {
    nodes.forEach(function (n) {
      n.style.setProperty("--px", "0px");
      n.style.setProperty("--py", "0px");
    });
  }

  function activate(i) {
    if (i === current) return;
    if (current > -1) {
      nodes[current].classList.remove("is-active");
      nodes[current].style.removeProperty("--cardx");
      nodes[current].style.removeProperty("--cardy");
    }
    current = i;
    stage.classList.add("has-active");
    var a = nodes[i];
    a.classList.add("is-active");

    var ac = geom[i];
    var gap = 12;
    var minDist = bigR + baseR * 0.55 + gap;   // neighbours must clear the big photo

    nodes.forEach(function (n, j) {
      if (j === i) { n.style.setProperty("--px", "0px"); n.style.setProperty("--py", "0px"); return; }
      var dx = geom[j].cx - ac.cx, dy = geom[j].cy - ac.cy;
      var dist = Math.hypot(dx, dy) || 0.0001;
      var over = minDist - dist;
      if (over > 0) {
        var ux = dx / dist, uy = dy / dist;
        n.style.setProperty("--px", (ux * over).toFixed(1) + "px");
        n.style.setProperty("--py", (uy * over).toFixed(1) + "px");
      } else {
        n.style.setProperty("--px", "0px");
        n.style.setProperty("--py", "0px");
      }
    });

    /* slide the text circle toward the stage centre (keeps it on-screen) */
    var tx = sw / 2 - ac.cx, ty = sh / 2 - ac.cy;
    var tl = Math.hypot(tx, ty);
    var dirx, diry;
    if (tl < 1) { dirx = 0.62; diry = 0.62; }          // centre node → down-right
    else { dirx = tx / tl; diry = ty / tl; }
    var offset = (bigR + cardR) * 0.78;                // partial overlap = duo look
    a.style.setProperty("--cardx", (dirx * offset).toFixed(1) + "px");
    a.style.setProperty("--cardy", (diry * offset).toFixed(1) + "px");
  }

  function deactivate() {
    if (current > -1) {
      nodes[current].classList.remove("is-active");
      nodes[current].style.removeProperty("--cardx");
      nodes[current].style.removeProperty("--cardy");
    }
    current = -1;
    stage.classList.remove("has-active");
    clearPushes();
  }

  /* touch devices don't hover — tell them to tap */
  if (!canHover) {
    var hint = document.querySelector(".players-cloud__hint");
    if (hint) hint.textContent = "Tap a player to study them";
  }

  measure();
  clearPushes();

  if (canHover) {
    /* One deterministic hit-test drives everything: whatever the pointer is
       actually over wins. Over a node (its photo OR its slid-out text circle)
       → that node is the active one; over empty space → snap back to rest.
       Because it reads the live pixel under the cursor, it's immune to the
       enter/leave quirks of an element that is mid-balloon. */
    stage.addEventListener("pointermove", function (e) {
      var pn = e.target.closest && e.target.closest(".pnode");
      if (pn) {
        var i = nodes.indexOf(pn);
        if (i > -1) activate(i);          // idempotent when already active
      } else {
        deactivate();
      }
    });
    stage.addEventListener("pointerleave", deactivate);

    /* keyboard access: tabbing focuses a disc; focus opens, blur closes */
    nodes.forEach(function (n, i) {
      var disc = n.querySelector(".pnode__disc");
      disc.addEventListener("focus", function () { activate(i); });
      disc.addEventListener("blur", function () { if (current === i) deactivate(); });
    });
  } else {
    nodes.forEach(function (n, i) {
      n.querySelector(".pnode__disc").addEventListener("click", function (e) {
        e.stopPropagation();
        if (current === i) deactivate(); else activate(i);
      });
    });
    document.addEventListener("click", function (e) {
      if (!stage.contains(e.target)) deactivate();
    });
  }

  /* keep geometry correct on resize/orientation change */
  var rt;
  window.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () {
      var wasHoverable = canHover;
      canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
      deactivate();
      measure();
      void wasHoverable;
    }, 150);
  });
})();
