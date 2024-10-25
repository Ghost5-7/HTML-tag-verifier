#include <iostream>
#include <fstream>
#include <string>
#include <stack>

using namespace std;

int main() {
    // Define the path to the file you want to read
    string filePath = "uploads/your_file_name.html"; // Replace with the actual file name

    // Create an input file stream
    ifstream file(filePath);

    // Check if the file was opened successfully
    if (!file.is_open()) {
        cerr << "Error opening file: " << filePath << endl;
        return 1;
    }

    // Stack to track opening tags
    stack<char> tagStack;

    // Read the file line by line
    string line;
    while (getline(file, line)) {
        // Process each character in the line
        for (char ch : line) {
            if (ch == '<') {
                // Push opening tag onto the stack
                tagStack.push(ch);
            } else if (ch == '>') {
                // Check if there's a matching opening tag
                if (!tagStack.empty() && tagStack.top() == '<') {
                    tagStack.pop(); // Pop the matching opening tag
                } else {
                    // Unmatched closing tag
                    cout << "The tag parentheses are not balanced." << endl;
                    return 1;
                }
            }
        }
    }

    // Check if all opening tags have been matched
    if (tagStack.empty()) {
        cout << "The tag parentheses are balanced." << endl;
    } else {
        cout << "The tag parentheses are not balanced." << endl;
    }

    // Close the file
    file.close();

    return 0;
}
