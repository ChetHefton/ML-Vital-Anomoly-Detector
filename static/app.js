function colorForHR(hr) {
  if (hr < 55 || hr > 110) return "bad";
  if (hr < 65 || hr > 95) return "warn";
  return "good";
}

function colorForSpO2(spo2) {
  if (spo2 < 90) return "bad";
  if (spo2 < 95) return "warn";
  return "good";
}

function colorForRR(rr) {
  if (rr < 10 || rr > 24) return "bad";
  if (rr < 12 || rr > 20) return "warn";
  return "good";
}

function colorForTemp(t) {
  if (t < 96 || t > 100.4) return "bad";
  if (t < 97 || t > 99.5) return "warn";
  return "good";
}

async function tick() {
  const status = document.getElementById("status");
  const dot = document.getElementById("dot");

  try {
    const res = await fetch("/api/vitals", { cache: "no-store" });
    const v = await res.json();

    document.getElementById("time").textContent = v.ts;

    const hrEl = document.getElementById("hr");
    hrEl.textContent = v.hr;
    hrEl.className = `value ${colorForHR(v.hr)}`;

    const spo2El = document.getElementById("spo2");
    spo2El.textContent = v.spo2;
    spo2El.className = `value ${colorForSpO2(v.spo2)}`;

    const rrEl = document.getElementById("rr");
    rrEl.textContent = v.rr;
    rrEl.className = `value ${colorForRR(v.rr)}`;

    const tempEl = document.getElementById("temp");
    tempEl.textContent = v.temp_f;
    tempEl.className = `value ${colorForTemp(v.temp_f)}`;

    dot.className = "status-dot ok";
    status.textContent = "Live";
  } catch (e) {
    dot.className = "status-dot err";
    status.textContent = "Disconnected (retrying)";
  }
}

tick();
setInterval(tick, 1000);