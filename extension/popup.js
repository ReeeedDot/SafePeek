document.addEventListener("DOMContentLoaded", async () => {
  const urlInput = document.getElementById("urlInput");
  const scanBtn = document.getElementById("scanBtn");
  const resultBox = document.getElementById("resultBox");
  const statusTitle = document.getElementById("statusTitle");
  const riskScore = document.getElementById("riskScore");
  const reasonList = document.getElementById("reasonList");

  // Automatically grab current active tab URL
  try {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url && tab.url.startsWith("http")) {
      urlInput.value = tab.url;
    }
  } catch (err) {
    console.log("Tab URL fetch skipped");
  }

  scanBtn.addEventListener("click", async () => {
    const url = urlInput.value.trim();
    if (!url) return;

    resultBox.style.display = "block";
    resultBox.style.backgroundColor = "#f1f3f4";
    resultBox.style.borderColor = "#dadce0";
    resultBox.style.color = "#202124";
    statusTitle.textContent = "Scanning URL...";
    riskScore.textContent = "";
    reasonList.innerHTML = "";

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });

      if (!response.ok) throw new Error("API Error");
      const data = await response.json();

      statusTitle.textContent = `Status: ${data.status}`;
      riskScore.textContent = `Phishing Probability: ${data.risk_score}%`;

      data.reasons.forEach((reason) => {
        const li = document.createElement("li");
        li.textContent = reason;
        reasonList.appendChild(li);
      });

      if (data.status === "Phishing") {
        resultBox.style.backgroundColor = "#fce8e6";
        resultBox.style.borderColor = "#f6aea9";
        resultBox.style.color = "#c5221f";
      } else if (data.status === "Suspicious") {
        resultBox.style.backgroundColor = "#fef7e0";
        resultBox.style.borderColor = "#fde293";
        resultBox.style.color = "#b06000";
      } else {
        resultBox.style.backgroundColor = "#e6f4ea";
        resultBox.style.borderColor = "#a8dab5";
        resultBox.style.color = "#137333";
      }
    } catch (error) {
      statusTitle.textContent = "Server Offline";
      riskScore.textContent = "Please start FastAPI server (uvicorn app:app --reload)";
    }
  });
});