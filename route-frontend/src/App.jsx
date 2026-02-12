import { useState } from "react";
import axios from "axios";

export default function App() {
  const [form, setForm] = useState({
    start: "",
    end: "",
    mpg: 10,
    tank_size: 50,
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/optimize-route/",
        {
          start_coords: [77.5946, 12.9716],
          end_coords: [72.8777, 19.076],
          mpg: 15,
          tank_size: 50,
        }
      );
      console.log("SUCCESS RESPONSE:", response);
      console.log("DATA:", response.data);
      setResult(response.data);
    } catch (error) {
      console.log("ERROR OBJECT:", error);
      console.log("ERROR RESPONSE:", error.response);
      console.log("ERROR DATA:", error.response?.data);
      setError("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        {/* Header */}
        <div style={styles.header}>
          <div style={styles.iconWrapper}>
            <svg
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
          </div>
          <h1 style={styles.title}>Route Optimization</h1>
          <p style={styles.subtitle}>
            Find the most fuel-efficient route for your journey
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <span style={styles.labelText}>Starting Location</span>
              <input
                type="text"
                name="start"
                value={form.start}
                onChange={handleChange}
                placeholder="Enter starting point"
                style={styles.input}
              />
            </label>
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>
              <span style={styles.labelText}>Destination</span>
              <input
                type="text"
                name="end"
                value={form.end}
                onChange={handleChange}
                placeholder="Enter destination"
                style={styles.input}
              />
            </label>
          </div>

          <div style={styles.row}>
            <div style={styles.inputGroup}>
              <label style={styles.label}>
                <span style={styles.labelText}>MPG (Miles Per Gallon)</span>
                <input
                  type="number"
                  name="mpg"
                  value={form.mpg}
                  onChange={handleChange}
                  placeholder="15"
                  style={styles.input}
                />
              </label>
            </div>

            <div style={styles.inputGroup}>
              <label style={styles.label}>
                <span style={styles.labelText}>Tank Size (Gallons)</span>
                <input
                  type="number"
                  name="tank_size"
                  value={form.tank_size}
                  onChange={handleChange}
                  placeholder="50"
                  style={styles.input}
                />
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.button,
              ...(loading ? styles.buttonDisabled : {}),
            }}
          >
            {loading ? (
              <span style={styles.buttonContent}>
                <span style={styles.spinner}></span>
                Optimizing Route...
              </span>
            ) : (
              <span style={styles.buttonContent}>
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <polyline points="9 11 12 14 22 4"></polyline>
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
                </svg>
                Optimize Route
              </span>
            )}
          </button>
        </form>

        {/* Error Message */}
        {error && (
          <div style={styles.errorCard}>
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>{error}</span>
          </div>
        )}

        {/* Results */}
        {result && (
          <div style={styles.resultsCard}>
            <h2 style={styles.resultsTitle}>Route Summary</h2>

            <div style={styles.statsGrid}>
              <div style={styles.statCard}>
                <div style={styles.statIcon}>
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                  </svg>
                </div>
                <div style={styles.statContent}>
                  <p style={styles.statLabel}>Total Distance</p>
                  <p style={styles.statValue}>
                    {result.total_distance_miles}
                    <span style={styles.statUnit}>miles</span>
                  </p>
                </div>
              </div>

              <div style={styles.statCard}>
                <div style={styles.statIcon}>
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                    <polyline points="9 22 9 12 15 12 15 22"></polyline>
                  </svg>
                </div>
                <div style={styles.statContent}>
                  <p style={styles.statLabel}>Fuel Used</p>
                  <p style={styles.statValue}>
                    {result.total_gallons_used}
                    <span style={styles.statUnit}>gal</span>
                  </p>
                </div>
              </div>

              <div style={styles.statCard}>
                <div style={styles.statIcon}>
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <line x1="12" y1="1" x2="12" y2="23"></line>
                    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                  </svg>
                </div>
                <div style={styles.statContent}>
                  <p style={styles.statLabel}>Total Cost</p>
                  <p style={styles.statValue}>
                    ${result.total_fuel_cost}
                  </p>
                </div>
              </div>

              <div style={styles.statCard}>
                <div style={styles.statIcon}>
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <rect x="1" y="3" width="15" height="13"></rect>
                    <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon>
                    <circle cx="5.5" cy="18.5" r="2.5"></circle>
                    <circle cx="18.5" cy="18.5" r="2.5"></circle>
                  </svg>
                </div>
                <div style={styles.statContent}>
                  <p style={styles.statLabel}>Fuel Stops</p>
                  <p style={styles.statValue}>{result.fuel_stops.length}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    padding: "40px 20px",
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
  },
  card: {
    maxWidth: "700px",
    margin: "0 auto",
    background: "white",
    borderRadius: "20px",
    boxShadow: "0 20px 60px rgba(0, 0, 0, 0.3)",
    overflow: "hidden",
  },
  header: {
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    padding: "40px 30px",
    color: "white",
    textAlign: "center",
  },
  iconWrapper: {
    width: "64px",
    height: "64px",
    margin: "0 auto 20px",
    background: "rgba(255, 255, 255, 0.2)",
    borderRadius: "50%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    backdropFilter: "blur(10px)",
  },
  title: {
    margin: "0 0 8px 0",
    fontSize: "32px",
    fontWeight: "700",
    letterSpacing: "-0.5px",
  },
  subtitle: {
    margin: "0",
    fontSize: "16px",
    opacity: "0.9",
    fontWeight: "400",
  },
  form: {
    padding: "30px",
  },
  inputGroup: {
    marginBottom: "20px",
    flex: "1",
  },
  label: {
    display: "block",
    width: "100%",
  },
  labelText: {
    display: "block",
    marginBottom: "8px",
    fontSize: "14px",
    fontWeight: "600",
    color: "#374151",
  },
  input: {
    width: "100%",
    padding: "12px 16px",
    fontSize: "15px",
    border: "2px solid #e5e7eb",
    borderRadius: "10px",
    transition: "all 0.2s",
    outline: "none",
    boxSizing: "border-box",
  },
  row: {
    display: "flex",
    gap: "16px",
    marginBottom: "20px",
  },
  button: {
    width: "100%",
    padding: "14px 24px",
    fontSize: "16px",
    fontWeight: "600",
    color: "white",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    transition: "all 0.3s",
    boxShadow: "0 4px 15px rgba(102, 126, 234, 0.4)",
  },
  buttonDisabled: {
    opacity: "0.7",
    cursor: "not-allowed",
  },
  buttonContent: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
  },
  spinner: {
    width: "16px",
    height: "16px",
    border: "2px solid rgba(255, 255, 255, 0.3)",
    borderTopColor: "white",
    borderRadius: "50%",
    animation: "spin 0.8s linear infinite",
    display: "inline-block",
  },
  errorCard: {
    margin: "0 30px 30px",
    padding: "16px 20px",
    background: "#fee2e2",
    border: "2px solid #fca5a5",
    borderRadius: "10px",
    color: "#991b1b",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    fontSize: "15px",
    fontWeight: "500",
  },
  resultsCard: {
    margin: "0 30px 30px",
    padding: "24px",
    background: "#f9fafb",
    borderRadius: "12px",
    border: "1px solid #e5e7eb",
  },
  resultsTitle: {
    margin: "0 0 20px 0",
    fontSize: "20px",
    fontWeight: "700",
    color: "#111827",
  },
  statsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(2, 1fr)",
    gap: "16px",
  },
  statCard: {
    background: "white",
    padding: "20px",
    borderRadius: "10px",
    border: "1px solid #e5e7eb",
    display: "flex",
    alignItems: "flex-start",
    gap: "12px",
  },
  statIcon: {
    width: "48px",
    height: "48px",
    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    borderRadius: "10px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "white",
    flexShrink: "0",
  },
  statContent: {
    flex: "1",
  },
  statLabel: {
    margin: "0 0 6px 0",
    fontSize: "13px",
    fontWeight: "500",
    color: "#6b7280",
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  statValue: {
    margin: "0",
    fontSize: "24px",
    fontWeight: "700",
    color: "#111827",
  },
  statUnit: {
    fontSize: "14px",
    fontWeight: "500",
    color: "#6b7280",
    marginLeft: "4px",
  },
};

// Add keyframe animation for spinner
const styleSheet = document.styleSheets[0];
styleSheet.insertRule(
  `
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`,
  styleSheet.cssRules.length
);