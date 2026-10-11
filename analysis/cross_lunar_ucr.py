"""Exploratory NASA/JPL lunar join to UCR sleep diaries, fixed local evening."""
import csv, hashlib, io, json, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import pyreadr

PIN='ed90d9ac91b9fa81c0869dafbe6efb3c8d9faed3'
SITE=(-84.0509,9.9372,0) # source campus coordinates; elevation unspecified, assume 0 km
TZ=ZoneInfo('America/Costa_Rica')

def run(input_path, out):
    out.mkdir(parents=True,exist_ok=True)
    diary=next(iter(pyreadr.read_r(str(input_path)).values()))
    prepared=[]
    for _,r in diary.iterrows():
        bed=r.bedtime.to_pydatetime().replace(tzinfo=timezone.utc).astimezone(TZ)
        evening=bed.date()-timedelta(days=1) if bed.hour<12 else bed.date()
        prepared.append(dict(participant_id=r.Id,evening_date=str(evening),bedtime_local=bed.isoformat(),sleepdelay_minutes=float(r.sleepdelay),sleep_duration_hours=float(r.sleep_duration),daytype=str(r.daytype2)))
    keys=[(r['participant_id'],r['evening_date']) for r in prepared]
    if len(keys)!=len(set(keys)): raise ValueError('Ambiguous participant/evening duplicates')
    dates=[datetime.fromisoformat(r['evening_date']).date() for r in prepared]
    start=datetime.combine(min(dates),datetime.min.time()).replace(hour=18,tzinfo=TZ).astimezone(timezone.utc)
    stop=datetime.combine(max(dates)+timedelta(days=1),datetime.min.time()).replace(tzinfo=TZ).astimezone(timezone.utc)
    params={'format':'json','COMMAND':"'301'",'EPHEM_TYPE':"'OBSERVER'",'CENTER':"'coord@399'",'COORD_TYPE':"'GEODETIC'",'SITE_COORD':"'-84.0509,9.9372,0'",'START_TIME':"'"+start.strftime('%Y-%m-%d %H:%M')+"'",'STOP_TIME':"'"+stop.strftime('%Y-%m-%d %H:%M')+"'",'STEP_SIZE':"'1 h'",'QUANTITIES':"'4,10,24'",'CSV_FORMAT':"'YES'",'APPARENT':"'AIRLESS'"}
    cache=out/'horizons_response.json'
    if not cache.exists():
        url='https://ssd.jpl.nasa.gov/api/horizons.api?'+urllib.parse.urlencode(params)
        cache.write_bytes(urllib.request.urlopen(url,timeout=55).read())
    data=json.loads(cache.read_text())
    if data.get('error'): raise ValueError(data['error'])
    result=data['result']; block=result.split('$$SOE')[1].split('$$EOE')[0]
    moon={}
    for cells in csv.reader(io.StringIO(block)):
        if not cells or not cells[0].strip(): continue
        utc=datetime.strptime(cells[0].strip(),'%Y-%b-%d %H:%M').replace(tzinfo=timezone.utc)
        local=utc.astimezone(TZ)
        if 18<=local.hour<24:
            # JPL CSV: datetime, solar marker, lunar marker, azimuth, elevation, illumination%, phase angle
            moon.setdefault(str(local.date()),[]).append((float(cells[4]),float(cells[5]),float(cells[6])))
    for r in prepared:
        samples=moon[r['evening_date']]
        if len(samples)!=6: raise ValueError('Incomplete evening ephemeris')
        r.update(lunar_illuminated_percent_at_18h=samples[0][1],lunar_phase_angle_deg_at_18h=samples[0][2],moon_above_horizon_hour_samples=sum(e>0 for e,_,_ in samples),site_proxy='UCR_campus')
    with (out/'joined_diaries.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(prepared[0]));w.writeheader();w.writerows(prepared)
    audit={'input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),'source_commit':PIN,'rows':len(prepared),'participants':len({r['participant_id'] for r in prepared}),'evenings':len(set(r['evening_date'] for r in prepared)),'first_evening':str(min(dates)),'last_evening':str(max(dates)),'horizons_signature':data.get('signature'),'horizons_response_sha256':hashlib.sha256(cache.read_bytes()).hexdigest(),'parameters':params,'timezone':'America/Costa_Rica','timezone_check':'UCR_S001 raw diary 2025-06-16 21:20 local matches RData 2025-06-17 03:20 UTC; metadata gives Costa Rica timezone.','site_coordinates_source':'data/Metadata_Melidos_UCR.xlsx, study geographical location: 9.9372 N, 84.0509 W','limitations':['Campus location is a city-level proxy, not individual residence or night location. Site elevation assumed 0 km.','Six hourly geometric moon elevations at 18:00–23:00 local; count is not exact visible duration or first six hours after dusk.','No clouds, buildings, indoor exposure, or actual moonlight lux measured. Illuminated percent is lunar disk fraction, not personal illuminance.','Sleep diary duration in hours and delay in minutes; distinct outcomes from Blume laboratory latency.','Light-glasses subset (6 people) has not been merged; analysis cannot control actual personal light exposure.','Astronomical covariates are calculated NASA ephemerides; sleep observations are UCR terrestrial data, not NASA astronaut data.']}
    (out/'join_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    return audit

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--input',type=Path,required=True); p.add_argument('--output',type=Path,default=Path('analysis/lunar_ucr')); a=p.parse_args()
    print(json.dumps(run(a.input,a.output),indent=2))
