#!/usr/bin/env python3
"""
Script de prueba para el microservicio de verificación de lista negra
Ejecuta pruebas básicas contra el API REST
"""

import requests
import json
import sys

# Configuración
BASE_URL = "http://localhost:8000"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjk5OTk5OTk5OTl9.Jz8n5r7Y5oU8i6A2cX4l8N3vB9u1K6t3R7yW5qE8zF2"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_health():
    """Test del endpoint de salud"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health Check - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health Check failed: {e}")
        return False

def test_verificar_persona_bloqueada():
    """Test verificando persona que SÍ está en lista negra"""
    try:
        data = {"nombre_completo": "Juan Pérez González"}
        response = requests.post(f"{BASE_URL}/verificar", headers=headers, json=data)
        print(f"✅ Verificar persona bloqueada - Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        return response.status_code == 200 and result.get("encontrado") == True
    except Exception as e:
        print(f"❌ Verificar persona bloqueada failed: {e}")
        return False

def test_verificar_persona_no_bloqueada():
    """Test verificando persona que NO está en lista negra"""
    try:
        data = {"nombre_completo": "Persona No Bloqueada"}
        response = requests.post(f"{BASE_URL}/verificar", headers=headers, json=data)
        print(f"✅ Verificar persona no bloqueada - Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result}")
        return response.status_code == 200 and result.get("encontrado") == False
    except Exception as e:
        print(f"❌ Verificar persona no bloqueada failed: {e}")
        return False

def test_sin_autenticacion():
    """Test sin token de autenticación"""
    try:
        data = {"nombre_completo": "Juan Pérez González"}
        response = requests.post(f"{BASE_URL}/verificar", json=data)
        print(f"✅ Test sin autenticación - Status: {response.status_code}")
        print(f"   Response: {response.json() if response.content else 'No content'}")
        return response.status_code in [401, 403]  # Esperamos error de autenticación
    except Exception as e:
        print(f"❌ Test sin autenticación failed: {e}")
        return False

def test_datos_invalidos():
    """Test con datos inválidos"""
    try:
        data = {"nombre_completo": ""}
        response = requests.post(f"{BASE_URL}/verificar", headers=headers, json=data)
        print(f"✅ Test datos inválidos - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"❌ Test datos inválidos failed: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas del microservicio de verificación...")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Verificar persona bloqueada", test_verificar_persona_bloqueada),
        ("Verificar persona no bloqueada", test_verificar_persona_no_bloqueada),
        ("Test sin autenticación", test_sin_autenticacion),
        ("Test datos inválidos", test_datos_invalidos)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Ejecutando: {test_name}")
        if test_func():
            passed += 1
            print(f"   ✅ PASÓ")
        else:
            print(f"   ❌ FALLÓ")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
        sys.exit(0)
    else:
        print("💥 Algunas pruebas fallaron")
        sys.exit(1)

if __name__ == "__main__":
    main()
