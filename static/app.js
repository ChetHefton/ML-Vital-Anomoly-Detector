//data history to store previous points for the wave
const history = {
  hr: [],
  spo2: [],
  rr: [],
  temp: []
};

//increased points for a longer smoother signal trail
const maxPoints = 800; 
const colors = { 
  good: "#22c55e", 
  warn: "#f59e0b", 
  bad: "#ef4444" 
};

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

function drawWave(id, data, colorClass) {
  const canvas = document.getElementById(`chart-${id}`);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);
  ctx.beginPath();
  ctx.strokeStyle = colors[colorClass] || "#64748b";
  ctx.lineWidth = 2;
  ctx.lineJoin = "round";

  const step = w / (maxPoints - 1);
  
  //find min/max of current buffer to scale wave height
  let min, max;
  if (id === 'hr') {
    min = -0.5; max = 1.5; //fixed scale for heart spikes
  } else {
    min = Math.min(...data); max = Math.max(...data);
  }
  const range = (max - min) || 1;

  for (let i = 0; i < data.length; i++) {
    const x = i * step;
    //invert y and scale to canvas height
    const y = h - ((data[i] - min) / range) * h;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

async function tick() {
  const status = document.getElementById("status");
  const dot = document.getElementById("dot");

  try {
    const res = await fetch("/api/vitals", { cache: "no-store" });
    const v = await res.json();

    document.getElementById("time").textContent = v.ts;

    //mapping data to elements and colors
    const metrics = [
      { id: "hr", val: v.hr, wave: v.hr_wave, colorFn: colorForHR },
      { id: "spo2", val: v.spo2, wave: null, colorFn: colorForSpO2 },
      { id: "rr", val: v.rr, wave: v.rr_wave, colorFn: colorForRR },
      { id: "temp", val: v.temp_f, wave: null, colorFn: colorForTemp }
    ];

    metrics.forEach(m => {
      const el = document.getElementById(m.id);
      const colorClass = m.colorFn(m.val);
      
      //update numerical readout
      el.textContent = m.val;
      el.className = `value ${colorClass}`;

      //if we have high-speed wave data from wfdb push the whole chunk
      if (m.wave && Array.isArray(m.wave)) {
        history[m.id].push(...m.wave);
      } else {
        //fallback for metrics without high-speed buffers
        history[m.id].push(m.val);
      }

      //keep history from growing indefinitely
      while (history[m.id].length > maxPoints) {
        history[m.id].shift();
      }

      //render the wave
      drawWave(m.id, history[m.id], colorClass);
    });

    dot.className = "status-dot ok";
    status.textContent = "Live";
  } catch (e) {
    dot.className = "status-dot err";
    status.textContent = "Disconnected (retrying)";
  }
}

//run at 50ms intervals to handle the 20-sample chunks smoothly
tick();
setInterval(tick, 50);