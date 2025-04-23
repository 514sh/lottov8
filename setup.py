if __name__ == "__main__":
    from lotto.config import BASE_DIR, OWNERS, GAME_DATE
    from lotto.utilities import generate_filename

    directories = ["input", "all", "tulog", "result"]

    base_dir_path = BASE_DIR
    base_dir_path.mkdir(parents=True, exist_ok=True)

    for directory in directories:
        dir_path = base_dir_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        if directory == "input":
            for owner in OWNERS:
                filename = generate_filename(owner=owner, date=GAME_DATE)
                file_path = dir_path / filename
                file_path.touch(exist_ok=True)
    print("Setup finished!")