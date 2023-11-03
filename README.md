Steps to run this app:
- create an image named "demo" using Dockerfile

- run any blue or green stack. (e.g running blue)
   _docker-compose -f docker-compose-blue.yml up --build -d_

-  blue server handles all request

- run another stack:
   _docker-compose -f docker-compose-green.yml up --build -d_  

- to transfer 10% traffic to green:
   python dynamic_config.py green 10

- to transfer more traffic increase the percentage
