import logging
logging.basicConfig(
    filename='user_actions.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
print("Simple File Logger (Type 'exit' to quit)")
while True:
    try:

        action = input("Enter an action to log: ")
        
        if action.lower() == 'exit':
            logging.info("System: User terminated the session.")
            break
        
        
        logging.info(f"User Action: {action}")
        print(f"Logged: {action}")


    except Exception as e:
        logging.error(f"Failed to log action: {e}")
        print(f"An error occurred: {e}")