import time


class Effect:
    PAUSE_DURATION = 2

    def display_logo(logo_name):
        filepath = f"logos/{logo_name}.txt"

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            print(content)
        except FileNotFoundError:
            return "Error: ファイルが見つかりません。"
        except Exception as e:
            return f"Error: {e}"

    def highlight_line(text):
        line = "*" * (len(text) * 2)
        print(line)
        print(text)
        print(line)

    def display_with_pause():
        time.sleep(Effect.PAUSE_DURATION)
