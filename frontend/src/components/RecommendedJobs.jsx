import { useEffect, useState } from "react";
import api from "../api";

function RecommendedJobs({
  resumeId,
  onApplicationCreated,
}) {
  const [jobs, setJobs] = useState([]);
  const [message, setMessage] =
    useState("");

  useEffect(() => {
    if (resumeId) {
      loadJobs();
    }
  }, [resumeId]);

  const loadJobs = async () => {
    try {
      const response = await api.get(
        `/jobs/hr/matches/${resumeId}`
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

      setMessage(
        "✅ Application submitted successfully"
      );

      if (
        onApplicationCreated
      ) {
        onApplicationCreated();
      }

      setTimeout(() => {
        setMessage("");
      }, 3000);

    } catch (error) {
      console.error(error);

      setMessage(
        "❌ Failed to apply"
      );
    }
  };

  return (
    <div className="card">
      <h2>
        🔥 Top ATS Matching HR Jobs
      </h2>

      {message && (
        <p
          style={{
            color: "green",
            fontWeight: "bold",
            marginBottom: "15px",
          }}
        >
          {message}
        </p>
      )}

      {!resumeId ? (
        <p>
          Upload a resume first
        </p>
      ) : jobs.length === 0 ? (
        <p>
          Loading matching jobs...
        </p>
      ) : (
        jobs.map((job) => (
          <div
            key={job.job_id}
            style={{
              borderBottom:
                "1px solid #ddd",
              padding: "12px 0",
              marginBottom: "10px",
            }}
          >
            <div>
              <strong>
                {job.title}
              </strong>
            </div>

            <div>
              {job.company}
            </div>

            <div>
              {job.location}
            </div>

            <div>
              Match Score:
              <strong>
                {" "}
                {job.match_score}%
              </strong>
            </div>

            <button
              onClick={() =>
                applyJob(
                  job.job_id
                )
              }
              style={{
                marginTop:
                  "10px",
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