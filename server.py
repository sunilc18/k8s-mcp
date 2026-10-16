import subprocess
from mcp.server.fastmcp import FastMCP # import modules from mcp package

mcp = FastMCP(name="Kubernetes MCP Server", json_response=True)

# -----------------------
# Helper function
#------------------------
def run_command(command: list[str]) -> str:   # helper function to run a command in the shell and return the output
    try:
        result =  subprocess.run(
            command, capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e: # if the command fails, return the error message and don't panic
        return f"error: {e.stderr}"
    
    
#-----------------------
# Tools: Get namespaces
#-----------------------
@mcp.tool()
def get_namespaces() -> str:
    """
    Get the list of Kubernetes namespaces.
    """
    return run_command(
        ["kubectl", "get", "ns"]
    )

#-----------------------
# Tools: Get pods
#-----------------------
@mcp.tool()
def get_pods(namespace: str = "default") -> str:
    """
    Get the list of pods from a namespace.
    """
    return run_command(
        ["kubectl", "get", "pods", "-n", namespace]
    )

#-----------------------
# Tools: Get Pod logs
#-----------------------
@mcp.tool()
def get_pod_logs(pod_name: str, namespace: str = "default") -> str:
    """
    Get the logs of a specific pod.
    """
    return run_command(
        ["kubectl", "logs", pod_name, "-n", namespace]
    )

#-----------------------
# Tools: Restart Deployment
#-----------------------
@mcp.tool()
def restart_deployment(deployment: str, namespace: str = "default") -> str:
    """
    Restart a specific deployment.
    """
    return run_command(
        ["kubectl", "rollout", "restart", f"deployment/{deployment}", "-n", namespace]
    )

#-----------------------
# Resource example: Get cluster info
#-----------------------
@mcp.resource("cluster://info")
def get_cluster_info() -> str:
    """
    Get cluster information.
    """
    return run_command(
        ["kubectl", "cluster-info"]
    )


#-----------------------
# Prompt example
#-----------------------
@mcp.prompt()
def pod_troubleshooting_prompt(pod_name: str) -> str:
    """
    Generate a troubleshooting prompt for a specific pod.
    """
    return f"""
You are a Kubernetes troubleshooting expert.

Analze pod: {pod_name}

check:
- CrashLoopBackOff
- ImagePullBackOff
- OOMKilled
- Readiness and Liveness probes
- Restart count
"""

#-----------------------
# Run the MCP server
#-----------------------
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )




