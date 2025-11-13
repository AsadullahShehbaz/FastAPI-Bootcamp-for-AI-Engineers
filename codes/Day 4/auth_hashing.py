from passlib.context import CryptContext

from logging_config import logger 


# 🔒 Switch to Argon2 (modern & recommended)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using the configured hashing algorithm.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The resulting hashed password.
    """
    logger.debug("Hashing password")
    hashed = pwd_context.hash(password)
    logger.debug("Password hashed successfully")
    return hashed

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against its hashed version.

    Args:
        plain_password (str): The plain-text password to check.
        hashed_password (str): The hashed password from the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    logger.debug("Verifying password")
    result = pwd_context.verify(plain_password, hashed_password)
    if result:
        logger.info("Password verification succeeded")
    else:
        logger.warning("Password verification failed")
    return result
