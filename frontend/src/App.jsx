import { useState, useEffect } from "react";
import "./App.css";
import { motion } from "framer-motion";

import ResumeUpload from "./components/ResumeUpload";
import RecommendedJobs from "./components/RecommendedJobs";
import ATSScore from "./components/ATSScore";
import CandidateProfile from "./components/CandidateProfile";
import ApplicationTracker from "./components/ApplicationTracker";

function App() {
  const [resumeId, setResumeId] = useState(
    localStorage.getItem("resumeId")
      ? Number(localStorage.getItem("resumeId"))
      : null
  );

  const [applicationRefresh, setApplicationRefresh] =
    useState(0);

  useEffect(() => {
    if (resumeId) {
      localStorage.setItem(
        "resumeId",
        resumeId
      );
    }
  }, [resumeId]);

  return (
    <div className="app">
      <div className="hero">
        <motion.h1
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          🚀 Job AI Platform
        </motion.h1>

        <p>
          AI Resume Matching & Job Recommendations
        </p>
      </div>

      <div className="dashboard">
        <ResumeUpload
          setResumeId={setResumeId}
        />

        <CandidateProfile
          resumeId={resumeId}
        />

        <ATSScore
          resumeId={resumeId}
        />

        <RecommendedJobs
          resumeId={resumeId}
          onApplicationCreated={() =>
            setApplicationRefresh(
              (prev) => prev + 1
            )
          }
        />

        <ApplicationTracker
          refreshTrigger={
            applicationRefresh
          }
        />
      </div>
    </div>
  );
}

export default App;