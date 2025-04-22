import sys

from lotto.interfaces import cli
        
if __name__ == "__main__":
    while True:
        cli.run()
        again = input(f"Generate report again? \n\r  - [Y] = yes\n\r  - [any key] = exit\n")
        if again.lower() not in ["y", "yes"]:
            break
    sys.stdout.write("Lotto report generator - program exit...")
        
         