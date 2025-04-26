import os
import argparse
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

voicevox_core_path = os.environ.get("VOICEVOX_CORE_PATH", "./voicevox_core")
voicevox_model_name = os.environ.get("VOICEVOX_MODEL_NAME", "0.vvm")
output_dir_path = os.environ.get("OUTPUT_DIR_PATH", "./output_dir")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=str)
    args = parser.parse_args()
    target_text = args.text or "サンプル音声です"

    # Synthesizerの初期化
    voicevox_onnxruntime_path = os.path.join(voicevox_core_path, "onnxruntime", "lib", Onnxruntime.LIB_VERSIONED_FILENAME)
    open_jtalk_dict_dir = os.path.join(voicevox_core_path, "dict", "open_jtalk_dic_utf_8-1.11")
    synthesizer = Synthesizer(Onnxruntime.load_once(filename=voicevox_onnxruntime_path), OpenJtalk(open_jtalk_dict_dir))

    # 音声モデルの読み込み
    voice_model_path = os.path.join(voicevox_core_path, "models", "vvms", voicevox_model_name)
    with VoiceModelFile.open(voice_model_path) as model:
        synthesizer.load_voice_model(model)

    # テキスト音声合成
    style_id = 3  # ずんだもん/ノーマル
    wav = synthesizer.tts(target_text, style_id)
    output_path = os.path.join(output_dir_path, "output.wav")
    with open(output_path, "wb") as f:
        f.write(wav)

if __name__ == "__main__":
    main()
