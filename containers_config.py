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

def check_container_running(cont_name):
    running_containers = list_running_containers()
    containers = []

    if running_containers:
        for container_info in running_containers:
            _, container_name = container_info.split()
            containers.append(container_name)
        if cont_name in containers:
            return True
    
    return False