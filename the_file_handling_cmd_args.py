import os
import sys

from utils.path_normalizer import normalize_path


def main():
    # Example of handling command-line arguments for paths
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            # Assuming arg is a path, normalize it before use
            normalized_path = normalize_path(arg)
            
            # Hypothetical file operation using the normalized path
            if os.path.exists(normalized_path):
                print(f"Path exists: {normalized_path}")
                # Further operations on the path can be added here, all using normalized_path

if __name__ == "__main__":
    main()
