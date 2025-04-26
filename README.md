# trial VOICEVOX

手順
https://github.com/VOICEVOX/voicevox_core/blob/main/docs/guide/user/usage.md

## セットアップ手順のメモ

### uvプロジェクト作成
```sh
uv init vox-server
```

### voicevox_core のダウンロード
```sh
downloader_path="downloader/download-osx-arm64"
chmod +x $downloader_path
ls -l $downloader_path

(cd vox-server && ./../$downloader_path --exclude c-api)
```

### Python ライブラリのインストール
```sh
whl_path="https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.0/voicevox_core-0.16.0-cp310-abi3-macosx_11_0_arm64.whl"

(cd vox-server && uv add $whl_path)
```