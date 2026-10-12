const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.join(__dirname,'..'),E=require('../simulator.js');
const main=E.benchmark();
const scipy=[-1.019,-1.334,-1.395,-1.407,-1.409,-1.410];
main.windows.forEach((r,i)=>assert.ok(Math.abs(r.contrast_h-scipy[i])<.0006,'Python/browser window agreement'));
assert.ok(Math.abs(main.delta+1.329)<.0006);
const fine=E.benchmark({dt:1/240});
assert.ok(Math.abs(main.delta-fine.delta)*60<.01,'RK4 convergence');
const saved=E.lights.L1.DLS;
try{E.lights.L1.DLS=E.lights.L1.SLS;assert.ok(Math.abs(E.benchmark().delta)<1e-10,'Identical-light control');}finally{E.lights.L1.DLS=saved;}
for(const tau of [23.8,24.6])assert.ok(E.benchmark({tau}).delta<0);
assert.ok(Math.abs(E.benchmark({tau:24.6}).delta-(-1.142467905426063))<.00001,'Refined Python sensitivity agreement');
assert.ok(Math.abs(E.benchmark({location:'L2'}).delta+1.113)<.001);
for(const tau of [NaN,23,26])assert.throws(()=>E.simulate({tau}));
for(const days of [0,181,1.5])assert.throws(()=>E.simulate({days}));
for(const profile of ['static','dynamic','late']){
 const r=E.simulate({mode:'exploratory',profile,days:180});
 assert.ok(r.length>170);assert.ok(r.every(x=>Number.isFinite(x.clock_proxy_hours)));
}
// Exercise actual UI handlers with a minimal DOM; no browser rendering asserted.
const html=fs.readFileSync(path.join(root,'index.html'),'utf8'),nodes={};
for(const [,id]of html.matchAll(/id="([^"]+)"/g))nodes[id]={value:'',innerHTML:'',textContent:'',disabled:false,hidden:false,listeners:{},addEventListener(k,f){this.listeners[k]=f;},click(){this.listeners.click?.();}};
Object.assign(nodes.mode,{value:'hera'});Object.assign(nodes.period,{value:'24.2'});Object.assign(nodes.location,{value:'L1'});Object.assign(nodes.profile,{value:'dynamic'});Object.assign(nodes.days,{value:'45'});
const context={SpaceSleepEngine:E,document:{getElementById:id=>{assert.ok(nodes[id],`Missing UI element ${id}`);return nodes[id];},createElement:()=>({click(){}})},Blob,URL:{createObjectURL:()=>'',revokeObjectURL(){}},setTimeout:f=>f()};
vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'ui.js'),'utf8'),context);
assert.equal(nodes.dose.textContent,'1.33');assert.equal(nodes.phase.textContent,'7.9');assert.ok(nodes.phaseChart.innerHTML.includes('polyline'));assert.equal(nodes.export.disabled,false);
nodes.agentExplain.click();assert.ok(nodes.agentAnswer.textContent.includes('HERA'));
nodes.export.click();
nodes.location.value='L2';nodes.location.listeners.change();assert.equal(nodes.dose.textContent,'1.11');
nodes.mode.value='exploratory';nodes.mode.listeners.change();assert.equal(nodes.durationControl.hidden,false);assert.ok(nodes.legend.innerHTML.includes('Late bright'));
nodes.days.value='1';nodes.days.listeners.change();assert.ok(!nodes.phaseChart.innerHTML.includes('NaN'));
nodes.period.value='26';nodes.period.listeners.change();assert.ok(nodes.error.textContent);assert.equal(nodes.export.disabled,true);assert.equal(nodes.dose.textContent,'—');
console.log('PASS: SciPy agreement, numerical convergence, light control, sensitivity, long runs and UI handlers. Browser layout not checked.');
