import json,re,sys
sys.path.insert(0,'.')
from tag import tags
t=open('template.html').read()
data=[json.load(open(f'../data/{f}.json')) for f in ['fish','insects','flora','archaeology']]
ORDER=["Any","Sunny","Rain","Storm","Windy","Snow"]
for w in data:
    for s in w['sets']:
        for it in s['items']:
            it.setdefault('weather',['Any']); it.setdefault('time','Any')
            for k in ('location','method','notes'): it.setdefault(k,'')
            if not it['weather']: it['weather']=['Any']
            it['seasons']=[x for x in ["Spring","Summer","Fall","Winter"] if x in it['seasons']] or ["Spring","Summer","Fall","Winter"]
            it['weather']=[{'Rainy':'Rain','Blizzard':'Snow','Thunderstorm':'Storm','All':'Any'}.get(x,x) for x in it['weather']]
            it['weather']=sorted(set(it['weather']), key=lambda x: ORDER.index(x) if x in ORDER else 9)
            it['notes']='; '.join(p.strip() for p in it['notes'].split(';') if p.strip() and not re.match(r'(?i)^wiki weather',p.strip()))
            it['tags']=tags(it['location'])
# in-game set order (Insects order supplied by the player)
ORDER_BY_WING={
 "Insects":["Multi-Season","Spring","Summer","Fall","Winter","Rare","Bee",
   "Honey","Bug Pheromone","Terrarium","Grass","Beach","Deep Woods",
   "Upper Mines","Tide Caverns","Deep Earth","Lava Caves","Ruins","Legendary"],
}
for w in data:
    order=ORDER_BY_WING.get(w['wing'])
    if order:
        idx={n:i for i,n in enumerate(order)}
        missing=[s['set'] for s in w['sets'] if s['set'] not in idx]
        assert not missing, ('unordered sets',w['wing'],missing)
        w['sets'].sort(key=lambda s: idx[s['set']])

SIZES=json.load(open('fishsizes.json'))
for w in data:
    if w['wing']!='Fish': continue
    for s in w['sets']:
        for it in s['items']:
            if SIZES.get(it['name']): it['size']=SIZES[it['name']]

icons=json.load(open('icons.json'))
out=t.replace('__DATA__', json.dumps(data,ensure_ascii=False)).replace('__ICONS__', json.dumps(icons))
open('mistria-museum-tracker.html','w').write(out)
print(round(len(out)/1024),'KB')
