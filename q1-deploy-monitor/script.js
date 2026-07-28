let requestCount = 0;

async function checkHealth() {
  const startTime = Date.now();
  try {
    const response = await fetch('/health');
    const latency = Date.now() - startTime;
    requestCount++;
    
    if (response.ok) {
      document.getElementById('status').innerHTML = `
        <span class="status-indicator good"></span>
        <span class="text good">متصل ويعمل</span>
      `;
    } else {
      document.getElementById('status').innerHTML = `
        <span class="status-indicator bad"></span>
        <span class="text bad">خطأ بالخادم</span>
      `;
    }
    
    document.getElementById('latency').innerHTML = `<span class="good">${latency}</span> <span style="font-size:1rem; color:var(--text-muted)">ms</span>`;
    document.getElementById('requests').innerHTML = requestCount.toLocaleString();

  } catch (error) {
    document.getElementById('status').innerHTML = `
      <span class="status-indicator bad"></span>
      <span class="text bad">غير متصل</span>
    `;
    document.getElementById('latency').innerHTML = `<span class="unknown">-</span> <span style="font-size:1rem; color:var(--text-muted)">ms</span>`;
  }
}

setInterval(checkHealth, 5000);
checkHealth();
