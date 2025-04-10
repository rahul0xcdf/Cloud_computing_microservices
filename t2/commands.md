docker build -t os-concepts-api .

Run the container:
docker run -p 5000:5000 os-concepts-api


 Testing the API

You can use tools like curl or Postman to test the endpoint. Here’s an example using curl:

curl -X POST http://localhost:5000/api/os-concept \
     -H "Content-Type: application/json" \
     -d '{"concept": "fork"}'
Expected JSON response (formatted for clarity):

{
  "concept": "fork",
  "code": "/* C code for fork */\n#include <stdio.h> ...",
  "explanation": "The code demonstrates how the fork() system call creates a new process ...",
  "potential_output": "Parent Process: PID = 1000, Child PID = 1001\nChild Process: PID = 1001"
}