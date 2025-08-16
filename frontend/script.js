const form = document.getElementById('tripForm');
const resultDiv = document.getElementById('result');
const loaderDiv = document.getElementById('loader');
const resetBtn = document.getElementById('resetBtn');
const downloadPdfBtn = document.getElementById('downloadPdfBtn');

form.addEventListener('submit', async function (e) {
  e.preventDefault();

  // Hide result and buttons, show loader
  resultDiv.innerHTML = '';
  resultDiv.style.display = 'none';
  resetBtn.style.display = 'none';
  downloadPdfBtn.style.display = 'none';
  loaderDiv.style.display = 'block';
  loaderDiv.innerHTML = `<div class="spinner"></div><div style="margin-top:10px;">Generating your travel plan...</div>`;

  const data = {
    name: document.getElementById('name').value.trim(),
    email: document.getElementById('email').value.trim(),
    destination: document.getElementById('destination').value.trim(),
    days: parseInt(document.getElementById('days').value),
    group_size: parseInt(document.getElementById('group_size').value),
    trip_type: document.getElementById('trip_type').value,
    budget: document.getElementById('budget').value.trim(),
    preferences: document.getElementById('preferences').value.trim(),
    source_location: document.getElementById('source_location').value.trim()
  };

  try {
    const response = await fetch('http://localhost:5001/plan-trip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    loaderDiv.style.display = 'none';
    resultDiv.style.display = 'block';

    if (!response.ok) throw new Error("Server error");

    const result = await response.json();

    if (result.error) {
      resultDiv.innerHTML = `<p style="color:#e53e3e;">Error: ${result.error}</p>`;
      resetBtn.style.display = 'block';
      return;
    }

    function formatTextToHtml(text) {
      const lines = text.split('\n');
      let html = '';
      let inList = false;
      lines.forEach(line => {
        const trimmed = line.trim();
        if (/^(\*|-)+\s+/.test(trimmed)) {
          if (!inList) {
            inList = true;
            html += '<ul>';
          }
          const listItem = trimmed.replace(/^(\*|-)+\s+/, '');
          html += `<li>${listItem}</li>`;
        } else {
          if (inList) {
            inList = false;
            html += '</ul>';
          }
          let processedLine = trimmed.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
          processedLine = processedLine.replace(/^#+\s*/, '');
          processedLine = processedLine.replace(/(Group Size:|Budget per Person:|Trip Type:|Cost Level:|Preferences:)/g, '<span class="key-detail">$1</span>');
          if (processedLine) {
            html += `<p>${processedLine}</p>`;
          }
        }
      });
      if (inList) {
        html += '</ul>';
      }
      return html;
    }

    let html = '';
    for (const [section, content] of Object.entries(result.agent_outputs)) {
      html += `<div class="section"><h3>${section}</h3>${formatTextToHtml(content)}</div>`;
    }
    html += `<p><strong>Email status:</strong> ${result.message}</p>`;

    resultDiv.innerHTML = html;
    resetBtn.style.display = 'block';
    downloadPdfBtn.style.display = 'block';
    // Store the latest form data for PDF download
    downloadPdfBtn.dataset.form = JSON.stringify(data);

  } catch (error) {
    loaderDiv.style.display = 'none';
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `<p style="color:#e53e3e;">Failed to fetch: ${error.message}</p>`;
    resetBtn.style.display = 'block';
  }
});

resetBtn.addEventListener('click', function () {
  form.reset();
  resultDiv.innerHTML = '';
  resultDiv.style.display = 'none';
  resetBtn.style.display = 'none';
  downloadPdfBtn.style.display = 'none';
});

downloadPdfBtn.addEventListener('click', async function () {
  // Use the latest form data to request the PDF
  const data = JSON.parse(downloadPdfBtn.dataset.form || '{}');
  try {
    const response = await fetch('http://localhost:5001/plan-trip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to generate PDF');
    const blob = await response.blob();
    // Try to get PDF from response (if backend supports PDF download)
    if (blob.type === 'application/pdf') {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'TripTacticx_TravelPlan.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } else {
      // If not PDF, show error
      alert('PDF download not available. Please check your email for the PDF.');
    }
  } catch (err) {
    alert('Failed to download PDF. Please check your email for the PDF.');
  }
});

// Add a simple CSS spinner
const style = document.createElement('style');
style.innerHTML = `
.spinner {
  border: 5px solid #e0e7ff;
  border-top: 5px solid #2563eb;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}`;
document.head.appendChild(style);
