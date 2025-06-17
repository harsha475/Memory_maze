import streamlit as st
import random
import time

st.set_page_config(page_title="Memory Maze", layout="centered")

# Initialize session state
if "level" not in st.session_state:
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.total_time = 0
    st.session_state.time_left = 0
    st.session_state.pattern = []
    st.session_state.correct = []
    st.session_state.start_time = time.time()
    st.session_state.dog_position = 0
    st.session_state.positions = [0, 25, 50, 75, 100]  # % across progress bar
    st.session_state.show_input = False
    st.session_state.scrambled = ""
    st.session_state.display = ""
    st.session_state.start_chamber = time.time()

# Dog Progress Visual
def dog_progress():
    pos = st.session_state.positions[st.session_state.level]
    st.progress(pos, text=f"🐶 Dog progress to 🏠")

# Restart game
def restart():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.total_time = 0
    st.session_state.pattern = []
    st.session_state.correct = []
    st.session_state.dog_position = 0
    st.session_state.start_time = time.time()
    st.session_state.scrambled = ""
    st.session_state.display = ""
    st.rerun()

# Timer
def timer_expired(seconds):
    elapsed = time.time() - st.session_state.start_chamber
    return elapsed > seconds

# Level 0: Array Chamber
if st.session_state.level == 0:
    st.title("🔢 Array Chamber")
    dog_progress()
    if not st.session_state.pattern:
        st.session_state.pattern = [random.randint(1, 20) for _ in range(5)]
        st.session_state.start_chamber = time.time()
    st.info(f"Memorize this: {st.session_state.pattern}")
    time.sleep(3)
    st.write("Now enter the pattern within 7 seconds:")
    guess = st.text_input("Enter numbers separated by space")
    if guess and not timer_expired(10):
        try:
            user = list(map(int, guess.strip().split()))
            if user == st.session_state.pattern:
                st.success("Correct! Moving forward 🐶")
                st.session_state.level += 1
                st.session_state.score += 1
                st.session_state.pattern = []
                st.session_state.start_chamber = time.time()
                st.rerun()
            else:
                st.error("Incorrect! Astra resets the Maze.")
                restart()
        except:
            st.error("Enter valid numbers.")
    elif timer_expired(10):
        st.warning("⏰ Time's up!")
        restart()

# Level 1: String Scramble
elif st.session_state.level == 1:
    st.title("🔤 String Chamber")
    dog_progress()
    word = "DATASTRUCTURES"
    if not st.session_state.scrambled:
        distractors = random.choices("ZXCVBNMASDFGHJKLQWERTYUIOP", k=3)
        letters = list(word + ''.join(distractors))
        random.shuffle(letters)
        st.session_state.scrambled = ''.join(letters)
        st.session_state.correct = word
        st.session_state.start_chamber = time.time()

    st.info(f"Unscramble this: {st.session_state.scrambled}")
    guess = st.text_input("Your answer")
    if guess and not timer_expired(7):
        if guess.upper() == st.session_state.correct:
            st.success("Correct! Moving to next chamber 🐶")
            st.session_state.level += 1
            st.session_state.scrambled = ""
            st.rerun()
        else:
            st.error("Wrong! Astra resets the Maze.")
            restart()
    elif timer_expired(7):
        st.warning("⏰ Time's up!")
        restart()

# Level 2: Linked List Chamber
elif st.session_state.level == 2:
    st.title("🔗 Linked List Chamber")
    dog_progress()
    sequence = ["KHAITHI", "VIKRAM", "LEO"]
    if not st.session_state.correct:
        extra = random.sample(["KHAITHI 2", "ROLEX", "LEO 2"], 1)
        full_seq = sequence + extra
        display = full_seq[:]
        random.shuffle(display)
        st.session_state.correct = full_seq
        st.session_state.display = display
        st.session_state.start_chamber = time.time()

    st.info(f"Fix the path: {' -> '.join(st.session_state.display)}")
    st.write("Connect these LCU movies in sequence:")
    guess = st.text_input("Enter order with ->")
    if guess and not timer_expired(20):
        user = [x.strip().upper() for x in guess.split("->")]
        if user == [x.upper() for x in st.session_state.correct]:
            st.success("Correct! Next chamber unlocked 🐶")
            st.session_state.level += 1
            st.session_state.correct = []
            st.rerun()
        else:
            st.warning(f"Expected: {' -> '.join(st.session_state.correct)}")
            restart()
    elif timer_expired(20):
        st.warning("⏰ Time's up!")
        restart()

# Level 3: Queue Chamber
elif st.session_state.level == 3:
    st.title("📥 Queue Chamber")
    dog_progress()
    tasks = ["Disable Alarm", "Collect Key", "Open Gate", "Go To Office"]
    if not st.session_state.correct:
        extra = random.sample(["Close Vault", "Alert Guard"], 1)
        all_tasks = tasks + extra
        random.shuffle(all_tasks)
        st.session_state.correct = tasks + extra
        st.session_state.display = all_tasks
        st.session_state.start_chamber = time.time()

    st.info(f"Arrange in FIFO order: {', '.join(st.session_state.display)}")
    guess = st.text_input("Enter tasks comma-separated")
    if guess and not timer_expired(30):
        user = [x.strip().title() for x in guess.split(",")]
        if user == st.session_state.correct:
            st.success("🎉 All Chambers Cleared! 🐶 reached 🏠")
            st.session_state.level += 1
            st.rerun()
        else:
            st.error(f"Incorrect! Expected: {', '.join(st.session_state.correct)}")
            restart()
    elif timer_expired(30):
        st.warning("⏰ Time's up!")
        restart()

# Final Result
elif st.session_state.level >= 4:
    st.title("🏁 Final Result")
    st.balloons()
    total_time = int(time.time() - st.session_state.start_time)
    minutes = total_time // 60
    seconds = total_time % 60
    if st.session_state.score == 4:
        st.success(f"You escaped the loop! Time Taken: {minutes}m {seconds}s")
    else:
        st.error(f"You're still in the loop. Try again! Time: {minutes}m {seconds}s")

    if st.button("🔁 Play Again"):
        restart()
