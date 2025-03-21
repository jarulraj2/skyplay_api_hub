document.addEventListener("DOMContentLoaded", function () {
    fetchDashboardData(); // Initial fetch
    setInterval(fetchDashboardData, 30000); // Auto-refresh every 30s
});

// Initialize Chart Variables
let activationsChart = null;
let revenueChart = null;
let activationsOverTimeChart = null;

function fetchDashboardData() {
    document.getElementById("loading").style.display = "block"; // Show loader
    fetch("/ott_subscription/api/dashboard-data/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("loading").style.display = "none"; // Hide loader
            
            // Update Summary Cards
            animateValue("total-activations", data.total_activations);
            animateValue("total-transactions", data.total_transactions);
            animateValue("total-revenue", parseFloat(data.total_revenue).toFixed(2));

            // Render Charts with Updated Data
            activationsChart = renderChart(activationsChart, "activationsChart", data.activations_by_platform, "Activations", "pie");
            revenueChart = renderChart(revenueChart, "revenueChart", data.revenue_by_platform, "Spend (Rs)", "bar");

            activationsOverTimeChart = renderChart(activationsOverTimeChart, "activationsOverTimeChart", data.activations_over_time, "Activations", "line");
        })
        .catch(error => console.error("Error fetching dashboard data:", error));
}

// 📊 Universal Chart Rendering Function (Optimized)
function renderChart(chartInstance, canvasId, data, label, type) {
    if (chartInstance) {
        chartInstance.destroy();
    }

    const ctx = document.getElementById(canvasId).getContext("2d");

    // Limit data points for large datasets
    const maxDataPoints = 15; // Reduce to avoid slow UI
    const trimmedData = data.slice(-maxDataPoints); // Show latest data

    chartInstance = new Chart(ctx, {
        type: type,
        data: {
            labels: trimmedData.map(item => item.date),
            datasets: [{
                label: label,
                data: trimmedData.map(item => item.count || item.total),
                backgroundColor: type === "line" ? "#007bff" : generateColors(data.length),
                borderColor: "#007bff",
                borderWidth: 2,
                fill: false,
                tension: 0.4 // Smooth curves
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Prevents unnecessary stretching
            animation: { duration: 500 }, // Faster animation
            scales: {
                x: { 
                    ticks: { autoSkip: true, maxTicksLimit: 10 } 
                },
                y: { 
                    beginAtZero: true 
                }
            }
        }
    });

    return chartInstance;
}

// 🎨 Dynamic Colors for Charts
function generateColors(count) {
    return Array.from({ length: count }, () => `#${Math.floor(Math.random()*16777215).toString(16)}`);
}

// 🔢 Number Animation Effect
function animateValue(id, newValue) {
    const el = document.getElementById(id);
    const startValue = parseInt(el.textContent.replace(/[^0-9]/g, "")) || 0;
    const endValue = parseInt(newValue);
    const duration = 1000;
    let startTime = null;

    function animateStep(currentTime) {
        if (!startTime) startTime = currentTime;
        const progress = Math.min((currentTime - startTime) / duration, 1);
        el.textContent = Math.floor(progress * (endValue - startValue) + startValue);
        if (progress < 1) requestAnimationFrame(animateStep);
    }
    requestAnimationFrame(animateStep);
}
