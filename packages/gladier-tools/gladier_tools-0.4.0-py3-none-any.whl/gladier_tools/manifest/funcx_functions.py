

def manifest_to_funcx_tasks(data):
    """Create funcx execution tasks given a manifest"""
    import os
    import requests
    from urllib.parse import urlparse
    required = [
        'manifest_to_funcx_tasks_manifest_id',
        'manifest_to_funcx_tasks_funcx_endpoint_compute',
        'manifest_to_funcx_tasks_callback_funcx_id',
    ]
    missing = [r for r in required if r not in data.keys()]
    if any(missing):
        raise ValueError(f'{missing} inputs MUST be included')

    url = (f'https://develop.concierge.nick.globuscs.info/api/manifest/'
           f'{data["manifest_to_funcx_tasks_manifest_id"]}/remote_file_manifest/')
    response = requests.get(url).json()
    paths = [m['url'] for m in response['remote_file_manifest']]
    if data.get('manifest_to_funcx_tasks_suffixes'):
        paths = [p for p in paths
                 if any((p.endswith(s) for s in data['manifest_to_funcx_tasks_suffixes']))]
    if data.get('manifest_to_funcx_tasks_use_dirs') is True:
        paths = list({os.path.dirname(p) for p in paths})
    tasks = []
    for path in paths:
        task = dict(
            endpoint=data['manifest_to_funcx_tasks_funcx_endpoint_compute'],
            func=data['manifest_to_funcx_tasks_callback_funcx_id'],
        )
        purl = urlparse(path)
        task['payload'] = data.get('manifest_to_funcx_tasks_payload', {})
        task['payload']['protocol'] = purl.scheme
        task['payload']['host'] = purl.netloc
        task['payload']['path'] = purl.path
        tasks.append(task)
    return {'tasks': tasks}


def manifest_dummy_compute_callback(data):
    return f'Dummy callback on manifest path: {data["path"]}'
