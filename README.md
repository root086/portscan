# 🔎 PortScan — Lucas Vitor

**Status:** ✅ Em Desenvolvimento...

PortScan é um scanner TCP simples e direto: pede **apenas o host** e varre **10 portas padrão** (rápido, leve, ideal para laboratório e estudo). Feito para aprendizado — não é uma ferramenta de pentest profissional.

> ⚠️ Use somente em alvos que você tem permissão para testar. Scans não autorizados podem ser ilegais.

---

## 📋 Descrição

Script em Python que realiza varredura paralela (threads) nas 10 portas mais comuns, tenta capturar banners curtos quando disponíveis e classifica cada porta como `OPEN`, `CLOSED` ou `FILTERED`. Prático para checks rápidos em redes/VMs próprias.

---

## 🛠 Tecnologias

- **Python 3.8+**
- Bibliotecas padrão: `socket`, `concurrent.futures`, `time`

---

## 🔢 Portas padrão (10)

`21, 22, 23, 25, 53, 80, 110, 139, 443, 445`

> Edite `DEFAULT_PORTS` no topo do script para alterar essa lista.

---

## ✅ Funcionalidades

- Varredura paralela (threads) das 10 portas padrão
- Banner grabbing curto (quando o serviço enviar algo)  
- Tratamento básico de timeouts e erros de SO  
- Saída legível no terminal + resumo de portas abertas  
- Proteção contra `Ctrl+C` (KeyboardInterrupt)

---

## 🚀 Como usar

```bash
# clonar o repositório
git clone https://github.com/root086/portscan
cd portscan

# rodar o script
python3 portscan.py
