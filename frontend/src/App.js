import React, { useState, useEffect } from "react";

function App() {
  const [gesture, setGesture] = useState("Waiting for gesture...");

  useEffect(() => {
    const fetchGesture = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/gesture");
        const data = await response.json();
        setGesture(data.message);
      } catch (error) {
        console.error("Error fetching gesture:", error);
      }
    };

    fetchGesture();
    const interval = setInterval(fetchGesture, 2000); // Fetch every 2 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Gesture-Based HCI System</h1>
      <h2>Detected Gesture: {gesture}</h2>
    </div>
  );
}

export default App;
