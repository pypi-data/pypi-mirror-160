import argparse
import functions


def parse_args():
    """
    Parse CLI arguments given to sca3s-cli.
    """
    parser = argparse.ArgumentParser(description='SCA3S CLI')
    parser.add_argument('function', help='SCA3S function to utilise')
    parser.add_argument('-f', '--file', help='File path of SCA3S compatible JSON')
    parser.add_argument('-j', '--job', help='SCA3S Job ID')
    parser.add_argument('-s', '--scope', help='Credential scope of SCA3S', default='default')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    """
    Main invocation point for sca3s-cli
    """
    args = parse_args()
    if args.function == 'submit_job':
        functions.submit_job(args)
    elif args.function == 'list_jobs':
        functions.list_jobs(args)
    elif args.function == 'get_job':
        functions.get_job(args)
    elif args.function == 'delete_job':
        functions.delete_job(args)
