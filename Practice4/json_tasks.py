import json 
with open('sample-data.json', 'r') as f:
    data = json.load(f)
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<15} {'Speed':<10} {'MTU':<6}")
print(f"{'-'*50} {'-'*15} {'-'*10} {'-'*6}")
for item in data['imdata']:
    attr = item['l1PhysIf']['attributes']
    dn    = attr['dn']
    descr = attr['descr']
    speed = attr['speed']
    mtu   = attr['mtu']
    print(f"{dn:<50} {descr:<15} {speed:<10} {mtu:<6}")
