# start.py

import argparse
import sys
# Import the function from your main script.
# Make sure main.py is in the same directory or PYTHONPATH.
import main

def main_cli():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Process Instagram reels using AI classification.",
        epilog="Example: python start.py --relogin true --it 40"
    )

    # Add arguments
    parser.add_argument(
        '-r', '--relogin',
        type=str.lower,  # Convert input to lowercase for easier comparison
        choices=['true', 'false'],
        default='false',
        help='Whether to trigger a relogin flow. (default: false)'
    )
    parser.add_argument(
        '-i', '--it', '--iterations', # Allow multiple flags for the same argument
        type=int,
        default=None, # Use None to distinguish from a default integer value
        help='Number of iterations (reels batches) to run. If not provided, runs indefinitely (like iterations=True).'
    )

    # Parse arguments
    args = parser.parse_args()

    # Convert string arguments to boolean for the function call
    # argparse's 'store_true' is cleaner for booleans, but this works with string input
    relogin_flag = args.relogin == 'true'
    
    # Decide on the 'iterations' argument value
    # If --it N is provided, pass N. If not provided, pass True to mimic original behavior.
    iterations_value = args.it if args.it is not None else True

    print(f"Starting script with relogin={relogin_flag}, iterations={iterations_value}")

    # Call your main function
    try:
        main.starting_point(iterations=iterations_value, relogin=relogin_flag)
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main_cli()