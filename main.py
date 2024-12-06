from src.classes.Log import Log
log = Log()

def main():
    try:
        log.debug("The 'main' function has been executed.")
        for i in range(10):
            log.info(f"i = {i}")
        input("Press 'Enter' to exit...")
    except Exception as e:
        log.error(f"Unexpected error in 'main' function:\n{e}")
    finally:
        log.debug("The 'main' function has completed.")

if __name__ == "__main__":
    main()
