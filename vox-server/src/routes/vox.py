from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse

from src.internal.synthesizer import synthesize
from src.schemas.vox import VoxRequest

router = APIRouter()


@router.post(
    path="",
)
def synthesize_voicevox(
    background_tasks: BackgroundTasks,
    request_body: VoxRequest,
) -> FileResponse:
    temp_dir = mkdtemp()
    background_tasks.add_task(rmtree, temp_dir)
    dst_file_name = "output.wav"
    dst_file_path = Path(temp_dir) / dst_file_name

    synthesize(
        dst_file_path=dst_file_path,
        target_text=request_body.text,
    )

    return FileResponse(path=dst_file_path, filename=dst_file_name)
