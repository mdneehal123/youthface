(function(){
  'use strict';
  var WA='919980881230', ADVANCE=99, KEY='yf-cart', DETAILS='yf-details', ORDERS='yf-orders', PENDING='yf-pending', NUDGE='yf-nudge';
  var COMBO_MSG='Combo price applied: Cream + Lotion for ₹999';
  var P=null, $=function(id){return document.getElementById(id);};
  function rs(n){return '₹'+Number(n).toLocaleString('en-IN');}
  function el(tag,cls,text){var e=document.createElement(tag);if(cls){e.className=cls;}if(text!=null){e.textContent=text;}return e;}
  function load(k,d){try{var v=JSON.parse(localStorage.getItem(k)||'null');return v==null?d:v;}catch(e){return d;}}
  function save(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
  function cart(){var c=load(KEY,{});return (c&&typeof c==='object')?c:{};}
  // Pack of 1 + Body Lotion together become the Combo (same rule as the server). Returns true if a pair was combined.
  function setCart(c){Object.keys(c).forEach(function(k){if(!(c[k]>0)||(P&&!P[k])){delete c[k];}else{c[k]=Math.min(10,Math.floor(c[k]));}});
    var n=(P&&P.combo)?Math.min(c.p1||0,c.lotion||0,10-(c.combo||0)):0;
    if(n>0){c.combo=(c.combo||0)+n;c.p1-=n;c.lotion-=n;if(!c.p1){delete c.p1;}if(!c.lotion){delete c.lotion;}}
    save(KEY,c);badge();return n>0;}
  function count(){var c=cart();return Object.keys(c).reduce(function(a,k){return a+c[k];},0);}
  function badge(){var b=document.querySelector('.cart-count');if(!b){return;}var n=count();b.textContent=n;b.hidden=!n;}
  function lines(){var c=cart();return Object.keys(c).filter(function(k){return P&&P[k];}).map(function(k){var p=P[k];return {id:k,qty:c[k],p:p,sub:p.price*c[k],mrp:p.mrp*c[k]};});}
  function totals(){var l=lines();return {lines:l,total:l.reduce(function(a,x){return a+x.sub;},0),mrp:l.reduce(function(a,x){return a+x.mrp;},0)};}
  function add(id,q){var c=cart();c[id]=(c[id]||0)+(q||1);return setCart(c);}
  function toast(text){var t=document.querySelector('.toast');if(!t){t=el('div','toast');t.setAttribute('role','status');document.body.appendChild(t);}
    t.textContent='';t.appendChild(el('span',null,text));var a=el('a',null,'View cart');a.href='/cart/';t.appendChild(a);
    t.classList.add('show');clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('show');},3200);}
  function qtyOf(btn){if(!btn.hasAttribute('data-useqty')){return 1;}var o=document.querySelector('[data-qty] output');return o?Number(o.textContent)||1:1;}

  // menu
  var mb=document.querySelector('.menu-btn');if(mb){mb.addEventListener('click',function(){var n=$('nav');var open=!n.classList.contains('open');n.classList.toggle('open',open);mb.setAttribute('aria-expanded',String(open));});}

  // product page: gallery and quantity
  [].slice.call(document.querySelectorAll('.thumbs button')).forEach(function(b,i,all){b.addEventListener('click',function(){$('pdp-img').src=b.getAttribute('data-src');all.forEach(function(x){x.classList.toggle('on',x===b);});});});
  var qty=document.querySelector('[data-qty]');
  if(qty){var out=qty.querySelector('output');qty.querySelector('[data-dec]').addEventListener('click',function(){out.textContent=Math.max(1,Number(out.textContent)-1);});qty.querySelector('[data-inc]').addEventListener('click',function(){out.textContent=Math.min(10,Number(out.textContent)+1);});}

  function boot(){
    badge();
    document.addEventListener('click',function(e){
      var a=e.target.closest('[data-add]'),b=e.target.closest('[data-buy]');
      if(a){var paired=add(a.getAttribute('data-add'),qtyOf(a));toast(paired?COMBO_MSG:(P[a.getAttribute('data-add')]||{}).card+' added to cart');}
      if(b){add(b.getAttribute('data-buy'),qtyOf(b));location.href='/checkout/';}
    });
    // old WooCommerce links like ?add-to-cart=17 keep working
    var q=new URLSearchParams(location.search), wc=q.get('add-to-cart');
    if(wc){Object.keys(P).forEach(function(k){if(String(P[k].wc)===wc){add(k,1);toast(P[k].card+' added to cart');}});history.replaceState(null,'',location.pathname);}
    if($('cart-lines')){renderCart();}
    if($('checkout')){checkout();}
    if($('track-form')){trackPage();}
    if(!$('checkout')&&!$('ro-form')){resumeStrip();nudge();}
    buyBar();deliveryCheck();
  }
  fetch('/assets/products.json').then(function(r){return r.json();}).then(function(d){P=d;boot();}).catch(function(){P={};badge();});

  function sumRows(box,rows){box.textContent='';rows.forEach(function(r){var d=el('div',r[2]||'');d.appendChild(el('span',null,r[0]));d.appendChild(el('b',null,r[1]));box.appendChild(d);});}
  function lineNode(x,editable,after){
    var row=el('div','line');var im=el('img');im.src=x.p.img;im.alt='';im.width=76;im.height=76;row.appendChild(im);
    var mid=el('div');var a=el('a',null,null);a.href=x.p.url;a.style.textDecoration='none';a.appendChild(el('b',null,x.p.name));mid.appendChild(a);
    if(editable){var q=el('div','qty');var dec=el('button',null,'−'),o=el('output',null,String(x.qty)),inc=el('button',null,'+');[dec,inc].forEach(function(bt){bt.type='button';});
      dec.addEventListener('click',function(){var c=cart();c[x.id]=Math.max(0,c[x.id]-1);setCart(c);after();});
      inc.addEventListener('click',function(){var c=cart();c[x.id]=Math.min(10,c[x.id]+1);setCart(c);after();});
      q.appendChild(dec);q.appendChild(o);q.appendChild(inc);var w=el('div');w.appendChild(q);var rm=el('button','rm','Remove');rm.type='button';rm.addEventListener('click',function(){var c=cart();delete c[x.id];setCart(c);after();});w.appendChild(rm);mid.appendChild(w);}
    else{mid.appendChild(el('span','sub','Qty '+x.qty));}
    row.appendChild(mid);var amt=el('div','amt',rs(x.sub));if(x.mrp>x.sub){amt.appendChild(el('s',null,rs(x.mrp)));}row.appendChild(amt);return row;
  }
  // "Add X for ₹Y more" box: shown when one half of the combo is in the cart without the other.
  function upsell(box,after){
    var c=cart();if(!P||!P.combo){return;}var want=null;
    if(c.p1&&!c.lotion){want='lotion';}else if(c.lotion&&!c.p1){want='p1';}
    if(!want){return;}var have=want==='lotion'?'p1':'lotion',more=P.combo.price-P[have].price;
    var u=el('div','upsell');var im=el('img');im.src=P[want].img;im.alt='';im.width=56;im.height=56;u.appendChild(im);
    var tx=el('div');tx.appendChild(el('b',null,want==='lotion'?'Add the Body Lotion for just '+rs(more)+' more':'Add the Beauty Cream for just '+rs(more)+' more'));
    tx.appendChild(el('span',null,'Get the Combo (Cream + Lotion) for '+rs(P.combo.price)+' instead of '+rs(P.p1.price+P.lotion.price)+'.'));u.appendChild(tx);
    var b=el('button','btn sm','Add +'+rs(more));b.type='button';b.addEventListener('click',function(){add(want,1);toast(COMBO_MSG);after();});u.appendChild(b);box.appendChild(u);
  }
  function renderCart(){
    var box=$('cart-lines'),t=totals();box.textContent='';
    if(!t.lines.length){var e=el('div','empty');e.appendChild(el('h2',null,'Your cart is empty'));e.appendChild(el('p','muted','Add a pack to get started.'));var s=el('a','btn','Shop now');s.href='/shop/';s.style.marginTop='16px';e.appendChild(s);box.appendChild(e);$('to-checkout').hidden=true;sumRows($('cart-sum'),[]);return;}
    t.lines.forEach(function(x){box.appendChild(lineNode(x,true,renderCart));});upsell(box,renderCart);$('to-checkout').hidden=false;
    sumRows($('cart-sum'),[['MRP',rs(t.mrp)],['Discount','− '+rs(t.mrp-t.total),'save'],['Shipping','Free'],['Total',rs(t.total),'total']]);
  }

  /* ---------------- checkout ---------------- */
  function checkout(){
    // Until online payment is switched on, do not ask for personal details: offer WhatsApp ordering instead.
    fetch('/api/config').then(function(r){return r.ok?r.json():null;}).then(function(c){
      if(!c||c.razorpay){return;}
      var form=$('co-form');if(!form){return;}form.hidden=true;
      var t=totals(),box=el('div','setup-note');
      box.appendChild(el('h2',null,'Order on WhatsApp'));
      box.appendChild(el('p',null,'Our online checkout is being set up. You can still order right now: tap below to send your cart to us on WhatsApp. We confirm your order on chat and you pay cash on delivery.'));
      var msg='Hi Youth Face, I would like to order:\n'+t.lines.map(function(x){return '- '+x.p.name+' x'+x.qty+' = '+rs(x.sub);}).join('\n')+'\nTotal: '+rs(t.total);
      var a=el('a','btn block','Send my order on WhatsApp');a.href='https://wa.me/'+WA+'?text='+encodeURIComponent(msg);a.target='_blank';a.rel='noopener';
      if(!t.lines.length){a.href='/shop/';a.removeAttribute('target');a.textContent='Go to the shop';}
      box.appendChild(a);box.appendChild(el('p','muted','Free shipping · Cash on Delivery · WhatsApp '+'+91 99808 81230'));
      form.parentNode.insertBefore(box,form);
    }).catch(function(){});
    var F={name:$('co-name'),phone:$('co-phone'),address:$('co-address'),pin:$('co-pin'),city:$('co-city')};
    var btn=$('co-pay'),err=$('co-err'),bad=null,busy=false,lastMode='online';
    var saved=load(DETAILS,null);if(saved){Object.keys(F).forEach(function(k){if(typeof saved[k]==='string'){F[k].value=saved[k].slice(0,300);}});}
    function mode(){return document.querySelector('input[name=pay]:checked').value;}
    function mobile(v){var d=String(v).replace(/\D/g,'');if(d.length===12&&d.slice(0,2)==='91'){d=d.slice(2);}else if(d.length===11&&d.charAt(0)==='0'){d=d.slice(1);}return /^[6-9]\d{9}$/.test(d)&&!/^(\d)\1{9}$/.test(d)?d:'';}
    function problem(){bad=null;
      if(!lines().length){return 'Your cart is empty.';}
      if(F.name.value.trim().length<2){bad=F.name;return 'Please enter your full name.';}
      if(!mobile(F.phone.value)){bad=F.phone;return 'Please enter a 10-digit Indian mobile number.';}
      if(F.address.value.trim().length<8){bad=F.address;return 'Please enter your full address with house number and street.';}
      if(!/^[1-9]\d{5}$/.test(F.pin.value.trim())){bad=F.pin;return 'Please enter a 6-digit pincode.';}
      if(F.city.value.trim().length<2){bad=F.city;return 'Please enter your city.';}
      return '';}
    function mark(){[].slice.call(document.querySelectorAll('.fielderr')).forEach(function(x){x.remove();});Object.keys(F).forEach(function(k){F[k].classList.toggle('bad',F[k]===bad);});}
    function show(p){err.textContent=p;err.hidden=false;mark();if(bad){var fe=el('p','fielderr',p);bad.insertAdjacentElement('afterend',fe);bad.focus({preventScroll:true});bad.scrollIntoView({block:'center',behavior:'smooth'});}}
    Object.keys(F).forEach(function(k){F[k].addEventListener('input',function(){F[k].classList.remove('bad');var n=F[k].nextElementSibling;if(n&&n.className==='fielderr'){n.remove();}if(!err.hidden&&!problem()){err.hidden=true;}});});
    function remember(){var o={};Object.keys(F).forEach(function(k){o[k]=F[k].value.trim();});save(DETAILS,o);}
    function render(){
      var t=totals(),box=$('co-lines');box.textContent='';
      if(!t.lines.length){box.appendChild(el('p','muted','Your cart is empty.'));var s=el('a','btn','Shop now');s.href='/shop/';box.appendChild(s);btn.disabled=true;return;}
      t.lines.forEach(function(x){box.appendChild(lineNode(x,true,render));});upsell(box,render);btn.disabled=false;
      var m=mode();
      $('amt-online').textContent=rs(t.total);$('amt-cod').textContent=rs(t.total);$('amt-wa').textContent=rs(t.total);
      $('cod-note').textContent='Pay '+rs(ADVANCE)+' now, '+rs(Math.max(0,t.total-ADVANCE))+' at delivery';
      $('cod-terms').hidden=m!=='cod';
      var rows=[['MRP',rs(t.mrp)],['Discount','− '+rs(t.mrp-t.total),'save'],['Shipping','Free']];
      if(m==='cod'){rows.push(['Pay now (advance)',rs(ADVANCE),'total']);rows.push(['Pay at delivery',rs(t.total-ADVANCE)]);}
      else{rows.push([m==='wa'?'Order total':'You pay',rs(t.total),'total']);}
      sumRows($('co-sum'),rows);
      if(!busy){btn.textContent=m==='online'?'Pay '+rs(t.total)+' securely':m==='cod'?'Pay '+rs(ADVANCE)+' to confirm order':'Send order on WhatsApp';}
    }
    [].slice.call(document.querySelectorAll('input[name=pay]')).forEach(function(r){r.addEventListener('change',render);});
    var pend=load(PENDING,null);
    if(pend&&Date.now()-pend.at<3*864e5&&lines().length){var r0=document.querySelector('input[name=pay][value='+(pend.mode==='cod'?'cod':'online')+']');if(r0){r0.checked=true;}
      var wb=el('p','welcome','Welcome back! Your details are already filled in. One tap below and your order is placed.');btn.insertAdjacentElement('beforebegin',wb);}
    render();
    // pincode → city and delivery estimate
    var pinSeen='',cityAuto='';
    function pinLookup(){var pin=F.pin.value.trim();if(!/^[1-9]\d{5}$/.test(pin)){$('pin-note').hidden=true;pinSeen='';return;}if(pin===pinSeen){return;}pinSeen=pin;
      fetch('/api/pincode?pin='+pin).then(function(r){return r.ok?r.json():null;}).then(function(d){if(!d||!d.ok||F.pin.value.trim()!==pin){return;}
        if(d.city&&(!F.city.value.trim()||F.city.value===cityAuto)){F.city.value=d.city;cityAuto=d.city;}
        var parts=[[d.city,d.state].filter(Boolean).join(', ')];
        if(d.days){var by=new Date();by.setDate(by.getDate()+2+d.days);parts.push('estimated delivery by '+by.toLocaleDateString('en-IN',{weekday:'short',day:'numeric',month:'short'}));}
        var codR=document.querySelector('input[name=pay][value=cod]'),codL=codR.closest('label');
        codR.disabled=d.cod===false;codL.classList.toggle('off',d.cod===false);
        if(d.cod===false){parts.push('Cash on Delivery is not available for this pincode, please pay online');if(codR.checked){document.querySelector('input[name=pay][value=online]').checked=true;render();}}
        if(d.serviceable===false){parts=['Sorry, our courier does not deliver to '+pin+' yet. Message us on WhatsApp and we will try to arrange it.'];}
        $('pin-note').textContent=parts.filter(Boolean).join(' · ');$('pin-note').hidden=false;if(!err.hidden&&!problem()){err.hidden=true;mark();}}).catch(function(){});}
    F.pin.addEventListener('input',pinLookup);pinLookup();

    function waUrl(){var t=totals();var msg='New Youth Face order\n'+t.lines.map(function(x){return '- '+x.p.name+' x'+x.qty+' = '+rs(x.sub);}).join('\n')+'\nTotal: '+rs(t.total)+'\nPayment: please confirm with me on WhatsApp\n\nName: '+F.name.value.trim()+'\nMobile: '+F.phone.value.trim()+'\nAddress: '+F.address.value.trim()+'\nCity: '+F.city.value.trim()+'\nPincode: '+F.pin.value.trim();return 'https://wa.me/'+WA+'?text='+encodeURIComponent(msg);}
    function loadRzp(done,fail){if(window.Razorpay){done();return;}var s=document.createElement('script');s.src='https://checkout.razorpay.com/v1/checkout.js';s.onload=done;s.onerror=fail;document.head.appendChild(s);}
    function stop(text){busy=false;render();if(text){err.textContent=text;err.hidden=false;}}
    function pay(advance){
      var t=totals();lastMode=advance?'cod':'online';$('not-yet').hidden=true;err.hidden=true;busy=true;btn.textContent='Opening secure payment…';remember();
      fetch('/api/create-order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({items:t.lines.map(function(x){return {id:x.id,qty:x.qty};}),mode:advance?'advance':'full',name:F.name.value.trim(),phone:mobile(F.phone.value),address:F.address.value.trim(),city:F.city.value.trim(),pincode:F.pin.value.trim(),remind:!!($('co-remind')&&$('co-remind').checked)})})
      .then(function(r){return r.ok?r.json():Promise.reject(r.status);})
      .then(function(o){loadRzp(function(){var done=false;
        var rz=new window.Razorpay({key:o.key_id,order_id:o.order_id,amount:o.amount,currency:o.currency,name:'Youth Face',description:advance?'Advance for Cash on Delivery':'Youth Face order',
          prefill:{name:F.name.value.trim(),contact:mobile(F.phone.value)},theme:{color:'#740817'},
          handler:function(resp){done=true;fetch('/api/verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(resp)}).then(function(r){return r.json();})
            .then(function(v){thanks(resp.razorpay_payment_id,o,!!v.ok);}).catch(function(){thanks(resp.razorpay_payment_id,o,false);});},
          modal:{ondismiss:function(){stop();if(!done){save(PENDING,{mode:lastMode,at:Date.now()});$('ny-switch').textContent=lastMode==='cod'?'Pay the full amount online instead':'Switch to Cash on Delivery (₹99 now)';$('not-yet').hidden=false;$('not-yet').scrollIntoView({block:'center',behavior:'smooth'});}}}});
        rz.on('payment.failed',function(){stop('The payment did not go through. Nothing is charged unless your bank shows a debit. Please try again.');});rz.open();},
        function(){stop('The payment window could not load. Check your connection and try again, or order on WhatsApp.');});})
      .catch(function(){stop('Online payment is not available right now. Please try again in a few minutes, or order on WhatsApp.');});
    }
    $('ny-retry').addEventListener('click',function(){pay(lastMode==='cod');});
    $('ny-switch').addEventListener('click',function(){var v=lastMode==='cod'?'online':'cod';document.querySelector('input[name=pay][value='+v+']').checked=true;render();pay(v==='cod');});
    $('co-form').addEventListener('submit',function(e){e.preventDefault();if(busy){return;}var p=problem();if(p){show(p);return;}mark();var m=mode();
      if(m==='wa'){remember();window.open(waUrl(),'_blank','noopener');return;}pay(m==='cod');});
    function thanks(pid,o,ok){
      var t=totals(),cod=o.balance>0;var past=load(ORDERS,[]).filter(function(x){return x&&x.id!==pid;});past.unshift({id:pid,at:Date.now(),items:t.lines.map(function(x){return x.p.card+(x.qty>1?' ×'+x.qty:'');}).join(', ')});save(ORDERS,past.slice(0,5));
      setCart({});try{localStorage.removeItem(PENDING);}catch(e){}
      var wrap=$('checkout');wrap.textContent='';var box=el('div','panel thanks');box.style.gridColumn='1 / -1';
      box.appendChild(el('span','tick','✓'));box.appendChild(el('h2',null,ok?(cod?'Order confirmed. Thank you!':'Payment received. Thank you!'):'Payment submitted. We are confirming it.'));
      box.appendChild(el('p','muted','We will pack your order within 1 to 3 business days and send it with free shipping.'));
      if($('co-remind')&&$('co-remind').checked){var jars=t.lines.reduce(function(a,x){return a+x.qty*({p1:1,p2:2,p3:3,combo:1}[x.id]||0);},0);
        if(jars){var rd=new Date();rd.setDate(rd.getDate()+jars*30);box.appendChild(el('p','remind-note','We will remind you on WhatsApp around '+rd.toLocaleDateString('en-IN',{day:'numeric',month:'long'})+', when your cream is about to run out.'));}}
      var s=el('div','sum');var rows=[['Items',t.lines.map(function(x){return x.p.card+(x.qty>1?' ×'+x.qty:'');}).join(', ')]];
      if(cod){rows.push(['Advance paid',rs(ADVANCE)]);rows.push(['Pay at delivery',rs(o.balance),'total']);}else{rows.push(['Paid online',rs(o.total),'total']);}
      rows.push(['You saved on MRP',rs(t.mrp-t.total),'save']);rows.push(['Order number',pid]);sumRows(s,rows);box.appendChild(s);
      var tr=el('a','btn block','Track this order');tr.href='/track-order/?id='+encodeURIComponent(pid);box.appendChild(tr);
      var wa=el('a','btn ghost block','Get updates on WhatsApp');wa.href='https://wa.me/'+WA+'?text='+encodeURIComponent('Hi Youth Face, I placed an order. Order number: '+pid);wa.target='_blank';wa.rel='noopener';box.appendChild(wa);
      wrap.appendChild(box);window.scrollTo({top:0,behavior:'smooth'});
      if(typeof gtag==='function'){gtag('event','purchase',{transaction_id:pid,value:o.total,currency:'INR'});}
      if(typeof fbq==='function'){fbq('track','Purchase',{value:o.total,currency:'INR'},{eventID:pid});}
    }
  }

  /* ---------------- track ---------------- */
  function trackPage(){
    var byPhone=true,out=$('t-out'),go=$('t-go');
    function setMode(p){byPhone=p;$('by-phone-box').hidden=!p;$('by-id-box').hidden=p;$('by-phone').classList.toggle('on',p);$('by-id').classList.toggle('on',!p);}
    $('by-phone').addEventListener('click',function(){setMode(true);});$('by-id').addEventListener('click',function(){setMode(false);});
    function day(s){var d=new Date(String(s).replace(' ','T'));return isNaN(d)?String(s):d.toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'});}
    function showNodes(n){out.textContent='';n.forEach(function(x){if(x){out.appendChild(x);}});out.hidden=false;}
    function help(){var a=el('a','btn ghost','Ask us on WhatsApp');a.href='https://wa.me/'+WA+'?text='+encodeURIComponent('Hi Youth Face, I want to check my order.');a.target='_blank';a.rel='noopener';a.style.marginTop='14px';return a;}
    function steps(n){var ol=el('ol','tsteps');['Order placed','Packed','Shipped','Delivered'].forEach(function(t,i){ol.appendChild(el('li',i<n?'done':'',t));});return ol;}
    function render(d){
      var extra=d.others>0?el('p','muted','Showing your latest order. You have '+d.others+' more with this number.'):null;
      if(d.paid===false){return showNodes([el('h2',null,'Payment not completed'),el('p','muted','This order was not paid, so it has not been dispatched.'),help()]);}
      if(!d.shipped){return showNodes([el('h2',null,'Order received'),d.placed?el('p','muted','Placed on '+day(d.placed)):null,steps(1),el('p',null,(d.items?d.items+'. ':'')+(d.due?rs(d.due)+' to pay on delivery. ':'')+'Your order is being packed. Tracking appears here once the courier collects it.'),extra,help()]);}
      var delivered=/deliver/i.test(d.status||'')&&!/out for|undeliver|not deliver/i.test(d.status||'');
      var n=[el('h2',null,d.status||'Shipped'),steps(delivered?4:3)];var bits=[];if(d.courier){bits.push('Courier: '+d.courier);}if(d.awb){bits.push('Tracking number: '+d.awb);}if(d.due&&!delivered){bits.push(rs(d.due)+' to pay on delivery');}
      if(delivered&&d.delivered_on){bits.push('Delivered on '+day(d.delivered_on));}else if(d.expected){bits.push('Expected by '+day(d.expected));}n.push(el('p',null,bits.join(' · ')));
      if(d.events&&d.events.length){var ul=el('ul','tlog');d.events.forEach(function(e){var li=el('li');li.appendChild(el('b',null,e.text));li.appendChild(el('span',null,[day(e.date),e.place].filter(Boolean).join(' · ')));ul.appendChild(li);});n.push(ul);}
      if(d.track_url){var a=el('a','btn','Open courier tracking');a.href=d.track_url;a.target='_blank';a.rel='noopener';a.style.marginTop='14px';n.push(a);}
      n.push(extra);showNodes(n);
    }
    function run(){
      var url;
      if(byPhone){var ph=$('t-phone').value.replace(/\D/g,'').slice(-10),pn=$('t-pin').value.trim();
        if(!/^[6-9]\d{9}$/.test(ph)){return showNodes([el('p','oerr','Please enter the 10-digit mobile number used on the order.')]);}
        if(!/^[1-9]\d{5}$/.test(pn)){return showNodes([el('p','oerr','Please enter the 6-digit delivery pincode.')]);}
        url='/api/track?phone='+ph+'&pin='+pn;}
      else{var id=$('t-id').value.trim().replace(/\s+/g,'');if(id.length<8){return showNodes([el('p','oerr','Please enter your payment ID or tracking number.')]);}url='/api/track?id='+encodeURIComponent(id);}
      go.disabled=true;go.textContent='Checking…';
      fetch(url).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});}).then(function(x){
        if(x.ok&&x.j.found){render(x.j);}
        else if(x.j&&/not_found|bad_/.test(x.j.error||'')){showNodes([el('h2',null,'We could not find that order'),el('p','muted',byPhone?'No paid order in the last 90 days matches this mobile number and pincode. Check both, or use your payment ID.':'Check the ID and try again. The payment ID starts with pay_.'),help()]);}
        else{showNodes([el('h2',null,'Tracking is not available right now'),el('p','muted','Please try again in a few minutes, or message us.'),help()]);}
      }).catch(function(){showNodes([el('h2',null,'Tracking is not available right now'),help()]);}).then(function(){go.disabled=false;go.textContent='Track order';});
    }
    $('track-form').addEventListener('submit',function(e){e.preventDefault();run();});
    var mine=load(ORDERS,[]).filter(function(o){return o&&/^pay_/.test(o.id);});
    var q=new URLSearchParams(location.search).get('id');
    if(q){setMode(false);$('t-id').value=q;run();}else if(mine.length){setMode(false);$('t-id').value=mine[0].id;run();}
  }
  /* ---------------- unfinished-order strip (all pages except checkout) ---------------- */
  function resumeStrip(){
    var t=totals();if(!t.lines.length){return;}
    var pend=load(PENDING,null),det=load(DETAILS,null);if(!pend&&!det){return;}
    try{if(sessionStorage.getItem('yf-strip-x')){return;}}catch(e){}
    var n=count(),bar=el('div','resume');bar.setAttribute('role','region');bar.setAttribute('aria-label','Unfinished order');
    var w=el('div','wrap resume-in');
    w.appendChild(el('p',null,pend?'Your order is one tap away. The payment didn’t finish last time, and your details are saved.':'You left '+(n===1?'a jar':n+' items')+' in your cart ('+rs(t.total)+'). Your details are saved.'));
    var go=el('a','btn sm','Finish my order');go.href='/checkout/';w.appendChild(go);
    var x=el('button','resume-x','×');x.type='button';x.setAttribute('aria-label','Hide');x.addEventListener('click',function(){bar.remove();try{sessionStorage.setItem('yf-strip-x','1');}catch(e){}});w.appendChild(x);
    bar.appendChild(w);var main=$('main');main.insertBefore(bar,main.firstChild);
  }

  /* ---------------- delivery check on product pages ---------------- */
  function deliveryCheck(){
    var inp=$('dc-pin'),go=$('dc-go'),out=$('dc-out');if(!inp){return;}
    var det=load(DETAILS,null);if(det&&/^[1-9]\d{5}$/.test(det.pin||'')){inp.value=det.pin;}
    function say(cls,text){out.className='dc-out '+cls;out.textContent=text;out.hidden=false;}
    function run(){var pin=inp.value.replace(/\D/g,'').slice(0,6);inp.value=pin;
      if(!/^[1-9]\d{5}$/.test(pin)){say('bad','Please enter a 6-digit pincode.');return;}
      var d0=load(DETAILS,{})||{};d0.pin=pin;save(DETAILS,d0);
      go.disabled=true;say('','Checking…');
      fetch('/api/pincode?pin='+pin).then(function(r){return r.ok?r.json():null;}).then(function(d){
        if(!d||!d.ok){say('','We could not check this pincode right now. We deliver across India; order and we will confirm on WhatsApp if there is any issue.');return;}
        if(d.serviceable===false){say('bad','Sorry, our courier does not deliver to '+pin+' yet. Message us on WhatsApp and we will try to arrange it.');return;}
        var where=[d.city,d.state].filter(Boolean).join(', '),bits=['Delivers to '+(where||pin)];
        if(d.days){var by=new Date();by.setDate(by.getDate()+2+d.days);bits[0]+=' by '+by.toLocaleDateString('en-IN',{weekday:'short',day:'numeric',month:'short'});}
        bits.push(d.cod===false?'Prepaid only for this pincode':'Cash on Delivery available');bits.push('Free shipping');
        say('ok','✓ '+bits.join(' · '));
      }).catch(function(){say('','We could not check this pincode right now. Please try again.');}).then(function(){go.disabled=false;});}
    go.addEventListener('click',run);
    inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();run();}});
    inp.addEventListener('input',function(){if(/^[1-9]\d{5}$/.test(inp.value.trim())){run();}});
    if(inp.value){run();}
  }

  /* ---------------- sticky Buy bar on product pages ---------------- */
  function buyBar(){
    var bar=$('buybar'),acts=document.querySelector('.pdp .acts');if(!bar||!acts){return;}
    var ticking=false;
    function check(){ticking=false;var show=acts.getBoundingClientRect().bottom<0;if(bar.hidden===show){bar.hidden=!show;document.body.classList.toggle('has-bar',show);}}
    window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(check);}},{passive:true});check();
  }

  /* ---------------- 3½-minute pop-up (once every 3 days, never on cart/checkout) ---------------- */
  var NUDGE_ON=false; // switched off while Google Ads is under review; set to true to bring the 3½-minute pop-up back
  function nudge(){
    if(!NUDGE_ON){return;}
    if(/^\/(cart|checkout|reorder)\//.test(location.pathname)){return;}
    var last=load(NUDGE,0);if(Date.now()-last<3*864e5){return;}
    if(load(ORDERS,[]).some(function(o){return o&&Date.now()-o.at<30*864e5;})){return;}
    var secs=0,timer=setInterval(function(){if(document.visibilityState==='visible'){secs++;}if(secs>=210){clearInterval(timer);open();}},1000);
    function open(){
      if(document.querySelector('.nudge')){return;}save(NUDGE,Date.now());
      var p2=P.p2||{},bg=el('div','nudge');bg.setAttribute('role','dialog');bg.setAttribute('aria-modal','true');bg.setAttribute('aria-labelledby','nudge-h');
      var box=el('div','nudge-box'),x=el('button','nudge-x','×');x.type='button';x.setAttribute('aria-label','Close');
      var im=el('img');im.src=p2.img||'';im.alt='Youth Face Beauty Cream, Pack of 2';im.width=600;im.height=600;
      var tx=el('div','nudge-tx');tx.appendChild(el('span','eyebrow','3½ minutes and counting'));
      var h=el('h2',null,'Still scrolling? Your skin noticed.');h.id='nudge-h';tx.appendChild(h);
      tx.appendChild(el('p','muted','That’s longer than most people spend choosing a sunscreen. Your dark spots won’t read the guides for you — but a jar can sit on your shelf by next week.'));
      var pr=el('p','nudge-pr');pr.appendChild(el('b',null,'Pack of 2 · '+rs(p2.price||999)));if(p2.mrp>p2.price){pr.appendChild(el('s',null,rs(p2.mrp)));}pr.appendChild(el('span',null,'Free shipping · Cash on Delivery'));tx.appendChild(pr);
      var go=el('button','btn block','Okay fine, I’ll take the Pack of 2');go.type='button';go.setAttribute('data-buy','p2');tx.appendChild(go);
      var no=el('button','nudge-no','Still browsing. Let me be.');no.type='button';tx.appendChild(no);
      box.appendChild(x);box.appendChild(im);box.appendChild(tx);bg.appendChild(box);document.body.appendChild(bg);
      var prev=document.activeElement;go.focus({preventScroll:true});
      function close(){bg.remove();document.removeEventListener('keydown',esc);if(prev&&prev.focus){prev.focus({preventScroll:true});}}
      function esc(e){if(e.key==='Escape'){close();}}
      x.addEventListener('click',close);no.addEventListener('click',close);bg.addEventListener('click',function(e){if(e.target===bg){close();}});document.addEventListener('keydown',esc);
      if(typeof gtag==='function'){gtag('event','nudge_shown');}
    }
  }
})();
