import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from environment variables
api_key = os.getenv('API_KEY')

def main():
    logger.info('Starting application...')
    print("Huzza! It's working!")

if __name__ == "__main__":
    main()
