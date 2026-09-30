from security.audit_logger import AuditLogger
from security.encryption_manager import EncryptionManager
from security.threat_detector import ThreatDetector


def test_audit_logger_accumulates_events():
    logger = AuditLogger()
    first = {"event": "start"}
    second = {"event": "complete"}

    logger.record(first)
    logger.record(second)

    assert logger.history() == [first, second]


def test_encryption_manager_returns_protected_shape():
    assert EncryptionManager().protect("secret") == {
        "data": "secret",
        "encrypted": True,
    }


def test_threat_detector_returns_scan_shape():
    assert ThreatDetector().scan("payload") == {
        "target": "payload",
        "threats": [],
        "status": "scanned",
    }
