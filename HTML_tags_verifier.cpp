#include <iostream>
#include <fstream>
#include <string>
#include <stack>
#include <set>
using namespace std;

bool isSelfClosingTag(const string& tag) {
    static const set<string> selfClosingTags = {
        "area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"
    };
    return selfClosingTags.find(tag) != selfClosingTags.end();
}

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
    stack<string> tagStack;

    // Read the file line by line
    string line;
    while (getline(file, line)) {
        size_t pos = 0;
        while ((pos = line.find('<', pos)) != string::npos) {
            size_t endPos = line.find('>', pos);
            if (endPos == string::npos) {
                cout << "Malformed tag found." << endl;
                return 1;
            }

            string tag = line.substr(pos + 1, endPos - pos - 1);
            bool isClosingTag = tag[0] == '/';
            if (isClosingTag) {
                tag = tag.substr(1); // Remove the '/' from closing tag
                if (!tagStack.empty() && tagStack.top() == tag) {
                    tagStack.pop(); // Pop the matching opening tag
                } else {
                    cout << "Unmatched closing tag: </" << tag << ">" << endl;
                    return 1;
                }
            } else {
                // Check for self-closing tag
                if (!isSelfClosingTag(tag)) {
                    tagStack.push(tag);
                }
            }
            pos = endPos + 1;
        }
    }

    // Check if all opening tags have been matched
    if (tagStack.empty()) {
        cout << "All tags are properly matched." << endl;
    } else {
        cout << "There are unmatched opening tags." << endl;
    }

    // Close the file
    file.close();

    return 0;
}