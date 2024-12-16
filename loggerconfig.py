import logging

def logger_config():
    logger = logging.getLogger()
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler('isotech.logs')
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
