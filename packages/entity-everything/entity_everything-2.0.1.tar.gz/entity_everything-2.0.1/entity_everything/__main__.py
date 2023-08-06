import sys
from entity_everything.libs import html_entities_decode, html_entities_encode


def _load_data():
    """ If no arguments passed: read text from the standard input.
    Else: take all arguments and join them to a single string"""
    if len(sys.argv) == 2:
        return sys.stdin.read().rstrip("\n")
    else:
        return " ".join(sys.argv[2::])


def main():
    if len(sys.argv) == 1:
        print("Usage: ")
        print(sys.argv[0] + ' encode "text"')
        print(sys.argv[0] + ' decode "&123;&124;"')
        exit(0)

    data_to_process = _load_data()

    if sys.argv[1] == "encode":
        print(html_entities_encode(data_to_process))
    elif sys.argv[1] == "decode":
        print(html_entities_decode(data_to_process))
    else:
        print("Invalid action: " + sys.argv[1])
        exit(1)


if __name__ == "__main__":
    main()
