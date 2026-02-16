function showResult(status, elementId){
    let card = document.getElementById(elementId);
    card.style.display = "block";

    if(status.includes("SAFE")){
        card.className = "result-card safe-card";
        card.innerText = "✔ SAFE: No threats detected.";
    } else {
        card.className = "result-card danger-card";
        card.innerText = "⚠ ALERT: Potential cyber threat detected!";
    }
}
// ================= CHART.JS =================

const ctx = document.getElementById('attackChart');

if(ctx){
    const attackChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Phishing', 'Malware', 'Identity Theft', 'SMS Scam'],
            datasets: [{
                label: 'Attacks (Last Hour)',
                data: [12, 7, 5, 9],
                backgroundColor: [
                    '#00ADB5',
                    '#ff4c4c',
                    '#ffcc00',
                    '#00ff88'
                ]
            }]
        }
    });

    // Simulated live update
    setInterval(() => {
        attackChart.data.datasets[0].data =
            attackChart.data.datasets[0].data.map(val => val + Math.floor(Math.random()*3));
        attackChart.update();

        updateRiskLevel();
    }, 4000);
}

// ================= RISK METER =================

function updateRiskLevel(){
    let risk = Math.floor(Math.random() * 100);
    let bar = document.getElementById("riskBar");
    let text = document.getElementById("riskText");

    if(bar){
        bar.style.width = risk + "%";
        text.innerText = "Risk Level: " + risk + "%";
    }
}

