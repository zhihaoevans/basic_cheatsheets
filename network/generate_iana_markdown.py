#!/usr/bin/env python3
"""
Generate markdown files for:
- IP protocol numbers (from IANA Protocol Numbers registry)
- TCP ports (from IANA Service Name and Port Number registry)
- UDP ports (from IANA Service Name and Port Number registry)

Outputs into the current directory:
- ip_protocol_numbers.md
- tcp_ports.md
- udp_ports.md

Source registries:
- Protocol Numbers CSV: https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv
- Service Names & Port Numbers CSV: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv
"""

import csv
import io
import sys
import urllib.request
from datetime import datetime


PROTOCOL_NUMBERS_CSV = (
    "https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv"
)
SERVICE_PORTS_CSV = (
    "https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.csv"
)


def fetch_csv(url: str) -> csv.DictReader:
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    # IANA CSVs are UTF-8
    text = data.decode("utf-8", errors="replace")
    return csv.DictReader(io.StringIO(text))


def sanitize(s: str) -> str:
    if s is None:
        return ""
    s = s.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    return s.strip()


def write_ip_protocol_numbers_md(rows: list[dict], out_path: str):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# IP 协议号 (IANA)")
        f.write("\n\n")
        f.write(
            "来源与完整清单: https://www.iana.org/assignments/protocol-numbers\n"
        )
        f.write(f"生成时间: {now}\n\n")
        f.write(
            "说明: IPv4 中该字段称为 Protocol，IPv6 中称为 Next Header。部分值同时也是 IPv6 扩展头类型。\n\n"
        )
        # Table header
        f.write(
            "| 十进制 | 关键字 | 协议 | IPv6 扩展头 | 参考 |\n|---:|---|---|:---:|---|\n"
        )
        for r in rows:
            dec = sanitize(r.get("Decimal", ""))
            kw = sanitize(r.get("Keyword", ""))
            proto = sanitize(r.get("Protocol", ""))
            ipv6_ext = sanitize(r.get("IPv6 Extension Header", ""))
            ref = sanitize(r.get("Reference", ""))
            f.write(
                f"| {dec} | {kw} | {proto} | {ipv6_ext or ''} | {ref} |\n"
            )


def parse_port_number_for_sort(val: str) -> int:
    # Handles single numbers and ranges like "5147-5149" by taking the first
    try:
        if not val:
            return 10_000_000
        if "-" in val:
            return int(val.split("-", 1)[0])
        return int(val)
    except ValueError:
        return 10_000_000


def write_ports_md(rows: list[dict], transport: str, out_path: str):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    filtered = [r for r in rows if sanitize(r.get("Transport Protocol", "")).lower() == transport]
    # Sort by Port Number (numeric/range-aware), then Service Name
    filtered.sort(
        key=lambda r: (parse_port_number_for_sort(sanitize(r.get("Port Number", ""))), sanitize(r.get("Service Name", "")).lower())
    )

    with open(out_path, "w", encoding="utf-8") as f:
        title = f"# {transport.upper()} 端口号与协议 (IANA)"
        f.write(title)
        f.write("\n\n")
        f.write(
            "来源与完整清单: https://www.iana.org/assignments/service-names-port-numbers\n"
        )
        f.write(f"生成时间: {now}\n\n")
        f.write(
            "范围: 系统端口 0-1023、用户端口 1024-49151、动态/私有端口 49152-65535。\n\n"
        )
        # Table header
        f.write(
            "| 端口 | 服务名 | 传输协议 | 简短说明 | 参考 |\n|---:|---|---|---|---|\n"
        )
        for r in filtered:
            port = sanitize(r.get("Port Number", ""))
            name = sanitize(r.get("Service Name", "")) or "(无)"
            proto = sanitize(r.get("Transport Protocol", ""))
            desc = sanitize(r.get("Description", ""))
            ref = sanitize(r.get("Reference", ""))
            f.write(
                f"| {port} | {name} | {proto} | {desc} | {ref} |\n"
            )


def main():
    print("Fetching IANA CSVs...")
    proto_reader = fetch_csv(PROTOCOL_NUMBERS_CSV)
    ports_reader = fetch_csv(SERVICE_PORTS_CSV)

    proto_rows = list(proto_reader)
    port_rows = list(ports_reader)

    print(f"Protocol numbers rows: {len(proto_rows)}")
    print(f"Service/port rows: {len(port_rows)}")

    write_ip_protocol_numbers_md(proto_rows, "ip_protocol_numbers.md")
    write_ports_md(port_rows, "tcp", "tcp_ports.md")
    write_ports_md(port_rows, "udp", "udp_ports.md")

    print("Done. Files written:")
    print(" - ip_protocol_numbers.md")
    print(" - tcp_ports.md")
    print(" - udp_ports.md")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)