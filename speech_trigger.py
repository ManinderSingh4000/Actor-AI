import speech_recognition as sr

def wait_for_action():
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("Say 'Action' to begin...")

    while True:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.3)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio).lower()
            print(f"[DEBUG] Heard: {text}")

            if "action" in text:
                return True

        except sr.UnknownValueError:
            print("[WARN] Didn't catch that. Try again.")
        except sr.RequestError as e:
            print(f"[ERROR] Speech service failed: {e}")
            return False



# import speech_recognition as sr

# def wait_for_action():
#     """
#     Waits for user to type 'action' in CMD.
#     Once triggered, performs speech recognition once.
#     """

#     r = sr.Recognizer()
#     mic = sr.Microphone()

#     print("Type 'action' and press Enter to start speech recognition.")
#     print("Type 'exit' to quit.")

#     while True:
#         cmd = input(">> ").strip().lower()

#         if cmd == "exit":
#             print("[INFO] Exiting action listener.")
#             return False

#         if cmd != "action":
#             print("[INFO] Unknown command. Type 'action' or 'exit'.")
#             continue

#         print("[INFO] Action triggered. Listening...")

#         with mic as source:
#             r.adjust_for_ambient_noise(source, duration=0.3)
#             audio = r.listen(source)

#         try:
#             text = r.recognize_google(audio).lower()
#             print(f"[DEBUG] Heard: {text}")
#             return True

#         except sr.UnknownValueError:
#             print("[WARN] Speech not understood. Try again.")
#         except sr.RequestError as e:
#             print(f"[ERROR] Speech service failed: {e}")
#             return False
