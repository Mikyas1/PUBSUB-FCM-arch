from wiring.wiring import wire_entities
from utils.parse_args import parse_args

if __name__ == '__main__':
    args = parse_args()
    wire_entities(args)
