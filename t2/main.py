from flask import Flask, request, jsonify

app = Flask(__name__)

# Pre-written C code snippets for system calls
# Each snippet includes the code, explanation, and a sample potential output.
snippets = {
    "fork": {
        "code": r"""
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid;
    
    // Create a new process
    pid = fork();
    
    if (pid < 0) {
        // Error handling
        perror("fork failed");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        // Child process
        printf("Child Process: PID = %d\n", getpid());
    } else {
        // Parent process
        printf("Parent Process: PID = %d, Child PID = %d\n", getpid(), pid);
    }
    return 0;
}
""",
        "explanation": "The code demonstrates how the fork() system call creates a new process. After fork(), two processes continue executing the code: the child (when pid == 0) and the parent (when pid > 0). Basic error handling is included.",
        "potential_output": "Parent Process: PID = 1000, Child PID = 1001\nChild Process: PID = 1001"
    },
    "pipe": {
        "code": r"""
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define BUFFER_SIZE 25

int main() {
    int fd[2];
    char write_msg[BUFFER_SIZE] = "Hello via pipe!";
    char read_msg[BUFFER_SIZE];
    
    // Create a pipe
    if (pipe(fd) == -1) {
        perror("Pipe failed");
        exit(EXIT_FAILURE);
    }
    
    pid_t pid = fork();
    if (pid < 0) {
        perror("Fork failed");
        exit(EXIT_FAILURE);
    }
    
    if (pid == 0) {
        // Child process: reading from pipe
        close(fd[1]);  // close unused write end
        read(fd[0], read_msg, BUFFER_SIZE);
        printf("Child Process Read: %s\n", read_msg);
        close(fd[0]);
    } else {
        // Parent process: writing to pipe
        close(fd[0]);  // close unused read end
        write(fd[1], write_msg, strlen(write_msg)+1);
        close(fd[1]);
    }
    
    return 0;
}
""",
        "explanation": "This code demonstrates the use of pipe() for IPC between a parent and child process. The parent writes a message to the pipe and the child reads it. The code includes proper closing of unused file descriptors.",
        "potential_output": "Child Process Read: Hello via pipe!"
    },
    "open": {
        "code": r"""
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int main() {
    int fd;
    // Open file.txt in read-only mode
    fd = open("file.txt", O_RDONLY);
    if (fd == -1) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }
    
    printf("File opened successfully with file descriptor: %d\n", fd);
    close(fd);
    return 0;
}
""",
        "explanation": "The code snippet shows how to open a file using open() in read-only mode. It includes error checking and closes the file descriptor after use.",
        "potential_output": "File opened successfully with file descriptor: 3"
    },
    "read": {
        "code": r"""
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

#define BUFFER_SIZE 100

int main() {
    int fd;
    char buffer[BUFFER_SIZE];
    
    // Open file.txt in read-only mode
    fd = open("file.txt", O_RDONLY);
    if (fd == -1) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }
    
    // Read contents into buffer
    ssize_t bytesRead = read(fd, buffer, BUFFER_SIZE-1);
    if (bytesRead == -1) {
        perror("Error reading file");
        close(fd);
        exit(EXIT_FAILURE);
    }
    
    // Null-terminate and print the buffer
    buffer[bytesRead] = '\0';
    printf("Content read from file: %s\n", buffer);
    
    close(fd);
    return 0;
}
""",
        "explanation": "This code snippet demonstrates using read() to retrieve data from a file. It opens a file, reads up to BUFFER_SIZE-1 bytes, null-terminates the string, and prints the content. Basic error handling is included.",
        "potential_output": "Content read from file: (contents of file.txt)"
    }
}

@app.route('/api/os-concept', methods=['POST'])
def get_os_concept():
    data = request.get_json()
    concept = data.get("concept", "").lower().strip()

    if not concept:
        return jsonify({"error": "The 'concept' field is required."}), 400

    # Retrieve snippet using the 'concept' parameter
    snippet = snippets.get(concept)
    if snippet is None:
        return jsonify({"error": f"Concept '{concept}' not found. Supported concepts: {list(snippets.keys())}"}), 404

    response = {
        "concept": concept,
        "code": snippet["code"],
        "explanation": snippet["explanation"],
        "potential_output": snippet["potential_output"]
    }

    return jsonify(response), 200

if __name__ == '__main__':
    # Start the service on port 5000
    app.run(host='0.0.0.0', port=5000)
