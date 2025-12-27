import pytest
from unittest.mock import patch, MagicMock
from src.verify import ImageVerifier
import subprocess

# Test 1: Geçerli bir imza başarıyla doğrulanmalı
@patch("subprocess.run")
def test_verify_signature_success(mock_subprocess):
    # Simülasyon: Cosign komutu başarılı (returncode=0) dönüyor
    mock_subprocess.return_value = MagicMock(returncode=0, stdout="Verification successful", stderr="")
    
    verifier = ImageVerifier()
    success, output = verifier.verify_signature("ghcr.io/test/image:latest")
    
    assert success is True
    assert "Verification successful" in output

# Test 2: Geçersiz imza veya imzasız imaj reddedilmeli
@patch("subprocess.run")
def test_verify_signature_failure(mock_subprocess):
    # Simülasyon: Cosign hata veriyor (CalledProcessError)
    mock_subprocess.side_effect = subprocess.CalledProcessError(1, "cosign", stderr="No signature found")
    
    verifier = ImageVerifier()
    success, output = verifier.verify_signature("ghcr.io/test/fake:latest")
    
    assert success is False
    assert "No signature found" in output

# Test 3: Politika kontrolü - Temiz çıktı kabul edilmeli
def test_policy_check_pass():
    verifier = ImageVerifier()
    # "critical" kelimesi geçmeyen temiz bir çıktı
    dummy_output = '{"diger_bilgiler": "ok"}'
    result = verifier.check_policy(dummy_output)
    assert result is True

# Test 4: Politika kontrolü - Yasaklı kelime varsa reddedilmeli
def test_policy_check_fail():
    verifier = ImageVerifier()
    # İçinde "critical" geçen bir çıktı (Simüle edilmiş risk)
    dummy_output = '{"vulnerability": "critical"}'
    result = verifier.check_policy(dummy_output)
    assert result is False

# Test 5: Boş çıktı politika kontrolünden geçmemeli
def test_policy_check_empty():
    verifier = ImageVerifier()
    result = verifier.check_policy("")
    assert result is False