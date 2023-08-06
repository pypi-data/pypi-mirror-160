import hashlib, argparse

parser = argparse.ArgumentParser(description='Get information about your IP or any other IP')
parser.add_argument('-f', type=str, help='Enter file name to calculate hash of file')
parser.add_argument('-t', type=str, help='Enter text to calculate hash of text')
parser.add_argument('-m', type=str, help='Method(Default is SHA256)')
parser.add_argument('-lm', action=argparse.BooleanOptionalAction, help='Get list of methods')
args = parser.parse_args()

algs = ["md5","sha1", "sha224", "sha256", "sha384", "sha512", "blake2b", "blake2s", "shake_128", "shake_256"]

def algs_list():
    algs = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b", "blake2s", "shake_128", "shake_256"]
    for i in algs:
        print(i)

def hash_text(text, method):
    h = hashlib.new(method)
    h.update(text.encode())
    return h.hexdigest()

def hash_file(filename, method):
    h = hashlib.new(method)
    with open(filename, "rb") as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()

def main():
    if args.m == None:
        method = "sha256"
    else:
        method = args.m
    if args.lm != None:
        algs_list()
    elif args.f != None:
        print(hash_file(args.f, method))
    elif args.t != None:
        print(hash_text(args.t, method))
    else:
        print("Ivalid arguments\nUse -h for help")

if __name__ == "__main__":
    main()