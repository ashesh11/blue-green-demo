import os
import sys
import time
from containers_config import check_container_running


# According to the command inputed on the terminal, respective config file is copied to the default nginx configuration.
# e.g. If run_blue command is provided then blue config file is set as default nginx configurtaion file.
class BlueGreenNginxConfig:
    def __init__(self):
        pass

    def update_weights(self):
        pass
    
    def run_blue(self):
        blue_server_container_name = 'demo_blue_1'
        container_running = check_container_running(blue_server_container_name)

        if not container_running:
            os.system(f'docker start {blue_server_container_name}')

        # copy the configuration file of blue server
        with open('./nginx/configs/blue.conf', 'r') as blue_config:
            content = blue_config.read()

        with open('./nginx/default.conf', 'w') as config_file:
            config_file.write(content)

        print("Green server fully active")

        # Reload Nginx to apply the changes
        os.system('docker exec -it demo_nginx_1 nginx -s reload')

    def run_green(self):
        green_server_container_name = 'demo_blue_1'
        container_running = check_container_running(green_server_container_name)
        
        if not container_running:
            os.system(f'docker start {green_server_container_name}')

        # copy the configuration file of green server

        with open('./nginx/configs/green.conf', 'r') as green_config:
            content = green_config.read()

        with open('./nginx/default.conf', 'w') as config_file:
            config_file.write(content)

        print("Green server fully active")

        # Reload Nginx to apply the changes
        os.system('docker exec -it demo_nginx_1 nginx -s reload')

    def run_blue_green(self):
        blue_server_container_name = 'demo_blue_1'
        green_server_container_name = 'demo_green_1'

        # Todo: count total requests and set it here
        total_requests_per_minute = 60 # assumed the request count to be 60
        shift_ratio = 0.9

        container_running = check_container_running(blue_server_container_name)

        if container_running == blue_server_container_name:
            blue_weight = int(shift_ratio * 60)
            green_weight = total_requests_per_minute - blue_weight

        elif container_running == green_server_container_name:
            green_weight = int(shift_ratio * 60)
            blue_weight = total_requests_per_minute - green_weight

        while shift_ratio > 0:

            # Read the Nginx configuration template
            with open('./nginx/configs/blue-green.conf', 'r') as blue_green_config:
                content = blue_green_config.read()

            # Replace placeholders in the template with the updated values
            updated_config = content.replace('__BLUE_WEIGHT__', str(blue_weight)).replace('__GREEN_WEIGHT__', str(green_weight))

            # Write the updated content to the Nginx configuration file
            with open('./nginx/default.conf', 'w') as config_file:
                config_file.write(updated_config)

            print(f"Nginx configuration updated. {100 -int(shift_ratio * 100)}% traffic shifted to green server.")

            # Reload Nginx to apply the changes
            os.system('docker exec -it demo_nginx_1 nginx -s reload')

            shift_ratio -= 0.1 # 10% traffic is shifted every 10 seconds

            time.sleep(1) # traffic is shifted every 10 seconds

        os.system('docker stop demo_blue_1')
        config_nginx.run_green()

if __name__ == '__main__':
    config_nginx = BlueGreenNginxConfig()
    function_name = sys.argv[1]

    if function_name == 'run_blue':
        config_nginx.run_blue()
        
    if function_name == 'run_green':
        config_nginx.run_green()

    if function_name == 'run_blue_green':
        config_nginx.run_blue_green()

