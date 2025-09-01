import requests
import time
from chatbot.models import Employees  # Change 'chatbot' to your Django app name

class GeminiChatbot:
    """A class to handle interactions with the Gemini API."""
    def __init__(self):
        self.api_key = "AIzaSyD1pP1isttdQ32QzibHi7Vf8weHtTHv_rI"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"

    def generate_response(self, prompt, retries=3, delay=5):
        """Sends a prompt to the Gemini API and retries if rate-limited."""
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"You are an internal HR assistant chatbot.\n\n{prompt}"}
                    ]
                }
            ]
        }

        for attempt in range(retries):
            try:
                response = requests.post(
                    f"{self.base_url}?key={self.api_key}",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    wait_time = delay * (2 ** attempt)
                    print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    return f"HTTP error: {e}"
            except Exception as e:
                return f"Error talking to Gemini API: {e}"

        return "Rate limit reached. Please wait and try again."


class EmployeeAssistant:
    """A chatbot assistant to provide all employee information (no privacy restrictions)."""
    def __init__(self):
        self.llm = GeminiChatbot()

    def get_employee_info(self, name_or_id):
        """Fetches a single employee's data from the database."""
        try:
            if str(name_or_id).isdigit():
                employee = Employees.objects.get(employee_id=int(name_or_id))
            else:
                employee = Employees.objects.get(name__iexact=name_or_id)

            # Return all fields exactly as stored in DB
            return {
                "name": employee.name,
                "age": employee.age,
                "mobile_number": employee.mobile_number,
                "date_of_birth": employee.date_of_birth,
                "date_of_joining": employee.date_of_joining,
                "taken_leave": employee.taken_leave,
                "available_leave": employee.available_leave,
                "sick_leave": employee.sick_leave,
                "casual_leave": employee.casual_leave,
                "aadhar_number": employee.aadhar_number,
                "pan_card_number": employee.pan_card_number
            }
        except Employees.DoesNotExist:
            return None

    def ask_about_employee(self, query):
        """Handles the user query with full access to data."""
        employee_info = self.get_employee_info(query)
        if not employee_info:
            return f"Employee '{query}' not found in the database."

        # Include all fields in prompt
        formatted_info = "\n".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in employee_info.items())

        prompt = (
            f"Here is the employee information from the company database:\n\n"
            f"{formatted_info}\n\n"
            f"Answer the user's question accurately based on the above data."
        )

        return self.llm.generate_response(prompt)


# Example usage
if __name__ == "__main__":
    assistant = EmployeeAssistant()

    # Test: Request for sensitive info
    response_sensitive = assistant.ask_about_employee("Bharath mobile number")
    print("Bot:", response_sensitive)

    print("\n---")

    # Test: General request
    response_general = assistant.ask_about_employee("Bharath")
    print("Bot:", response_general)
