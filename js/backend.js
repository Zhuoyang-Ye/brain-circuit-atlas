/* Brain Circuit Atlas: Local Backend & Cloudflare R2 Integration */
(function () {
  'use strict';
  const CA = window.CA || (window.CA = {});
  CA.backend = null;
  CA.hasBackend = false;

  async function checkBackend() {
    try {
      const res = await fetch('/api/status', { cache: 'no-store' });
      if (res.ok) {
        CA.backend = await res.json();
        CA.hasBackend = true;
        initBackendUI();
      }
    } catch (e) {
      // Backend not running (e.g. running on GitHub Pages)
      CA.hasBackend = false;
    }
  }

  function initBackendUI() {
    // Add local app badge in top bar
    const brand = document.querySelector('.brand');
    if (brand && !document.getElementById('backend-badge')) {
      const badge = document.createElement('span');
      badge.id = 'backend-badge';
      badge.className = 'pill';
      badge.style.cssText = 'margin-left: 8px; font-size: 11px; padding: 2px 7px; background: rgba(56, 139, 253, 0.15); color: #58a6ff; border: 1px solid rgba(56, 139, 253, 0.4); border-radius: 10px; cursor: pointer;';
      badge.textContent = CA.backend.r2_configured ? '● Cloud Synced' : '● Local App';
      badge.title = 'Click to open Cloudflare R2 & Website Sync Settings';
      badge.onclick = (e) => { e.preventDefault(); openCloudModal(); };
      brand.appendChild(badge);
    }
  }

  // --- Cloudflare R2 & Website Sync Modal ---
  CA.openCloudModal = openCloudModal;
  async function openCloudModal() {
    const m = CA.clear(document.getElementById('modal'));
    const h = CA.h;
    
    let config = { account_id: '', access_key_id: '', secret_key_masked: '', bucket_name: '', public_url: '' };
    try {
      const r = await fetch('/api/r2/config');
      if (r.ok) config = await r.json();
    } catch (e) {}

    const accInput = h('input', { class: 'text', value: config.account_id || '', placeholder: 'e.g. 9a8b7c6d5e4f3a2b1...', style: { width: '100%' } });
    const keyInput = h('input', { class: 'text', value: config.access_key_id || '', placeholder: 'e.g. 1a2b3c4d5e...', style: { width: '100%' } });
    const secretInput = h('input', { class: 'text', type: 'password', placeholder: config.secret_key_masked || 'Enter Secret Access Key', style: { width: '100%' } });
    const bucketInput = h('input', { class: 'text', value: config.bucket_name || '', placeholder: 'e.g. brain-circuit-atlas-bucket', style: { width: '100%' } });
    const pubUrlInput = h('input', { class: 'text', value: config.public_url || '', placeholder: 'e.g. https://pub-xxx.r2.dev (optional)', style: { width: '100%' } });

    const statusMsg = h('div', { class: 'small muted', style: { margin: '8px 0' } }, '');

    const testBtn = h('button', { class: 'btn', onclick: async () => {
      statusMsg.textContent = 'Testing connection to Cloudflare R2...';
      try {
        const res = await fetch('/api/r2/test', { method: 'POST' });
        const d = await res.json();
        statusMsg.textContent = d.message || (d.ok ? 'Connection successful!' : 'Connection failed');
        statusMsg.style.color = d.ok ? '#3fb950' : '#f85149';
      } catch (err) {
        statusMsg.textContent = 'Error testing R2: ' + err.message;
        statusMsg.style.color = '#f85149';
      }
    } }, 'Test Connection');

    const saveBtn = h('button', { class: 'btn primary', onclick: async () => {
      statusMsg.textContent = 'Saving configuration...';
      try {
        const payload = {
          account_id: accInput.value.trim(),
          access_key_id: keyInput.value.trim(),
          bucket_name: bucketInput.value.trim(),
          public_url: pubUrlInput.value.trim()
        };
        if (secretInput.value.trim()) payload.secret_access_key = secretInput.value.trim();
        const res = await fetch('/api/r2/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const d = await res.json();
        statusMsg.textContent = d.configured ? 'Credentials saved and active.' : 'Saved (incomplete credentials).';
        statusMsg.style.color = '#3fb950';
        const badge = document.getElementById('backend-badge');
        if (badge) badge.textContent = d.configured ? '● Cloud Synced' : '● Local App';
      } catch (err) {
        statusMsg.textContent = 'Failed to save: ' + err.message;
        statusMsg.style.color = '#f85149';
      }
    } }, 'Save Settings');

    const syncMeshesBtn = h('button', { class: 'btn', onclick: async () => {
      statusMsg.textContent = 'Syncing 3D meshes to Cloudflare R2...';
      try {
        const res = await fetch('/api/r2/sync_meshes', { method: 'POST' });
        const d = await res.json();
        if (d.ok) {
          statusMsg.textContent = `Successfully uploaded ${d.uploaded.length} mesh datasets to Cloudflare R2!`;
          statusMsg.style.color = '#3fb950';
        } else {
          statusMsg.textContent = 'Sync failed: ' + d.message;
          statusMsg.style.color = '#f85149';
        }
      } catch (err) {
        statusMsg.textContent = 'Error: ' + err.message;
        statusMsg.style.color = '#f85149';
      }
    } }, 'Sync 3D Meshes to R2');

    const rebuildSiteBtn = h('button', { class: 'btn', onclick: async () => {
      statusMsg.textContent = 'Rebuilding data bundles for website...';
      try {
        const res = await fetch('/api/website/rebuild', { method: 'POST' });
        const d = await res.json();
        if (d.success) {
          statusMsg.textContent = 'Website data bundle regenerated successfully (ready for GitHub Pages).';
          statusMsg.style.color = '#3fb950';
        } else {
          statusMsg.textContent = 'Rebuild failed: ' + d.stderr;
          statusMsg.style.color = '#f85149';
        }
      } catch (err) {
        statusMsg.textContent = 'Error: ' + err.message;
        statusMsg.style.color = '#f85149';
      }
    } }, 'Rebuild Website Bundle');

    const card = h('div', { class: 'card', style: { maxWidth: '580px', width: '90%' }, onclick: (e) => e.stopPropagation() },
      h('div', { class: 'row', style: { justifyContent: 'space-between' } },
        h('h3', { style: { margin: 0 } }, 'Cloudflare R2 & Website Sync'),
        h('button', { class: 'icon-btn', onclick: () => m.classList.add('hidden') }, '✕')),
      h('p', { class: 'small muted', style: { margin: '8px 0 16px' } },
        'Connect Cloudflare R2 (10 GB free storage, $0 download fees) to store 3D brain meshes and sync updates to your free website.'),
      h('div', { style: { display: 'grid', gridTemplateColumns: '140px 1fr', gap: '10px', alignItems: 'center' } },
        h('label', { class: 'small' }, 'Account ID:'), accInput,
        h('label', { class: 'small' }, 'Access Key ID:'), keyInput,
        h('label', { class: 'small' }, 'Secret Access Key:'), secretInput,
        h('label', { class: 'small' }, 'Bucket Name:'), bucketInput,
        h('label', { class: 'small' }, 'Public URL:'), pubUrlInput),
      statusMsg,
      h('div', { class: 'row', style: { marginTop: '16px', gap: '8px', flexWrap: 'wrap' } },
        saveBtn, testBtn, syncMeshesBtn, rebuildSiteBtn));

    m.appendChild(card);
    m.classList.remove('hidden');
  }

  // Auto-check backend on DOM load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkBackend);
  } else {
    checkBackend();
  }
})();
