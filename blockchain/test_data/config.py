from uuid import uuid4

hash = "sha256"

sender_id = str(uuid4()).replace('-', '')
recipient_id = str(uuid4()).replace('-', '')

puzzle = 4  # Increased default puzzle difficulty
chain_length = 15  # Increased number of blocks per round
tx_per_block = 8  # Increased transactions per block
tx_amount = 200  # Increased transaction amount

port = 4544
tx_endpoint = "/tx/new"
mining_endpoint = "/mine"
results_file = "test_data/results"

"""
always 10 blocks

round1:
    puzzle=2:
        tx per block=2

round2:
    puzzle=2:
        tx per block=4

round3:
    puzzle=2:
        tx per block=6

round4:
    puzzle=4:
        tx per block=2

round5:
    puzzle=4:
        tx per block=4

round6:
    puzzle=4:
        tx per block=6
        
round7:
    puzzle=6:
        tx per block=2

round8:
    puzzle=6:
        tx per block=4

round9:
    puzzle=6:
        tx per block=6    
"""