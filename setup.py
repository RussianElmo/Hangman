import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Hangman",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["easy_words.txt", "gallows.png", "hard_words.txt", "head.png",
                                             "left_arm.png", "left_leg.png", "medium_words.txt", "right_arm.png",
                                             "torso.png", "trophy.png"]}},
    executables=executables

)
