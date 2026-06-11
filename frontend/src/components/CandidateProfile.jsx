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
      const response = await api.get(`/resumes/${resumeId}`);
      setProfile(response.data);
    } catch (error) {
      console.error("Error loading profile:", error);
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

  const displayedSkills = profile.skills?.slice(0, 12) || [];
  const remainingSkills =
    profile.skills?.length > 12 ? profile.skills.length - 12 : 0;

  return (
    <div className="card">
      <h2>👤 Candidate Profile</h2>

      <div style={{ marginBottom: "15px" }}>
        <p>
          <strong>Name:</strong> {profile.name}
        </p>

        <p>
          <strong>Email:</strong> {profile.email}
        </p>

        <p>
          <strong>Phone:</strong> {profile.phone}
        </p>

        <p>
          <strong>Experience:</strong> {profile.experience}
        </p>
      </div>

      <h3>Skills</h3>

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          justifyContent: "center",
        }}
      >
        {displayedSkills.map((skill, index) => (
          <span
            key={index}
            style={{
              background: "#dbeafe",
              color: "#2563eb",
              padding: "6px 10px",
              borderRadius: "15px",
              fontSize: "12px",
            }}
          >
            {skill}
          </span>
        ))}
      </div>

      {remainingSkills > 0 && (
        <p
          style={{
            marginTop: "12px",
            color: "#666",
            fontSize: "14px",
            textAlign: "center",
          }}
        >
          +{remainingSkills} more skills
        </p>
      )}
    </div>
  );
}

export default CandidateProfile;