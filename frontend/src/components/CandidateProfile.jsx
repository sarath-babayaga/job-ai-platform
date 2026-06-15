import { useEffect, useState } from "react";
import api from "../api";

function CandidateProfile({ resumeId }) {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    if (resumeId) {
      loadProfile();
    }
  }, [resumeId]);

  const loadProfile = async () => {
    try {
      const response = await api.get(
        `/resumes/${resumeId}/analyze`
      );

      setProfile(response.data.analysis);
    } catch (error) {
      console.error(
        "Error loading profile:",
        error
      );
    }
  };

  if (!resumeId) {
    return (
      <div className="card">
        <h2>👤 Candidate Profile</h2>
        <p>Upload a resume to view profile</p>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="card">
        <h2>👤 Candidate Profile</h2>
        <p>Loading...</p>
      </div>
    );
  }

  const displayedSkills =
    profile.skills?.slice(0, 12) || [];

  const remainingSkills =
    profile.skills?.length > 12
      ? profile.skills.length - 12
      : 0;

  return (
    <div className="card">
      <h2>👤 Candidate Profile</h2>

      <p>
        <strong>Name:</strong>{" "}
        {profile.name || "N/A"}
      </p>

      <p>
        <strong>Email:</strong>{" "}
        {profile.email || "N/A"}
      </p>

      <p>
        <strong>Phone:</strong>{" "}
        {profile.phone || "N/A"}
      </p>

      <p>
        <strong>Experience:</strong>{" "}
        {profile.experience || "N/A"}
      </p>

      <h3>Skills</h3>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          marginTop: "10px",
        }}
      >
        {displayedSkills.map(
          (skill, index) => (
            <span
              key={index}
              style={{
                background: "#dbeafe",
                color: "#1d4ed8",
                padding: "6px 10px",
                borderRadius: "12px",
                fontSize: "12px",
              }}
            >
              {skill}
            </span>
          )
        )}
      </div>

      {remainingSkills > 0 && (
        <p
          style={{
            marginTop: "10px",
            color: "#666",
          }}
        >
          +{remainingSkills} more skills
        </p>
      )}
    </div>
  );
}

export default CandidateProfile;