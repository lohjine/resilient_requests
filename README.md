# resilient_requests
 
Python requests library is awesome, and makes it really quick to just requests.get(url) for something. But oftentimes when this gets used in long-running processes, it will eventually run into errors of some sort, or retrieving unexpected results.

Hence the next step is to make your call resilient by adding retry code, checking for correct status code. This gets tedious quick as it has to be added to every single call. This wrapper helps you to make your call resilient, and starts off with sane defaults.