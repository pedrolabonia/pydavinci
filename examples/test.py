from pydavinci import davinci

resolve = davinci.Resolve(headless=True)
print(resolve._obj)
