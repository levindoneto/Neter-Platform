import logging

LOG  = path.join(PATH, "log", path.basename(__file__).replace(".py", ".log"))

logging.basicConfig(
    filename=LOG,
    level=logging.INFO,
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt='%d-%b-%Y %H:%M:%S')