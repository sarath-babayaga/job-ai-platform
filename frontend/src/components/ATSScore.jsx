import { useEffect, useState } from "react";
import api from "../api";

function ATSScore({ resumeId }) {
  const [score, setScore] = useState(null);

  useEffect(() => {
    if (resumeId) {
      loadScore();
    }
  }, [resumeId]);

  const loadScore = async () => {
    try {
      const response = await api.get(
        `/match/${resumeId}/1`
      );

      setScore(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  if (!score) {
    return (
      <div className="card">
        <h2>🎯 ATS Match Score</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>🎯 ATS Match Score</h2>

      <div className="score">
        {score.match_score}%
      </div>

      <p>
        <strong>Skills Matched:</strong>
      </p>

      <div
        style={{
          marginTop: "10px",
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          justifyContent: "center",
        }}
      >
        {score.matched_skills.map((skill) => (
          <span
            key={skill}
            style={{
              background: "#dcfce7",
              color: "#166534",
              padding: "6px 12px",
              borderRadius: "20px",
              fontSize: "14px",
            }}
          >
            {skill}
          </span>
        ))}
      </div>
    </div>
  );
}

export default ATSScore;