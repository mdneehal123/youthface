(function(){
  'use strict';
  var $=function(id){return document.getElementById(id);};
  var form=$('ro-form'),keyIn=$('ro-key'),out=$('ro-out'),btn=$('ro-go'),range=$('ro-range');
  function el(t,c,x){var e=document.createElement(t);if(c){e.className=c;}if(x!=null){e.textContent=x;}return e;}
  function rs(n){return '₹'+Number(n).toLocaleString('en-IN');}
  function sent(){try{return JSON.parse(localStorage.getItem('yf-reminded')||'{}');}catch(e){return {};}}
  function mark(id){var s=sent();s[id]=Date.now();try{localStorage.setItem('yf-reminded',JSON.stringify(s));}catch(e){}}
  try{var k=localStorage.getItem('yf-admin');if(k){keyIn.value=k;}}catch(e){}
  function msgLeft(c){return 'Hello '+(c.name||'')+', this is Youth Face. You started an order for '+(c.items||'Youth Face Beauty Cream')+' on our website, but the payment did not go through. Can I help? Your cart is still saved, so you can finish here: https://youthfacebeautycream.com/checkout/ or just reply and I will place it for you. Reply STOP if you would rather not hear from us.';}
  function msgAgain(c,asked){return 'Hello '+(c.name||'')+', this is Youth Face. '+(asked?'You asked us to remind you when your cream is about to run out, so here we are! ':'Thank you for your order. ')+'Your jar may be running low by now, and regular use matters for results. You can reorder here: https://youthfacebeautycream.com/shop/ (Pack of 2 is Rs 999, Pack of 3 is Rs 1,444). Reply STOP if you would rather not get reminders.';}
  function wa(c,text,row){var done=sent()[c.id];var a=el('a','btn sm'+(done?' ghost':''),done?'Sent':text[0]);
    a.href='https://wa.me/91'+c.phone+'?text='+encodeURIComponent(text[1]);a.target='_blank';a.rel='noopener';
    a.addEventListener('click',function(){mark(c.id);row.classList.add('is-sent');a.textContent='Sent';});return a;}
  function msgBox(text,cls){out.textContent='';out.hidden=false;out.appendChild(el('p',cls||'muted',text));}

  function renderOrders(d){
    out.textContent='';out.hidden=false;var t=d.totals,list=d.orders||[];
    out.appendChild(el('p','byline',d.days===1?'Paid orders today':'Paid orders in the last 7 days'));
    var tiles=el('div','ro-tiles');
    [['Orders',t.count],['Prepaid',t.prepaid],['Cash on Delivery',t.cod],['Money received',rs(t.received)],['Cash to collect',rs(t.to_collect)]].forEach(function(x){var b=el('div');b.appendChild(el('b',null,String(x[1])));b.appendChild(el('span',null,x[0]));tiles.appendChild(b);});
    out.appendChild(tiles);
    if(!list.length){out.appendChild(el('p','muted',d.days===1?'No paid orders yet today.':'No paid orders in the last 7 days.'));return;}
    list.forEach(function(o){var row=el('div','ro-row'),info=el('div');
      info.appendChild(el('b',null,o.name||'Customer'));info.appendChild(el('span',null,o.items));
      info.appendChild(el('span',null,o.cod?'Cash on Delivery: '+rs(o.paid)+' paid, '+rs(o.collect)+' to collect':'Prepaid: '+rs(o.paid)));
      info.appendChild(el('span',null,[o.city,o.pincode,o.when].filter(Boolean).join(' · ')));info.appendChild(el('span',null,'+91 '+o.phone));
      var a=el('a','btn sm ghost','Track');a.href='/track-order/?id='+encodeURIComponent(o.id);a.target='_blank';a.rel='noopener';
      row.appendChild(info);row.appendChild(a);out.appendChild(row);});
  }
  function renderPeople(d){
    out.textContent='';out.hidden=false;var list=d.customers||[],left=d.kind==='abandoned',done=sent();
    var refill=d.kind==='refill';out.appendChild(el('p','byline',left?list.length+' customer'+(list.length===1?'':'s')+' started an order in the last 3 days and did not pay.':refill?list.length+' customer'+(list.length===1?'':'s')+' asked for a refill reminder and should be running low now.':list.length+' customer'+(list.length===1?'':'s')+' ordered '+d.from+' to '+d.to+' days ago.'));
    if(!list.length){out.appendChild(el('p','muted',left?'Nobody has left an unpaid order in the last 3 days.':refill?'No refill reminders are due today. Check again tomorrow.':'Nobody in this range yet. Check again in a few days.'));return;}
    list.forEach(function(c){var row=el('div','ro-row'+(done[c.id]?' is-sent':'')),info=el('div');
      info.appendChild(el('b',null,c.name||'Customer'));info.appendChild(el('span',null,c.items));
      info.appendChild(el('span',null,[(c.cod?'Cash on Delivery, ':'')+rs(c.amount),c.city,left?(c.hours<1?'under an hour ago':c.hours+' hours ago'):c.days+' days ago'].filter(Boolean).join(' · ')));
      info.appendChild(el('span',null,'+91 '+c.phone));if(c.remind){info.appendChild(el('span','tagok','Asked for a reminder'));}
      row.appendChild(info);row.appendChild(wa(c,left?['Message on WhatsApp',msgLeft(c)]:['Send reminder',msgAgain(c,refill)],row));out.appendChild(row);});
  }
  form.addEventListener('submit',function(e){
    e.preventDefault();var key=keyIn.value.trim(),v=range.value,r=v.split('-');
    if(!key){msgBox('Enter the admin key.','oerr');return;}
    var url=v==='today'?'kind=orders&days=1':v==='week'?'kind=orders&days=7':v==='left'?'kind=abandoned':v==='refill'?'kind=refill':'from='+r[0]+'&to='+r[1];
    btn.disabled=true;btn.textContent='Loading…';
    fetch('/api/reorder?'+url,{headers:{'x-admin-key':key}}).then(function(x){return x.json().then(function(j){return {ok:x.ok,j:j};});})
    .then(function(x){
      if(x.ok){try{localStorage.setItem('yf-admin',key);}catch(e){}if(x.j.kind==='orders'){renderOrders(x.j);}else{renderPeople(x.j);}}
      else{msgBox(x.j.error==='wrong_key'?'That key is not correct.':x.j.error==='admin_key_not_set'?'The admin key has not been set in Vercel yet (ADMIN_KEY).':x.j.error==='not_configured'?'Razorpay keys are not set in Vercel yet.':'Could not load the list. Please try again.','oerr');}
    }).catch(function(){msgBox('Could not load the list. Check your connection.','oerr');})
    .then(function(){btn.disabled=false;btn.textContent='Show';});
  });
})();
