document.addEventListener("DOMContentLoaded", () => {
  console.log("Mood tracking script loaded");

  const token = localStorage.getItem("token");
  const moodForm = document.getElementById("mood-form");
  const moodInput = document.getElementById("mood-input");
  const resultDiv = document.getElementById("mood-result");
  const moodHistoryList = document.getElementById("mood-history");

  if (!moodForm || !moodInput || !resultDiv || !moodHistoryList) {
    console.warn("Mood form elements not found on this page.");
    return;
  }

  if (!token) {
    resultDiv.textContent = "Please login to submit your mood.";
    return;
  }

  // Function to fetch and display past moods
  async function loadMoodHistory() {
    try {
      const response = await fetch("http://localhost:5001/get_mood", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch mood history.");
      }

      const moods = await response.json();

      moodHistoryList.innerHTML = ""; // Clear existing list
      if (moods.length === 0) {
        moodHistoryList.innerHTML = "<li>No mood entries yet.</li>";
        return;
      }

      moods.forEach((entry) => {
        const listItem = document.createElement("li");
        listItem.textContent = `${entry.timestamp} - ${entry.mood_text}`;
        moodHistoryList.appendChild(listItem);
      });
    } catch (err) {
      console.error("Error loading mood history:", err);
      moodHistoryList.innerHTML = "<li>Error loading mood history.</li>";
    }
  }

  // Initial load of mood history
  loadMoodHistory();

  // Handle mood submission
  moodForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const moodText = moodInput.value.trim();

    if (!moodText) {
      resultDiv.textContent = "Please enter your mood.";
      return;
    }

    try {
      // 1. Send to /add_mood
      const moodResponse = await fetch("http://localhost:5001/add_mood", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ mood_text: moodText }),
      });

      if (!moodResponse.ok) {
        throw new Error("Failed to submit mood.");
      }

      // 2. Send to /analyze for sentiment
      const sentimentResponse = await fetch("http://localhost:5001/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: moodText }),
      });

      const sentimentData = await sentimentResponse.json();

      if (!sentimentData || !sentimentData.compound) {
        throw new Error("Invalid sentiment analysis response.");
      }

      resultDiv.innerHTML = `
        <p><strong>Mood submitted!</strong></p>
        <p>Sentiment score: ${sentimentData.compound}</p>
      `;

      moodInput.value = "";
      loadMoodHistory(); // Refresh history after new entry
    } catch (err) {
      console.error(err);
      resultDiv.textContent = "Something went wrong. Try again.";
    }
  });
});
