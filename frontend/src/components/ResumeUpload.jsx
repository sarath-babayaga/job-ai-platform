import { useState } from "react";
import api from "../api";

function ResumeUpload({ setResumeId }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const uploadResume = async () => {
    if (!file) {
      alert("Select a resume first");
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

      const uploadedResumeId =
        response.data.id ||
        response.data.resume_id;

      setResumeId(uploadedResumeId);

      setMessage(
        `Uploaded successfully. Resume ID: ${uploadedResumeId}`
      );
    } catch (error) {
      console.error(error);
      setMessage("Upload failed");
    }
  };

  return (
    <div className="card">
      <h2>📄 Resume Upload</h2>

      <input
        type="file"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br />
      <br />

      <button onClick={uploadResume}>
        Upload Resume
      </button>

      <p>{message}</p>
    </div>
  );
}

export default ResumeUpload;