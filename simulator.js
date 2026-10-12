(function(root){
  'use strict';
  const sampleDays=[5,12,19,26,33,43], observedDelta=-1.46;
  const lights={L1:{SLS:[122,122],DLS:[264,13]},L2:{SLS:[143,143],DLS:[80,4]}};
  const wrap=h=>((h+12)%24+24)%24-12;
  function rhs(y,tau,I){
    const [x,xc,n]=y,alpha=I>0?.05*Math.sqrt(I/9500):0;
    const B=33.75*(1-n)*alpha*(1-.4*x)*(1-.4*xc);
    return [Math.PI/12*(xc+B),Math.PI/12*(.23*(xc-4*xc**3/3)-x*((24/(.99669*tau))**2+.55*B)),60*(alpha*(1-n)-.0075*n)];
  }
  function rk4(y,tau,I,dt){
    const a=rhs(y,tau,I),b=rhs(y.map((v,i)=>v+a[i]*dt/2),tau,I);
    const c=rhs(y.map((v,i)=>v+b[i]*dt/2),tau,I),d=rhs(y.map((v,i)=>v+c[i]*dt),tau,I);
    return y.map((v,i)=>v+dt*(a[i]+2*b[i]+2*c[i]+d[i])/6);
  }
  function simulate({tau=24.2,days=45,mode='hera',condition='SLS',location='L1',profile='dynamic',offset=0,dt=1/120}={}){
    if(!Number.isFinite(tau)||tau<23.5||tau>25)throw Error('Intrinsic period must be 23.5–25 hours.');
    if(!Number.isInteger(days)||days<1||days>180)throw Error('Duration must be 1–180 days.');
    if(!['hera','exploratory'].includes(mode)||!lights[location]||!['SLS','DLS'].includes(condition)||!['static','dynamic','late'].includes(profile))throw Error('Unknown scenario.');
    if(!Number.isFinite(dt)||dt<=0||dt>1/60)throw Error('Integrator step must be positive and at most one minute.');
    let state=[1,0,.5], times=[], values=[];
    function segment(start,end,I,record){
      const steps=Math.ceil((end-start)/dt),step=(end-start)/steps;
      for(let k=0;k<steps;k++){
        if(record){times.push(start+k*step);values.push(state[0]);}
        state=rk4(state,tau,I,step);
      }
    }
    for(let day=-21;day<0;day++){segment(day*24,day*24+16,150,false);segment(day*24+16,(day+1)*24,0,false);}
    for(let day=0;day<days;day++){
      let segments;
      if(mode==='hera'){
        const awake=(day+offset)%7<2?16:19,[bright,dim]=lights[location][condition];
        segments=[[0,awake-3,bright],[awake-3,awake,dim],[awake,24,0]];
      }else segments=profile==='static'?[[0,16,210],[16,24,0]]:profile==='late'?[[0,10,210],[10,16,420],[16,24,0]]:[[0,10,420],[10,13,210],[13,16,90],[16,24,0]];
      for(const [start,end,I] of segments)segment(day*24+start,day*24+end,I,true);
    }
    const minima=[];
    for(let i=1;i<values.length-1;i++)if(values[i]<values[i-1]&&values[i]<=values[i+1]){
      const [a,b,c]=values.slice(i-1,i+2),shift=.5*(a-c)/(a-2*b+c);
      const time=times[i]+Math.max(-1,Math.min(1,shift))*(times[i+1]-times[i]);
      minima.push({day:Math.floor(time/24)+1,time_hours:time,clock_proxy_hours:(time+7)%24});
    }
    if(!state.every(Number.isFinite))throw Error('Non-finite oscillator state.');
    return minima;
  }
  function circularMean(arr){
    if(!arr.length)return null;
    const a=arr.reduce((s,v)=>s+Math.sin(v*Math.PI/12),0),b=arr.reduce((s,v)=>s+Math.cos(v*Math.PI/12),0);
    return (Math.atan2(a,b)*12/Math.PI+24)%24;
  }
  function benchmark(options={}){
    const sls=simulate({...options,mode:'hera',condition:'SLS',days:45});
    const dls=simulate({...options,mode:'hera',condition:'DLS',days:45});
    const windows=sampleDays.map(day=>{
      const select=a=>a.filter(r=>r.time_hours>=(day-1)*24&&r.time_hours<(day+1)*24).map(r=>r.clock_proxy_hours);
      const s=circularMean(select(sls)),d=circularMean(select(dls));
      if(s===null||d===null)throw Error('Missing phase minimum in collection window.');
      return {day,SLS_proxy_h:s,DLS_proxy_h:d,contrast_h:wrap(d-s)};
    });
    const delta=windows.reduce((a,r)=>a+r.contrast_h,0)/windows.length;
    return {windows,sls,dls,delta,observedDelta,discrepancyMinutes:Math.abs(delta-observedDelta)*60};
  }
  const api={rhs,simulate,benchmark,wrap,lights,sampleDays,observedDelta};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.SpaceSleepEngine=api;
})(typeof window!=='undefined'?window:globalThis);
