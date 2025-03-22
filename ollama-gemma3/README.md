# Ollama Gemma3

Ollama で Gemma3 をセルフホストして、画像解析を試すサンプル
サンプル図面は [CADDi Tech Blog](https://caddi.tech/2024/12/06/080000) より入手

## install ollama

```sh
apt install lshw 

curl -fsSL https://ollama.com/install.sh | sh
```

```sh
docker build -t ollama-gemma .

docker run -d --name ollama-container -p 8080:8080 -v ollama-models:/models ollama-gemma 
```

```sh
curl -X POST http://localhost:8080/api/generate \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gemma3:4b",
       "prompt": "あなたは機械図面の製図者です。この図面に記載されている材質と表面処理を教えてください。日本語で json 形式で答えてください。",
       "stream": false,
       "format": "json",
       "images": ["'$(base64 -w 0 caddi_sample_image.png)'"]
     }'
```

## References

- https://cloud.google.com/run/docs/tutorials/gpu-gemma-with-ollama?hl=ja
- https://github.com/ollama/ollama/blob/main/docs/api.md
