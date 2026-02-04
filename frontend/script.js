let pmChart;
let gasChart;

const API_URL = "https://aqi-8jok.onrender.com/";

// Dynamic Chart defaults based on theme
function updateChartDefaults() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const textColor = isDark ? 'rgba(255, 255, 255, 0.6)' : 'rgba(15, 23, 42, 0.6)';

    Chart.defaults.color = textColor;
    Chart.defaults.font.family = "'Outfit', sans-serif";
    Chart.defaults.font.size = 12;
}

updateChartDefaults();

// Listen for theme changes to update chart defaults (though current charts need manual re-render to change color)
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    updateChartDefaults();
    // If charts exist, we could trigger a re-render here if needed
});

/* -------------------- INTERACTION HANDLERS -------------------- */

document.getElementById("cityInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") getAQI();
});

/* -------------------- CORE LOGIC -------------------- */

async function getAQI() {
    const city = document.getElementById("cityInput").value.trim();

    if (!city) {
        showError("Please enter a city name to begin.");
        clearUI();
        return;
    }

    showLoading(true);
    hideError();
    clearUI();

    try {
        const res = await fetch(`${API_URL}?city=${city}`);
        if (!res.ok) throw new Error("City not found");

        const data = await res.json();
        renderDataFluid(data);
    } catch (err) {
        showError("We couldn't find data for that location. Please check the spelling.");
    } finally {
        showLoading(false);
    }
}

/* -------------------- FLUID RENDERING -------------------- */

function renderDataFluid(data) {
    const aqiCard = document.getElementById("aqiCard");
    const healthAlert = document.getElementById("healthAlert");
    const tableContainer = document.querySelector(".table-container");
    const chartContainer = document.querySelector(".charts");
    const table = document.getElementById("pollutantTable");

    // Reset visibility
    [aqiCard, healthAlert, tableContainer, chartContainer, table].forEach(el => el.classList.remove("hidden"));

    // Populate Data
    document.getElementById("cityName").innerText = data.city;
    document.getElementById("aqiValue").innerText = data.aqi;
    document.getElementById("aqiCategory").innerText = data.risk_level;

    updateAQIColor(data.aqi);

    // Health Guidance
    healthAlert.innerHTML =
        "<h3>HEALTH RECOMMENDATIONS</h3><ul>" +
        data.health_recommendations.map(item => `<li>${item}</li>`).join("") +
        "</ul>";

    // Pollutants
    document.getElementById("pm25").innerText = `${data.pollutants.pm2_5} µg/m³`;
    document.getElementById("pm10").innerText = `${data.pollutants.pm10} µg/m³`;
    document.getElementById("co").innerText = `${data.pollutants.co} mg/m³`;

    // Charts
    drawModernCharts(data);

    // Trigger Fluid Staggered Animation
    triggerStaggeredEntrance();
}

function triggerStaggeredEntrance() {
    const items = document.querySelectorAll(".stagger-item");
    items.forEach((item, index) => {
        item.classList.remove("show");
        setTimeout(() => {
            item.classList.add("show");
        }, index * 100);
    });
}

/* -------------------- VISUAL UPDATES -------------------- */

function updateAQIColor(aqi) {
    const valueEl = document.getElementById("aqiValue");
    let color = "#6366f1";

    if (aqi <= 50) color = "#10b981";
    else if (aqi <= 100) color = "#f59e0b";
    else if (aqi <= 150) color = "#f97316";
    else if (aqi <= 200) color = "#ef4444";
    else if (aqi <= 300) color = "#8b5cf6";
    else color = "#4c1d95";

    valueEl.style.color = color;
    valueEl.style.textShadow = `0 10px 30px ${color}33`;
}

function drawModernCharts(data) {
    const pmCtx = document.getElementById("pmChart");
    const gasCtx = document.getElementById("gasChart");
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const gridColor = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';

    [pmCtx, gasCtx].forEach(el => el.classList.remove("hidden"));

    if (pmChart) pmChart.destroy();
    if (gasChart) gasChart.destroy();

    pmChart = new Chart(pmCtx, {
        type: 'bar',
        data: {
            labels: ['PM2.5', 'PM10'],
            datasets: [{
                data: [data.pollutants.pm2_5, data.pollutants.pm10],
                backgroundColor: ['#6366f1cc', '#06b6d4cc'],
                borderColor: ['#6366f1', '#06b6d4'],
                borderWidth: 2,
                borderRadius: 12,
                barThickness: 40
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false }, title: { display: true, text: 'Particulate Matter' } },
            scales: {
                y: { grid: { color: gridColor }, beginAtZero: true },
                x: { grid: { display: false } }
            }
        }
    });

    gasChart = new Chart(gasCtx, {
        type: 'bar',
        data: {
            labels: ['CO'],
            datasets: [{
                data: [data.pollutants.co],
                backgroundColor: '#10b981cc',
                borderColor: '#10b981',
                borderWidth: 2,
                borderRadius: 12,
                barThickness: 40
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false }, title: { display: true, text: 'Gaseous Analytics' } },
            scales: {
                y: { grid: { color: gridColor }, beginAtZero: true },
                x: { grid: { display: false } }
            }
        }
    });
}

/* -------------------- UI HELPERS -------------------- */

function showLoading(show) {
    const loader = document.getElementById("loading");
    loader.classList.toggle("hidden", !show);
    if (show) loader.innerHTML = "Gathering atmospheric data...";
}

function showError(msg) {
    const err = document.getElementById("error");
    err.innerText = msg;
    err.classList.remove("hidden");
}

function hideError() {
    document.getElementById("error").classList.add("hidden");
}

function clearUI() {
    const items = document.querySelectorAll(".stagger-item");
    items.forEach(item => {
        item.classList.add("hidden");
        item.classList.remove("show");
    });
    if (pmChart) pmChart.destroy();
    if (gasChart) gasChart.destroy();
}
