"""Runtime verification script"""
from src.app import app
import json

def test_runtime():
    client = app.test_client()
    
    tests = [
        ('Health Check', 'GET', '/api/health', None, 200),
        ('ISO Format', 'POST', '/api/register', 
         {'username':'user1','email':'u1@test.com','birth_date':'1995-08-20'}, 201),
        ('US Format', 'POST', '/api/register', 
         {'username':'user2','email':'u2@test.com','birth_date':'08/20/1995'}, 201),
        ('EU Format', 'POST', '/api/register', 
         {'username':'user3','email':'u3@test.com','birth_date':'20/08/1995'}, 201),
        ('Missing Data', 'POST', '/api/register', 
         {'username':'u4'}, 400),
    ]
    
    print("\n=== Runtime Verification ===\n")
    for name, method, path, payload, expected in tests:
        if method == 'GET':
            resp = client.get(path)
        else:
            resp = client.post(path, json=payload)
        
        status = 'PASS' if resp.status_code == expected else 'FAIL'
        print(f"{name}: HTTP {resp.status_code} (expected {expected}) [{status}]")
        
        if resp.status_code != expected:
            print(f"  Response: {resp.get_json()}")
    
    print("\n=== All runtime tests completed ===\n")

if __name__ == '__main__':
    test_runtime()
