import subprocess

def list_running_containers():
    try:
        # Run the Docker command to list all running containers
        result = subprocess.run(['docker', 'ps', '--format', '{{.ID}} {{.Names}}', '--filter', 'status=running'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        if result.stdout:
            return result.stdout.strip().split('\n')
        else:
            return []
    except subprocess.CalledProcessError:
        return []

def check_container_running(container_name_contains):
    running_containers = list_running_containers()

    if running_containers:
        for container_info in running_containers:
            container_id, container_name = container_info.split()
            if container_name_contains in container_name:
                return container_name
            return None
    else:
        print("No running containers found.")
        return None
