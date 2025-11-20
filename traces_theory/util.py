
def get_transaction(trans_file: str) -> str:
    with open(trans_file) as file:
        text = file.read()
    
