import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/fetch/gmail")
      .then(response => {
        console.log("Fetched emails:", response.data);
        if (response.data && Array.isArray(response.data.emails)) {
         
          const storedStatuses = JSON.parse(localStorage.getItem("emailStatuses")) || {};

          
          const updatedEmails = response.data.emails.map(email => ({
            ...email,
            status: storedStatuses[email.Subject] || "Not Opened",
          }));

          setEmails(updatedEmails);
        } else {
          console.error("Invalid response structure:", response.data);
        }
      })
      .catch(error => console.error("Error fetching emails:", error));
  }, []);

  // Function to generate context-aware quick replies
  const generateQuickReply = (email) => {
    const { Subject, Summary } = email;
    const text = `${Subject} ${Summary}`.toLowerCase();

    if (text.includes("security alert") || text.includes("password")) {
      return "Thanks for the security update. I'll review this immediately.";
    }
    if (text.includes("internship") || text.includes("job opportunity")) {
      return "Thanks for the opportunity! I'll check the details and get back to you.";
    }
    if (text.includes("event") || text.includes("webinar") || text.includes("hackathon")) {
      return "Sounds interesting! I'll review the details soon.";
    }
    if (text.includes("payment") || text.includes("invoice") || text.includes("subscription")) {
      return "I'll check the payment details and confirm. Thanks!";
    }
    if (text.includes("reminder") || text.includes("follow-up")) {
      return "Thanks for the reminder! I'll take action soon.";
    }
    if (text.includes("meeting") || text.includes("schedule a call")) {
      return "Sure, let me check my availability and get back to you.";
    }
    if (text.includes("hi") || text.includes("hello") || text.includes("how are you")) {
      return "Hey! Hope you're doing great. What's up?";
    }
    if (text.includes("happy new year") || text.includes("merry christmas")) {
      return "Happy holidays! Wishing you all the best.";
    }
    if (text.includes("technical issue") || text.includes("not working")) {
      return "I'm looking into this now. I'll update you soon!";
    }
    if (text.includes("miss you") || text.includes("catch up soon")) {
      return "Miss you too! Let's plan something soon.";
    }
    if (text.includes("spam") || text.includes("lottery") || text.includes("prize")) {
      return "Not interested, thanks!";
    }

    return "Noted, I'll review this when I get time.";
  };

  
  const handleReply = (index, email) => {
    
    const replyUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(email.From)}&su=${encodeURIComponent(email.Subject)}&body=${encodeURIComponent(generateQuickReply(email))}`;
    window.open(replyUrl, "_blank");

  
    setEmails(prevEmails => {
      const updatedEmails = prevEmails.map((e, i) =>
        i === index ? { ...e, status: "Replied" } : e
      );

      // Storing updated statuses in localStorage
      const updatedStatuses = updatedEmails.reduce((acc, e) => {
        acc[e.Subject] = e.status;
        return acc;
      }, {});

      localStorage.setItem("emailStatuses", JSON.stringify(updatedStatuses));

      return updatedEmails;
    });
  };

  return (
    <div>
      <h1>📩 AI Email Assistant Dashboard</h1>
      {emails.length === 0 ? (
        <p>📭 No emails found.</p>
      ) : (
        <table border="1">
          <thead>
            <tr>
              <th>From</th>
              <th>Subject</th>
              <th>Date</th>
              <th>Priority</th>
              <th>Summary</th>
              <th>Quick Reply</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {emails.map((email, index) => (
              <tr key={index}>
                <td>{email.From}</td>
                <td>{email.Subject}</td>
                <td>{email.Date}</td>
                <td>{email.Priority}</td>
                <td>{email.Summary}</td>
                <td>{generateQuickReply(email)}</td>
                <td>{email.status}</td>
                <td>
                  <button onClick={() => handleReply(index, email)}>Reply</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
