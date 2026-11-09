Security Assistant
An AI-powered assistant that answers questions about code scan results and internal security policy. It combines open-source scanners, a local language model, and retrieval over policy documents.
What it does
• Runs Bandit (Python code scanning) and pip-audit (dependency vulnerabilities) and saves the results as JSON reports.
• Parses the reports with plain Python, so the counts come from code rather than the model.
• Searches the policy documents in standards/ for the text relevant to a question.
• Uses a local model (Ollama, Qwen 2.5) with two tools: get_summary for scan results and search_standards for policy.
• Runs Gitleaks, Bandit, and pip-audit automatically on every push through GitHub Actions.
Project structure
File
Purpose
app.py
Intentionally flawed sample code, used as scanner test input
findings.py
Reads and counts Bandit findings
deps.py
Reads and lists pip-audit findings
summary.py
Combines both scanners into one result
rag.py
Loads and searches the policy documents
security_agent.py
Agent loop that chooses which tool to call
standards/
Security policy documents
.github/workflows/security.yml
CI pipeline
How to run it
1. Install Ollama and pull the model qwen2.5:7b.
2. Create and activate a virtual environment, then install the requirements with python -m pip install -r requirements.txt.
3. Generate the reports with Bandit and pip-audit, writing them to the reports/ folder.
4. Run python summary.py to see the combined results.
5. Run python security_agent.py and ask a question, such as "How fast must critical secret findings be fixed?"
Results so far
• Gitleaks: passed with no leaks detected.
• Bandit: flagged one high-severity issue, the os.system call in app.py (command injection risk).
• pip-audit: flagged five known vulnerabilities in chromadb 1.5.9. The package was removed until a patched version is confirmed.
• Agent: answered the fix-deadline question by searching the policy and citing 24 hours, and answered the findings question by calling get_summary.
Concepts covered
• RAG: split documents into chunks, retrieve the relevant ones, and pass them to the model.
• Tools: a function with a name, a description, and typed inputs. The model chooses when to call it, and your code runs it.
• Separation of duties: code handles counting and arithmetic; the model explains the results.
• CI scanning: a failing scanner job blocks the change until it's fixed.
Security notes
• The API key in app.py is a fake test value. Real keys belong in a .env file, which is excluded from Git.
• reports/, .venv/, and .env are listed in .gitignore.
• Scan reports can contain code snippets, so redact them before sending them to a hosted model.
• Fix dependency findings by upgrading to a patched release, not by ignoring the scanner.
