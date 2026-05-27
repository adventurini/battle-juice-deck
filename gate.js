(function () {
  var STORAGE_KEY = "bj-deck-unlock";
  var PASS_HASH = "76b97fceaf7d9db5b2bb38598fb41c4e4e9d33b0b8063c0e7336610afad13a43";

  function sha256(text) {
    if (!window.crypto || !crypto.subtle) return null;
    var enc = new TextEncoder().encode(text);
    return crypto.subtle.digest("SHA-256", enc).then(function (buf) {
      return Array.from(new Uint8Array(buf))
        .map(function (b) {
          return b.toString(16).padStart(2, "0");
        })
        .join("");
    });
  }

  function unlock() {
    sessionStorage.setItem(STORAGE_KEY, "1");
    document.documentElement.classList.remove("gate-locked");
    var gate = document.getElementById("deck-gate");
    if (gate) gate.remove();
  }

  if (sessionStorage.getItem(STORAGE_KEY) === "1") return;

  document.documentElement.classList.add("gate-locked");

  function mountGate() {
    if (document.getElementById("deck-gate")) return;

    var gate = document.createElement("div");
    gate.id = "deck-gate";
    gate.setAttribute("role", "dialog");
    gate.setAttribute("aria-modal", "true");
    gate.setAttribute("aria-label", "Deck access");
    gate.innerHTML =
      '<div class="gate-panel">' +
      '  <img class="gate-logo" src="assets/battle-juice-logo.png" alt="Battle Juice">' +
      '  <p class="gate-kicker">Confidential · Investor deck</p>' +
      '  <h2 class="gate-title">Enter password</h2>' +
      '  <form id="deck-gate-form" autocomplete="off">' +
      '    <input id="deck-gate-input" type="password" name="password" placeholder="Password" required autofocus>' +
      '    <button type="submit">View deck</button>' +
      '    <p id="deck-gate-error" class="gate-error" hidden>Incorrect password.</p>' +
      "  </form>" +
      "</div>";

    document.body.appendChild(gate);

    var form = document.getElementById("deck-gate-form");
    var input = document.getElementById("deck-gate-input");
    var error = document.getElementById("deck-gate-error");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      error.hidden = true;
      sha256(input.value).then(function (hash) {
        if (hash === PASS_HASH) {
          unlock();
          return;
        }
        error.hidden = false;
        input.value = "";
        input.focus();
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountGate);
  } else {
    mountGate();
  }
})();
