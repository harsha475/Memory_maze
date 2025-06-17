import streamlit as st, random, time

st.set_page_config(page_title="Memory Ghazer - DSA", layout="centered")

# --- Setup session state ---
if "level" not in st.session_state:
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.phase_start = time.time()
    st.session_state.pattern = []
    st.session_state.correct = ""
    st.session_state.scrambled = ""
    st.session_state.display = ""
    st.session_state.show_input = False

# --- Helpers ---
def reset_all():
    st.session_state.level = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.phase_start = time.time()
    st.session_state.pattern = []
    st.session_state.correct = ""
    st.session_state.scrambled = ""
    st.session_state.display = ""
    st.session_state.show_input = False
    st.rerun()

def show_dog():
    pos = "🐶" + " " * (st.session_state.level * 4) + "🏠"
    st.markdown(f"### {pos}")

def check_timer(limit):
    elapsed = time.time() - st.session_state.phase_start
    remaining = int(limit - elapsed)
    if remaining >= 0:
        st.info(f"⏳ Time left: {remaining}s")
        return True
    else:
        st.error("⏰ Time expired. Resetting game...")
        time.sleep(2)
        reset_all()
        return False

def on_correct():
    st.success("✅ Correct! Moving forward")
    st.session_state.score += 1
    st.session_state.level += 1
    st.session_state.phase_start = time.time()
    st.experimental_rerun()

# --- Level Logic ---

# Chamber 1: Array
if st.session_state.level == 0:
    st.title("🧩 Chamber 1: Array Chamber")
    show_dog()
    if not st.session_state.pattern:
        st.session_state.pattern = [random.randint(1,20) for _ in range(5)]
        st.info(f"Memorize: {st.session_state.pattern}")
        time.sleep(3)
        st.session_state.phase_start = time.time()

    if check_timer(10):
        ans = st.text_input("Enter numbers separated by spaces")
        if st.button("Submit"):
            try:
                guess = list(map(int, ans.strip().split()))
                if guess == st.session_state.pattern:
                    on_correct()
                else:
                    st.error("❌ Wrong pattern!")
                    time.sleep(1)
                    reset_all()
            except:
                st.error("Invalid input. Use numbers only.")

# Chamber 2: String scramble
elif st.session_state.level == 1:
    st.title("🧩 Chamber 2: String Chamber")
    show_dog()
    if not st.session_state.scrambled:
        word = "DATASTRUCTURES"
        x = random.choices("ZXCVBNMASDFGHJKLQWERTYUIOP", k=3)
        letters = list(word + "".join(x))
        random.shuffle(letters)
        st.session_state.scrambled = "".join(letters)
        st.session_state.correct = word
        st.session_state.phase_start = time.time()

    st.info(f"Unscramble: {st.session_state.scrambled}")
    if check_timer(7):
        ans = st.text_input("Your answer")
        if st.button("Submit"):
            if ans.strip().upper() == st.session_state.correct:
                on_correct()
            else:
                st.error("❌ Wrong!")
                time.sleep(1)
                reset_all()

# Chamber 3: Linked List
elif st.session_state.level == 2:
    st.title("🧩 Chamber 3: Linked List Chamber")
    show_dog()
    if not st.session_state.correct:
        base = ["KHAITHI","VIKRAM","LEO"]
        extra = random.sample(["KHAITHI 2","ROLEX","LEO 2"],1)
        seq = base + extra
        st.session_state.correct = " -> ".join(seq).upper()
        temp = seq[:]; random.shuffle(temp)
        st.session_state.display = " -> ".join(temp)
        st.session_state.phase_start = time.time()

    st.info(f"Fix path (LCU): {st.session_state.display}")
    if check_timer(25):
        ans = st.text_input("Enter using -> between")
        if st.button("Submit"):
            if ans.strip().upper() == st.session_state.correct:
                on_correct()
            else:
                st.error("❌ Incorrect!")
                time.sleep(1)
                reset_all()

# Chamber 4: Queue
elif st.session_state.level == 3:
    st.title("🧩 Chamber 4: Queue Chamber")
    show_dog()
    if not st.session_state.correct:
        base = ["Disable Alarm","Collect Key","Open Gate","Go To Office"]
        extra = random.sample(["Close Vault","Alert Guard"],1)
        full = base + extra
        st.session_state.correct = ", ".join(full).title()
        temp = full[:]; random.shuffle(temp)
        st.session_state.display = ", ".join(temp)
        st.session_state.phase_start = time.time()

    st.info(f"Arrange FIFO: {st.session_state.display}")
    if check_timer(30):
        ans = st.text_input("Enter comma-separated list")
        if st.button("Submit"):
            if ans.strip().title() == st.session_state.correct:
                on_correct()
            else:
                st.error("❌ Incorrect!")
                time.sleep(1)
                reset_all()

# Final
else:
    st.title("🏁 Final Result")
    show_dog()
    total = int(time.time() - st.session_state.start_time)
    mins,secs = divmod(total,60)
    st.balloons()
    st.success(f"You escaped! ⏱️ {mins}m {secs}s")
    if st.button("🔁 Play Again"):
        reset_all()
