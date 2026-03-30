document.addEventListener('DOMContentLoaded', () => {
    // Tab Navigation Logic
    const navLinks = document.querySelectorAll('.nav-links li');
    const tabPanes = document.querySelectorAll('.tab-pane');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Remove active class from all
            navLinks.forEach(l => l.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            // Add active class to clicked link and corresponding pane
            link.classList.add('active');
            const targetId = link.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');

            // Render chart if insights tab is clicked
            if (targetId === 'model-insights' && !window.chartRendered) {
                fetchMetrics();
            }
        });
    });

    // Score Prediction Form Handler (Linear Regression)
    const scoreForm = document.getElementById('score-form');
    scoreForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(scoreForm);
        const data = Object.fromEntries(formData.entries());
        
        // Disable button and animate
        const btn = scoreForm.querySelector('button');
        const origText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Predicting...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/predict-score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            const circle = document.getElementById('score-result-circle');
            const valueSpan = circle.querySelector('.score-value');

            if (result.success) {
                // Animate counting up
                let currentVal = 0;
                const targetVal = result.predicted_score;
                const duration = 1000;
                const steps = 30;
                const stepVal = targetVal / steps;
                
                circle.classList.remove('empty');
                circle.classList.add('success');
                
                const interval = setInterval(() => {
                    currentVal += stepVal;
                    if (currentVal >= targetVal) {
                        currentVal = targetVal;
                        clearInterval(interval);
                    }
                    valueSpan.textContent = currentVal.toFixed(1);
                }, duration / steps);
            } else {
                alert('Error: ' + result.error);
            }
        } catch (err) {
            console.error(err);
            alert('Failed to connect to the prediction server.');
        } finally {
            btn.innerHTML = origText;
            btn.disabled = false;
        }
    });

    // Grade Prediction Form Handler (Classifier)
    const gradeForm = document.getElementById('grade-form');
    gradeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(gradeForm);
        const data = Object.fromEntries(formData.entries());
        
        const btn = gradeForm.querySelector('button');
        const origText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/predict-grade', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            const circle = document.getElementById('grade-result-circle');
            const letterSpan = circle.querySelector('.grade-letter');
            const probContainer = document.getElementById('prob-bars-container');

            if (result.success) {
                circle.classList.remove('empty');
                circle.classList.add('badge-success');
                
                // Add minor pop animation
                letterSpan.style.transform = 'scale(0.5)';
                setTimeout(() => {
                    letterSpan.textContent = result.predicted_grade;
                    letterSpan.style.transition = 'transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                    letterSpan.style.transform = 'scale(1)';
                }, 200);

                // Render probabilities
                probContainer.style.display = 'block';
                // keep existing h4
                probContainer.innerHTML = '<h4>Class Probabilities</h4>';
                
                const probs = result.probabilities;
                // sort classes A B C D F 
                ['A', 'B', 'C', 'D', 'F'].forEach(cls => {
                    if (probs[cls] !== undefined) {
                        const val = probs[cls];
                        const color = val > 50 ? 'var(--primary-blue)' : 'var(--primary-purple)';
                        
                        const row = document.createElement('div');
                        row.className = 'prob-row';
                        row.innerHTML = `
                            <div class="prob-label">${cls}</div>
                            <div class="prob-bar-container">
                                <div class="prob-bar-fill" style="width: 0%; background:${color}"></div>
                            </div>
                            <div class="prob-val">${val}%</div>
                        `;
                        probContainer.appendChild(row);
                        
                        // animate filling
                        setTimeout(() => {
                            row.querySelector('.prob-bar-fill').style.width = `${val}%`;
                        }, 100);
                    }
                });

            } else {
                alert('Error: ' + result.error);
            }
        } catch (err) {
            console.error(err);
            alert('Failed to connect to the prediction server.');
        } finally {
            btn.innerHTML = origText;
            btn.disabled = false;
        }
    });

    // Fetch and Display Model Metrics
    async function fetchMetrics() {
        try {
            const response = await fetch('/api/model-metrics');
            if (response.ok) {
                const data = await response.json();
                
                // Update text stats
                document.getElementById('metric-r2').textContent = data.regression.r2_score.toFixed(3);
                document.getElementById('metric-rmse').textContent = data.regression.rmse.toFixed(2);
                document.getElementById('metric-acc').textContent = (data.classification.accuracy * 100).toFixed(1) + '%';

                // Render Chart.js for Feature Importance
                renderChart(data.features.names, data.features.importances);
                window.chartRendered = true;
            }
        } catch (e) {
            console.log("Metrics not ready or server down");
        }
    }

    function renderChart(labels, data) {
        const ctx = document.getElementById('importanceChart').getContext('2d');
        
        // Formatting labels for display
        const friendlyLabels = labels.map(l => l.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()));

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: friendlyLabels,
                datasets: [{
                    label: 'Relative Importance',
                    data: data,
                    backgroundColor: 'rgba(157, 78, 221, 0.6)',
                    borderColor: 'rgba(157, 78, 221, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: '#adb5bd' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { 
                            color: '#adb5bd',
                            maxRotation: 45,
                            minRotation: 45
                        }
                    }
                }
            }
        });
    }
});
