
import google.generativeai as genai
import argparse


class TextToEmoji:
    def __init__(self):
        api_key = 'AIzaSyA7fQKCBtHPQUHGX1nZXDOWiJMlO31-uk8'
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, prompt):
        try:
            response = self.model.generate_content(
                f"Generate only emojis (no text) that represent: {prompt}. Return just 1-5 relevant emojis with no explanation."
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating content: {e}")
            try:
                response = self.model.generate_content([
                    {"text": f"Generate only emojis (no text) that represent: {prompt}. Return just 1-5 relevant emojis with no explanation."}
                ])
                return response.text.strip()
            except Exception as e2:
                print(f"Error generating content: {e2}")


if __name__ == "__main__":
    t2e = TextToEmoji()

    print("🎭 Text to Emoji Generator 🎭")
    print("Type 'exit' to quit")

    while True:
        user_input = input("\nEnter text to convert to emojis: ")
        if user_input.lower() in ('exit', 'quit'):
            break

        emojis = t2e.generate(user_input)
        print(f"\nEmojis: {emojis}")
