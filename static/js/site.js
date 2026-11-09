"use strict";

document.addEventListener("click", (event) => {
  const video = event.target.closest("[data-youtube-id]");
  if (!video) return;
  const frame = document.createElement("iframe");
  frame.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(video.dataset.youtubeId)}?autoplay=1`;
  frame.allow = "autoplay; encrypted-media; picture-in-picture";
  frame.allowFullscreen = true;
  frame.title = video.getAttribute("aria-label") || "Video";
  frame.className = "video-frame";
  video.replaceWith(frame);
});
