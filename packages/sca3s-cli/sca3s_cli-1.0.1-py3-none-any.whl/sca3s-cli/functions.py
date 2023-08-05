import requests
import json
from rich import print as rprint
from parser import get_token


def submit_job(args):
    """
    Submit job to SCA3S
    :param args: Arguments passed to argparser.
    """
    with open(args.file, 'r') as fd:
        json_data = json.load(fd)
    res = requests.post(url="https://sca3s.scarv.org/api/acquire/job",
                        headers=_header_builder(args.scope),
                        json=json_data)
    if res.status_code != 200:
        return 1
    return


def list_jobs(args):
    """
    List jobs on SCA3S
    :param args: Arguments passed to argparser.
    """
    res = requests.get(url="https://sca3s.scarv.org/api/acquire/jobs",
                       headers=_header_builder(args.scope))
    if res.status_code != 200:
        return 1
    rprint(res.json())


def get_job(args):
    """
    List jobs on SCA3S
    :param args: Arguments passed to argparser.
    """
    res = requests.get(url="https://sca3s.scarv.org/api/acquire/job/" + args.job,
                       headers=_header_builder(args.scope))
    if res.status_code != 200:
        return 1
    rprint(res.json())
    return


def delete_job(args):
    """
    Delete job from SCA3S
    :param args: Arguments passed to argparser.
    """
    res = requests.delete(url="https://sca3s.scarv.org/api/acquire/job/" + args.job,
                          headers=_header_builder(args.scope))
    if res.status_code != 200:
        return 1
    return


def _header_builder(scope):
    """
    Builds a header for requests for SCA3S.
    """
    return {
        'Authorization': 'token ' + get_token(scope),
        'Accept-Version': '2.0'
    }
