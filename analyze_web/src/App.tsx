import { useState } from "react";
import snarkdown from "snarkdown";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState("");
  const [summary, setSummary] = useState("");

  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVideoUrl(e.target.value);
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(
        `/api/video/transcript?url=${encodeURIComponent(videoUrl)}`
      );
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error("Error fetching summary:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>YouTube Video Analyzer</h1>
        <p>Analyze and summarize YouTube video transcripts with ease.</p>
      </div>
      <div className="card">
        <div className="input-section">
          <input type="text" onChange={handleOnChange} />
          <button onClick={handleAnalyze} disabled={isLoading}>
            {isLoading ? "Analyzing..." : "Analyze Video"}
          </button>
        </div>
      </div>

      <div className="card summary">
        <h2>Summary</h2>
        {summary ? (
          <p
            className="summary-text"
            dangerouslySetInnerHTML={{
              __html: snarkdown(summary),
            }}
          />
        ) : (
          <p>Your summarized transcript will appear here.</p>
        )}
      </div>
      <div className="footer">
        <p>Feel free to fork and do what you need :)</p>
      </div>
    </div>
  );
}

export default App;
