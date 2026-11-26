# Security boundaries

This stack is a local training lab. Its SSH and n8n ports bind to the host loopback address. The SSH target has two non-root accounts, accepts public-key authentication only, and disables root login, agent forwarding, and port forwarding for this first challenge. The target receives public client keys and its own host key; it does not mount the client private-key directory. n8n does not mount the Docker socket or the host's SSH directory.

The private keys in `state/keys/` are generated locally with restricted permissions. The `state/` directory is ignored by Git and excluded from Docker build context. The n8n credential helper sends the automation private key through a pipe to n8n's local CLI after owner setup; it does not write a plaintext credential export or print the key. n8n stores its own data in a persistent Compose volume.

The lab's passwords are random and unknown, and SSH password authentication is disabled. Do not put real infrastructure keys, customer data, or production hosts into this playground. Review `git status` and the staged file list before publishing this repository.
