import { useState } from "react";
import "./App.css";
import { motion } from "framer-motion";

import ResumeUpload from "./components/ResumeUpload";
import RecommendedJobs from "./components/RecommendedJobs";
import ATSScore from "./components/ATSScore";
import CandidateProfile from "./components/CandidateProfile";
import ApplicationTracker from "./components/ApplicationTracker";

function App() {
  const [resumeId, setResumeId] = useState(null);

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
        />
        
        <ApplicationTracker
          // resumeId={resumeId}
        />
      </div>
    </div>
  );
}

export default App;