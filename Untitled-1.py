
from picklehelpers import save, load
p = load("counter.pickle")
p["swimming.mp4"] = 0
save("counter.pickle", p)