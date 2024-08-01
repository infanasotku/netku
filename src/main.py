from configure import configure
import settings


def run():
    configure()
    settings.get()


if __name__ == "__main__":
    run()
