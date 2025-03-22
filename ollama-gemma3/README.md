# Ollama Gemma3

Ollama で Gemma3 をセルフホストして、画像解析を試すサンプル

## install ollama

```sh
apt install lshw 

curl -fsSL https://ollama.com/install.sh | sh
```

```sh
docker build -t ollama-gemma .

docker run -d --name ollama-container -p 8080:8080 -v ollama-models:/models ollama-gemma 
```