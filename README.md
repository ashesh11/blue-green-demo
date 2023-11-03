Steps to run this app:
- Create an image named "demo" using Dockerfile

- Run any blue or green stack. (e.g running blue)
   _docker-compose -f docker-compose-blue.yml up --build -d_

-  Blue server handles all request

- Run another stack:
   _docker-compose -f docker-compose-green.yml up --build -d_  

- To transfer 10% traffic to green:
   python dynamic_config.py green 10

- To transfer more traffic increase the percentage

- Messages are queued on individual server's message broker. To view message queues of blue goto localhost:15672 and for green localhost:15673. Use guest as both username and password.
