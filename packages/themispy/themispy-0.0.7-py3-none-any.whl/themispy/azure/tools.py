import json
import os

from azure.storage.blob import ContainerClient

from themispy.project.utils import build_path, get_files


# Azure Storage Connection
def get_connection_string() -> str:
    """Get Azure Web Jobs Storage Key from 'local.settings.json'."""
    with open(build_path('local.settings.json')) as local_settings:
        return json.load(local_settings)['Values']['AzureWebJobsStorage']


# Uploading files to blob storage    
def upload(container: str,
           src: os.path = 'temp/',
           overwrite: bool = True,
           remove_files: bool = True) -> None:
    """
    Upload data to Azure blob storage.
    Enter container path, e.g.: 'mycontainer/mysubcontainer'.
    """
    src = build_path(src)
    
    container_client = ContainerClient.from_connection_string(
        get_connection_string(), container)

    print('Uploading files to blob storage ...')
    
    for file in get_files(dir=src):
        blob_client = container_client.get_blob_client(file.name)
    
        with open(file.path, 'rb') as data:
            if not overwrite:
                blob_client.upload_blob(data, overwrite=overwrite,
                                        blob_type='AppendBlob')
            else:
                blob_client.upload_blob(data, overwrite=overwrite)
            
            if remove_files:
                os.remove(file)
            
            print('Data uploaded to blob storage.')
