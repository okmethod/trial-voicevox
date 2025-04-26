from datetime import UTC, datetime
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse

from src.internal.synthesizer import SynthesizerSingleton, synthesize
from src.schemas.vox import VoxRequest

router = APIRouter()
SynthesizerSingleton.initialize_synthesizer()


@router.post(
    path="",
)
def synthesize_voicevox(
    background_tasks: BackgroundTasks,
    request_body: VoxRequest,
) -> FileResponse:
    wav = synthesize(
        model_name=request_body.model or "0.vvm",
        style_id=request_body.style or 3,  # ずんだもん/ノーマル
        target_text=request_body.text,
    )

    temp_dir = mkdtemp()
    background_tasks.add_task(rmtree, temp_dir)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    dst_file_name = f"generated_{timestamp}.wav"
    dst_file_path = Path(temp_dir) / dst_file_name
    with dst_file_path.open("wb") as f:
        f.write(wav)

    return FileResponse(path=dst_file_path, filename=dst_file_name)
