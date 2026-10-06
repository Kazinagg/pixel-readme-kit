// Pixel Readme Kit Studio Core JavaScript
    let renderTimer = null;
    let sseSource = null;
    let debugMode = false;
    let editorMode = 'edit';
    let templateBlocks = [];
    let currentEditingBlockId = null;
    let currentEditingBlockOriginal = null;
    let targetInsertAfterId = -1;
    let isParsingRaw = false;
    let activePreviewTheme = 'dark';

    const PRESET_COLORS = {
      cyberpunk: { primary: "#00c8d7", accent: "#a855f7", tertiary: "#ff0055" },
      amber:     { primary: "#f59e0b", accent: "#ef4444", tertiary: "#ff0055" },
      matrix:    { primary: "#00ff41", accent: "#008f11", tertiary: "#ff0055" },
      tokyo:     { primary: "#f72585", accent: "#7209b7", tertiary: "#06b6d4" }
    };

    function toggleInspector() {
      const panel = document.getElementById("inspector-panel");
      panel.classList.toggle("collapsed");
      const btn = document.getElementById("btn-toggle-inspector");
      if (panel.classList.contains("collapsed")) {
        btn.classList.remove("active-btn");
      } else {
        btn.classList.add("active-btn");
      }
    }

    function openInspector() {
      const panel = document.getElementById("inspector-panel");
      panel.classList.remove("collapsed");
      document.getElementById("btn-toggle-inspector").classList.add("active-btn");
    }

    function toggleDebugMode() {
      debugMode = !debugMode;
      const box = document.getElementById("live-svg-box");
      const btn = document.getElementById("btn-debug");
      const body = document.body;

      if (debugMode) {
        box.classList.add("debug-active");
        body.classList.add("debug-active");
        btn.classList.add("active-btn");
        btn.style.background = "var(--studio-amber)";
        btn.style.color = "#000";
        btn.style.borderColor = "var(--studio-amber)";
      } else {
        box.classList.remove("debug-active");
        body.classList.remove("debug-active");
        btn.classList.remove("active-btn");
        btn.style.background = "";
        btn.style.color = "";
        btn.style.borderColor = "";
      }
    }

    function switchPreviewTheme(theme) {
      activePreviewTheme = theme;
      try { localStorage.setItem("pk_preview_theme", theme); } catch (_) {}
      const scrollArea = document.getElementById("preview-scroll-area");
      const mdBody = document.getElementById("readme-preview-content");
      const tabDark = document.getElementById("tab-dark");
      const tabLight = document.getElementById("tab-light");
      const liveBox = document.getElementById("live-svg-box");

      if (theme === "light") {
        if (scrollArea) {
          scrollArea.classList.add("light-theme");
          scrollArea.setAttribute("data-color-mode", "light");
          scrollArea.setAttribute("data-theme", "light");
        }
        if (mdBody) {
          mdBody.setAttribute("data-color-mode", "light");
          mdBody.setAttribute("data-theme", "light");
        }
        if (liveBox) liveBox.classList.add("light-preview");
        if (tabLight) tabLight.classList.add("active");
        if (tabDark) tabDark.classList.remove("active");
      } else {
        if (scrollArea) {
          scrollArea.classList.remove("light-theme");
          scrollArea.setAttribute("data-color-mode", "dark");
          scrollArea.setAttribute("data-theme", "dark");
        }
        if (mdBody) {
          mdBody.setAttribute("data-color-mode", "dark");
          mdBody.setAttribute("data-theme", "dark");
        }
        if (liveBox) liveBox.classList.remove("light-preview");
        if (tabDark) tabDark.classList.add("active");
        if (tabLight) tabLight.classList.remove("active");
      }
      loadCompiledPreview();
      renderCurrentBlock(false);
    }

    // --- View Mode vs Edit Mode Logic ---
    let currentStudioMode = "edit";
    let cachedEditHtml = "";
    let cachedViewHtml = "";

    function setStudioMode(mode) {
      currentStudioMode = mode;
      try { localStorage.setItem("pk_studio_mode", mode); } catch (_) {}
      const editTab = document.getElementById("tab-mode-edit");
      const viewTab = document.getElementById("tab-mode-view");
      const previewArea = document.getElementById("readme-preview-content");

      if (mode === "view") {
        if (editTab) editTab.classList.remove("active");
        if (viewTab) viewTab.classList.add("active");
        if (previewArea) {
          previewArea.classList.add("view-mode");
          if (cachedViewHtml) {
            previewArea.innerHTML = cachedViewHtml;
          }
        }
      } else {
        if (editTab) editTab.classList.add("active");
        if (viewTab) viewTab.classList.remove("active");
        if (previewArea) {
          previewArea.classList.remove("view-mode");
          if (cachedEditHtml) {
            previewArea.innerHTML = cachedEditHtml;
          }
          if (currentEditingBlockId !== null) {
            highlightBlockInPreview(currentEditingBlockId);
          }
        }
      }
    }

    // --- Global Theme Logic ---
    function onGlobalPresetChange() {
      const preset = document.getElementById("sel-global-preset").value;
      const primPicker = document.getElementById("picker-global-primary");
      const primText = document.getElementById("inp-global-primary");
      const accPicker = document.getElementById("picker-global-accent");
      const accText = document.getElementById("inp-global-accent");
      const tertPicker = document.getElementById("picker-global-tertiary");
      const tertText = document.getElementById("inp-global-tertiary");

      if (preset === "custom") {
        primPicker.style.boxShadow = "0 0 6px var(--studio-cyan)";
        accPicker.style.boxShadow = "0 0 6px var(--studio-purple)";
        if (tertPicker) tertPicker.style.boxShadow = "0 0 6px #ff0055";
        return;
      }
      primPicker.style.boxShadow = "none";
      accPicker.style.boxShadow = "none";
      if (tertPicker) tertPicker.style.boxShadow = "none";

      if (PRESET_COLORS[preset]) {
        primPicker.value = PRESET_COLORS[preset].primary;
        primText.value = PRESET_COLORS[preset].primary;
        accPicker.value = PRESET_COLORS[preset].accent;
        accText.value = PRESET_COLORS[preset].accent;
        if (tertPicker && tertText) {
          tertPicker.value = PRESET_COLORS[preset].tertiary || "#ff0055";
          tertText.value = PRESET_COLORS[preset].tertiary || "#ff0055";
        }
      }
    }

    function syncGlobalColor(type, from) {
      const picker = document.getElementById(`picker-global-${type}`);
      const text = document.getElementById(`inp-global-${type}`);
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
          picker.value = text.value;
        }
      }
      const selPreset = document.getElementById("sel-global-preset");
      if (selPreset && selPreset.value !== "custom") {
        selPreset.value = "custom";
        onGlobalPresetChange();
      }
    }

    async function applyGlobalThemeToAllBlocks(force = false) {
      const gStyle = document.getElementById("sel-global-style").value;
      const gPreset = document.getElementById("sel-global-preset").value;
      const gMode = document.getElementById("sel-global-mode").value;
      const gPrim = document.getElementById("inp-global-primary").value.trim();
      const gAcc = document.getElementById("inp-global-accent").value.trim();
      const gTert = document.getElementById("inp-global-tertiary") ? document.getElementById("inp-global-tertiary").value.trim() : "";

      try {
        const resp = await fetch("/api/template/apply_global_theme", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            style: gStyle,
            preset: gPreset,
            mode: gMode,
            primary: gPrim,
            accent: gAcc,
            tertiary: gTert,
            force: !!force
          })
        });
        if (resp.ok) {
          const msg = force ? "✓ FORCE OVERRIDE APPLIED TO ALL BLOCKS" : "✓ SOFT APPLY COMPLETED (ACCENTS PRESERVED)";
          flashNotification(msg, "var(--studio-green)");
          await loadTemplateBlocks(currentEditingBlockId);
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to apply global theme: " + err);
        }
      } catch (e) {
        alert("Error applying global theme: " + e);
      }
    }

    // --- Block Level Theme & Preset / Custom Hex Interaction ---
    function onInheritThemeToggle() {
      const inherit = document.getElementById("chk-inherit-theme").checked;
      const overrideBox = document.getElementById("block-theme-override-controls");
      if (inherit) {
        overrideBox.style.display = "none";
      } else {
        overrideBox.style.display = "block";
      }
      debounceRender();
    }

    function onBlockPresetChange() {
      const preset = document.getElementById("sel-preset").value;
      if (PRESET_COLORS[preset]) {
        document.getElementById("picker-primary").value = PRESET_COLORS[preset].primary;
        document.getElementById("inp-primary").value = PRESET_COLORS[preset].primary;
        document.getElementById("picker-accent").value = PRESET_COLORS[preset].accent;
        document.getElementById("inp-accent").value = PRESET_COLORS[preset].accent;
        if (document.getElementById("picker-tertiary")) {
          document.getElementById("picker-tertiary").value = PRESET_COLORS[preset].tertiary || "#ff0055";
          document.getElementById("inp-tertiary").value = PRESET_COLORS[preset].tertiary || "#ff0055";
        }
      }
      debounceRender();
    }

    function onBlockColorModeToggle() {
      const isCustom = document.getElementById("rad-custom").checked;
      const row = document.getElementById("row-custom-colors");
      if (isCustom) {
        row.style.opacity = "1";
        row.style.pointerEvents = "auto";
      } else {
        row.style.opacity = "0.4";
        row.style.pointerEvents = "none";
        onBlockPresetChange();
      }
      debounceRender();
    }

    function syncBlockColor(type, from) {
      document.getElementById("rad-custom").checked = true;
      document.getElementById("row-custom-colors").style.opacity = "1";
      document.getElementById("row-custom-colors").style.pointerEvents = "auto";

      const picker = document.getElementById(`picker-${type}`);
      const text = document.getElementById(`inp-${type}`);
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
          picker.value = text.value;
        }
      }
      debounceRender();
    }

    const GITHUB_ALERT_COLORS = {
      NOTE: "#2f81f7",
      TIP: "#238636",
      IMPORTANT: "#8957e5",
      WARNING: "#d29922",
      CAUTION: "#f85149",
      CRITICAL: "#f85149",
      SUCCESS: "#238636",
      INFO: "#8957e5"
    };

    function onQuoteBadgeChange() {
      const badge = document.getElementById("sel-quote-badge").value.toUpperCase();
      const isCustom = document.getElementById("chk-quote-custom-badge").checked;
      if (!isCustom && GITHUB_ALERT_COLORS[badge]) {
        document.getElementById("picker-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
        document.getElementById("inp-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
      }
      debounceRender();
    }

    function onQuoteCustomBadgeToggle() {
      const isCustom = document.getElementById("chk-quote-custom-badge").checked;
      document.getElementById("quote-badge-color-group").style.display = isCustom ? "block" : "none";
      if (!isCustom) {
        const badge = document.getElementById("sel-quote-badge").value.toUpperCase();
        if (GITHUB_ALERT_COLORS[badge]) {
          document.getElementById("picker-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
          document.getElementById("inp-quote-badge-color").value = GITHUB_ALERT_COLORS[badge];
        }
      }
      updateContextualVisibility();
      debounceRender();
    }

    function syncQuoteBadgeColor(from) {
      const picker = document.getElementById("picker-quote-badge-color");
      const text = document.getElementById("inp-quote-badge-color");
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) picker.value = text.value;
      }
      debounceRender();
    }

    function onCalloutTypeChange() {
      const ctype = document.getElementById("sel-callout-type").value.toUpperCase();
      const isCustom = document.getElementById("chk-callout-custom-badge").checked;
      if (!isCustom && GITHUB_ALERT_COLORS[ctype]) {
        document.getElementById("picker-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
        document.getElementById("inp-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
      }
      debounceRender();
    }

    function onCalloutCustomBadgeToggle() {
      const isCustom = document.getElementById("chk-callout-custom-badge").checked;
      document.getElementById("callout-badge-color-group").style.display = isCustom ? "block" : "none";
      if (!isCustom) {
        const ctype = document.getElementById("sel-callout-type").value.toUpperCase();
        if (GITHUB_ALERT_COLORS[ctype]) {
          document.getElementById("picker-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
          document.getElementById("inp-callout-badge-color").value = GITHUB_ALERT_COLORS[ctype];
        }
      }
      updateContextualVisibility();
      debounceRender();
    }

    function syncCalloutBadgeColor(from) {
      const picker = document.getElementById("picker-callout-badge-color");
      const text = document.getElementById("inp-callout-badge-color");
      if (from === "picker") {
        text.value = picker.value;
      } else {
        if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) picker.value = text.value;
      }
      debounceRender();
    }

    function syncProgressInput(from) {
      const rng = document.getElementById("rng-progress-val");
      const num = document.getElementById("inp-progress-val");
      const lbl = document.getElementById("lbl-progress-num");
      if (from === "range") {
        num.value = rng.value;
      } else {
        rng.value = num.value;
      }
      lbl.innerText = `${rng.value}%`;
      debounceRender();
    }

    function addSampleMilestone() {
      const area = document.getElementById("inp-timeline-milestones");
      const count = area.value.split("\n").filter(l => l.trim()).length + 1;
      const sample = `milestone title="PHASE ${count}: MILESTONE" date="2026-Q${count % 4 + 1}" status="PLANNED" desc="Milestone deliverables and specification"`;
      if (area.value.trim()) {
        area.value = area.value.trim() + "\n" + sample;
      } else {
        area.value = sample;
      }
      debounceRender();
    }

    function updateContextualVisibility() {
      const btype = document.getElementById("sel-type").value;
      if (btype === "chip") {
        const ct = document.getElementById("sel-chip-type").value;
        const gh = document.getElementById("sel-chip-gh").value;
        const gDecay = document.getElementById("group-decay-dir");
        const rChipForm = document.getElementById("row-chip-form");
        if (gDecay) {
          const isDecay = (ct === "decay");
          gDecay.style.display = isDecay ? "flex" : "none";
          if (rChipForm) rChipForm.style.gridTemplateColumns = isDecay ? "1fr 1fr" : "1fr";
        }
        const gRepo = document.getElementById("group-chip-repo");
        const rChipGh = document.getElementById("row-chip-gh");
        if (gRepo) {
          const hasGh = (gh !== "");
          gRepo.style.display = hasGh ? "flex" : "none";
          if (rChipGh) rChipGh.style.gridTemplateColumns = hasGh ? "1fr 1fr" : "1fr";
        }
      } else if (btype === "header") {
        const isCompact = document.getElementById("chk-compact").checked;
        const gSpecs = document.getElementById("group-header-specs");
        if (gSpecs) {
          gSpecs.style.display = isCompact ? "none" : "flex";
        }
      } else if (btype === "frame") {
        const fType = document.getElementById("sel-frame-type").value;
        const isBottom = (fType === "bottom");
        const gTag = document.getElementById("group-frame-tag");
        const rCap = document.getElementById("row-frame-cap");
        const gTitle = document.getElementById("group-frame-title");
        const gTagUrl = document.getElementById("group-frame-tag-url");
        const rLinks = document.getElementById("row-frame-links");

        if (gTag) gTag.style.display = isBottom ? "none" : "flex";
        if (rCap) rCap.style.gridTemplateColumns = isBottom ? "1fr" : "1fr 1fr";
        if (gTitle) gTitle.style.display = isBottom ? "none" : "flex";
        if (gTagUrl) gTagUrl.style.display = isBottom ? "none" : "flex";
        if (rLinks) rLinks.style.gridTemplateColumns = isBottom ? "1fr" : "1fr 1fr";
      } else if (btype === "quote") {
        const isCustom = document.getElementById("chk-quote-custom-badge").checked;
        const rBadge = document.getElementById("row-quote-badge");
        if (rBadge) rBadge.style.gridTemplateColumns = isCustom ? "1fr 1fr" : "1fr";
      } else if (btype === "callout") {
        const isCustom = document.getElementById("chk-callout-custom-badge").checked;
        const rBadge = document.getElementById("row-callout-badge");
        if (rBadge) rBadge.style.gridTemplateColumns = isCustom ? "1fr 1fr" : "1fr";
      }
    }

    function selectBlockFromPreview(blockId, event) {
      if (event) event.stopPropagation();
      openInspector();
      switchEditorMode('edit');

      const foundIdx = templateBlocks.findIndex(b => b.id === blockId);
      if (foundIdx !== -1) {
        document.getElementById("sel-existing-block").value = foundIdx;
        onSelectExistingBlock();
      }
      highlightBlockInPreview(blockId);
    }

    function highlightBlockInPreview(blockId) {
      document.querySelectorAll(".pk-block-wrapper").forEach(el => {
        el.classList.remove("selected-block");
      });
      const el = document.getElementById(`pk-block-${blockId}`);
      if (el) {
        el.classList.add("selected-block");
      }
    }

    function openInsertAt(afterId, event) {
      if (event) event.stopPropagation();
      targetInsertAfterId = afterId;
      openInspector();
      switchEditorMode('insert');

      const heading = document.getElementById("lbl-inspector-heading");
      heading.innerText = (afterId === -1) ? "■ INSERT BLOCK AT TOP" : `■ INSERT BLOCK AFTER #${afterId}`;

      document.getElementById("sel-type").value = "header";
      onTypeChange(true);
      document.getElementById("inp-title").value = "NEW PIXEL SECTION";
      document.getElementById("inp-subtitle").value = "SECTION DESCRIPTION // SUBTITLE";
      document.getElementById("inp-tag").value = "STATUS_OK";
      renderCurrentBlock();
    }

    function cancelInsertMode() {
      switchEditorMode('edit');
      if (templateBlocks.length > 0) {
        onSelectExistingBlock();
      }
    }

    function switchEditorMode(mode) {
      editorMode = mode;
      const grpExisting = document.getElementById("group-existing-blocks");
      const editActions = document.getElementById("edit-mode-actions");
      const insertActions = document.getElementById("insert-mode-actions");
      const heading = document.getElementById("lbl-inspector-heading");
      const selType = document.getElementById("sel-type");
      const badgeLock = document.getElementById("badge-lock-type");

      if (mode === "edit") {
        grpExisting.style.display = "flex";
        editActions.style.display = "grid";
        insertActions.style.display = "none";
        heading.innerText = "■ EDIT BLOCK PARAMETERS";
        selType.disabled = true;
        selType.title = "Block type cannot be changed after creation. To use another type, insert a new block.";
        if (badgeLock) badgeLock.style.display = "inline-block";
      } else {
        grpExisting.style.display = "none";
        editActions.style.display = "none";
        insertActions.style.display = "grid";
        selType.disabled = false;
        selType.title = "";
        if (badgeLock) badgeLock.style.display = "none";
      }
    }

    async function loadTemplateBlocks(preferredId = null) {
      try {
        const resp = await fetch("/api/template/blocks");
        if (resp.ok) {
          const data = await resp.json();
          templateBlocks = data.blocks || [];
          const sel = document.getElementById("sel-existing-block");
          sel.innerHTML = "";

          const badge = document.getElementById("block-counter-badge");
          if (badge) badge.innerText = `${templateBlocks.length} blocks`;

          if (templateBlocks.length === 0) {
            sel.innerHTML = "<option value=''>No pixel-kit blocks found</option>";
            return;
          }

          templateBlocks.forEach((blk, idx) => {
            const opt = document.createElement("option");
            opt.value = idx;
            const btype = blk.type.toUpperCase();
            const title = blk.attrs.title || blk.attrs.text || blk.attrs.label || blk.attrs.status || (blk.type === "divider" ? "DIVIDER" : "");
            const displayTitle = title ? ` // ${title.slice(0, 30)}` : "";
            opt.innerText = `[#${blk.id}] ${btype}${displayTitle}`;
            sel.appendChild(opt);
          });

          let targetIndex = 0;
          if (preferredId !== null) {
            const foundIdx = templateBlocks.findIndex(b => b.id === preferredId);
            if (foundIdx !== -1) targetIndex = foundIdx;
          }
          sel.value = targetIndex;
          if (editorMode === "edit" && templateBlocks[targetIndex]) {
            onSelectExistingBlock();
          }
        }
      } catch (e) {
        console.error("Failed to load template blocks:", e);
      }
    }

    function onSelectExistingBlock() {
      const sel = document.getElementById("sel-existing-block");
      const idx = parseInt(sel.value, 10);
      if (isNaN(idx) || !templateBlocks[idx]) return;

      const blk = templateBlocks[idx];
      currentEditingBlockId = blk.id;
      currentEditingBlockOriginal = blk;

      const heading = document.getElementById("lbl-inspector-heading");
      heading.innerText = `■ EDIT BLOCK #${blk.id}: ${blk.type.toUpperCase()}`;

      const selType = document.getElementById("sel-type");
      selType.value = blk.type;
      onTypeChange(false);

      const attrs = blk.attrs || {};

      // Check whether this block uses custom theme overrides or inherits
      const hasCustomStyle = !!attrs.style;
      const hasCustomPreset = !!attrs.preset;
      const hasCustomColors = !!(attrs.primary || attrs.accent || attrs.tertiary);
      const isCustomOverride = hasCustomStyle || hasCustomPreset || hasCustomColors;

      const chkInherit = document.getElementById("chk-inherit-theme");
      chkInherit.checked = !isCustomOverride;
      onInheritThemeToggle();

      if (attrs.style) document.getElementById("sel-style").value = attrs.style;
      if (attrs.preset) document.getElementById("sel-preset").value = attrs.preset;
      if (attrs.mode) document.getElementById("sel-mode").value = attrs.mode;

      if (hasCustomColors) {
        document.getElementById("rad-custom").checked = true;
        document.getElementById("row-custom-colors").style.opacity = "1";
        document.getElementById("row-custom-colors").style.pointerEvents = "auto";
        if (attrs.primary) {
          document.getElementById("inp-primary").value = attrs.primary;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.primary)) document.getElementById("picker-primary").value = attrs.primary;
        }
        if (attrs.accent) {
          document.getElementById("inp-accent").value = attrs.accent;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.accent)) document.getElementById("picker-accent").value = attrs.accent;
        }
        if (attrs.tertiary) {
          document.getElementById("inp-tertiary").value = attrs.tertiary;
          if (/^#[0-9A-Fa-f]{6}$/.test(attrs.tertiary)) document.getElementById("picker-tertiary").value = attrs.tertiary;
        }
      } else {
        document.getElementById("rad-preset").checked = true;
        document.getElementById("row-custom-colors").style.opacity = "0.4";
        document.getElementById("row-custom-colors").style.pointerEvents = "none";
        onBlockPresetChange();
      }

      // 1. Header
      document.getElementById("inp-title").value = attrs.title || attrs.text || attrs.label || attrs.status || "";
      document.getElementById("inp-subtitle").value = attrs.subtitle || attrs.sub || "";
      document.getElementById("inp-tag").value = attrs.tag || "";
      document.getElementById("inp-spec1").value = attrs.spec1 || "";
      document.getElementById("inp-spec2").value = attrs.spec2 || "";
      document.getElementById("inp-spec3").value = attrs.spec3 || "";
      document.getElementById("inp-tag-url").value = attrs.tag_url || attrs.tag_href || "";
      document.getElementById("inp-close-url").value = attrs.close_url || attrs.close_href || "";
      document.getElementById("chk-compact").checked = (attrs.compact === "true" || attrs.compact === "1");

      // 2. Timeline
      document.getElementById("inp-timeline-milestones").value = blk.body || "";

      // 3. Window
      document.getElementById("inp-window-title").value = attrs.title || "SYSTEM.WINDOW";
      document.getElementById("inp-window-tag").value = attrs.tag || "[SYS_LOG]";
      document.getElementById("inp-window-tag-url").value = attrs.tag_url || "";
      document.getElementById("inp-window-close-url").value = attrs.close_url || "";

      // 4. Terminal
      document.getElementById("inp-terminal-title").value = attrs.title || "HUD.TERMINAL";
      document.getElementById("sel-terminal-state").value = (attrs.state && attrs.state.toLowerCase() === "closed") ? "closed" : "open";

      // 5. Quote
      document.getElementById("inp-quote-title").value = attrs.title || "SPECIFICATION NOTICE";
      document.getElementById("inp-quote-sub").value = attrs.subtitle || "";
      const qBadgeVal = (attrs.badge || "NOTE").toUpperCase();
      document.getElementById("sel-quote-badge").value = qBadgeVal;
      if (attrs.badge_color) {
        document.getElementById("chk-quote-custom-badge").checked = true;
        document.getElementById("quote-badge-color-group").style.display = "block";
        document.getElementById("picker-quote-badge-color").value = attrs.badge_color;
        document.getElementById("inp-quote-badge-color").value = attrs.badge_color;
      } else {
        document.getElementById("chk-quote-custom-badge").checked = false;
        document.getElementById("quote-badge-color-group").style.display = "none";
        const defCol = GITHUB_ALERT_COLORS[qBadgeVal] || "#2f81f7";
        document.getElementById("picker-quote-badge-color").value = defCol;
        document.getElementById("inp-quote-badge-color").value = defCol;
      }

      // 6. Chip
      document.getElementById("inp-chip-text").value = attrs.text || attrs.title || "CHIP";
      if (attrs.type) document.getElementById("sel-chip-type").value = attrs.type;
      if (attrs.decay_dir) document.getElementById("sel-decay-dir").value = attrs.decay_dir;
      if (attrs.github) document.getElementById("sel-chip-gh").value = attrs.github;
      if (attrs.repo) document.getElementById("inp-chip-repo").value = attrs.repo;
      document.getElementById("inp-chip-width").value = attrs.width || "";
      document.getElementById("inp-chip-url").value = attrs.url || attrs.href || "";

      // 7. Metrics
      document.getElementById("inp-metrics-items").value = attrs.items || blk.body || "";
      document.getElementById("inp-metrics-label").value = attrs.label || attrs.title || "";
      document.getElementById("inp-metrics-val").value = attrs.value || attrs.subtitle || "";
      document.getElementById("inp-metrics-delta").value = attrs.delta || attrs.tag || "";
      document.getElementById("inp-metrics-status").value = attrs.status || "";

      // 8. Progress
      const pVal = parseInt(attrs.value || attrs.tag || "75", 10) || 75;
      document.getElementById("rng-progress-val").value = pVal;
      document.getElementById("inp-progress-val").value = pVal;
      document.getElementById("lbl-progress-num").innerText = `${pVal}%`;
      document.getElementById("inp-progress-label").value = attrs.label || attrs.title || "PROGRESS";
      document.getElementById("inp-progress-sub").value = attrs.sub || attrs.subtitle || "";

      // 9. Techstack
      document.getElementById("inp-techstack-items").value = attrs.items || attrs.subtitle || "python,cpp,docker,git";
      document.getElementById("inp-techstack-cols").value = attrs.columns || attrs.tag || "5";

      // 10. Callout
      const cTypeVal = (attrs.type || "note").toLowerCase();
      document.getElementById("sel-callout-type").value = cTypeVal;
      document.getElementById("inp-callout-title").value = attrs.title || "SYSTEM SPECIFICATION";
      document.getElementById("inp-callout-sub").value = attrs.subtitle || "";
      document.getElementById("chk-callout-quote").checked = (attrs.quote === "true" || attrs.quote === "1");
      if (attrs.badge_color) {
        document.getElementById("chk-callout-custom-badge").checked = true;
        document.getElementById("callout-badge-color-group").style.display = "block";
        document.getElementById("picker-callout-badge-color").value = attrs.badge_color;
        document.getElementById("inp-callout-badge-color").value = attrs.badge_color;
      } else {
        document.getElementById("chk-callout-custom-badge").checked = false;
        document.getElementById("callout-badge-color-group").style.display = "none";
        const defCol = GITHUB_ALERT_COLORS[cTypeVal.toUpperCase()] || "#2f81f7";
        document.getElementById("picker-callout-badge-color").value = defCol;
        document.getElementById("inp-callout-badge-color").value = defCol;
      }

      // 11. Frame
      if (attrs.type) document.getElementById("sel-frame-type").value = attrs.type;
      document.getElementById("inp-frame-title").value = attrs.title || "SYSTEM.CORE";
      document.getElementById("inp-frame-tag").value = attrs.tag || "[OPEN_HUD]";
      document.getElementById("inp-frame-tag-url").value = attrs.tag_url || "";
      document.getElementById("inp-frame-close-url").value = attrs.close_url || "";

      // 13. Splitter
      document.getElementById("inp-splitter-label").value = attrs.label || attrs.title || "[SUB_MODULE]";

      // 14. Footer
      document.getElementById("inp-footer-status").value = attrs.status || attrs.title || "SESSION_ACTIVE // STANDBY";
      document.getElementById("inp-footer-nav").value = attrs.nav || attrs.tag || "▲ RETURN TO TOP";
      document.getElementById("inp-footer-sub").value = attrs.sub || attrs.subtitle || "";

      // 15. Social
      document.getElementById("inp-social-title").value = attrs.title || "PIXEL README KIT";
      document.getElementById("inp-social-sub").value = attrs.subtitle || "";
      document.getElementById("inp-social-repo").value = attrs.repo || "Kazinagg/pixel-readme-kit";
      document.getElementById("inp-social-tags").value = attrs.tags || attrs.tag || "PYTHON,SVG";

      // Generic container body
      document.getElementById("inp-body").value = blk.body || "";

      highlightBlockInPreview(blk.id);
      updateContextualVisibility();
      renderCurrentBlock();
    }

    function onTypeChange(resetValues = true) {
      const type = document.getElementById("sel-type").value;

      const sections = {
        header: document.getElementById("section-header"),
        timeline: document.getElementById("section-timeline"),
        window: document.getElementById("section-window"),
        terminal: document.getElementById("section-terminal"),
        quote: document.getElementById("section-quote"),
        chip: document.getElementById("section-chip"),
        metrics: document.getElementById("section-metrics"),
        progress: document.getElementById("section-progress"),
        techstack: document.getElementById("section-techstack"),
        callout: document.getElementById("section-callout"),
        frame: document.getElementById("section-frame"),
        divider: document.getElementById("section-divider"),
        splitter: document.getElementById("section-splitter"),
        footer: document.getElementById("section-footer"),
        social: document.getElementById("section-social"),
        body: document.getElementById("section-body")
      };

      for (let k in sections) {
        if (sections[k]) sections[k].style.display = "none";
      }

      if (sections[type]) {
        sections[type].style.display = "flex";
      }

      if (type === "header" || type === "starchart" || type === "profile") {
        if (sections.header) sections.header.style.display = "flex";
      }

      // Container markdown body section
      if (type === "window" || type === "terminal" || type === "quote") {
        sections.body.style.display = "flex";
      }

      updateCharCounters();
      updateContextualVisibility();
      renderCurrentBlock();
    }

    function generateDirectiveCode() {
      const btype = document.getElementById("sel-type").value;
      const inheritTheme = document.getElementById("chk-inherit-theme").checked;

      let style = document.getElementById("sel-global-style").value;
      let preset = document.getElementById("sel-global-preset").value;
      let mode = document.getElementById("sel-global-mode").value;
      let isCustomColors = false;
      let prim = "";
      let acc = "";
      let tert = "";

      if (!inheritTheme) {
        style = document.getElementById("sel-style").value;
        preset = document.getElementById("sel-preset").value;
        mode = document.getElementById("sel-mode").value;
        isCustomColors = document.getElementById("rad-custom").checked;
        if (isCustomColors) {
          prim = document.getElementById("inp-primary").value.trim();
          acc = document.getElementById("inp-accent").value.trim();
          tert = document.getElementById("inp-tertiary") ? document.getElementById("inp-tertiary").value.trim() : "";
        }
      }

      const origAttrs = (currentEditingBlockOriginal && currentEditingBlockOriginal.attrs) ? currentEditingBlockOriginal.attrs : {};

      let opening = `<!-- pixel-kit:${btype}`;
      if (!inheritTheme) {
        if (style) opening += ` style="${style}"`;
        if (preset) opening += ` preset="${preset}"`;
        if (mode && mode !== "auto") opening += ` mode="${mode}"`;
        if (isCustomColors && prim) opening += ` primary="${prim}"`;
        if (isCustomColors && acc) opening += ` accent="${acc}"`;
        if (isCustomColors && tert) opening += ` tertiary="${tert}"`;
      }

      let innerBody = "";

      if (btype === "header") {
        const title = document.getElementById("inp-title").value.trim();
        const sub = document.getElementById("inp-subtitle").value.trim();
        const tag = document.getElementById("inp-tag").value.trim();
        const s1 = document.getElementById("inp-spec1").value.trim();
        const s2 = document.getElementById("inp-spec2").value.trim();
        const s3 = document.getElementById("inp-spec3").value.trim();
        const tUrl = document.getElementById("inp-tag-url").value.trim();
        const cUrl = document.getElementById("inp-close-url").value.trim();
        const compact = document.getElementById("chk-compact").checked;

        if (title) opening += ` title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (tag) opening += ` tag="${tag}"`;
        if (!compact && s1) opening += ` spec1="${s1}"`;
        if (!compact && s2) opening += ` spec2="${s2}"`;
        if (!compact && s3) opening += ` spec3="${s3}"`;
        if (tUrl) opening += ` tag_url="${tUrl}"`;
        if (cUrl) opening += ` close_url="${cUrl}"`;
        if (compact) opening += ` compact="true"`;
      } else if (btype === "timeline") {
        innerBody = document.getElementById("inp-timeline-milestones").value.trim();
      } else if (btype === "window") {
        const title = document.getElementById("inp-window-title").value.trim();
        const tag = document.getElementById("inp-window-tag").value.trim();
        const tUrl = document.getElementById("inp-window-tag-url").value.trim();
        const cUrl = document.getElementById("inp-window-close-url").value.trim();
        if (title) opening += ` title="${title}"`;
        if (tag) opening += ` tag="${tag}"`;
        if (tUrl) opening += ` tag_url="${tUrl}"`;
        if (cUrl) opening += ` close_url="${cUrl}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "terminal") {
        const title = document.getElementById("inp-terminal-title").value.trim();
        const state = document.getElementById("sel-terminal-state").value;
        if (title) opening += ` title="${title}"`;
        if (state) opening += ` state="${state}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "quote") {
        const title = document.getElementById("inp-quote-title").value.trim();
        const sub = document.getElementById("inp-quote-sub").value.trim();
        const badge = document.getElementById("sel-quote-badge").value;
        const isCustomBadge = document.getElementById("chk-quote-custom-badge").checked;
        const bCol = document.getElementById("inp-quote-badge-color").value.trim();
        if (title) opening += ` title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (badge) opening += ` badge="${badge}"`;
        if (isCustomBadge && bCol) opening += ` badge_color="${bCol}"`;
        innerBody = document.getElementById("inp-body").value;
      } else if (btype === "chip") {
        const text = document.getElementById("inp-chip-text").value.trim();
        const ctype = document.getElementById("sel-chip-type").value;
        const decay = document.getElementById("sel-decay-dir").value;
        const gh = document.getElementById("sel-chip-gh").value;
        const repo = document.getElementById("inp-chip-repo").value.trim();
        const w = document.getElementById("inp-chip-width").value.trim();
        const url = document.getElementById("inp-chip-url").value.trim();

        if (text) opening += ` text="${text}"`;
        if (ctype && ctype !== "closed") opening += ` type="${ctype}"`;
        if (ctype === "decay" && decay && decay !== "right") opening += ` decay_dir="${decay}"`;
        if (gh) opening += ` github="${gh}"`;
        if (gh && repo) opening += ` repo="${repo}"`;
        if (w) opening += ` width="${w}"`;
        if (url) opening += ` url="${url}"`;
      } else if (btype === "metrics") {
        const items = document.getElementById("inp-metrics-items").value.trim();
        const lbl = document.getElementById("inp-metrics-label").value.trim();
        const val = document.getElementById("inp-metrics-val").value.trim();
        const delta = document.getElementById("inp-metrics-delta").value.trim();
        const st = document.getElementById("inp-metrics-status").value.trim();

        if (items.includes("\n") || items.startsWith("-")) {
          innerBody = items;
        } else if (items) {
          opening += ` items="${items}"`;
        } else {
          if (lbl) opening += ` label="${lbl}"`;
          if (val) opening += ` value="${val}"`;
          if (delta) opening += ` delta="${delta}"`;
          if (st) opening += ` status="${st}"`;
        }
      } else if (btype === "progress") {
        const val = document.getElementById("inp-progress-val").value;
        const lbl = document.getElementById("inp-progress-label").value.trim();
        const sub = document.getElementById("inp-progress-sub").value.trim();
        opening += ` value="${val}" label="${lbl}"`;
        if (sub) opening += ` sub="${sub}"`;
      } else if (btype === "techstack") {
        const items = document.getElementById("inp-techstack-items").value.trim();
        const cols = document.getElementById("inp-techstack-cols").value.trim();
        opening += ` items="${items}" columns="${cols}"`;
      } else if (btype === "callout") {
        const ctype = document.getElementById("sel-callout-type").value;
        const title = document.getElementById("inp-callout-title").value.trim();
        const sub = document.getElementById("inp-callout-sub").value.trim();
        const quote = document.getElementById("chk-callout-quote").checked;
        const isCustomBadge = document.getElementById("chk-callout-custom-badge").checked;
        const bCol = document.getElementById("inp-callout-badge-color").value.trim();
        opening += ` type="${ctype}" title="${title}"`;
        if (sub) opening += ` subtitle="${sub}"`;
        if (quote) opening += ` quote="true"`;
        if (isCustomBadge && bCol) opening += ` badge_color="${bCol}"`;
      } else if (btype === "frame") {
        const ftype = document.getElementById("sel-frame-type").value;
        const title = document.getElementById("inp-frame-title").value.trim();
        const tag = document.getElementById("inp-frame-tag").value.trim();
        const tUrl = document.getElementById("inp-frame-tag-url").value.trim();
        const cUrl = document.getElementById("inp-frame-close-url").value.trim();
        if (ftype === "bottom") {
          opening += ` type="bottom"`;
          if (cUrl) opening += ` close_url="${cUrl}"`;
        } else {
          opening += ` type="top" title="${title}" tag="${tag}"`;
          if (tUrl) opening += ` tag_url="${tUrl}"`;
          if (cUrl) opening += ` close_url="${cUrl}"`;
        }
      } else if (btype === "splitter") {
        const lbl = document.getElementById("inp-splitter-label").value.trim();
        opening += ` label="${lbl}"`;
      } else if (btype === "footer") {
        const st = document.getElementById("inp-footer-status").value.trim();
        const nav = document.getElementById("inp-footer-nav").value.trim();
        const sub = document.getElementById("inp-footer-sub").value.trim();
        opening += ` status="${st}" nav="${nav}"`;
        if (sub) opening += ` sub="${sub}"`;
      } else if (btype === "social") {
        const title = document.getElementById("inp-social-title").value.trim();
        const sub = document.getElementById("inp-social-sub").value.trim();
        const repo = document.getElementById("inp-social-repo").value.trim();
        const tags = document.getElementById("inp-social-tags").value.trim();
        opening += ` title="${title}" subtitle="${sub}" repo="${repo}" tags="${tags}"`;
      } else if (btype === "starchart") {
        const repo = document.getElementById("inp-title").value.trim() || "Kazinagg/pixel-readme-kit";
        opening += ` repo="${repo}" points="15,65,190,480,950,1650" current="1,650" delta="+78% past 6m" title="STAR GROWTH TRAJECTORY"`;
      } else if (btype === "profile") {
        const name = document.getElementById("inp-title").value.trim() || "ALEX DEVELOPER";
        const role = document.getElementById("inp-subtitle").value.trim() || "FULLSTACK & SYSTEMS ARCHITECT";
        opening += ` name="${name}" role="${role}" bio="Building high-performance runtimes and resilient developer tooling." status="AVAILABLE FOR HIRE" location="REMOTE" badge="LEVEL_99"`;
      }

      if (origAttrs.out) opening += ` out="${origAttrs.out}"`;
      opening += ` -->`;

      const isContainerType = (btype === "window" || btype === "terminal" || btype === "quote" || btype === "timeline" || (btype === "metrics" && innerBody));
      if (isContainerType) {
        return `${opening}\n${innerBody}\n<!-- /pixel-kit:${btype} -->`;
      }
      return opening;
    }

    function onRawDirectiveManualEdit() {
      if (isParsingRaw) return;
      const raw = document.getElementById("txt-raw-directive").value;
      const m = raw.match(/<!--\s*pixel-kit:([a-zA-Z0-9_\-]+)\b([\s\S]*?)-->/i);
      if (!m) return;

      isParsingRaw = true;
      try {
        const btype = m[1].toLowerCase();
        const attrStr = m[2];
        const selType = document.getElementById("sel-type");
        if (editorMode === "insert" && selType.querySelector(`option[value="${btype}"]`)) {
          selType.value = btype;
          onTypeChange(false);
        }

        const attrRegex = /([\w\-]+)=(?:"([^"]*)"|'([^']*)'|([^\s>]+))/g;
        let match;
        const parsed = {};
        while ((match = attrRegex.exec(attrStr)) !== null) {
          const key = match[1].toLowerCase();
          const val = match[2] !== undefined ? match[2] : (match[3] !== undefined ? match[3] : match[4]);
          parsed[key] = val;
        }

        const hasCustom = parsed.style || parsed.preset || parsed.primary || parsed.accent;
        document.getElementById("chk-inherit-theme").checked = !hasCustom;
        onInheritThemeToggle();

        if (parsed.style) document.getElementById("sel-style").value = parsed.style;
        if (parsed.preset) document.getElementById("sel-preset").value = parsed.preset;
        if (parsed.mode) document.getElementById("sel-mode").value = parsed.mode;
        if (parsed.primary || parsed.accent) {
          document.getElementById("rad-custom").checked = true;
          document.getElementById("row-custom-colors").style.opacity = "1";
          document.getElementById("row-custom-colors").style.pointerEvents = "auto";
          if (parsed.primary) {
            document.getElementById("inp-primary").value = parsed.primary;
            if (/^#[0-9A-Fa-f]{6}$/.test(parsed.primary)) document.getElementById("picker-primary").value = parsed.primary;
          }
          if (parsed.accent) {
            document.getElementById("inp-accent").value = parsed.accent;
            if (/^#[0-9A-Fa-f]{6}$/.test(parsed.accent)) document.getElementById("picker-accent").value = parsed.accent;
          }
        }

        if (parsed.title) document.getElementById("inp-title").value = parsed.title;
        if (parsed.subtitle) document.getElementById("inp-subtitle").value = parsed.subtitle;
        if (parsed.tag) document.getElementById("inp-tag").value = parsed.tag;
        if (parsed.spec1) document.getElementById("inp-spec1").value = parsed.spec1;
        if (parsed.spec2) document.getElementById("inp-spec2").value = parsed.spec2;
        if (parsed.spec3) document.getElementById("inp-spec3").value = parsed.spec3;
        if (parsed.compact !== undefined) document.getElementById("chk-compact").checked = (parsed.compact === "true" || parsed.compact === "1");

        updateCharCounters();
        updateContextualVisibility();
        renderCurrentBlock(false);
      } finally {
        isParsingRaw = false;
      }
    }

    function updateCharCounters() {
      const title = document.getElementById("inp-title").value || "";
      const sub = document.getElementById("inp-subtitle").value || "";
      const s1 = document.getElementById("inp-spec1").value || "";
      const s2 = document.getElementById("inp-spec2").value || "";
      const s3 = document.getElementById("inp-spec3").value || "";

      const bTitle = document.getElementById("badge-title-budget");
      const bSub = document.getElementById("badge-sub-budget");
      const bS1 = document.getElementById("badge-spec1-budget");
      const bS2 = document.getElementById("badge-spec2-budget");
      const bS3 = document.getElementById("badge-spec3-budget");

      if (bTitle) {
        const len = title.length;
        bTitle.innerText = `${len} chars`;
        bTitle.className = "char-badge " + (len <= 14 ? "badge-optimal" : (len <= 20 ? "badge-warning" : "badge-danger"));
      }
      if (bSub) {
        const len = sub.length;
        bSub.innerText = `${len} chars`;
        bSub.className = "char-badge " + (len <= 45 ? "badge-optimal" : "badge-warning");
      }
      if (bS1) {
        const len = s1.length;
        bS1.innerText = `${len} chars`;
        bS1.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
      if (bS2) {
        const len = s2.length;
        bS2.innerText = `${len} chars`;
        bS2.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
      if (bS3) {
        const len = s3.length;
        bS3.innerText = `${len} chars`;
        bS3.className = "char-badge " + (len <= 32 ? "badge-optimal" : "badge-warning");
      }
    }

    function debounceRender() {
      updateCharCounters();
      if (!isParsingRaw) {
        const rawCode = generateDirectiveCode();
        document.getElementById("txt-raw-directive").value = rawCode;
      }
      clearTimeout(renderTimer);
      renderTimer = setTimeout(renderCurrentBlock, 60);
    }

    async function renderCurrentBlock(updateRaw = true) {
      const t0 = performance.now();
      const btype = document.getElementById("sel-type").value;
      const inheritTheme = document.getElementById("chk-inherit-theme").checked;

      let style = document.getElementById("sel-global-style").value;
      let preset = document.getElementById("sel-global-preset").value;
      let mode = document.getElementById("sel-global-mode").value;
      let prim = "";
      let acc = "";
      let tert = "";

      if (!inheritTheme) {
        style = document.getElementById("sel-style").value;
        preset = document.getElementById("sel-preset").value;
        mode = document.getElementById("sel-mode").value;
        if (document.getElementById("rad-custom").checked) {
          prim = document.getElementById("inp-primary").value.trim();
          acc = document.getElementById("inp-accent").value.trim();
          tert = document.getElementById("inp-tertiary") ? document.getElementById("inp-tertiary").value.trim() : "";
        }
      }

      // If mode is auto, force the current preview theme mode so the user sees the SVG in chosen theme
      let effectiveRenderMode = mode;
      if (mode === "auto") {
        effectiveRenderMode = activePreviewTheme;
      }

      if (updateRaw && !isParsingRaw) {
        const rawCode = generateDirectiveCode();
        document.getElementById("txt-raw-directive").value = rawCode;
      }

      const params = new URLSearchParams({
        block_type: btype,
        style: style,
        preset: preset,
        mode: effectiveRenderMode
      });
      if (prim) params.set("primary", prim);
      if (acc) params.set("accent", acc);
      if (tert) params.set("tertiary", tert);

      if (btype === "header") {
        params.set("title", document.getElementById("inp-title").value);
        params.set("subtitle", document.getElementById("inp-subtitle").value);
        params.set("tag", document.getElementById("inp-tag").value);
        params.set("spec1", document.getElementById("inp-spec1").value);
        params.set("spec2", document.getElementById("inp-spec2").value);
        params.set("spec3", document.getElementById("inp-spec3").value);
        params.set("tag_url", document.getElementById("inp-tag-url").value);
        params.set("close_url", document.getElementById("inp-close-url").value);
        params.set("compact", document.getElementById("chk-compact").checked ? "true" : "false");
      } else if (btype === "timeline") {
        params.set("body", document.getElementById("inp-timeline-milestones").value);
      } else if (btype === "window") {
        params.set("title", document.getElementById("inp-window-title").value);
        params.set("tag", document.getElementById("inp-window-tag").value);
      } else if (btype === "terminal") {
        params.set("title", document.getElementById("inp-terminal-title").value);
      } else if (btype === "quote") {
        params.set("title", document.getElementById("inp-quote-title").value);
        params.set("subtitle", document.getElementById("inp-quote-sub").value);
        const qBadge = document.getElementById("sel-quote-badge").value;
        params.set("badge", qBadge);
        if (document.getElementById("chk-quote-custom-badge").checked) {
          const bCol = document.getElementById("inp-quote-badge-color").value.trim();
          if (bCol) params.set("badge_color", bCol);
        } else if (GITHUB_ALERT_COLORS[qBadge.toUpperCase()]) {
          params.set("badge_color", GITHUB_ALERT_COLORS[qBadge.toUpperCase()]);
        }
      } else if (btype === "chip") {
        params.set("title", document.getElementById("inp-chip-text").value);
        params.set("type", document.getElementById("sel-chip-type").value);
        params.set("decay_dir", document.getElementById("sel-decay-dir").value);
        params.set("github", document.getElementById("sel-chip-gh").value);
        params.set("repo", document.getElementById("inp-chip-repo").value);
        params.set("width", document.getElementById("inp-chip-width").value);
      } else if (btype === "metrics") {
        params.set("items", document.getElementById("inp-metrics-items").value);
        params.set("title", document.getElementById("inp-metrics-label").value);
        params.set("subtitle", document.getElementById("inp-metrics-val").value);
        params.set("delta", document.getElementById("inp-metrics-delta").value);
        params.set("status", document.getElementById("inp-metrics-status").value);
      } else if (btype === "progress") {
        params.set("value", document.getElementById("inp-progress-val").value);
        params.set("title", document.getElementById("inp-progress-label").value);
        params.set("sub", document.getElementById("inp-progress-sub").value);
      } else if (btype === "techstack") {
        params.set("items", document.getElementById("inp-techstack-items").value);
        params.set("columns", document.getElementById("inp-techstack-cols").value);
      } else if (btype === "callout") {
        const cType = document.getElementById("sel-callout-type").value;
        params.set("type", cType);
        params.set("title", document.getElementById("inp-callout-title").value);
        params.set("subtitle", document.getElementById("inp-callout-sub").value);
        params.set("quote", document.getElementById("chk-callout-quote").checked ? "true" : "false");
        if (document.getElementById("chk-callout-custom-badge").checked) {
          const bCol = document.getElementById("inp-callout-badge-color").value.trim();
          if (bCol) params.set("badge_color", bCol);
        } else if (GITHUB_ALERT_COLORS[cType.toUpperCase()]) {
          params.set("badge_color", GITHUB_ALERT_COLORS[cType.toUpperCase()]);
        }
      } else if (btype === "frame") {
        params.set("type", document.getElementById("sel-frame-type").value);
        params.set("title", document.getElementById("inp-frame-title").value);
        params.set("tag", document.getElementById("inp-frame-tag").value);
        params.set("tag_url", document.getElementById("inp-frame-tag-url").value);
        params.set("close_url", document.getElementById("inp-frame-close-url").value);
      } else if (btype === "splitter") {
        params.set("title", document.getElementById("inp-splitter-label").value);
      } else if (btype === "footer") {
        params.set("status", document.getElementById("inp-footer-status").value);
        params.set("nav", document.getElementById("inp-footer-nav").value);
        params.set("sub", document.getElementById("inp-footer-sub").value);
      } else if (btype === "social") {
        params.set("title", document.getElementById("inp-social-title").value);
        params.set("subtitle", document.getElementById("inp-social-sub").value);
        params.set("repo", document.getElementById("inp-social-repo").value);
        params.set("tags", document.getElementById("inp-social-tags").value);
      } else if (btype === "starchart") {
        params.set("repo", document.getElementById("inp-title").value || "Kazinagg/pixel-readme-kit");
        params.set("title", "STAR GROWTH TRAJECTORY");
        params.set("points", "15,65,190,480,950,1650");
        params.set("current", "1,650");
        params.set("delta", "+78% past 6m");
      } else if (btype === "profile") {
        params.set("name", document.getElementById("inp-title").value || "ALEX DEVELOPER");
        params.set("role", document.getElementById("inp-subtitle").value || "FULLSTACK & SYSTEMS ARCHITECT");
        params.set("status", "AVAILABLE FOR HIRE");
        params.set("location", "REMOTE // UTC+3");
        params.set("badge", "LEVEL_99");
      }

      try {
        const resp = await fetch(`/api/render?${params.toString()}`);
        if (resp.ok) {
          const svgText = await resp.text();
          const mount = document.getElementById("svg-render-mount");
          // Use Shadow DOM to prevent any <style>:root in SVG from leaking into Studio UI
          if (!mount.shadowRoot) {
            mount.attachShadow({ mode: "open" });
          }
          mount.shadowRoot.innerHTML = svgText;
          const dt = Math.round(performance.now() - t0);
          document.getElementById("render-latency").innerText = `${dt}ms`;
        }
      } catch (err) {
        console.error("Render block error:", err);
      }
    }

    async function saveExistingBlockChanges() {
      if (currentEditingBlockId === null) {
        alert("No block selected to update.");
        return;
      }
      const newRaw = document.getElementById("txt-raw-directive").value.trim() || generateDirectiveCode();
      try {
        const resp = await fetch("/api/template/update_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            id: currentEditingBlockId,
            directive_raw: newRaw
          })
        });
        if (resp.ok) {
          flashNotification("✓ BLOCK SAVED & RECOMPILED", "var(--studio-green)");
          const keepId = currentEditingBlockId;
          await loadTemplateBlocks(keepId);
          await loadCompiledPreview();
          highlightBlockInPreview(keepId);
        } else {
          const err = await resp.text();
          alert("Failed to update block: " + err);
        }
      } catch (e) {
        alert("Error saving block: " + e);
      }
    }

    async function executeInsertBlock() {
      const newRaw = document.getElementById("txt-raw-directive").value.trim() || generateDirectiveCode();
      try {
        const resp = await fetch("/api/template/insert_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            after_id: targetInsertAfterId,
            directive_raw: newRaw
          })
        });
        if (resp.ok) {
          flashNotification("✓ NEW BLOCK INSERTED", "var(--studio-green)");
          switchEditorMode('edit');
          await loadTemplateBlocks();
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to insert block: " + err);
        }
      } catch (e) {
        alert("Error inserting block: " + e);
      }
    }

    function confirmDeleteBlock(blockId, event) {
      if (event) event.stopPropagation();
      currentEditingBlockId = blockId;
      deleteExistingBlock();
    }

    async function deleteExistingBlock() {
      if (currentEditingBlockId === null) return;
      if (!confirm(`Delete block #${currentEditingBlockId} from template?`)) return;
      try {
        const resp = await fetch("/api/template/delete_block", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id: currentEditingBlockId })
        });
        if (resp.ok) {
          flashNotification("✓ BLOCK REMOVED", "var(--studio-amber)");
          currentEditingBlockId = null;
          currentEditingBlockOriginal = null;
          await loadTemplateBlocks(0);
          await loadCompiledPreview();
        } else {
          const err = await resp.text();
          alert("Failed to delete block: " + err);
        }
      } catch (e) {
        alert("Error deleting block: " + e);
      }
    }

    function copyDirective() {
      const code = document.getElementById("txt-raw-directive").value;
      navigator.clipboard.writeText(code).then(() => {
        flashNotification("✓ COPIED TO CLIPBOARD", "var(--studio-cyan)");
      });
    }

    function flashNotification(text, color) {
      const s = document.getElementById("sse-status");
      if (s) {
        const oldText = s.innerText;
        const oldColor = s.style.color;
        s.innerText = text;
        s.style.color = color;
        setTimeout(() => {
          s.innerText = oldText;
          s.style.color = oldColor;
        }, 2500);
      }
    }

    async function pushReadmeToGit() {
      const btn = document.getElementById("btn-git-push");
      if (!btn) return;
      const originalText = btn.innerText;
      btn.disabled = true;
      btn.innerText = "[ PUSHING... ]";
      flashNotification("SYNCING README & PUSHING TO GIT...", "var(--studio-amber)");

      try {
        const resp = await fetch("/api/git/push_readme", {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        const data = await resp.json();
        if (resp.ok && data.ok) {
          flashNotification(data.committed ? "✓ README PUSHED TO GITHUB" : "✓ ALREADY UP TO DATE IN GIT", "var(--studio-green)");
          await loadCompiledPreview();
        } else {
          flashNotification("✗ PUSH FAILED: " + (data.error || "Unknown error"), "var(--studio-danger)");
          alert("Git Push Error: " + (data.error || "Failed to push to Git"));
        }
      } catch (err) {
        flashNotification("✗ NETWORK ERROR DURING PUSH", "var(--studio-danger)");
        alert("Network / Server error: " + err);
      } finally {
        btn.disabled = false;
        btn.innerText = originalText;
      }
    }

    async function loadCompiledPreview() {
      try {
        const resp = await fetch(`/api/preview?theme=${activePreviewTheme}&t=${Date.now()}`, { cache: "no-store" });
        if (resp.ok) {
          const data = await resp.json();
          const bustTimestamp = Date.now();
          const applyTheme = (htmlStr) => (htmlStr || "").replace(
            /(<img\b[^>]*?\bsrc=")([^"]+)(\")/gi,
            function(match, p1, p2, p3) {
              const cleanUrl = p2.split("?")[0];
              return `${p1}${cleanUrl}?theme=${activePreviewTheme}&t=${bustTimestamp}${p3}`;
            }
          );
          cachedEditHtml = applyTheme(data.html || "");
          cachedViewHtml = applyTheme(data.view_html || data.html || "");

          const previewArea = document.getElementById("readme-preview-content");
          if (previewArea) {
            if (currentStudioMode === "view") {
              previewArea.innerHTML = cachedViewHtml;
            } else {
              previewArea.innerHTML = cachedEditHtml;
            }
          }
          document.getElementById("template-filename").innerText = data.filename || "README.template.md";
          if (data.lines) document.getElementById("gh-stats-lines").innerText = `${data.lines} lines`;
          if (data.bytes) {
            const kb = (data.bytes / 1024).toFixed(1);
            document.getElementById("gh-stats-bytes").innerText = `${kb} KB`;
          }
          if (currentStudioMode !== "view" && currentEditingBlockId !== null) {
            highlightBlockInPreview(currentEditingBlockId);
          }
        }
      } catch (e) {
        console.error("Load preview error:", e);
      }
    }

    function attachPreviewClickInterceptor() {
      const container = document.getElementById("readme-preview-content");
      if (!container) return;
      container.addEventListener("click", function(e) {
        if (currentStudioMode === "view") return;
        const link = e.target.closest("a");
        if (link && !e.target.closest(".pk-block-hud-bar")) {
          e.preventDefault();
          e.stopPropagation();
        }
        const wrapper = e.target.closest(".pk-block-wrapper");
        if (wrapper && !e.target.closest(".pk-hud-actions")) {
          const blkId = parseInt(wrapper.getAttribute("data-pk-id"), 10);
          if (!isNaN(blkId)) {
            selectBlockFromPreview(blkId, e);
          }
        }
      });
    }

    function initSSE() {
      if (sseSource) sseSource.close();
      sseSource = new EventSource("/events");
      sseSource.addEventListener("reload", () => {
        loadTemplateBlocks(currentEditingBlockId);
        loadCompiledPreview();
      });
      sseSource.onopen = () => {
        const el = document.getElementById("sse-status");
        if (el) { el.innerText = "HUD STUDIO SYNC: ONLINE"; el.style.color = "var(--studio-green)"; }
      };
      sseSource.onerror = () => {
        const el = document.getElementById("sse-status");
        if (el) { el.innerText = "HUD STUDIO SYNC: RECONNECTING..."; el.style.color = "var(--studio-amber)"; }
      };
    }

    // Global Keyboard Shortcuts
    document.addEventListener("keydown", function(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        if (editorMode === "edit") {
          saveExistingBlockChanges();
        } else {
          executeInsertBlock();
        }
      }
    });

    window.addEventListener("DOMContentLoaded", () => {
      try {
        const savedMode = localStorage.getItem("pk_studio_mode");
        if (savedMode === "view") {
          setStudioMode("view");
        }
        const savedTheme = localStorage.getItem("pk_preview_theme");
        if (savedTheme === "light") {
          switchPreviewTheme("light");
        }
      } catch (_) {}
      onGlobalPresetChange();
      onBlockPresetChange();
      loadTemplateBlocks();
      loadCompiledPreview();
      attachPreviewClickInterceptor();
      initSSE();
    });
