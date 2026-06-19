import { useState } from "react";
import api from "../api";

function ResumeUpload({ setResumeId }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const uploadResume = async () => {
    if (!file) {
      setMessage("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post(
        "/resumes/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const resumeId = response.data.id;

      setResumeId(resumeId);

      // Save for refresh persistence
      localStorage.setItem(
        "resumeId",
        resumeId
      );

      setMessage(
        `Uploaded successfully. Resume ID: ${resumeId}`
      );
    } catch (error) {
      console.error(error);

      setMessage(
        "Failed to upload resume"
      );
    }
  };

  return (
    <div className="card">
      <h2>📄 Resume Upload</h2>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br />
      <br />

      <button onClick={uploadResume}>
        Upload Resume
      </button>

      <p
        style={{
          marginTop: "15px",
        }}
      >
        {message}
      </p>
    </div>
  );
}

export default ResumeUpload;