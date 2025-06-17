import streamlit as st
import random
import time

st.set_page_config(page_title="Memory Maze", layout="centered")

# Initialize session state variables
if "level" not in st.session_state:
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.pattern = []
    st.session_state.correct = ""
    st.session_state.show_timer = False
    st.session_state.show_input = False
    st.session_state.message = ""

# Restart game function
def restart_game():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.pattern = []
    st.session_state.correct = ""
    st.session_state.message = ""

# Timer display
def display_timer():
    elapsed = int(time.time() - st.session_state.start_time)
    st.markdown(f"⏳ Time Elapsed: {elapsed} seconds")

# Chamber 1: Array Pattern
if st.session_state.level == 0:
    st.title("🧩 Chamber 1: Array Pattern")
    if not st.session_state.pattern:
        st.session_state.pattern = [random.randint(1, 20) for _ in range(5)]
    st.info(f"Memorize this pattern: {st.session_state.pattern}")
    st.write("(Wait for 5 seconds before input...)")
    time.sleep(5)
    display_timer()
    guess = st.text_input("Enter the pattern separated by spaces:")
    if st.button("Submit"):
        try:
            user_guess = list(map(int, guess.split()))
            if user_guess == st.session_state.pattern:
                st.success("Correct!")
                st.session_state.level += 1
                st.session_state.pattern = []
            else:
                st.error("Incorrect! Restarting the game...")
                restart_game()
        except:
            st.error("Please enter numbers separated by spaces.")

# Chamber 2: String Scramble
elif st.session_state.level == 1:
    st.title("🧩 Chamber 2: String Scramble")
    word = "DATASTRUCTURES"
    if not st.session_state.correct:
        distractors = random.choices("ZXCVBNMASDFGHJKLQWERTYUIOP", k=3)
        letters = list(word + ''.join(distractors))
        random.shuffle(letters)
        st.session_state.correct = word
        st.session_state.scrambled = ''.join(letters)
    display_timer()
    st.info(f"Unscramble this: {st.session_state.scrambled}")
    guess = st.text_input("Your answer:")
    if st.button("Submit"):
        if guess.upper() == st.session_state.correct:
            st.success("Correct!")
            st.session_state.level += 1
            st.session_state.correct = ""
        else:
            st.error("Incorrect! Restarting the game...")
            restart_game()

# Chamber 3: Linked List Order
elif st.session_state.level == 2:
    st.title("🧩 Chamber 3: Linked List Order")
    sequence = ["KHAITHI", "VIKRAM", "LEO"]
    extra = random.sample(["KHAITHI 2", "ROLEX", "LEO 2"], 1)
    full_seq = sequence + extra
    if not st.session_state.correct:
        display_seq = full_seq[:]
        random.shuffle(display_seq)
        st.session_state.correct = " -> ".join(full_seq)
        st.session_state.display = " -> ".join(display_seq)
    display_timer()
    st.info(f"Fix the path: {st.session_state.display}")
    guess = st.text_input("Enter in order with -> in between:")
    if st.button("Submit"):
        if guess.upper() == st.session_state.correct.upper():
            st.success("Correct!")
            st.session_state.level += 1
            st.session_state.correct = ""
        else:
            st.error(f"Incorrect! Expected: {st.session_state.correct}")
            restart_game()

# Chamber 4: Queue Order
elif st.session_state.level == 3:
    st.title("🧩 Chamber 4: Queue Order")
    tasks = ["Disable Alarm", "Collect Key", "Open Gate", "Go To Office"]
    extra = random.sample(["Close Vault", "Alert Guard"], 1)
    all_tasks = tasks + extra
    if not st.session_state.correct:
        random.shuffle(all_tasks)
        st.session_state.correct = ", ".join(tasks + extra)
        st.session_state.shuffled = ", ".join(all_tasks)
    display_timer()
    st.info(f"Arrange in FIFO order: {st.session_state.shuffled}")
    guess = st.text_input("Enter tasks separated by comma:")
    if st.button("Submit"):
        if guess.title() == st.session_state.correct:
            st.success("🎉 All Chambers Cleared!")
            st.session_state.level += 1
        else:
            st.error(f"Incorrect! Expected: {st.session_state.correct}")
            restart_game()

# Final Result
elif st.session_state.level >= 4:
    elapsed = int(time.time() - st.session_state.start_time)
    st.title("🏁 Final Result")
    st.success("You completed all chambers!")
    st.balloons()
    st.write(f"Total time taken: {elapsed} seconds")
    time.sleep(3)
    if st.button("🔁 Play Again"):
        restart_game()
  
