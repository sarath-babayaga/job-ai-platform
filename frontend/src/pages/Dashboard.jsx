import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  const resumeId = 1; // replace later with uploaded resume id

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/jobs/hr/matches/${resumeId}`
      );

      setJobs(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <h2>Loading jobs...</h2>;

  return (
    <div className="container">
      <h1>Top ATS Matching HR Jobs</h1>

      <div className="job-grid">
        {jobs.map((job) => (
          <div className="job-card" key={job.id}>
            <h3>{job.title}</h3>

            <p>
              <strong>Company:</strong> {job.company}
            </p>

            <p>
              <strong>Location:</strong> {job.location}
            </p>

            <p>
              <strong>Match Score:</strong> {job.match_score}%
            </p>

            <button>
              Apply
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}