import os
from pathlib import Path

from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

voicevox_core_path = Path(os.environ.get("VOICEVOX_CORE_PATH", "./voicevox_core"))
output_dir_path = Path(os.environ.get("OUTPUT_DIR_PATH", "./output"))


def synthesize(target_text: str) -> None:
    # Synthesizerの初期化
    voicevox_onnxruntime_path = (
        voicevox_core_path / "onnxruntime" / "lib" / Onnxruntime.LIB_VERSIONED_FILENAME  # type: ignore[attr-defined]
    )
    open_jtalk_dict_dir = voicevox_core_path / "dict" / "open_jtalk_dic_utf_8-1.11"
    synthesizer = Synthesizer(
        Onnxruntime.load_once(filename=str(voicevox_onnxruntime_path)),  # type: ignore[attr-defined]
        OpenJtalk(open_jtalk_dict_dir),
    )

    # 音声モデルの読み込み
    voicevox_model_name = "0.vvm"
    voice_model_path = voicevox_core_path / "models" / "vvms" / voicevox_model_name
    with VoiceModelFile.open(voice_model_path) as model:  # type: ignore[attr-defined]
        synthesizer.load_voice_model(model)

    # テキスト音声合成
    style_id = 3  # ずんだもん/ノーマル
    wav = synthesizer.tts(target_text, style_id)
    output_path = output_dir_path / "output.wav"
    output_dir_path.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        f.write(wav)
