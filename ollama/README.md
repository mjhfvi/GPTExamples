curl -fsSL https://ollama.com/install.sh | sh

ollama pull qwen2.5-coder:7b
ollama pull qwen2.5-coder:3b
ollama pull qwen2.5-coder:1.5b
ollama pull llama3.2-vision:11b
ollama pull codellama:7b
ollama pull mistral:7b
ollama pull codegemma:2b
ollama pull llama3.2:3b

# get environment variables
ollama help serve

[Service]
Environment="OLLAMA_DEBUG=1" "OLLAMA_HOST=0.0.0.0" "OLLAMA_INTEL_GPU=true" "OLLAMA_NUM_GPU=999"


[Service]
Environment="OLLAMA_DEBUG=1"
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_INTEL_GPU=true"
Environment="OLLAMA_NUM_GPU=999"


sudo systemctl daemon-reload
sudo systemctl resatrt ollama

ollama
ssh-keygen -t ed25519 -C "mjhfvi@gmail.com"
