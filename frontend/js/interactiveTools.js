const BASE_URL = 'http://127.0.0.1:5001';
const token = localStorage.getItem('token');
if (!token) {
    alert("You are not logged in. Please log in first.");
    window.location.href = '/login.html';
}

// DOM Elements
const moodForm = document.getElementById('mood-form');
const moodSelect = document.getElementById('mood-select');
const moodHistoryList = document.getElementById('mood-history');
const moodAnalysisText = document.getElementById('moodAnalysis');
const meditationSuggestionText = document.getElementById('meditationSuggestion');
const analysisSection = document.getElementById('result');
const quizModal = document.getElementById('quiz-modal');
const openQuizBtn = document.getElementById('open-quiz');
const closeQuizBtn = document.querySelector('.quiz-modal-card .cross-icon');
const quizForm = document.getElementById('quiz-form');
const suggestionResult = document.querySelector('.suggestion-div .result');
const ctx = document.getElementById('moodChart')?.getContext('2d');

let moodChart = null;

// ---------------- MOOD TRACKER ----------------
async function fetchMoods() {
    if (!token) return;

    try {
        const res = await fetch(`${BASE_URL}/get_mood`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });
        
        if (!res.ok) {
            console.warn("Failed to fetch moods:", res.status);
            return;
        }
        
        const data = await res.json();
        console.log("Fetched moods:", data);
        
        if (data.success && Array.isArray(data.moods)) {
            // Optional: Log sentiment and suggestion
            console.log("Sentiment:", data.sentiment);
            console.log("Suggestion:", data.suggestion);
        
            // Group moods for chart
            const moodCounts = data.moods.reduce((acc, m) => {
                const date = new Date(m.timestamp).toLocaleDateString(); // Group by date
                if (!acc[date]) acc[date] = { happy: 0, sad: 0, anxious: 0, stressed: 0, calm: 0, excited: 0, neutral: 0 };
                const mood = m.mood.toLowerCase();
                acc[date][mood] = (acc[date][mood] || 0) + 1;
                return acc;
            }, {});
        
            renderChart(moodCounts);
            renderMoodHistory(data.moods);
            renderMoodAnalysis(data.moods, data.sentiment, data.suggestion);
        }        
    } catch (err) {
        console.error("Error fetching moods:", err);
    }
}

// Function to submit mood data to the backend
function submitMood() {
    const mood = document.getElementById('mood-selector').value; // Get selected mood from the UI
    const quizData = getQuizData(); // Function to retrieve the quiz data (if any)

    // Make the POST request to add the mood
    fetch(`${BASE_URL}/add_mood`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,  // Ensure JWT token is sent in the header
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            mood: mood,  // Mood value (required)
            quiz_data: quizData,  // Optional quiz data (if any)
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Mood added successfully');
            fetchMoods(); // Ensure the mood list is updated
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to get quiz data (replace this with your actual quiz data logic)
function getQuizData() {
    // For demo purposes, assuming you have quiz answers stored somewhere
    return {
        score: 85,  // Example score from quiz
        answers: ['A', 'C', 'B']  // Example answers array
    };
}

function renderMoodHistory(moods) {
    if (!moodHistoryList) return;

    moodHistoryList.innerHTML = '';

    if (moods.length === 0) {
        const emptyMsg = document.createElement('li');
        emptyMsg.textContent = 'No mood data yet. Start tracking today!';
        moodHistoryList.appendChild(emptyMsg);
        if (moodChart) {
            moodChart.destroy();
            moodChart = null;
        }
        analysisSection.style.display = 'none';
        return;
    }

    moods.slice(0, 5).forEach(mood => {
        const li = document.createElement('li');
        li.textContent = `${mood.mood} – ${new Date(mood.timestamp).toLocaleString()}`;
        moodHistoryList.appendChild(li);
    });
}

function renderMoodAnalysis(moods, sentiment, suggestion) {
    if (!moodAnalysisText || !meditationSuggestionText || !analysisSection) return;

    if (moods.length === 0) {
        analysisSection.style.display = 'none';
        return;
    }

    const recentMood = moods[0]?.mood || 'neutral';
    suggestion = suggestion || '';

    moodAnalysisText.textContent = `Recent Mood: ${recentMood}`;
    meditationSuggestionText.textContent = suggestion;
    analysisSection.style.display = 'block';
}

function renderChart(moodCounts) {
    if (!ctx) return;

    // Prepare chart data
    const dates = Object.keys(moodCounts);
    const happyCounts = dates.map(date => moodCounts[date].happy);
    const sadCounts = dates.map(date => moodCounts[date].sad);
    const anxiousCounts = dates.map(date => moodCounts[date].anxious);
    const angryCounts = dates.map(date => moodCounts[date].angry);
    const neutralCounts = dates.map(date => moodCounts[date].neutral);

    if (moodChart) moodChart.destroy();

    moodChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Happy Mood',
                    data: happyCounts,
                    borderColor: 'rgba(39, 174, 96, 0.8)',
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Sad Mood',
                    data: sadCounts,
                    borderColor: 'rgba(231, 76, 60, 0.8)',
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Anxious Mood',
                    data: anxiousCounts,
                    borderColor: 'rgba(243, 156, 18, 0.8)',
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Angry Mood',
                    data: angryCounts,
                    borderColor: 'rgba(255, 87, 34, 0.8)',
                    fill: false,
                    tension: 0.1
                },
                {
                    label: 'Neutral Mood',
                    data: neutralCounts,
                    borderColor: 'rgba(189, 195, 199, 0.8)',
                    fill: false,
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                tooltip: { enabled: true }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Date' },
                    grid: { color: '#444' }
                },
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Mood Count' },
                    ticks: { color: '#fff' },
                    grid: { color: '#444' }
                }
            }
        }
    });
}

if (moodForm && moodSelect) {
    moodForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!token) {
            alert("You must be logged in.");
            return;
        }

        const selectedMood = moodSelect.value;

        try {
            const res = await fetch(`${BASE_URL}/add_mood`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ mood: selectedMood })
            });

            if (res.status === 401) {
                alert('Session expired. Please log in again.');
                localStorage.removeItem('token');
                window.location.href = '/login.html';
                return;
            }

            const data = await res.json();

            if (data.success || res.ok) {
                fetchMoods();
                moodForm.reset();
            } else {
                alert('Failed to save mood.');
            }
        } catch (err) {
            console.error('Error submitting mood:', err);
        }
    });
}

// ---------------- NAV TOGGLE ----------------
function openNav() {
    document.getElementById("mobile-nav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mobile-nav").style.width = "0";
}

// ---------------- QUIZ MODAL ----------------
function openModal() {
    quizModal.style.display = 'flex';
}

function closeModal() {
    quizModal.style.display = 'none';
}

if (openQuizBtn && quizModal) {
    openQuizBtn.addEventListener('click', openModal);
}

if (closeQuizBtn && quizModal) {
    closeQuizBtn.addEventListener('click', closeModal);
}

if (quizForm && suggestionResult) {
    quizForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(quizForm);
        let combinedText = '';
        for (const entry of formData.entries()) {
            combinedText += `${entry[1]} `;
        }

        try {
            const res = await fetch(`${BASE_URL}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: combinedText })
            });

            const data = await res.json();

            if (data.success) {
                suggestionResult.innerHTML = `
                    <p><strong>Sentiment:</strong> ${data.sentiment}</p>
                    <p><strong>Suggestion:</strong> ${data.suggestion}</p>
                `;
                closeModal();
                quizForm.reset();
            } else {
                suggestionResult.innerHTML = `<p>There was an issue analyzing your response.</p>`;
            }
        } catch (err) {
            console.error('Error during sentiment analysis:', err);
        }
    });
}

fetchMoods();
