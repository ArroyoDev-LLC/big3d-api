import json
from pathlib import Path
from tempfile import TemporaryDirectory

from awslambdaric.lambda_context import LambdaContext
from fastapi import FastAPI, File, UploadFile
from loguru import logger
from mangum import Mangum
from threedframe import utils
from threedframe.config import config

# Setup threedframe.
DATA_DIR = Path("/tmp/big3d_api")
config.RENDERS_DIR = DATA_DIR / "renders"
config.setup_solid()

app = FastAPI()


@app.post("/compute")
async def compute(model: UploadFile = File(...)):
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


def handler(event, context: LambdaContext):
    """Root handler."""
    logger.info("event: {}", event)
    logger.info("context: {}", context)
    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    logger.info("response {}", response)
    return response
