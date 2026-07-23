import importlib,pkgutil,traceback,tests
tot=ok=0
for m in pkgutil.iter_modules(tests.__path__,"tests."):
    mod=importlib.import_module(m.name)
    for n in dir(mod):
        if n.startswith("test_"):
            tot+=1
            try: getattr(mod,n)(); ok+=1; print(f"PASS {m.name}.{n}")
            except Exception: print(f"FAIL {m.name}.{n}"); traceback.print_exc()
print(f"\n{ok}/{tot} tests passed")
raise SystemExit(0 if ok==tot else 1)
