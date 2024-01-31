import{r as A,I as ie,o as re,w as ce,a as q,b as D,p as O,i as F,c as v,d as z,e as V,g as ve,s as K,f as U,h as pe,j as fe,k as W,l as x,m as de,n as X,q as Y,t as G,u as me,v as ye,x as ge}from"./index-7227f80c.js";import{m as J,a as he,u as Q}from"./tag-749aa356.js";function xe(e){let r=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"content";const t=A(),s=A();if(ie){const a=new ResizeObserver(n=>{e==null||e(n,a),n.length&&(r==="content"?s.value=n[0].contentRect:s.value=n[0].target.getBoundingClientRect())});re(()=>{a.disconnect()}),ce(t,(n,u)=>{u&&(a.unobserve(q(u)),s.value=void 0),n&&a.observe(q(n))},{flush:"post"})}return{resizeRef:t,contentRect:D(s)}}const P=Symbol.for("vuetify:layout"),_e=Symbol.for("vuetify:layout-item"),Z=1e3,be=O({overlaps:{type:Array,default:()=>[]},fullHeight:Boolean},"layout");function Ie(){const e=F(P);if(!e)throw new Error("[Vuetify] Could not find injected layout");return{getLayoutItem:e.getLayoutItem,mainRect:e.mainRect,mainStyles:e.mainStyles}}const we=(e,r,t,s)=>{let a={top:0,left:0,right:0,bottom:0};const n=[{id:"",layer:{...a}}];for(const u of e){const d=r.get(u),y=t.get(u),g=s.get(u);if(!d||!y||!g)continue;const _={...a,[d.value]:parseInt(a[d.value],10)+(g.value?parseInt(y.value,10):0)};n.push({id:u,layer:_}),a=_}return n};function Re(e){const r=F(P,null),t=v(()=>r?r.rootZIndex.value-100:Z),s=A([]),a=z(new Map),n=z(new Map),u=z(new Map),d=z(new Map),y=z(new Map),{resizeRef:g,contentRect:_}=xe(),ee=v(()=>{const l=new Map,p=e.overlaps??[];for(const o of p.filter(c=>c.includes(":"))){const[c,i]=o.split(":");if(!s.value.includes(c)||!s.value.includes(i))continue;const m=a.get(c),h=a.get(i),R=n.get(c),S=n.get(i);!m||!h||!R||!S||(l.set(i,{position:m.value,amount:parseInt(R.value,10)}),l.set(c,{position:h.value,amount:-parseInt(S.value,10)}))}return l}),b=v(()=>{const l=[...new Set([...u.values()].map(o=>o.value))].sort((o,c)=>o-c),p=[];for(const o of l){const c=s.value.filter(i=>{var m;return((m=u.get(i))==null?void 0:m.value)===o});p.push(...c)}return we(p,a,n,d)}),T=v(()=>!Array.from(y.values()).some(l=>l.value)),I=v(()=>b.value[b.value.length-1].layer),te=v(()=>({"--v-layout-left":V(I.value.left),"--v-layout-right":V(I.value.right),"--v-layout-top":V(I.value.top),"--v-layout-bottom":V(I.value.bottom),...T.value?void 0:{transition:"none"}})),w=v(()=>b.value.slice(1).map((l,p)=>{let{id:o}=l;const{layer:c}=b.value[p],i=n.get(o),m=a.get(o);return{id:o,...c,size:Number(i.value),position:m.value}})),E=l=>w.value.find(p=>p.id===l),B=ve("createLayout"),k=K(!1);U(()=>{k.value=!0}),pe(P,{register:(l,p)=>{let{id:o,order:c,position:i,layoutSize:m,elementSize:h,active:R,disableTransitions:S,absolute:se}=p;u.set(o,c),a.set(o,i),n.set(o,m),d.set(o,R),S&&y.set(o,S);const H=fe(_e,B==null?void 0:B.vnode).indexOf(l);H>-1?s.value.splice(H,0,o):s.value.push(o);const N=v(()=>w.value.findIndex($=>$.id===o)),C=v(()=>t.value+b.value.length*2-N.value*2),ae=v(()=>{const $=i.value==="left"||i.value==="right",L=i.value==="right",ue=i.value==="bottom",j={[i.value]:0,zIndex:C.value,transform:`translate${$?"X":"Y"}(${(R.value?0:-110)*(L||ue?-1:1)}%)`,position:se.value||t.value!==Z?"absolute":"fixed",...T.value?void 0:{transition:"none"}};if(!k.value)return j;const f=w.value[N.value];if(!f)throw new Error(`[Vuetify] Could not find layout item "${o}"`);const M=ee.value.get(o);return M&&(f[M.position]+=M.amount),{...j,height:$?`calc(100% - ${f.top}px - ${f.bottom}px)`:h.value?`${h.value}px`:void 0,left:L?void 0:`${f.left}px`,right:L?`${f.right}px`:void 0,top:i.value!=="bottom"?`${f.top}px`:void 0,bottom:i.value!=="top"?`${f.bottom}px`:void 0,width:$?h.value?`${h.value}px`:void 0:`calc(100% - ${f.left}px - ${f.right}px)`}}),le=v(()=>({zIndex:C.value-1}));return{layoutItemStyles:ae,layoutItemScrimStyles:le,zIndex:C}},unregister:l=>{u.delete(l),a.delete(l),n.delete(l),d.delete(l),y.delete(l),s.value=s.value.filter(p=>p!==l)},mainRect:I,mainStyles:te,getLayoutItem:E,items:w,layoutRect:_,rootZIndex:t});const ne=v(()=>["v-layout",{"v-layout--full-height":e.fullHeight}]),oe=v(()=>({zIndex:r?t.value:void 0,position:r?"relative":void 0,overflow:r?"hidden":void 0}));return{layoutClasses:ne,layoutStyles:oe,getLayoutItem:E,items:w,layoutRect:_,layoutRef:g}}function Se(){const e=K(!1);return U(()=>{window.requestAnimationFrame(()=>{e.value=!0})}),{ssrBootStyles:v(()=>e.value?void 0:{transition:"none !important"}),isBooted:D(e)}}const $e=O({scrollable:Boolean,...J(),...he({tag:"main"})},"VMain"),ze=W()({name:"VMain",props:$e(),setup(e,r){let{slots:t}=r;const{mainStyles:s}=Ie(),{ssrBootStyles:a}=Se();return Q(()=>x(e.tag,{class:["v-main",{"v-main--scrollable":e.scrollable},e.class],style:[s.value,a.value,e.style]},{default:()=>{var n,u;return[e.scrollable?x("div",{class:"v-main__scroller"},[(n=t.default)==null?void 0:n.call(t)]):(u=t.default)==null?void 0:u.call(t)]}})),{}}}),Ve={__name:"View",setup(e){return(r,t)=>{const s=de("router-view");return X(),Y(ze,null,{default:G(()=>[x(s)]),_:1})}}};const Be=O({...J(),...be({fullHeight:!0}),...me()},"VApp"),Ce=W()({name:"VApp",props:Be(),setup(e,r){let{slots:t}=r;const s=ye(e),{layoutClasses:a,getLayoutItem:n,items:u,layoutRef:d}=Re(e),{rtlClasses:y}=ge();return Q(()=>{var g;return x("div",{ref:d,class:["v-application",s.themeClasses.value,a.value,y.value,e.class],style:[e.style]},[x("div",{class:"v-application__wrap"},[(g=t.default)==null?void 0:g.call(t)])])}),{getLayoutItem:n,items:u,theme:s}}}),Pe={__name:"Default",setup(e){return(r,t)=>(X(),Y(Ce,null,{default:G(()=>[x(Ve)]),_:1}))}};export{Pe as default};
