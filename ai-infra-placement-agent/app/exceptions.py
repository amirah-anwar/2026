from fastapi import HTTPException


def cluster_not_found():

    raise HTTPException(
        status_code=404,
        detail="Cluster not found"
    )