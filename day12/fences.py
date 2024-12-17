#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass(eq=True,frozen=True)
class Fence:
    x: int
    y: int
    kind: bytes

def nearby(fence: Fence, region: set) -> bool:
    near = False
    for cell in region:
        xdist = abs(cell.x-fence.x)
        ydist = abs(cell.y-fence.y)
        print(f"distance {xdist} {ydist}")
        if (xdist + ydist) <= 1:
            near = True
            break
    return near


def main():
    with open("example3", "r") as reader:
        fencemap = []
        fencekind = set()
        y = 0
        line = reader.readline()
        while line != "":  # The EOF char is an empty string
            line = line.rstrip()
            xlimit = len(line)
#            fencemap.append([c for c in line])
            fencemap.extend([Fence (x,y,f) for x, f in enumerate(line)])

            fencekind |= {c for c in line}
            line = reader.readline()
            y += 1
    ylimit = y
    #print(fencemap)
    #print(list(filter(lambda x: x.kind == 'A', fencemap)))
    regions = dict()
    for k in fencekind:
        regions[k] = []
        for f in filter(lambda x: x.kind == k, fencemap):
            if len(regions[k]) == 0:
                print(f"new region (first) {f.x} {f.y} {f.kind}")
                regions[k].append({f})
            else:
                found = False
                for region in regions[k]:
                    print(f"fence: {f} region: {region}")
                    if nearby(f,region):
                        print("Add to region")
                        found = True
                        region |= {f}
                if not found:
                    print(f"new region (seen) {f.x} {f.y} {f.kind}")
                    regions[k].append({f})
    for k,v in regions.items():
        print(k,len(v))



if __name__ == "__main__":
    main()
