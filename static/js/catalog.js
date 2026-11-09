"use strict";

const body = document.getElementById("catalog-body");

async function load(url, push) {
  body.setAttribute("aria-busy", "true");
  try {
    const response = await fetch(url, { headers: { "X-Requested-With": "fetch" } });
    if (!response.ok) throw new Error(String(response.status));
    body.innerHTML = await response.text();
    if (push) history.pushState({}, "", url);
  } catch {
    window.location.href = url;
  } finally {
    body.removeAttribute("aria-busy");
  }
}

body.addEventListener("click", (event) => {
  const link = event.target.closest("a[data-filter]");
  if (!link || event.metaKey || event.ctrlKey) return;
  event.preventDefault();
  load(link.href, true);
});

window.addEventListener("popstate", () => load(window.location.href, false));
