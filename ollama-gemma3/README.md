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

## Result

```
{"model":"gemma3:4b","created_at":"2025-03-22T13:51:55.735470078Z","response":"{\n  \"material\": \"SS400D\",\n  \"surface_treatment\": \"Melamine coating\"\n}","done":true,"done_reason":"stop","context":[105,2364,107,236840,3024,236772,236771,236842,108,229197,102749,239147,189831,238426,239147,237457,3652,236924,8978,239147,183916,68151,29468,107784,237032,52325,49945,237051,113040,15142,236924,94951,237007,8373,236743,36669,237007,238843,19230,15142,236924,106,107,105,4368,107,236782,107,236743,623,10236,1083,623,4033,236812,236771,236771,236796,827,107,236743,623,36593,236779,49085,1083,623,29294,13572,23671,236775,107,236783],"total_duration":3026438808,"load_duration":84915063,"prompt_eval_count":302,"prompt_eval_duration":190000000,"eval_count":28,"eval_duration":2749000000}
```

## References

- https://cloud.google.com/run/docs/tutorials/gpu-gemma-with-ollama?hl=ja
- https://github.com/ollama/ollama/blob/main/docs/api.md
