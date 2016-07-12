# apachedocker
A small example of apache running in a docker container using supervisord
One endpoint is exposed `fibonacci` which takes a positive integer `number` as a query parameter and returns a list of 'n' fibonacci numbers.

### Starting
After building the container with `docker build -t fooka03/apachedocker:testing https://github.com/fooka03/apachedocker.git`, the container can be started in detached mode via `docker run -d fooka03/apachedocker:testing`  This will start the container and execute the supervisor process, which in turn calls apache2ctl -DFOREGROUND.  This enables the container to run continuously without user intervention.

### Use
Once the container has been started, the `fibonacci` endpoint will be available.  This can be invoked from the host simply through the following command: `curl <container_ip>/fibonacci?number=5`  The REST service will then return the first five fibonacci numbers in sequence (0 through 4) or `[0, 1, 1, 2, 3]`  '5' can be replaced with any positive integer to receive the appropriate range of fibonacci numbers in return.

### States
 * A zero, or negative number will return a 400 BAD REQUEST response and tell the user they need to supply a positive integer.
 * A non-integer value will return a 400 BAD REQUEST response and tell the user they need to supply a positive integer.
 * A missing `number` parameter will return a 400 BAD REQUEST response and tell the user they need to provide the appropriate query parameter
 * Attempting to access any other endpoint on the server will return a 404 NOT FOUND response telling the user the endpoint is unavailable
 * If the server fails to process the requested number of fibonacci numbers, a 500 INTERNAL SERVER ERROR response is sent.
 * If the parameter is valid, and processed, a 200 OK response is sent along with the requested data string

### Testing
The fib.wsgi file includes unit tests around the `fibonacci` function, which performs the fibonacci number calculation.  It also has unit tests for the `fibrange` function which will return the lists of numbers in sequence.  These tests are invoked using either `python fib.wsgi` or `python2 fib.wsgi`

### Limitations
The fib.wsgi file uses the urlparse library, which is not present in python 3.  Therefore the tests must be run using python 2.7.x

### Considerations
In order to further support this application, the docker host could use apache2/nginx/haproxy to loadbalance requests to each of the available containers.  This in turn could be placed behind another level of loadbalancers to allow for multiple docker hosts each providing multiple containers providing this endpoint.  The implementation of this concept is not covered by this example.  Further, the logs from the containers could be collected and aggregated (ELK, Loggly, SumoLogic, etc) to provide pinpoint debugging in addition to the basic health checks afforded by the aforementioned loadbalancers.
