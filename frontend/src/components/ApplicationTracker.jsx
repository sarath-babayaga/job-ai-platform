import { useEffect, useState } from "react";
import api from "../api";

function ApplicationTracker() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = async () => {
    try {
      const response = await api.get(
        "/applications/"
      );

      setApplications(response.data);
    } catch (error) {
      console.error(
        "Failed to load applications:",
        error
      );
    }
  };

  return (
    <div className="card">
      <h2>📋 Applications</h2>

      {applications.length === 0 ? (
        <p>No applications yet</p>
      ) : (
        <table
          style={{
            width: "100%",
            marginTop: "10px",
          }}
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Resume</th>
              <th>Job</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {applications.map((app) => (
              <tr key={app.id}>
                <td>{app.id}</td>
                <td>{app.resume_id}</td>
                <td>{app.job_id}</td>
                <td>{app.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ApplicationTracker;