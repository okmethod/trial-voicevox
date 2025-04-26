from pathlib import Path

from src.settings import get_settings
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile


def synthesize(dst_file_path: Path, target_text: str) -> None:
    settings = get_settings()

    # Synthesizerの初期化
    voicevox_onnxruntime_path = (
        settings.voicevox_core_path / "onnxruntime" / "lib" / Onnxruntime.LIB_VERSIONED_FILENAME  # type: ignore[attr-defined]
    )
    open_jtalk_dict_dir = settings.voicevox_core_path / "dict" / "open_jtalk_dic_utf_8-1.11"
    synthesizer = Synthesizer(
        Onnxruntime.load_once(filename=str(voicevox_onnxruntime_path)),  # type: ignore[attr-defined]
        OpenJtalk(open_jtalk_dict_dir),
    )

    # 音声モデルの読み込み
    voicevox_model_name = "0.vvm"
    voice_model_path = settings.voicevox_core_path / "models" / "vvms" / voicevox_model_name
    with VoiceModelFile.open(voice_model_path) as model:  # type: ignore[attr-defined]
        synthesizer.load_voice_model(model)

    # テキスト音声合成
    style_id = 3  # ずんだもん/ノーマル
    wav = synthesizer.tts(target_text, style_id)
    with dst_file_path.open("wb") as f:
        f.write(wav)
