from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from awslambdaric.lambda_context import LambdaContext
from fastapi import Depends, FastAPI, File, UploadFile
from loguru import logger
from mangum import Mangum
from threedframe.config import config

# Setup threedframe.
DATA_DIR = Path("/tmp/big3d_api")  # noqa
config.RENDERS_DIR = DATA_DIR / "renders"  # noqa
config.setup_solid()  # noqa


from threedframe import utils
from threedframe.models import ModelData
from threedframe.scad import JointDirector, JointDirectorParams
from threedframe.scad.build import RenderFileType

import depends
import schemas

if TYPE_CHECKING:
    pass


app = FastAPI(title="Big3D Api")


@app.post("/compute")
async def compute(model: UploadFile = File(...)) -> ModelData:
    """Compute model properties from uploaded model."""
    with TemporaryDirectory() as tmpdir:
        model_path = Path(tmpdir) / "model.blend"
        model_path.unlink(missing_ok=True)
        model_path.write_bytes(await model.read())
        script_path = config.LIB_DIR.parent / "compute.py"
        assert script_path.exists(), f"Failed to find script path: {script_path}"
        data_path = model_path.with_suffix(".json")
        utils.exec_blender_script(Path(model_path), script_path, data_path)
        logger.info(f"Data written to: {data_path.absolute()}")
        data = json.loads(data_path.read_text())
    logger.info("computed results: {}", data)
    return data


@app.post("/generate")
async def generate(
    generate_in: schemas.GenerateRequest, s3: depends.S3Bucket = Depends(depends.RendersBucket)
):
    """Model generation endpoint."""
    model_data = generate_in.model_data
    vertex = generate_in.vertex
    params = JointDirectorParams(
        model=model_data, vertices=(vertex,), render=True, render_file_type=RenderFileType.STL
    )
    director = JointDirector(params=params)
    director.assemble()
    rndr_path = next(iter(director.render_paths.values()))
    hasher = hashlib.md5()
    rndr_data = rndr_path.read_bytes()
    hasher.update(rndr_data)
    render_hash = hasher.hexdigest()
    bucket_key = f"renders/{render_hash}.stl"
    s3.bucket.upload_file(Filename=str(rndr_path), Key=bucket_key)
    s3.client.get_object()
    presigned = s3.client.generate_presigned_url(
        "get_object", {"Bucket": s3.bucket.name, "Key": bucket_key}
    )
    return {"model": presigned}


def handler(event, context: LambdaContext):
    """Root handler."""
    logger.info("context: {}", context)
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    logger.info("response {}", response)
    return response
