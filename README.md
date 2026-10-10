# basic_cheatsheets

网络协议号与端口号速查资料，提供 IANA 注册表生成的 Markdown 表格，方便在协议分析和开发时检索。

## 直接查阅

| 资料 | 用途 |
| --- | --- |
| [IP 协议号](network/ip_protocol_numbers.md) | 查找 IPv4 Protocol / IPv6 Next Header 编号 |
| [TCP 端口](network/tcp_ports.md) | 查找 TCP 服务与端口登记 |
| [UDP 端口](network/udp_ports.md) | 查找 UDP 服务与端口登记 |

表格是生成时的快照，更新时间和来源见各文件；注册端口不能单独证明实际流量使用了对应协议。

## 更新资料

需要 **Python 3.9+** 与访问 IANA 的网络连接，生成器使用 Python 标准库。

```bash
git clone https://github.com/zhihaoevans/basic_cheatsheets.git
cd basic_cheatsheets/network
python3 generate_iana_markdown.py
```

[生成器](network/generate_iana_markdown.py)把三个 Markdown 文件写入**当前工作目录**。在 `network/` 运行才能更新仓库中的现有表格。

## 数据来源与维护

- [IANA Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/)
- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/)

更新后检查来源、时间和表格格式，再提交生成结果。仓库许可见 [LICENSE](LICENSE)。
