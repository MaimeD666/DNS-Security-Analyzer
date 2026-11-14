"""Проверка библиотек проекта без запуска анализатора и сетевой отправки."""

import importlib.metadata
import json
from pathlib import Path
import socket
import sys
import tempfile


def main() -> int:
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError("Для проекта требуется CPython 3.12")

    import dpkt
    import joblib
    import numpy as np
    import tldextract
    from sklearn.neural_network import MLPClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    def deny_connect(*args, **kwargs):
        raise RuntimeError("Проверка окружения не должна устанавливать сетевые соединения")

    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex
    socket.socket.connect = deny_connect
    socket.socket.connect_ex = deny_connect
    try:
        extractor = tldextract.TLDExtract(
            suffix_list_urls=(),
            cache_dir=None,
            include_psl_private_domains=True,
        )
        assert extractor("a.b.example.co.uk").top_domain_under_public_suffix == "example.co.uk"
        assert extractor("x.user.blogspot.com").top_domain_under_public_suffix == "user.blogspot.com"

        with tempfile.TemporaryDirectory(prefix="dns_environment_") as folder:
            capture = Path(folder) / "probe.pcap"
            question = dpkt.dns.DNS(id=1, qd=[dpkt.dns.DNS.Q(name="probe.example.test", type=dpkt.dns.DNS_A)])
            datagram = dpkt.udp.UDP(sport=53000, dport=53, data=bytes(question))
            datagram.ulen = len(datagram)
            ip = dpkt.ip.IP(src=bytes([192, 0, 2, 10]), dst=bytes([192, 0, 2, 53]), p=17, data=datagram)
            ip.len = len(ip)
            ethernet = dpkt.ethernet.Ethernet(
                src=b"\x02\x00\x00\x00\x00\x01", dst=b"\x02\x00\x00\x00\x00\x02", type=0x0800, data=ip
            )
            with capture.open("wb") as stream:
                writer = dpkt.pcap.Writer(stream)
                writer.writepkt(bytes(ethernet), ts=1.0)
            with capture.open("rb") as stream:
                restored = list(dpkt.pcap.Reader(stream))
            assert len(restored) == 1
            restored_dns = dpkt.dns.DNS(dpkt.ethernet.Ethernet(restored[0][1]).data.data.data)
            assert restored_dns.qd[0].name == "probe.example.test"

            # Искусственные числа проверяют API обучения, а не качество детектора.
            values = np.vstack((np.zeros((8, 10)), np.ones((8, 10))))
            labels = np.array([0] * 8 + [1] * 8)
            pipeline = Pipeline([
                ("scale", StandardScaler()),
                ("mlp", MLPClassifier(hidden_layer_sizes=(16, 8), solver="lbfgs", max_iter=1000, random_state=42)),
            ])
            pipeline.fit(values, labels)
            before = pipeline.predict_proba(values)
            model_path = Path(folder) / "probe.joblib"
            joblib.dump(pipeline, model_path)
            after = joblib.load(model_path).predict_proba(values)
            np.testing.assert_allclose(before, after, rtol=0, atol=1e-12)
            assert np.isfinite(after).all() and after.shape == (16, 2)
    finally:
        socket.socket.connect = original_connect
        socket.socket.connect_ex = original_connect_ex

    packages = ["dpkt", "tldextract", "numpy", "scipy", "scikit-learn", "joblib", "threadpoolctl"]
    print(json.dumps({"python": sys.version.split()[0], "packages": {
        name: importlib.metadata.version(name) for name in packages
    }, "checks": ["pcap_roundtrip", "offline_psl", "mlp_fit", "model_roundtrip"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
