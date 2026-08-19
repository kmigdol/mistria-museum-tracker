import json,re,collections
AREAS=["Farm","Sweetwater Farm","Mistria","The Narrows","Eastern Road","Western Ruins","The Beach","Deep Woods"]
WATER=["Ocean","River","Pond"]
MINES=["Upper Mines","Tide Caverns","Deep Earth","Lava Caves","Ancient Ruins"]
HOME=["Apiary/Terrarium"]
ALL=AREAS+WATER+MINES+HOME

def tags(loc):
    L=" "+loc.lower()+" "
    t=set()
    # home production
    if "apiary" in L or "terrarium" in L: t|=set(HOME)
    # mines layers
    layer=False
    for k,v in [("upper mines","Upper Mines"),("tide caverns","Tide Caverns"),("deep earth","Deep Earth"),
                ("lava caves","Lava Caves"),("ancient ruins","Ancient Ruins")]:
        if k in L: t.add(v); layer=True
    if not layer and ("the mines" in L or "any floor without a seal" in L or "ritual chambers" in L):
        t|=set(MINES)
    # water
    if re.search(r"any (fishable|divable) water|any water|fish trap \(any water\)", L): t|=set(WATER)
    else:
        if "ocean" in L: t.add("Ocean")
        if "river" in L: t.add("River")
        if "pond" in L: t.add("Pond")
    # overworld-wide
    wide = ("overworld" in L or "no set spawn area" in L or "dig spots (any area)" in L
            or "mist spots (any area)" in L)
    if wide: t|=set(AREAS)
    else:
        rest=L
        if "sweetwater farm" in rest: t.add("Sweetwater Farm"); rest=rest.replace("sweetwater farm"," ")
        if "manor" in rest or "mistria" in rest: t.add("Mistria")
        if re.search(r"\bfarm\b", rest): t.add("Farm")
        if "narrows" in rest: t.add("The Narrows")
        if "eastern road" in rest: t.add("Eastern Road")
        if "western ruins" in rest: t.add("Western Ruins")
        if "beach" in rest: t.add("The Beach")
        if "deep woods" in rest: t.add("Deep Woods")
    return [x for x in ALL if x in t]

if __name__=="__main__":
    c=collections.Counter(); none=[]
    for f in ['fish','insects','flora','archaeology']:
        d=json.load(open(f'/tmp/mistria/{f}.json'))
        for s in d['sets']:
            for it in s['items']:
                tg=tags(it['location'])
                if not tg: none.append((it['name'],it['location']))
                for x in tg: c[x]+=1
    for k in ALL: print(f"{k:18} {c[k]}")
    print("untagged:",none)
