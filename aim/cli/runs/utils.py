import fnmatch
import os

from typing import List, Tuple
import io
import zipfile
from datetime import datetime

from aim.storage.rockscontainer import RocksContainer


def list_repo_runs(repo_path: str, lookup_dir: str = None) -> List[str]:
    if lookup_dir is None:
        chunks_dir = os.path.join(repo_path, '.aim', 'meta', 'chunks')
    else:
        chunks_dir = os.path.join(repo_path, '.aim', lookup_dir)
    return os.listdir(chunks_dir)


def match_runs(repo_path: str, hashes: List[str], lookup_dir: str = None) -> List[str]:
    matched_hashes = set()
    all_run_hashes = None
    for run_hash in hashes:
        if '*' in run_hash:
            expr = run_hash  # for the sake of readability
            # avoiding multiple or unnecessary list_runs() calls
            if not all_run_hashes:
                all_run_hashes = list_repo_runs(repo_path, lookup_dir)
            if expr == '*':
                return all_run_hashes
            # update the matches set with current expression matches
            matched_hashes.update(fnmatch.filter(all_run_hashes, expr))
        else:
            matched_hashes.add(run_hash)

    return list(matched_hashes)


def make_zip_archive(repo_path: str) -> io.BytesIO:
    aim_dir = os.path.join(repo_path, '.aim')
    zip_buf = io.BytesIO()
    zipf = zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED)
    len_dir_path = len(aim_dir)
    for root, _, files in os.walk(aim_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path[len_dir_path:])
    zipf.close()
    return zip_buf


def upload_repo_runs(buffer: io.BytesIO, bucket_name: str) -> Tuple[bool, str]:
    try:
        import boto3
    except ImportError:
        raise RuntimeError(
            'This command requires \'boto3\' to be installed. '
            'Please install it with command: \n pip install boto3'
        )

    try:
        s3_client = boto3.client('s3')
        buckets = s3_client.list_buckets()
        bucket_names = [bucket['Name'] for bucket in buckets['Buckets']]
        if bucket_name not in bucket_names:
            s3_client.create_bucket(Bucket=bucket_name)

        key = f'aim-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.zip'
        s3_client.upload_fileobj(buffer, bucket_name, key)
        return True, key
    except Exception as e:
        return False, e


def optimize_container(path, extra_options):
    rc = RocksContainer(path, read_only=True, **extra_options)
    rc.optimize_for_read()
