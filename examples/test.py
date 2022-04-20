from pydavinci import davinci

resolve = davinci.Resolve(headless=True)
print(resolve)
print(resolve._obj)
print(resolve.version)
