import { useEffect, useState } from "react";
import api from "../api";

function RecommendedJobs({ resumeId }) {
  const [jobs, setJobs] = useState([]);

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

  return (
    <div className="card">
      <h2>💼 Recommended Jobs</h2>

      {jobs.length === 0 ? (
        <p>No jobs found</p>
      ) : (
        jobs.map((job) => (
          <div
            className="job"
            key={job.job_id}
          >
            <span>
              {job.title}
            </span>

            <span>
              {job.match_score}%
            </span>
          </div>
        ))
      )}
    </div>
  );
}

export default RecommendedJobs;