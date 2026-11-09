"use strict";

const lightbox = document.getElementById("lightbox");
if (lightbox && lightbox.showModal) {
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-lightbox]");
    if (!link || event.metaKey || event.ctrlKey) return;
    event.preventDefault();
    lightbox.querySelector("img").src = link.href;
    lightbox.showModal();
  });
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) lightbox.close();
  });
}

document.addEventListener("click", (event) => {
  const video = event.target.closest("[data-youtube-id]");
  if (!video) return;
  const frame = document.createElement("iframe");
  frame.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(video.dataset.youtubeId)}?autoplay=1`;
  frame.allow = "autoplay; encrypted-media; picture-in-picture";
  frame.allowFullscreen = true;
  frame.referrerPolicy = "strict-origin-when-cross-origin";
  frame.title = video.getAttribute("aria-label") || "Video";
  frame.className = "video-frame";
  video.replaceWith(frame);
});
