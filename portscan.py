#!/usr/bin/env python3

# PortScan — varre 10 portas padrão.

from __future__ import annotations
import socket
import concurrent.futures
import time
from typing import List, Tuple, Optional

DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445]  # 10 portas padrão

def try_connect(host: str, port: int, timeout: float = 0.2) -> Tuple[int, str, Optional[str]]:
    """
    Tenta conectar em TCP: retorna (porta, status, banner/info)
    status: OPEN / CLOSED / FILTERED
    """
    s = None
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.settimeout(0.5)
        banner = None
        try:
            data = s.recv(512)
            if data:
                try:
                    banner = data.decode(errors="ignore").strip()
                except Exception:
                    banner = repr(data)
        except socket.timeout:
            banner = None
        return (port, "OPEN", banner)
    except ConnectionRefusedError:
        return (port, "CLOSED", None)
    except socket.timeout:
        return (port, "FILTERED", "timeout")
    except OSError as e:
        # host unreachable, network unreachable, etc.
        return (port, "FILTERED", str(e))
    finally:
        if s:
            try:
                s.close()
            except Exception:
                pass

def scan_default_ports(host: str, ports: List[int] = DEFAULT_PORTS, timeout: float = 0.2, workers: int = 30):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(ports))) as ex:
        futures = { ex.submit(try_connect, host, p, timeout): p for p in ports }
        for fut in concurrent.futures.as_completed(futures):
            try:
                res = fut.result()
            except Exception as e:
                p = futures[fut]
                res = (p, "ERROR", str(e))
            results.append(res)
    results.sort(key=lambda x: x[0])
    return results

def main():
    try:
        print("=== PortScan - Lucas Vitor ===")
        host = input("Alvo: ").strip()
        if not host:
            print("Host do ALVO é obrigatório...")
            return

        # Host -> IP 
        try:
            ip = socket.getaddrinfo(host, None)[0][4][0]
        except Exception as e:
            print(f"Não foi possível resolver '{host}': {e}")
            return

        print(f"\nEscaneando {host} ({ip}) nas portas: {', '.join(map(str, DEFAULT_PORTS))}")
        t0 = time.time()
        results = scan_default_ports(ip)
        elapsed = time.time() - t0

        open_count = 0
        for port, status, info in results:
            if status == "OPEN":
                open_count += 1
                print(f"{port:5d}  OPEN    {info or ''}")
            elif status == "CLOSED":
                print(f"{port:5d}  CLOSED")
            elif status == "FILTERED":
                print(f"{port:5d}  FILTERED {info or ''}")
            else:
                print(f"{port:5d}  {status} {info or ''}")

        print(f"\nResumo: {open_count} portas abertas | tempo: {elapsed:.2f}s")
        print("Nota: use esse script somente em alvos que você tem autorização para testar.")
    except KeyboardInterrupt:
        print("\nScan abortado pelo usuário (Ctrl+C).")

if __name__ == "__main__":
    main()
