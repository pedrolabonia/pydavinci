from pydavinci import davinci

resolve = davinci.Resolve(
    headless=True, path="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve"
)

print(resolve._obj)
print(resolve.version)
