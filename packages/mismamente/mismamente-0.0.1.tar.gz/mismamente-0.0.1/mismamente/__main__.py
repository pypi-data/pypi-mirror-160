import logging
from mismamente import unreleased

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    logging.debug("We're started the package execution ")
    workshops = unreleased()
    logging.debug("We're finished the package execution")
