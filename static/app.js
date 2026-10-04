/**
 * 🍪 NIBBLE NANNY — FRONTEND APPLICATION LOGIC (app.js)
 * Manages photo capture, preset samples, API requests, theme toggle, and UI rendering.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const themeToggle = document.getElementById("themeToggle");
  const themeIcon = document.getElementById("themeIcon");
  const samplesList = document.getElementById("samplesList");
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  const browseBtn = document.getElementById("browseBtn");
  const cameraBtn = document.getElementById("cameraBtn");
  const fabCamera = document.getElementById("fabCamera");
  const previewContainer = document.getElementById("previewContainer");
  const imagePreview = document.getElementById("imagePreview");
  const clearImageBtn = document.getElementById("clearImageBtn");

  const loadingSection = document.getElementById("loadingSection");
  const loadingText = document.getElementById("loadingText");
  const errorBanner = document.getElementById("errorBanner");
  const errorMessage = document.getElementById("errorMessage");
  const closeErrorBtn = document.getElementById("closeErrorBtn");

  const resultsSection = document.getElementById("resultsSection");
  const productTitle = document.getElementById("productTitle");
  const vegPill = document.getElementById("vegPill");
  const servingPill = document.getElementById("servingPill");
  const packPill = document.getElementById("packPill");
  const sourcePill = document.getElementById("sourcePill");
  const rescanBtn = document.getElementById("rescanBtn");

  const verdictsGrid = document.getElementById("verdictsGrid");
  const tricksList = document.getElementById("tricksList");
  const educationList = document.getElementById("educationList");
  const trustGateStatus = document.getElementById("trustGateStatus");
  const nutritionTableBody = document.getElementById("nutritionTableBody");

  // =========================================================================
  // 1. THEME TOGGLE (Persistent)
  // =========================================================================
  const savedTheme = localStorage.getItem("nibble_nanny_theme") || "light";
  if (savedTheme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    themeIcon.textContent = "☀️";
  }

  themeToggle.addEventListener("click", () => {
    const isDark = document.documentElement.getAttribute("data-theme") === "dark";
    if (isDark) {
      document.documentElement.removeAttribute("data-theme");
      themeIcon.textContent = "🌙";
      localStorage.setItem("nibble_nanny_theme", "light");
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      themeIcon.textContent = "☀️";
      localStorage.setItem("nibble_nanny_theme", "dark");
    }
  });

  // =========================================================================
  // 2. LOAD & RENDER PRESET SAMPLES
  // =========================================================================
  async function loadSamples() {
    try {
      const res = await fetch("/api/samples");
      if (!res.ok) throw new Error("Failed to load sample packets");
      const samples = await res.json();

      samplesList.innerHTML = "";
      samples.forEach(sample => {
        const btn = document.createElement("button");
        btn.className = "sample-btn";
        btn.setAttribute("aria-label", `Test sample: ${sample.name}`);
        btn.innerHTML = `
          <span class="sample-badge">${sample.category}</span>
          <span class="sample-name">${sample.name}</span>
        `;
        btn.addEventListener("click", () => runSample(sample.id));
        samplesList.appendChild(btn);
      });
    } catch (e) {
      console.warn("Could not load samples:", e);
      samplesList.innerHTML = "<div class='sample-badge'>Upload a photo to begin</div>";
    }
  }

  async function runSample(sampleId) {
    showLoading("Testing sample packet...", "Running deterministic Atwater verification & evaluating rules");
    hideError();

    try {
      const res = await fetch(`/api/sample/${sampleId}`, { method: "POST" });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "Failed to process sample");
      }
      const data = await res.json();
      renderResults(data);
    } catch (err) {
      showError(err.message);
    } finally {
      hideLoading();
    }
  }

  // =========================================================================
  // 3. PHOTO UPLOAD & CAMERA CAPTURE
  // =========================================================================
  browseBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  cameraBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.setAttribute("capture", "environment");
    fileInput.click();
  });

  if (fabCamera) {
    fabCamera.addEventListener("click", () => {
      fileInput.setAttribute("capture", "environment");
      fileInput.click();
    });
  }

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  });

  // Drag and Drop
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("drag-over");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("drag-over");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("drag-over");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  function handleFileSelected(file) {
    if (!file.type.startsWith("image/")) {
      showError("Please upload a valid image file (JPG, PNG, WebP).");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      previewContainer.classList.remove("hidden");
    };
    reader.readAsDataURL(file);

    uploadImageFile(file);
  }

  clearImageBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    imagePreview.src = "";
    previewContainer.classList.add("hidden");
    fileInput.value = "";
    resultsSection.classList.add("hidden");
  });

  rescanBtn.addEventListener("click", () => {
    resultsSection.classList.add("hidden");
    previewContainer.classList.add("hidden");
    imagePreview.src = "";
    fileInput.value = "";
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  async function uploadImageFile(file) {
    showLoading("Reading label with Gemma Vision...", "Extracting nutrition values, ingredient listings, and allergen statements");
    hideError();

    const formData = new FormData();
    formData.append("photo", file);

    try {
      const res = await fetch("/api/scan", {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.error || "Scan failed. Please try a clearer photo.");
      }

      const data = await res.json();
      renderResults(data);
    } catch (err) {
      showError(err.message);
    } finally {
      hideLoading();
    }
  }

  // =========================================================================
  // 4. RENDER PIPELINE RESULTS
  // =========================================================================
  function renderResults(data) {
    // 1. Meta Pills & Product Title
    productTitle.textContent = data.product_name || "Packaged Snack";

    // Vegetarian pill
    if (data.is_nonveg_marked) {
      vegPill.textContent = "▲ Non-Vegetarian";
      vegPill.className = "badge badge-nonveg";
      vegPill.style.display = "inline-flex";
    } else if (data.is_vegetarian_marked) {
      vegPill.textContent = "● Vegetarian";
      vegPill.className = "badge badge-veg";
      vegPill.style.display = "inline-flex";
    } else {
      vegPill.style.display = "none";
    }

    // Serving & Pack pills
    const sv = data.serving_size;
    if (sv && sv.value) {
      servingPill.textContent = `Serving: ${sv.value}${sv.unit || 'g'}`;
      servingPill.style.display = "inline-flex";
    } else {
      servingPill.style.display = "none";
    }

    const pk = data.pack_size;
    const servCount = data.servings_per_pack;
    if (pk && pk.value) {
      packPill.textContent = `Pack: ${pk.value}${pk.unit || 'g'} (${servCount || 1} serv)`;
      packPill.style.display = "inline-flex";
    } else if (servCount) {
      packPill.textContent = `${servCount} servings/pack`;
      packPill.style.display = "inline-flex";
    } else {
      packPill.style.display = "none";
    }

    // AI Model Source Badge
    if (sourcePill) {
      if (data.source) {
        const isGemma = data.source.toLowerCase().includes("gemma");
        sourcePill.textContent = isGemma ? "💎 Google Gemma Open AI" : "⚡ Cloud Vision Engine";
        sourcePill.style.display = "inline-flex";
      } else {
        sourcePill.style.display = "none";
      }
    }

    // 2. HERO MATRIX: Render The Nibble Nanny Squad Cards
    verdictsGrid.innerHTML = "";
    const verdicts = data.verdicts || {};

    const profileOrder = ["no_dairy", "low_sugar", "low_salt", "jain_veg"];
    profileOrder.forEach(pid => {
      const v = verdicts[pid];
      if (!v) return;

      const card = document.createElement("div");
      const statusClass = `status-${v.status.toLowerCase().replace('_', '')}`;
      card.className = `squad-card ${statusClass}`;

      let reasonsHtml = "";
      (v.reasons || []).forEach(r => {
        reasonsHtml += `
          <li class="reason-item">
            <span class="reason-bullet" aria-hidden="true"></span>
            <span class="reason-text">${r}</span>
          </li>`;
      });

      let mathSummary = "";
      if (v.math_details && typeof v.math_details === "object" && Object.keys(v.math_details).length > 0) {
        if (v.math_details.sugar_per_serving_g !== undefined && v.math_details.sugar_per_serving_g !== null) {
          const serv = v.math_details.sugar_per_serving_g;
          const limit = v.math_details.max_serving_limit_g;
          const pack = v.math_details.sugar_per_pack_g;
          mathSummary = `Sugar: ${serv}g/serving (Limit: ${limit}g)${pack ? ` · Pack: ${pack}g` : ""}`;
        } else if (v.math_details.sodium_per_serving_mg !== undefined && v.math_details.sodium_per_serving_mg !== null) {
          const serv = v.math_details.sodium_per_serving_mg;
          const limit = v.math_details.max_serving_limit_mg;
          const pack = v.math_details.sodium_per_pack_mg;
          mathSummary = `Sodium: ${serv}mg/serving (Limit: ${limit}mg)${pack ? ` · Pack: ${pack}mg` : ""}`;
        }
      } else if (typeof v.math_details === "string" && v.math_details.trim().length > 0) {
        mathSummary = v.math_details.trim();
      }

      const mathHtml = mathSummary ? `
        <div class="card-math-chip">
          <span class="math-icon">📊</span>
          <span class="math-text">${mathSummary}</span>
        </div>` : "";

      card.innerHTML = `
        <div class="card-header">
          <div class="squad-identity">
            <div class="squad-emoji-box" aria-hidden="true">${v.avatar_emoji || '🍪'}</div>
            <div class="squad-titles">
              <h4 class="squad-name">${v.nanny_title}</h4>
              <div class="squad-for-friend">For <strong>${v.friend_name}</strong> · ${v.tagline}</div>
            </div>
          </div>
          <div class="status-badge-container">
            <span class="status-badge ${statusClass}">
              <span class="status-badge-icon">${v.status_emoji}</span>
              <span class="status-badge-text">${v.status.replace('_', ' ')}</span>
            </span>
          </div>
        </div>

        <div class="voice-bubble">
          <span class="quote-symbol">“</span>
          <p class="quote-text">${v.voice_note || v.summary_line}</p>
        </div>

        ${mathHtml}

        <div class="card-reasons-wrapper">
          <span class="reasons-heading">Nutrition & Health Evaluation:</span>
          <ul class="card-reasons">
            ${reasonsHtml}
          </ul>
        </div>
      `;

      verdictsGrid.appendChild(card);
    });

    // 3. WATCHDOG: Render Nanny Noir Trick Radar
    tricksList.innerHTML = "";
    const tricks = data.tricks || [];

    if (tricks.length === 0) {
      tricksList.innerHTML = `
        <div class="no-tricks-card">
          🛡️ No deceptive marketing tricks or dangerous chemical cocktails detected on this label!
        </div>
      `;
    } else {
      tricks.forEach(t => {
        const item = document.createElement("div");
        item.className = `trick-item severity-${t.severity}`;

        let sevLabel = "INFO ADVISORY";
        let sevIcon = "ℹ️";
        if (t.severity === "critical") {
          sevLabel = "CRITICAL DECEPTION";
          sevIcon = "🚨";
        } else if (t.severity === "warning") {
          sevLabel = "LABEL WARNING";
          sevIcon = "⚠️";
        }

        item.innerHTML = `
          <div class="trick-badge-row">
            <span class="trick-emoji">${t.emoji || sevIcon}</span>
            <span class="trick-severity-pill severity-${t.severity}">${sevLabel}</span>
          </div>
          <div class="trick-content">
            <h4 class="trick-title">${t.title}</h4>
            <p class="trick-explanation">${t.explanation}</p>
            <div class="trick-impact-box">
              <span class="impact-badge">💡 What It Means For You</span>
              <p class="impact-text">${t.impact}</p>
            </div>
          </div>
        `;
        tricksList.appendChild(item);
      });
    }

    // 4. TEACHER: Render The Ingredient Classroom
    educationList.innerHTML = "";
    const eduItems = data.education || [];

    eduItems.forEach(item => {
      const card = document.createElement("div");
      card.className = `ingredient-card color-${item.color}`;

      let statusText = "Safe & Beneficial";
      let statusClass = "badge-safe";
      if (item.color === "red") {
        statusText = "Restricted / Banned";
        statusClass = "badge-danger";
      } else if (item.color === "yellow") {
        statusText = "Use Caution";
        statusClass = "badge-warning";
      } else if (item.color === "neutral") {
        statusText = "General Food Base";
        statusClass = "badge-neutral";
      }

      let noteHtml = item.nanny_note ? `
        <div class="ing-nanny-note">
          <span class="nanny-note-icon">👩‍🏫</span>
          <div class="nanny-note-text"><strong>Nanny's Note:</strong> ${item.nanny_note}</div>
        </div>` : "";

      card.innerHTML = `
        <div class="ing-header">
          <div class="ing-title-group">
            <span class="ing-status-dot dot-${item.color}" aria-hidden="true"></span>
            <h4 class="ing-name">${item.name}</h4>
          </div>
          <span class="ing-status-pill ${statusClass}">${statusText}</span>
        </div>

        <div class="ing-category-row">
          <span class="ing-category-badge">${item.category.replace(/_/g, ' ')}</span>
        </div>

        <div class="ing-details">
          <div class="ing-detail-block">
            <span class="detail-label">What it is:</span>
            <p class="detail-value">${item.what}</p>
          </div>
          <div class="ing-detail-block">
            <span class="detail-label">Health & Body Impact:</span>
            <p class="detail-value">${item.health}</p>
          </div>
        </div>

        ${noteHtml}
      `;
      educationList.appendChild(card);
    });

    // 5. TRUST GATE: Render Math & Nutrition Table
    const val = data.validation || {};
    if (val.trusted) {
      trustGateStatus.className = "trust-status-box trusted";
      trustGateStatus.innerHTML = `
        <strong>✅ Mathematical Trust Gate: PASSED</strong><br>
        Stated energy (${val.normalized_per_100g?.energy_kcal || 0} kcal) verified against macronutrient Atwater formula (4C+4P+9F+2Fiber).
      `;
    } else {
      trustGateStatus.className = "trust-status-box untrusted";
      trustGateStatus.innerHTML = `
        <strong>⚠️ Mathematical Trust Gate: WARNINGS / ERRORS</strong><br>
        ${(val.errors || []).join("<br>") || (val.warnings || []).join("<br>")}
      `;
    }

    // Populate Nutrition Table
    nutritionTableBody.innerHTML = "";
    const nutrients = [
      { key: "energy_kcal", label: "Energy (kcal)", unit: "kcal" },
      { key: "carbohydrates_g", label: "Carbohydrates", unit: "g" },
      { key: "sugar_g", label: "of which Sugars", unit: "g" },
      { key: "protein_g", label: "Protein", unit: "g" },
      { key: "fat_g", label: "Total Fat", unit: "g" },
      { key: "saturated_fat_g", label: "Saturated Fat", unit: "g" },
      { key: "trans_fat_g", label: "Trans Fat", unit: "g" },
      { key: "fibre_g", label: "Dietary Fibre", unit: "g" },
      { key: "sodium_mg", label: "Sodium", unit: "mg" },
    ];

    const norm = val.normalized_per_100g || {};
    const pServ = val.per_serving || {};
    const pPack = val.per_pack || {};

    nutrients.forEach(n => {
      const v100 = norm[n.key] !== undefined && norm[n.key] !== null ? `${norm[n.key]} ${n.unit}` : "-";
      const vServ = pServ[n.key] !== undefined && pServ[n.key] !== null ? `${pServ[n.key]} ${n.unit}` : "-";
      const vPack = pPack[n.key] !== undefined && pPack[n.key] !== null ? `${pPack[n.key]} ${n.unit}` : "-";

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${n.label}</strong></td>
        <td>${v100}</td>
        <td>${vServ}</td>
        <td>${vPack}</td>
      `;
      nutritionTableBody.appendChild(tr);
    });

    // Reveal results and scroll smoothly
    resultsSection.classList.remove("hidden");
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // Helpers
  function showLoading(title, subtext) {
    loadingText.textContent = title;
    loadingSection.querySelector(".loading-subtext").textContent = subtext;
    loadingSection.classList.remove("hidden");
  }

  function hideLoading() {
    loadingSection.classList.add("hidden");
  }

  function showError(msg) {
    errorMessage.textContent = msg;
    errorBanner.classList.remove("hidden");
  }

  function hideError() {
    errorBanner.classList.add("hidden");
  }

  closeErrorBtn.addEventListener("click", hideError);

  // Initialize
  loadSamples();
});
