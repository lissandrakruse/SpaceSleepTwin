'use strict';
const $=id=>document.getElementById(id), E=SpaceSleepEngine;
let exportRows=[], currentResult=null;
const benchmarkCache=new Map();
function cachedBenchmark(options){
  const key=String(options.tau)+'/'+options.location;
  if(!benchmarkCache.has(key))benchmarkCache.set(key,E.benchmark(options));
  return benchmarkCache.get(key);
}
const fmt=(n,d=2)=>Number(n).toFixed(d);
function downloadCSV(filename,headers,rows){
  const csv=headers.join(',')+'\n'+rows.map(row=>headers.map(h=>row[h]??'').join(',')).join('\n');
  const a=document.createElement('a'),url=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
  a.href=url;a.download=filename;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function chart(id,series,{ylabel='Hours',reference=null}={}){
  const svg=$(id),W=900,H=290,L=72,R=865,T=26,B=235;
  const xs=series.flatMap(s=>s.points.map(p=>p[0])),ys=series.flatMap(s=>s.points.map(p=>p[1]));
  if(reference!==null)ys.push(reference);
  if(!xs.length){svg.innerHTML='<text x="450" y="140" text-anchor="middle" fill="#aec9d9">No phase minimum available for this duration.</text>';return;}
  let lo=Math.min(0,...ys),hi=Math.max(0,...ys),range=Math.max(.5,hi-lo);lo-=range*.16;hi+=range*.16;
  const xmax=Math.max(1,...xs),x=v=>L+v/xmax*(R-L),y=v=>B-(v-lo)/(hi-lo)*(B-T);
  let parts=[];
  for(let k=0;k<=4;k++){
    const v=lo+(hi-lo)*k/4;
    parts.push(`<line x1="${L}" x2="${R}" y1="${y(v)}" y2="${y(v)}" stroke="#24445b"/><text x="60" y="${y(v)+4}" text-anchor="end" fill="#aec9d9" font-size="12">${fmt(v)}</text>`);
  }
  for(let i=0;i<=5;i++)parts.push(`<text x="${x(xmax*i/5)}" y="256" fill="#aec9d9" text-anchor="middle" font-size="12">${fmt(xmax*i/5,0)}</text>`);
  if(reference!==null)parts.push(`<line x1="${L}" x2="${R}" y1="${y(reference)}" y2="${y(reference)}" stroke="#f8c27a" stroke-dasharray="7 5" stroke-width="2"/>`);
  for(const s of series){
    parts.push(`<polyline points="${s.points.map(p=>fmt(x(p[0]))+','+fmt(y(p[1]))).join(' ')}" fill="none" stroke="${s.color}" stroke-width="3"/>`);
    parts.push(...s.points.map(p=>`<circle cx="${x(p[0])}" cy="${y(p[1])}" r="4" fill="${s.color}"/>`));
  }
  parts.push(`<text x="450" y="282" fill="#aec9d9" font-size="12" text-anchor="middle">Mission day · ${ylabel}</text>`);
  svg.innerHTML=parts.join('');
}
function lightingChart(mode,location,profile){
  const x=h=>62+h/24*803,y=v=>210-v/500*178;
  const patterns=mode==='hera'?[
    {name:'SLS',color:'#91a8ba',data:[[0,16,E.lights[location].SLS[0]],[16,19,E.lights[location].SLS[1]],[19,24,0]]},
    {name:'DLS',color:'#5ce9ee',data:[[0,16,E.lights[location].DLS[0]],[16,19,E.lights[location].DLS[1]],[19,24,0]]}
  ]:[{name:profile,color:'#5ce9ee',data:profile==='static'?[[0,16,210],[16,24,0]]:profile==='late'?[[0,10,210],[10,16,420],[16,24,0]]:[[0,10,420],[10,13,210],[13,16,90],[16,24,0]]}];
  let parts=[];
  for(const lux of [0,250,500])parts.push(`<line x1="62" x2="865" y1="${y(lux)}" y2="${y(lux)}" stroke="#24445b"/><text x="10" y="${y(lux)+4}" fill="#aec9d9" font-size="12">${lux}</text>`);
  for(const p of patterns)parts.push(`<polyline points="${p.data.flatMap(([a,b,lux])=>[[x(a),y(lux)],[x(b),y(lux)]]).map(a=>a.join(',')).join(' ')}" stroke="${p.color}" stroke-width="3" fill="none"/>`);
  for(let h=0;h<=24;h+=4)parts.push(`<text x="${x(h)}" y="236" fill="#aec9d9" text-anchor="middle" font-size="12">${h===24?'07:00':String((h+7)%24).padStart(2,'0')+':00'}</text>`);
  parts.push('<text x="450" y="268" fill="#aec9d9" text-anchor="middle" font-size="12">Clock time · photopic lux at assumed eye level</text>');
  $('lightChart').innerHTML=parts.join('');
}
function draw(){
  const mode=$('mode').value,hera=mode==='hera',tau=Number($('period').value),location=$('location').value,profile=$('profile').value;
  $('durationControl').hidden=hera;$('profileControl').hidden=hera;$('locationControl').hidden=!hera;
  $('daysValue').textContent=$('days').value+' days';
  $('export').disabled=true;exportRows=[];currentResult=null;
  try{
    if(hera){
      const r=cachedBenchmark({tau,location});currentResult={...r,mode,tau,location};
      exportRows=r.windows.map(w=>({...w,scenario:'hera',tau_hours:tau,location,observed_aggregate_contrast_h:E.observedDelta}));
      $('duration').textContent='45';$('dose').textContent=fmt(-r.delta);$('phase').textContent=fmt(r.discrepancyMinutes,1);
      $('metric2Label').textContent='SIMULATED ADVANCE (H)';$('metric3Label').textContent='AGGREGATE DISCREPANCY (MIN)';
      $('phaseHeading').textContent='HERA: dynamic minus standard lighting';
      chart('phaseChart',[{color:'#5ce9ee',points:r.windows.map(w=>[w.day,w.contrast_h])}],{ylabel:'DLS − SLS (hours)',reference:E.observedDelta});
      $('legend').innerHTML='<span class="cyan">● Model phase proxy</span><span class="amber">┄ Published aggregate −1.46 h</span>';
      $('chartStatus').textContent=`${location} · τ = ${fmt(tau)} h · average contrast ${fmt(r.delta,3)} h across six 48-hour windows. Negative = earlier phase under DLS.`;
      $('phaseNote').textContent='The model extracts x minima. HERA measured urinary aMT6s acrophase. The dashed line is one published aggregate contrast, not an observed time series. Agreement is exploratory; it is not individual prediction accuracy.';
      $('resultTable').innerHTML='<thead><tr><th>Window start day</th><th>SLS proxy (h)</th><th>DLS proxy (h)</th><th>Difference (h)</th></tr></thead><tbody>'+r.windows.map(w=>`<tr><td>${w.day}</td><td>${fmt(w.SLS_proxy_h,3)}</td><td>${fmt(w.DLS_proxy_h,3)}</td><td>${fmt(w.contrast_h,3)}</td></tr>`).join('')+'</tbody>';
      $('tableCaption').textContent='Simulated clock hours are phase proxies, not predictions of melatonin peak time.';
      $('lightNote').textContent='Representative short-sleep day (02:00–07:00). DLS dims at 23:00. Two long-sleep nights per week are 23:00–07:00 and dim at 20:00. Sleep is modeled as zero eye exposure.';
      const adjustedContrast=-.91;
      $('baselineComparison').textContent=`The groups differed before the mission: SLS 4.24 h, DLS 3.69 h. Their descriptive mean changes are +1.98 and +1.07 h, a change contrast of −0.91 h. Against that alternative descriptive quantity, this simulation differs by ${fmt(Math.abs(r.delta-adjustedContrast)*60,1)} min. This is not a paired reanalysis or a causal estimate.`;
      $('sensitivityPanel').hidden=false;
      const scenarios=[{label:'Shorter intrinsic period',tau:23.8,location:'L1'},{label:'Default reconstruction',tau:24.2,location:'L1'},{label:'Longer intrinsic period',tau:24.6,location:'L1'},{label:'Alternative habitat level',tau:24.2,location:'L2'}];
      $('sensitivityTable').innerHTML='<thead><tr><th>Fixed scenario</th><th>τ (h)</th><th>Level</th><th>DLS − SLS (h)</th></tr></thead><tbody>'+scenarios.map(s=>{const delta=cachedBenchmark(s).delta;return `<tr><td>${s.label}</td><td>${fmt(s.tau,1)}</td><td>${s.location}</td><td>${fmt(delta,3)}</td></tr>`;}).join('')+'</tbody>';
    }else{
      const days=Number($('days').value),colors={static:'#91a8ba',dynamic:'#5ce9ee',late:'#f8c27a'},names={static:'Static',dynamic:'Dynamic',late:'Late bright'};
      const trajectories=Object.keys(colors).map(p=>{
        const a=E.simulate({tau,days,mode,profile:p});let phase=0;
        const points=a.map((r,i)=>{if(i)phase+=E.wrap(r.clock_proxy_hours-a[i-1].clock_proxy_hours);const entry={scenario:p,day:r.day,phase_change_h:phase,clock_proxy_h:r.clock_proxy_hours,tau_hours:tau};exportRows.push(entry);return [r.day,phase];});
        return {name:p,color:colors[p],points};
      });
      const selected=trajectories.find(s=>s.name===profile),last=selected.points.at(-1);
      currentResult={mode,tau,days,profile,last:last?.[1]??null};
      $('duration').textContent=days;$('dose').textContent=String(profile==='static'?3360:profile==='late'?4620:5100);$('phase').textContent=last?fmt(last[1]):'—';
      $('metric2Label').textContent='PHOTOPIC LUX·H / DAY';$('metric3Label').textContent='SELECTED PHASE CHANGE (H)';
      $('phaseHeading').textContent='Forger99: compare illustrative lighting schedules';
      chart('phaseChart',trajectories,{ylabel:'Phase change from first x minimum (hours)'});
      $('legend').innerHTML=Object.keys(colors).map(p=>`<span style="color:${colors[p]}">● ${names[p]}</span>`).join('');
      $('chartStatus').textContent=`${days} days · τ = ${fmt(tau)} h · ${names[profile]} selected. All three curves start from the same oscillator state.`;
      $('phaseNote').textContent='Each curve is relative to its first x minimum. Phase is a model proxy; light schedules are illustrative. Positive = later phase. No predicted latency or sleep benefit is inferred.';
      $('resultTable').innerHTML='<thead><tr><th>Schedule</th><th>Final phase change (h)</th></tr></thead><tbody>'+trajectories.map(s=>`<tr><td>${names[s.name]}</td><td>${s.points.length?fmt(s.points.at(-1)[1],3):'Unavailable'}</td></tr>`).join('')+'</tbody>';
      $('tableCaption').textContent='Relative model phase; not measured human sleep.';
      $('lightNote').textContent='Illustrative day: 07:00 wake, 23:00 lights off. These values are not NASA lighting prescriptions.';
      $('sensitivityPanel').hidden=true;
    }
    lightingChart(mode,location,profile);$('export').disabled=false;
    $('error').textContent='';
  }catch(error){$('error').textContent=error.message;$('chartStatus').textContent='Simulation unavailable: correct the parameters and run again.';for(const id of ['duration','dose','phase'])$(id).textContent='—';$('phaseChart').innerHTML='';$('resultTable').innerHTML='';$('legend').innerHTML='';}
}
for(const id of ['mode','location','profile','period'])$(id).addEventListener('change',draw);
$('days').addEventListener('input',()=>{$('daysValue').textContent=$('days').value+' days';});
$('days').addEventListener('change',draw);$('run').addEventListener('click',draw);
$('export').addEventListener('click',()=>{if(exportRows.length)downloadCSV('spacesleeptwin_'+currentResult.mode+'.csv',Object.keys(exportRows[0]),exportRows);});
function say(text){$('agentAnswer').textContent=text;}
$('agentExplain').addEventListener('click',()=>{if(!currentResult){say('Run a valid simulation first.');return;}const r=currentResult;say(r.mode==='hera'?`HERA reconstruction: ${r.location}, τ = ${fmt(r.tau)} h. Simulated DLS−SLS contrast ${fmt(r.delta)} h; published aggregate −1.46 h. The ${fmt(r.discrepancyMinutes,1)} min discrepancy compares different phase markers. It does not establish accuracy for an individual astronaut.`:`Illustrative ${r.profile} schedule, ${r.days} days. Phase change ${r.last===null?'unavailable':fmt(r.last)+' h'}. This is a mechanistic oscillator scenario, not a sleep outcome prediction.`);});
$('agentCompare').addEventListener('click',()=>say('Use HERA mode to compare standard and dynamic conditions with matched initial phase. Change τ or habitat level to inspect sensitivity. Use illustrative mode for all three schedules. Exported CSV values are simulated; the published HERA result is an aggregate benchmark.'));
$('agentLimits').addEventListener('click',()=>say('Forger99 is implemented in the browser using photopic lux. Individual exposure, spectral response, premission histories and a validated link from x minima to urinary aMT6s are missing. A common premission routine and darkness during sleep are assumed. This exploratory benchmark does not validate the full twin or an intervention in space.'));
draw();
