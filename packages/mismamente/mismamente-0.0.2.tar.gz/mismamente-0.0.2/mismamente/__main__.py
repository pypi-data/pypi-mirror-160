import logging
from mismamente import unreleased

logging.basicConfig(level=logging.INFO)


def main():
    logging.info(unreleased())


if __name__ == '__main__':
    logging.debug("We're started the package execution ")
    main()
    logging.debug("We're finished the package execution")
