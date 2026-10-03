
from http.server import BaseHTTPRequestHandler
import json
import os
from groq import Groq


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        response = {
            "message": "Natural Language to Code Generator API is running!"
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            task = data.get("task", "").strip()

            if not task:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"error": "Task is required"}).encode()
                )
                return

            client = Groq(
                api_key=os.environ.get("GROQ_API_KEY")
            )

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You generate only valid Python code. "
                            "Return ONLY code. "
                            "No explanations and no markdown code fences."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Generate Python code for this task:\n{task}"
                        )
                    }
                ]
            )

            code = response.choices[0].message.content.strip()

            if code.startswith("```python"):
                code = code[9:]

            if code.startswith("```"):
                code = code[3:]

            if code.endswith("```"):
                code = code[:-3]

            result = {
                "task": task,
                "code": code.strip()
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": str(e)}).encode()
            )