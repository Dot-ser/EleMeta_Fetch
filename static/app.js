// Copy metadata JSON via icon in metadata container
(() => {
  const copyIcon = document.getElementById('copyIcon');
  const metaBlock = document.getElementById('metadataBlock');
  if (copyIcon && metaBlock) {
    copyIcon.addEventListener('click', () => {
      const text = metaBlock.innerText || '';
      if (!text) {
        alert('No metadata to copy');
        return;
      }
      const iconEl = copyIcon.querySelector('i');
      const originalClasses = iconEl ? iconEl.className : '';
      const onSuccess = () => {
        if (iconEl) {
          iconEl.className = 'fa-solid fa-check';
          copyIcon.setAttribute('aria-label', 'Copied');
          setTimeout(() => {
            iconEl.className = originalClasses || 'fa-solid fa-clipboard';
            copyIcon.setAttribute('aria-label', 'Copy metadata');
          }, 1500);
        }
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(onSuccess).catch(fallbackCopy);
      } else {
        fallbackCopy();
      }

      function fallbackCopy() {
        try {
          const ta = document.createElement('textarea');
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          onSuccess();
        } catch (_) {
          // Swallow
        }
      }
    });
  }
})();

// Show selected file name(s) next to the file input
(() => {
  const fileInput = document.getElementById('image');
  const fileNameEl = document.getElementById('fileName');
  if (!fileInput || !fileNameEl) return;

  function prettySize(bytes) {
    if (!Number.isFinite(bytes) || bytes <= 0) return '';
    const units = ['B', 'KB', 'MB', 'GB'];
    let i = 0, v = bytes;
    while (v >= 1024 && i < units.length - 1) { v /= 1024; i++; }
    return `${v.toFixed(v < 10 && i > 0 ? 1 : 0)} ${units[i]}`;
  }

  fileInput.addEventListener('change', () => {
    const files = Array.from(fileInput.files || []);
    if (!files.length) {
      fileNameEl.textContent = '';
      fileNameEl.style.display = 'none';
      return;
    }
    if (files.length === 1) {
      const f = files[0];
      const size = prettySize(f.size);
      fileNameEl.textContent = size ? `${f.name} • ${size}` : f.name;
    } else {
      const total = files.reduce((acc, f) => acc + (f.size || 0), 0);
      const details = prettySize(total);
      fileNameEl.textContent = `${files.length} files selected${details ? ` • ${details}` : ''}`;
    }
    fileNameEl.style.display = 'block';
  });
})();
