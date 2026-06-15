import { useEffect, useState } from "react";
import api from "../api";

function RecommendedJobs({ resumeId }) {
  const [jobs, setJobs] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (resumeId) {
      loadJobs();
    }
  }, [resumeId]);

  const loadJobs = async () => {
    try {
      const response = await api.get(
        `/recommend-jobs/${resumeId}`
      );

      setJobs(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const applyJob = async (jobId) => {
    try {
      await api.post("/applications/", {
        resume_id: resumeId,
        job_id: jobId,
      });

      setMessage("✅ Application submitted successfully");
    } catch (error) {
      console.error(error);
      setMessage("❌ Failed to apply");
    }
  };

  return (
    <div className="card">
      <h2>💼 Recommended Jobs</h2>

      {message && (
        <p
          style={{
            color: "green",
            fontWeight: "bold",
          }}
        >
          {message}
        </p>
      )}

      {jobs.length === 0 ? (
        <p>No jobs found</p>
      ) : (
        jobs.map((job) => (
          <div
            key={job.job_id}
            style={{
              borderBottom: "1px solid #ddd",
              padding: "10px 0",
              marginBottom: "8px",
            }}
          >
            <div>
              <strong>{job.title}</strong>
            </div>

            <div>{job.company}</div>

            <div>{job.location}</div>

            <div>
              Match Score:{" "}
              <strong>
                {job.match_score}%
              </strong>
            </div>

            <button
              onClick={() =>
                applyJob(job.job_id)
              }
              style={{
                marginTop: "8px",
              }}
            >
              Apply
            </button>
          </div>
        ))
      )}
    </div>
  );
}

export default RecommendedJobs;