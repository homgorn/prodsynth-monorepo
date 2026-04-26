import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

const errorRate = new Rate("errors");
const synthesisDuration = new Trend("synthesis_duration");
const apiDuration = new Trend("api_duration");

export const options = {
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"],
    errors: ["rate<0.05"],
  },
  stages: [
    { duration: "30s", target: 10 },
    { duration: "1m", target: 50 },
    { duration: "2m", target: 100 },
    { duration: "1m", target: 200 },
    { duration: "30s", target: 0 },
  ],
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";

export default function () {
  const workspaceId = "test_ws_001";
  const headers = {
    "Content-Type": "application/json",
    "X-Workspace-ID": workspaceId,
  };

  // 1. Health check
  const health = http.get(`${BASE_URL}/health`);
  check(health, { "health check": (r) => r.status === 200 });
  sleep(0.5);

  // 2. Authentication
  const loginRes = http.post(
    `${BASE_URL}/api/v1/auth/login`,
    JSON.stringify({ email: "test@example.com", password: "test123" }),
    { headers }
  );
  const loginOk = check(loginRes, { "login": (r) => r.status === 200 });
  errorRate.add(!loginOk);
  let token = loginOk ? loginRes.json("access_token") : null;
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  sleep(0.5);

  // 3. List projects
  const projectsRes = http.get(`${BASE_URL}/api/v1/projects`, { headers });
  check(projectsRes, { "list projects": (r) => r.status === 200 });
  sleep(0.3);

  // 4. Create project
  const createRes = http.post(
    `${BASE_URL}/api/v1/projects`,
    JSON.stringify({ name: `load-test-${Date.now()}`, description: "k6 load test" }),
    { headers }
  );
  const projectOk = check(createRes, { "create project": (r) => r.status === 200 });
  errorRate.add(!projectOk);
  const projectId = projectOk ? createRes.json("id") : null;
  sleep(0.3);

  // 5. Get marketplace templates
  const templatesRes = http.get(`${BASE_URL}/api/v1/marketplace/templates`);
  check(templatesRes, { "marketplace templates": (r) => r.status === 200 });
  sleep(0.3);

  // 6. Get billing plans
  const plansRes = http.get(`${BASE_URL}/api/v1/billing/plans`);
  check(plansRes, { "billing plans": (r) => r.status === 200 });
  sleep(0.3);

  // 7. Run synthesis (heavy)
  if (projectId) {
    const start = Date.now();
    const synthRes = http.post(
      `${BASE_URL}/api/v1/synthesis/run`,
      JSON.stringify({ project_id: projectId, target: "docker" }),
      { headers }
    );
    check(synthRes, { "synthesis run": (r) => r.status === 200 });
    synthesisDuration.add(Date.now() - start);
    errorRate.add(synthRes.status !== 200);
  }

  sleep(1);
}