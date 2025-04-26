from threading import Lock
from typing import ClassVar

from src.settings import get_settings
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile


class SynthesizerSingleton:
    _instance: Synthesizer | None = None
    _lock: Lock = Lock()
    _loaded_models: ClassVar[set[str]] = set()

    @classmethod
    def initialize_synthesizer(cls) -> Synthesizer:
        settings = get_settings()
        voicevox_onnxruntime_path = (
            settings.voicevox_core_path / "onnxruntime" / "lib" / Onnxruntime.LIB_VERSIONED_FILENAME  # type: ignore[attr-defined]
        )
        open_jtalk_dict_dir = settings.voicevox_core_path / "dict" / "open_jtalk_dic_utf_8-1.11"
        return Synthesizer(
            Onnxruntime.load_once(filename=str(voicevox_onnxruntime_path)),  # type: ignore[attr-defined]
            OpenJtalk(open_jtalk_dict_dir),
        )

    @classmethod
    def get_instance(cls) -> Synthesizer:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # ダブルチェックロック
                    cls._instance = cls.initialize_synthesizer()
        return cls._instance

    @classmethod
    def load_model(cls, model_name: str) -> None:
        if model_name in cls._loaded_models:
            return

        settings = get_settings()
        model_path = settings.voicevox_core_path / "models" / "vvms" / model_name

        if cls._instance is not None:
            with VoiceModelFile.open(model_path) as model:  # type: ignore[attr-defined]
                cls._instance.load_voice_model(model)
            cls._loaded_models.add(model_name)
        else:
            error_message = "Synthesizer instance is not initialized"
            raise RuntimeError(error_message)


def synthesize(model_name: str, style_id: int, target_text: str) -> bytes:
    synthesizer = SynthesizerSingleton.get_instance()
    SynthesizerSingleton.load_model(model_name)
    return synthesizer.tts(target_text, style_id)
