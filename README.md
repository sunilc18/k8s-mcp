# k8s-mcp — Kubernetes MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes Kubernetes tools, resources, and prompts to AI agents like GitHub Copilot.

---

## 🚀 Setup & Integration Guide

### Step 1 — Install Dependencies

```bash
cd /path/to/k8s-mcp

# Initialize project and add mcp dependency
uv init --name k8s-mcp
uv add "mcp[cli]"
```

---

### Step 2 — Start the MCP Server

```bash
uv run server.py
```

The server starts at: **`http://127.0.0.1:8000/mcp`**

---

### Step 3 — Connect to Kubernetes (Rancher Desktop / any cluster)

The server uses `kubectl` under the hood. Ensure your cluster is running and `kubectl` is configured:

```bash
# Verify kubectl is pointing to the right cluster
kubectl config current-context

# Test connectivity
kubectl get ns
```

> ✅ No extra config needed — the MCP server automatically uses the active `kubectl` context.

---

### Step 4 — Integrate with GitHub Copilot CLI

In your **Copilot CLI terminal** (at the `>` prompt), run:

```
/mcp add
```

When prompted, fill in:

| Field | Value |
|---|---|
| **Name** | `k8s-mcp` |
| **Type** | `http` |
| **URL** | `http://127.0.0.1:8000/mcp` |

Or manually add to `~/.copilot/mcp.json`:

```json
{
  "mcpServers": {
    "k8s-mcp": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

---

### Step 5 — Test it in Copilot CLI

Once connected, ask Copilot in your terminal:

- _"List all Kubernetes namespaces"_ → uses `get_namespaces` tool
- _"Show pods in the default namespace"_ → uses `get_pods` tool
- _"Get logs for pod xyz"_ → uses `get_pod_logs` tool
- _"Restart deployment my-app"_ → uses `restart_deployment` tool

> 💡 When Copilot uses an MCP tool, you'll see it explicitly mention the tool call (e.g., `🔧 Using tool: get_namespaces (k8s-mcp)`).

---

## 🧰 Available MCP Primitives

### Tools
| Tool | Description |
|---|---|
| `get_namespaces()` | List all Kubernetes namespaces |
| `get_pods(namespace)` | List pods in a namespace (default: `default`) |
| `get_pod_logs(pod_name, namespace)` | Get logs of a specific pod |
| `restart_deployment(deployment, namespace)` | Restart a deployment |

### Resources
| URI | Description |
|---|---|
| `cluster://info` | Get Kubernetes cluster information |

### Prompts
| Prompt | Description |
|---|---|
| `pod_troubleshooting_prompt(pod_name)` | Generate a troubleshooting checklist for a pod |

---

## 🏭 Production Deployment

For production, host the MCP server centrally so all team members can use it:

- **Option 1 (Recommended):** Deploy as a pod **inside the Kubernetes cluster** with a ServiceAccount + RBAC
- **Option 2:** Run on a dedicated VM/server with a kubeconfig pointing to the cluster
- **Option 3:** Each user runs locally (current local dev setup)

### Security Checklist for Production
- [ ] Add authentication (API keys / OAuth)
- [ ] Configure RBAC to limit kubectl permissions
- [ ] Enable HTTPS/TLS
- [ ] Log all MCP tool calls for audit trail

---

## 📋 Architecture

```
Developer → GitHub Copilot CLI
                 ↕ MCP (HTTP)
           k8s-mcp server (server.py)
                 ↕ kubectl
           Kubernetes API Server
                 ↕
           Cluster Resources
```
