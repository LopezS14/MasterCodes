(() => {
  const $ = (id) => document.getElementById(id);

  // ======================
  // Canvas + Dibujo (amarillo) + Grosor
  // ======================
  const canvas = $("canvas");
  const brushEl = $("brush"); // <input id="brush" ...>
  let brushSize = brushEl ? Number(brushEl.value || 2) : 2;

  if (brushEl) {
    brushEl.addEventListener("input", () => {
      brushSize = Number(brushEl.value || 2);
    });
  }

  if (canvas) {
    const ctx = canvas.getContext("2d");

    // buffer para no perder dibujo al cambiar tamaño
    const buffer = document.createElement("canvas");
    const bctx = buffer.getContext("2d");

    function resize() {
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      if (w <= 0 || h <= 0) return;

      // guarda lo actual
      const old = document.createElement("canvas");
      old.width = canvas.width;
      old.height = canvas.height;
      old.getContext("2d").drawImage(canvas, 0, 0);

      // resize real
      canvas.width = w;
      canvas.height = h;

      // re-dibuja lo anterior escalado
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(old, 0, 0, old.width, old.height, 0, 0, canvas.width, canvas.height);

      // sincroniza buffer
      buffer.width = canvas.width;
      buffer.height = canvas.height;
      bctx.clearRect(0, 0, buffer.width, buffer.height);
      bctx.drawImage(canvas, 0, 0);
    }

    window.addEventListener("resize", resize);
    resize();

    let draw = false, lx = 0, ly = 0;

    canvas.addEventListener("mousedown", (e) => {
      if (e.button !== 0) return; // solo click izquierdo
      draw = true;
      lx = e.offsetX; ly = e.offsetY;
    });

    window.addEventListener("mouseup", () => { draw = false; });

    canvas.addEventListener("mousemove", (e) => {
      if (!draw) return;

      //  grosor  del slider
      ctx.strokeStyle = "yellow";
      ctx.lineWidth = brushSize;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";

      ctx.beginPath();
      ctx.moveTo(lx, ly);
      ctx.lineTo(e.offsetX, e.offsetY);
      ctx.stroke();

      // buffer: MISMO grosor (antes lo tenías en 5 fijo)
      bctx.strokeStyle = "yellow";
      bctx.lineWidth = brushSize;
      bctx.lineCap = "round";
      bctx.lineJoin = "round";
      bctx.beginPath();
      bctx.moveTo(lx, ly);
      bctx.lineTo(e.offsetX, e.offsetY);
      bctx.stroke();

      lx = e.offsetX; ly = e.offsetY;
    });

    // Borrar trazo
    const btnClearDraw = $("btnClearDraw");
    if (btnClearDraw) {
      btnClearDraw.addEventListener("click", () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        bctx.clearRect(0, 0, buffer.width, buffer.height);
      });
    }

    // ======================
    // Descargar PNG (COMPATIBLE): imagen base + trazos
    // ======================
    const btnDownload = $("btnDownload");
    const videoEl = $("video"); // <img id="video" ...>

    function drawContain(ctx2, img, W, H) {
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;
      const s = Math.min(W / iw, H / ih);
      const nw = iw * s;
      const nh = ih * s;
      const x = (W - nw) / 2;
      const y = (H - nh) / 2;

      ctx2.clearRect(0, 0, W, H);
      ctx2.fillStyle = "#000";
      ctx2.fillRect(0, 0, W, H);
      ctx2.drawImage(img, x, y, nw, nh);
    }

    if (btnDownload && videoEl) {
      btnDownload.addEventListener("click", (e) => {
        e.preventDefault();

        // espera a que la imagen (cámara o cargada) esté lista
        if (!videoEl.complete || videoEl.naturalWidth === 0) {
          alert("La imagen aún no está lista. Espera un momento y vuelve a intentar.");
          return;
        }

        const out = document.createElement("canvas");
        out.width = canvas.width;
        out.height = canvas.height;
        const outCtx = out.getContext("2d");

        // base (lo que ves)
        drawContain(outCtx, videoEl, out.width, out.height);
        // trazos
        outCtx.drawImage(canvas, 0, 0);

        const dataURL = out.toDataURL("image/png");
        btnDownload.href = dataURL;

        // fuerza la descarga
        btnDownload.click();
      });
    }
  }

  // ======================
  // Intensidad (slider)
  // ======================
  const intSlider = $("intSlider");
  const intVal = $("intVal");
  const intState = $("intState");

  function updateSlider() {
    if (!intSlider || !intVal || !intState) return;

    const v = Number(intSlider.value);
    intVal.textContent = v;

    const pct = (v / 5) * 100;
    intSlider.style.backgroundSize = `${pct}% 100%, 100% 100%`;

    if (v === 0) {
      intState.textContent = "Apagado";
      intState.style.opacity = "1";
    } else {
      intState.textContent = "";
      intState.style.opacity = "0";
    }
  }

  if (intSlider) {
    intSlider.addEventListener("input", updateSlider);
    updateSlider();
  }

  // ======================
  // Conexión (toggle UI)
  // ======================
  const btnToggle = $("btnToggleConn");
  const statusText = $("statusText");
  const statusDot = $("statusDot");
  let connected = false;

  function updateConnectionUI() {
    if (!btnToggle || !statusText || !statusDot) return;

    if (connected) {
      statusText.textContent = "Conectado";
      statusText.classList.remove("status-red");
      statusText.classList.add("status-green");

      statusDot.textContent = "✓";
      statusDot.classList.remove("dot-red");
      statusDot.classList.add("dot-green");

      btnToggle.textContent = "Desconectar";
      btnToggle.classList.remove("btn-green");
      btnToggle.classList.add("btn-red");
    } else {
      statusText.textContent = "Desconectado";
      statusText.classList.remove("status-green");
      statusText.classList.add("status-red");

      statusDot.textContent = "✕";
      statusDot.classList.remove("dot-green");
      statusDot.classList.add("dot-red");

      btnToggle.textContent = "Conectar";
      btnToggle.classList.remove("btn-red");
      btnToggle.classList.add("btn-green");
    }
  }

  if (btnToggle) {
    btnToggle.addEventListener("click", async () => {
      connected = !connected;
      updateConnectionUI();
    });
    updateConnectionUI();
  }

  // ======================
  // Modo Cámara / Imagen
  // ======================
  const videoEl = $("video");
  const fileImage = $("fileImage");
  const btnLoadImage = $("btnLoadImage");
  const btnBackCamera = $("btnBackCamera");

  let mode = "camera";
  let loadedImageURL = null;

  function setModeCamera() {
    if (!videoEl) return;
    mode = "camera";
    videoEl.src = "/video_feed?" + Date.now();
    if (loadedImageURL) {
      URL.revokeObjectURL(loadedImageURL);
      loadedImageURL = null;
    }
  }

  function setModeImage(url) {
    if (!videoEl) return;
    mode = "image";
    videoEl.src = url;
  }

  if (btnLoadImage && fileImage) {
    btnLoadImage.addEventListener("click", () => fileImage.click());

    fileImage.addEventListener("change", () => {
      const f = fileImage.files?.[0];
      if (!f) return;

      if (!f.type.startsWith("image/")) {
        alert("Selecciona un archivo de imagen.");
        return;
      }

      if (loadedImageURL) URL.revokeObjectURL(loadedImageURL);
      loadedImageURL = URL.createObjectURL(f);
      setModeImage(loadedImageURL);

      fileImage.value = "";
    });
  }

  if (btnBackCamera) {
    btnBackCamera.addEventListener("click", () => setModeCamera());
  }

  // ======================
  // Captura N (server /api/capture)
  // ======================
  const btnSnapN = $("btnSnapN");
  const folderName = $("folderName");
  const capN = $("capN");
  const capCountEl = $("capCount");
  let capCount = 0;
  let isCapturing = false;

  async function captureOnce() {
    const folder = (folderName?.value || "default").trim();

    const r = await fetch("/api/capture", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folder })
    });

    const j = await r.json();
    if (!j.ok) throw new Error(j.error || "Error al capturar");

    capCount += 1;
    if (capCountEl) capCountEl.textContent = `${capCount} capturas`;
    return j;
  }

  if (btnSnapN) {
    btnSnapN.addEventListener("click", async () => {
      if (mode === "image") {
        alert("Estás en modo imagen. Presiona 'Volver a cámara' para capturar.");
        return;
      }

      if (isCapturing) return;
      isCapturing = true;

      const n = Math.max(1, Math.min(9999, parseInt(capN?.value || "1", 10)));
      const oldText = btnSnapN.textContent;
      btnSnapN.textContent = "Capturando...";
      btnSnapN.disabled = true;

      try {
        for (let i = 0; i < n; i++) {
          await captureOnce();
          await new Promise(res => setTimeout(res, 120));
        }
      } catch (e) {
        alert("Se detuvo la captura: " + e.message);
      } finally {
        btnSnapN.textContent = oldText;
        btnSnapN.disabled = false;
        isCapturing = false;
      }
    });
        // ======================
    // Descargar PNG (COMPATIBLE): imagen base + trazos
    // ======================
    const btnDownload = $("btnDownload");
    const videoEl = $("video"); // <img id="video" ...>

    function drawContain(ctx2, img, W, H) {
      const iw = img.naturalWidth;
      const ih = img.naturalHeight;
      const s = Math.min(W / iw, H / ih);
      const nw = iw * s;
      const nh = ih * s;
      const x = (W - nw) / 2;
      const y = (H - nh) / 2;

      ctx2.clearRect(0, 0, W, H);
      ctx2.fillStyle = "#000";
      ctx2.fillRect(0, 0, W, H);
      ctx2.drawImage(img, x, y, nw, nh);
    }

    if (btnDownload && videoEl && canvas) {
      btnDownload.addEventListener("click", (e) => {
        e.preventDefault();

        if (!videoEl.complete || videoEl.naturalWidth === 0) {
          alert("La imagen aún no está lista. Espera un momento y vuelve a intentar.");
          return;
        }

        const out = document.createElement("canvas");
        out.width = canvas.width;
        out.height = canvas.height;
        const outCtx = out.getContext("2d");

        drawContain(outCtx, videoEl, out.width, out.height);
        outCtx.drawImage(canvas, 0, 0);

        const dataURL = out.toDataURL("image/png");

        // descarga 
        const a = document.createElement("a");
        a.href = dataURL;
        a.download = "Imagen_segementada.png";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      });
}

  }
})();
