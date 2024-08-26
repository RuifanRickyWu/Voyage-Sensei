import argparse, os
from CarTravel.config import API_KEY
from CarTravel.query_process.queryProcess_expansion import *
from CarTravel.LLM.GPTChatCompletion import *

MODE = {"expand", "reformulate", "elaborate"}

def main(args):
    llm = GPTChatCompletion(api_key=API_KEY)
    input_path = args.input_path
    # mode_name = args.mode
    output_dir = args.output_dir

    if not input_path.endswith('.txt'):
        raise ValueError(f"Invalid file type: {input_path} is not a .txt file")
    
    os.makedirs(output_dir, exist_ok=True)

    query_processor = queryProcessor(input_path=input_path, llm=llm, output_dir=output_dir)
    query_processor.process_queries()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some queries using an LLM.")

    input_path = os.path.join(os.path.dirname(__file__), 'queries.txt')
    output_dir = os.path.join(os.path.dirname(__file__), 'output_files')
    
    parser.add_argument("-i", "--input_path", required=False, help="Path to the input file containing queries", default=input_path)    
    parser.add_argument("-o", "--output_dir", help="Directory to store processed queries", default=output_dir)
    # parser.add_argument("--mode", required=False, default=None, choices=MODE, help="Processing mode (choose from: {})".format(", ".join(sorted(MODE))))
    
    args = parser.parse_args()
    main(args=args)

