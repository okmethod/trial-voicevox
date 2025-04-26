
手順
https://github.com/VOICEVOX/voicevox_core/blob/main/docs/guide/user/usage.md

```sh
chmod +x downloader/download-osx-arm64

./downloader/download-osx-arm64 --exclude c-api


whl_path="https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.0/voicevox_core-0.16.0-cp310-abi3-macosx_11_0_arm64.whl"

(cd vox-server && uv add $whl_path)
```