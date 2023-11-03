import os
import time
import sys
from containers_config import check_container_running

# According to the command inputed on the terminal, respective config file is copied to the default nginx configuration.
# e.g. If run_blue command is provided then blue config file is set as default nginx configurtaion file.


def update_weights(traffic_shift_percentage, server_name):
    if server_name == 'blue':
        blue_weight = int(traffic_shift_percentage * 0.1)
        green_weight = 10 - blue_weight
    if server_name == 'green':
        green_weight = int(traffic_shift_percentage * 0.1)
        blue_weight = 10 - green_weight

    with open('./nginx/configs/blue-green.conf', 'r') as blue_green_config:
            content = blue_green_config.read()

        # Replace placeholders in the template with the updated values
    updated_config = content.replace('__BLUE_WEIGHT__', str(blue_weight)).replace('__GREEN_WEIGHT__', str(green_weight))

        # Write the updated content to the Nginx configuration file
    with open('./nginx/default.conf', 'w') as config_file:
        config_file.write(updated_config)

    # Reload Nginx to apply the changes
    os.system('docker exec -it demo_nginx nginx -s reload')

    print(f"Nginx configuration updated. {traffic_shift_percentage}% traffic handled by {server_name} server.")

    time.sleep(5) # traffic is shifted every 10 seconds


def run_blue():
    # copy the configuration file of blue server
    with open('./nginx/configs/blue.conf', 'r') as blue_config:
        content = blue_config.read()

    with open('./nginx/default.conf', 'w') as config_file:
        config_file.write(content)

    print("Nginx configuration updated. 100% traffic shifted to blue server.")

    # Reload Nginx to apply the changes
    os.system('docker exec -it demo_nginx nginx -s reload')

def run_green():
    # copy the configuration file of green server

    with open('./nginx/configs/green.conf', 'r') as green_config:
        content = green_config.read()

    with open('./nginx/default.conf', 'w') as config_file:
        config_file.write(content)

    print("Nginx configuration updated. 100% traffic shifted to green server.")

    # Reload Nginx to apply the changes
    os.system('docker exec -it demo_nginx nginx -s reload')

def run_blue_green(server_name, traffic_shift_percentage):
    traffic_shift_percentage = int(traffic_shift_percentage)

    if server_name == 'blue':
        if not check_container_running('demo_blue'):
            print('Blue server of blue stack not running.')
        elif traffic_shift_percentage == 100:
            run_blue()
        else:
            update_weights(traffic_shift_percentage=traffic_shift_percentage, server_name=server_name)

    elif server_name == 'green':
        if not check_container_running('demo_green'):
            print('Green server of green stack not running.')
        elif traffic_shift_percentage == 100:
            run_green()
        else:
            update_weights(traffic_shift_percentage=traffic_shift_percentage, server_name=server_name)
    else:
        print('Invalid server name or percentage')


if __name__ == '__main__':
    run_blue_green(sys.argv[1], sys.argv[2])

