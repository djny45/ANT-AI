�

🐜 ANT AI
Autonomous Neural Taskforce
A personal AI operating system built from cooperating agents — swarm intelligence, local-first LLM routing, a persistent knowledge hive, and a security layer designed in from day one.
�
�
�
�
�
Vision • Architecture • Main Systems • Project Structure • Getting Started • Releases • Roadmap • Contributing
�

Vision
ANT AI is a personal AI operating system where specialized agents — not one monolithic model — collaborate to plan, research, code, and secure a task end to end. Each "ant" is purpose-built and coordinated by a central commander, with shared memory and a hardened security layer underneath.
Architecture
Text
The Commander receives a task, delegates it across the swarm, draws on the Knowledge Hive for context, and every action is written to a hash-chained audit ledger.
Main Systems
System
Description
🧠 Intelligence
Local inference via Ollama (Llama / Mistral / Phi), with OpenRouter as a cloud fallback and automatic model routing
🐜 Swarm Army
Commander Ant, Research Ant, Coding Ant, Security Ant, Analyst Ant — each scoped to a single responsibility
📚 Knowledge Hive
Document ingestion, vector memory, knowledge graph, and long-term memory shared across the swarm
🔐 Security
API key vault, rate limiting, encrypted memory, and hash-chain audit logs
♻️ Evolution Framework
Self-proposed improvements, generated code, tested in a sandbox before being adopted
Project Structure
Text
Getting Started
ANT AI is at v0.1 — Foundation stage. The systems above are scaffolded and under active development; see Development Status for what's implemented today.
Bash
Configuration lives in config.yaml — set your local Ollama endpoint and, optionally, an OPENROUTER_API_KEY for cloud fallback.
APK Releases
Production Android builds run through a signed release pipeline (.github/workflows/release-apk.yml):
✅ Signed release APK
✅ Automated security gate before release
✅ SHA256 checksum published with every release
Debug builds run on every push via android-apk.yml. See android_app/downloads/ANT_AI_Download_Link.md or the Releases page for the latest APK.
Development Status
ANT AI v0.1 — Foundation
Building toward a fully autonomous personal AI assistant ecosystem, with a roadmap toward dGEN1 ethOS integration. Architecture and module boundaries are in place; core agent logic is being built out system by system.
Contributing
Contributions are welcome — see CONTRIBUTING.md for guidelines. Please review SECURITY.md before submitting anything touching the security layer, model routing, or the autonomy/evolution modules.
License
Released under the MIT License.
