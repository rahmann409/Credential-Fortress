# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import socket
import urllib.request
import pytest
import sys

def test_no_outbound_network(monkeypatch):
    def mock_socket_connect(*args, **kwargs):
        raise RuntimeError("Network call attempted and blocked!")
        
    monkeypatch.setattr(socket.socket, "connect", mock_socket_connect)
    
    import credential_fortress.modules.analyzer
    
    # Ensure our analyzer doesn't make network calls
    res = credential_fortress.modules.analyzer.evaluate_strength("testpassword123", ["test"])
    assert res["status"] in ["Moderate", "Strong", "Weak", "Weak (Dictionary overlap)"]
