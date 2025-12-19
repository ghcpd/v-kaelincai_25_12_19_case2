import json
import urllib.request

BASE = 'http://127.0.0.1:5000'

def get(path):
    req = urllib.request.Request(BASE + path)
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode()
        return resp.status, body


def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=data, headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
            return resp.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


if __name__ == '__main__':
    print('Health check:')
    status, body = get('/api/health')
    print(status)
    print(body)

    tests = [
        ("Chrome(ISO)", {"username":"chromeuser","email":"chrome@test.com","birth_date":"1995-08-20"}),
        ("Safari(US)", {"username":"safariuser","email":"safari@test.com","birth_date":"08/20/1995"}),
        ("EU(EU)", {"username":"euuser","email":"eu@test.com","birth_date":"20/08/1995"}),
        ("Missing data", {"username":"testuser"}),
        ("Invalid JSON", "not json")
    ]

    for name, payload in tests:
        print('\nTest:', name)
        if name == 'Invalid JSON':
            # send invalid JSON raw
            req = urllib.request.Request(BASE + '/api/register', data=b'not json', headers={'Content-Type':'application/json'})
            try:
                with urllib.request.urlopen(req) as resp:
                    print(resp.status)
                    print(resp.read().decode())
            except urllib.error.HTTPError as e:
                print('HTTP', e.code)
                print(e.read().decode())
            continue

        status, body = post('/api/register', payload)
        print('HTTP', status)
        print(body)
