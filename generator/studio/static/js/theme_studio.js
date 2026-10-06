// ==============================================================================
// THEME STUDIO & COLOR HARMONIZER MODULE
// Dynamic palette creation, WCAG contrast calculation, and preset management
// ==============================================================================

let cachedThemesData = null;
let currentGeneratedTheme = null;

async function loadDynamicPresets() {
  try {
    const resp = await fetch("/api/themes");
    if (!resp.ok) return;
    cachedThemesData = await resp.json();
    const presets = cachedThemesData.presets || [];

    // 1. Update Global Preset Dropdown
    const globalSelect = document.getElementById("sel-global-preset");
    if (globalSelect) {
      const currentVal = globalSelect.value;
      globalSelect.innerHTML = '<option value="custom">-- Custom Colors --</option>';
      presets.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p;
        opt.textContent = p.replace(/-/g, " ").toUpperCase();
        globalSelect.appendChild(opt);
      });
      if (presets.includes(currentVal)) {
        globalSelect.value = currentVal;
      } else if (presets.length > 0) {
        globalSelect.value = "cyberpunk";
      }
    }

    // 2. Update Block Preset Dropdown
    const blockSelect = document.getElementById("sel-preset");
    if (blockSelect) {
      const currentVal = blockSelect.value;
      blockSelect.innerHTML = '<option value="">(Inherit Global / Custom)</option>';
      presets.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p;
        opt.textContent = p.replace(/-/g, " ").toUpperCase();
        blockSelect.appendChild(opt);
      });
      if (currentVal && presets.includes(currentVal)) {
        blockSelect.value = currentVal;
      }
    }

    // 3. Update PRESET_COLORS in global scope if present
    if (cachedThemesData.themes) {
      for (const [slug, data] of Object.entries(cachedThemesData.themes)) {
        if (data.dark) {
          window.PRESET_COLORS = window.PRESET_COLORS || {};
          window.PRESET_COLORS[slug] = {
            primary: data.dark.primary || "#00c8d7",
            accent: data.dark.accent || "#a855f7",
            tertiary: data.dark.tertiary || "#ff0055",
          };
        }
      }
    }
  } catch (err) {
    console.warn("Could not load dynamic presets:", err);
  }
}

function openThemeStudio() {
  let modal = document.getElementById("theme-studio-modal");
  if (!modal) {
    modal = createThemeStudioModal();
    document.body.appendChild(modal);
  }
  modal.style.display = "flex";
  syncThemeStudioColor("picker");
  generateHarmoniousTheme();
}

function closeThemeStudio() {
  const modal = document.getElementById("theme-studio-modal");
  if (modal) {
    modal.style.display = "none";
  }
}

function createThemeStudioModal() {
  const backdrop = document.createElement("div");
  backdrop.id = "theme-studio-modal";
  backdrop.className = "theme-studio-backdrop";
  backdrop.style.cssText = `
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(7, 9, 14, 0.88);
    backdrop-filter: blur(10px);
    z-index: 9999;
    align-items: center;
    justify-content: center;
    padding: 20px;
  `;

  backdrop.innerHTML = `
    <div class="theme-studio-window" style="
      background: var(--studio-panel);
      border: 1px solid var(--studio-panel-border);
      border-radius: 8px;
      width: 100%;
      max-width: 680px;
      box-shadow: 0 0 30px rgba(0, 200, 215, 0.25);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      font-family: var(--studio-font-mono);
    ">
      <div class="theme-studio-header" style="
        background: rgba(10, 14, 23, 0.95);
        border-bottom: 1px solid var(--studio-panel-border);
        padding: 12px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      ">
        <div style="font-family:var(--studio-font-hud); font-weight:800; font-size:14px; color:var(--studio-cyan); letter-spacing:1px;">
          ■ THEME STUDIO // PALETTE HARMONIZER & PRESETS
        </div>
        <button onclick="closeThemeStudio()" style="
          background: transparent;
          border: 1px solid rgba(239,68,68,0.5);
          color: #ef4444;
          cursor: pointer;
          font-family: var(--studio-font-mono);
          padding: 2px 8px;
          border-radius: 3px;
        ">[ × ]</button>
      </div>

      <div class="theme-studio-body" style="padding: 20px; overflow-y: auto; max-height: 80vh;">
        <!-- Inputs -->
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
          <div>
            <label style="font-size:11px; color:var(--studio-text-dim); display:block; margin-bottom:5px;">THEME NAME</label>
            <input type="text" id="ts-theme-name" value="Neon Matrix" style="
              width: 100%; background: #07090e; border: 1px solid var(--studio-panel-border);
              color: #fff; padding: 6px 10px; border-radius: 4px; font-family: var(--studio-font-mono);
            " oninput="debounceThemeStudioGenerate()">
          </div>
          <div>
            <label style="font-size:11px; color:var(--studio-text-dim); display:block; margin-bottom:5px;">HARMONIZATION STRATEGY</label>
            <select id="ts-strategy" style="
              width: 100%; background: #07090e; border: 1px solid var(--studio-panel-border);
              color: #fff; padding: 6px 10px; border-radius: 4px; font-family: var(--studio-font-mono);
            " onchange="generateHarmoniousTheme()">
              <option value="triadic">Triadic (Balanced High Contrast)</option>
              <option value="complementary">Complementary (Dual Dynamic)</option>
              <option value="analogous">Analogous (Harmonious Gradient)</option>
            </select>
          </div>
        </div>

        <div style="margin-bottom: 20px;">
          <label style="font-size:11px; color:var(--studio-text-dim); display:block; margin-bottom:5px;">PRIMARY BRAND COLOR (HEX)</label>
          <div style="display:flex; gap:10px; align-items:center;">
            <input type="color" id="ts-picker-primary" value="#00c8d7" style="
              width: 44px; height: 32px; background: transparent; border: 1px solid var(--studio-panel-border); cursor: pointer;
            " oninput="syncThemeStudioColor('picker')">
            <input type="text" id="ts-inp-primary" value="#00c8d7" style="
              flex: 1; background: #07090e; border: 1px solid var(--studio-panel-border);
              color: var(--studio-cyan); font-weight: bold; padding: 6px 10px; border-radius: 4px; font-family: var(--studio-font-mono);
            " oninput="syncThemeStudioColor('text')">
            <button onclick="generateHarmoniousTheme()" style="
              background: rgba(0, 200, 215, 0.15); border: 1px solid var(--studio-cyan);
              color: var(--studio-cyan); padding: 6px 14px; border-radius: 4px; cursor: pointer; font-weight: bold;
            ">[ HARMONIZE ]</button>
          </div>
        </div>

        <!-- Palette Preview Swatches -->
        <div style="background: rgba(10, 14, 23, 0.8); border: 1px solid rgba(0,200,215,0.2); border-radius:6px; padding:15px; margin-bottom:20px;">
          <div style="font-size:11px; color:var(--studio-cyan); font-weight:bold; margin-bottom:12px; letter-spacing:0.5px;">
            DERIVED HARMONIZED SWATCHES
          </div>
          <div id="ts-swatches-grid" style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
            <!-- Generated dynamically -->
          </div>
        </div>

        <!-- Live Component Mini Preview -->
        <div style="background: #0d1117; border: 1px solid #30363d; border-radius:6px; padding:15px; margin-bottom:20px;">
          <div style="font-size:11px; color:var(--studio-text-dim); margin-bottom:10px;">COMPONENT PREVIEW (SVG CHIP & FRAME)</div>
          <div id="ts-preview-mount" style="display:flex; flex-direction:column; gap:10px; align-items:center;">
            <div id="ts-chip-preview" style="display:flex; gap:10px;"></div>
          </div>
        </div>

        <!-- Action Row -->
        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid rgba(255,255,255,0.08); padding-top:15px;">
          <button onclick="applyCurrentThemeLocally()" style="
            background: rgba(168, 85, 247, 0.2); border: 1px solid var(--studio-purple);
            color: #d8b4fe; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold;
          ">APPLY TO STUDIO (SESSION)</button>
          <button onclick="saveCurrentCustomTheme()" style="
            background: rgba(0, 210, 106, 0.2); border: 1px solid var(--studio-green);
            color: #4ade80; padding: 8px 20px; border-radius: 4px; cursor: pointer; font-weight: bold;
          ">[ SAVE PRESET ] (*.json)</button>
        </div>
      </div>
    </div>
  `;

  return backdrop;
}

let tsTimer = null;
function debounceThemeStudioGenerate() {
  if (tsTimer) clearTimeout(tsTimer);
  tsTimer = setTimeout(generateHarmoniousTheme, 300);
}

function syncThemeStudioColor(from) {
  const picker = document.getElementById("ts-picker-primary");
  const text = document.getElementById("ts-inp-primary");
  if (!picker || !text) return;
  if (from === "picker") {
    text.value = picker.value;
  } else {
    if (/^#[0-9A-Fa-f]{6}$/.test(text.value)) {
      picker.value = text.value;
    }
  }
  debounceThemeStudioGenerate();
}

async function generateHarmoniousTheme() {
  const primInput = document.getElementById("ts-inp-primary");
  const nameInput = document.getElementById("ts-theme-name");
  const stratSelect = document.getElementById("ts-strategy");
  if (!primInput) return;

  const prim = primInput.value.trim() || "#00c8d7";
  const name = nameInput ? nameInput.value.trim() : "Custom Theme";
  const strategy = stratSelect ? stratSelect.value : "triadic";

  try {
    const resp = await fetch("/api/themes/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ primary: prim, name: name, strategy: strategy })
    });
    if (!resp.ok) return;
    const data = await resp.json();
    currentGeneratedTheme = data.theme;

    renderSwatchesGrid(currentGeneratedTheme);
    renderMiniComponents(currentGeneratedTheme);
  } catch (e) {
    console.error("Theme generation error:", e);
  }
}

function renderSwatchesGrid(themeData) {
  const container = document.getElementById("ts-swatches-grid");
  if (!container || !themeData) return;

  const preset = themeData.preset || {};
  const swatches = [
    { label: "PRIMARY", color: preset.primary },
    { label: "ACCENT", color: preset.secondary },
    { label: "TERTIARY", color: preset.accent },
    { label: "STATUS / OK", color: preset.success || "#00D26A" },
    { label: "WARNING", color: preset.warning || "#F59E0B" },
    { label: "BG GLASS", color: preset.bg_glass, isGlass: true },
    { label: "BORDER", color: preset.border_subtle, isGlass: true },
    { label: "TEXT MAIN", color: "#F8F8F2" },
  ];

  container.innerHTML = swatches.map(s => `
    <div style="background: rgba(15, 23, 38, 0.9); border: 1px solid rgba(255,255,255,0.06); border-radius:4px; padding:8px;">
      <div style="
        height: 28px; border-radius: 3px; background: ${s.color};
        border: 1px solid rgba(255,255,255,0.15); margin-bottom: 6px;
      "></div>
      <div style="font-size:9.5px; color:var(--studio-text-dim);">${s.label}</div>
      <div style="font-size:10px; font-weight:bold; color:#fff; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
        ${s.color}
      </div>
    </div>
  `).join("");
}

function renderMiniComponents(themeData) {
  const container = document.getElementById("ts-chip-preview");
  if (!container || !themeData) return;

  const preset = themeData.preset || {};
  container.innerHTML = `
    <div style="
      background: ${preset.bg_glass || 'rgba(10,14,23,0.8)'};
      border: 1px solid ${preset.primary || '#00c8d7'};
      padding: 6px 14px;
      border-radius: 3px;
      font-size: 11px;
      font-weight: bold;
      color: ${preset.primary || '#00c8d7'};
      box-shadow: 0 0 10px ${preset.primary}40;
    ">
      ${preset.name || 'THEME'} // ACTIVE
    </div>
    <div style="
      background: ${preset.bg_glass || 'rgba(10,14,23,0.8)'};
      border: 1px solid ${preset.secondary || '#a855f7'};
      padding: 6px 14px;
      border-radius: 3px;
      font-size: 11px;
      font-weight: bold;
      color: ${preset.secondary || '#a855f7'};
    ">
      ACCENT // PASS
    </div>
  `;
}

function applyCurrentThemeLocally() {
  if (!currentGeneratedTheme) return;
  const p = currentGeneratedTheme.preset;
  if (!p) return;

  const globalStyle = document.getElementById("sel-global-style");
  const globalPreset = document.getElementById("sel-global-preset");
  const primInput = document.getElementById("inp-global-primary");
  const primPicker = document.getElementById("picker-global-primary");
  const accInput = document.getElementById("inp-global-accent");
  const accPicker = document.getElementById("picker-global-accent");
  const tertInput = document.getElementById("inp-global-tertiary");
  const tertPicker = document.getElementById("picker-global-tertiary");

  if (globalPreset) globalPreset.value = "custom";
  if (primInput) primInput.value = p.primary;
  if (primPicker) primPicker.value = p.primary;
  if (accInput) accInput.value = p.secondary;
  if (accPicker) accPicker.value = p.secondary;
  if (tertInput) tertInput.value = p.accent;
  if (tertPicker) tertPicker.value = p.accent;

  closeThemeStudio();
  if (typeof applyGlobalThemeToAllBlocks === "function") {
    applyGlobalThemeToAllBlocks(true);
  }
}

async function saveCurrentCustomTheme() {
  if (!currentGeneratedTheme) return;
  const p = currentGeneratedTheme.preset;
  if (!p) return;

  try {
    const resp = await fetch("/api/themes/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: p.name,
        slug: p.theme,
        preset: p,
        dark: currentGeneratedTheme.dark,
        light: currentGeneratedTheme.light,
      })
    });
    if (!resp.ok) {
      alert("Failed to save theme to presets: " + await resp.text());
      return;
    }
    const data = await resp.json();
    alert(`[OK] Theme successfully saved to presets/${data.slug}.json!`);
    await loadDynamicPresets();
    closeThemeStudio();
  } catch (e) {
    alert("Error saving theme: " + e);
  }
}

// Auto-initialize presets on DOM ready
window.addEventListener("DOMContentLoaded", () => {
  loadDynamicPresets();
});
