(function () {

// Notifications
function eventNotification(msg='', flag='info') {
    let body = document.body;
    let container = document.getElementsByClassName('container')[1]
    let alertBox = document.createElement('div')
    let alertTime = 2000
    let alertTimeAnim = alertTime - 200
    alertBox.className = `alert alert-${flag}`
    alertBox.textContent = msg
    container.appendChild(alertBox)
    setTimeout(() => {
        alertBox.classList.add('animate')
    }, 100)
    setTimeout(() => {
        alertBox.classList.remove('animate')
    }, alertTimeAnim)
    setTimeout(() => {
        container.removeChild(alertBox)
    }, alertTime);
}

// Scroll Position
let pos = localStorage.getItem('chap_scroll', 0)
let pos_url = localStorage.getItem('chap_url', '')
let posList = localStorage.getItem('pos-list')
let list = []
posList = posList !== null ? posList : localStorage.setItem('pos-list', list)

window.onscroll = () => {
  const offset = 100;
  let scrollTop = window.pageYOffset;
  localStorage.setItem('chap_scroll', scrollTop);
  localStorage.setItem('chap_url', location.pathname)
}

if (pos_url === location.pathname) {
  window.scrollTo({
    top: pos,
    left: 0,
    behavior: 'auto'
  });
}

// Theming
function setBodyCls(cls) {
  let body = document.body.classList;
  let c_light = 'tm-color-light'
  let c_dark = 'tm-color-dark'
  let f_arial = 'tm-font-arial'
  let f_lora = 'tm-font-lora'
  let f_roboto = 'tm-font-roboto'
  let fz_18 = 'tm-fz-18'
  let fz_17 = 'tm-fz-17'
  let fz_16 = 'tm-fz-16'
  let fz_15 = 'tm-fz-15'
  let fz_14 = 'tm-fz-14'
  let lh_20 = 'tm-lh-20'
  let lh_15 = 'tm-lh-15'
  let lh_10 = 'tm-lh-10'
  let lh_5 = 'tm-lh-5'
  if (cls.includes('color')) {
    if (body.contains(c_light) || body.contains(c_dark)) {
      body.remove(c_light, c_dark);
    }
    body.add(cls)
  }
  if (cls.includes('font')) {
    if (body.contains(f_arial) || body.contains(f_lora) || body.contains(f_roboto)) {
      body.remove(f_arial, f_lora, f_roboto);
    }
    body.add(cls)
  }
  if (cls.includes('fz')) {
    if (body.contains(fz_18) || body.contains(fz_17) || body.contains(fz_16) || body.contains(fz_15) || body.contains(fz_14)) {
      body.remove(fz_18, fz_17, fz_16, fz_15, fz_14);
    }
    body.add(cls)
  }
  if (cls.includes('lh')) {
    if (body.contains(lh_20) || body.contains(lh_15) || body.contains(lh_10) || body.contains(lh_5)) {
      body.remove(lh_20, lh_15, lh_10, lh_5);
    }
    body.add(cls)
  }
}

const styles = document.body.querySelector('.chap-styles')
const stylesMenu = document.getElementById('stylesMenu')
const stylesBtn = document.getElementById('stylesBtn')

function manageStyles(e) {
  const tm_color = e.target.getAttribute('data-theme-color');
  const tm_font = e.target.getAttribute('data-theme-font');
  const tm_fz = e.target.getAttribute('data-theme-fz');
  const tm_lh = e.target.getAttribute('data-theme-lh');

  if (e.target === stylesBtn) {
    stylesMenu.classList.toggle('visible')
  }
  if (tm_color) {
    setBodyCls(tm_color)
  }
  if (tm_font) {
    setBodyCls(tm_font)
  }
  if (tm_fz) {
    setBodyCls(tm_fz)
  }
  if (tm_lh) {
    setBodyCls(tm_lh)
  }
}
styles.addEventListener('click', manageStyles)

// ChapNav
function getChapsAjax(btn) {
  let loaded = btn.attr("data-loaded");
  if (!!+loaded) {
    return false
  }
  $.ajax({
    url: btn.attr("data-url-chaps"),
    type: "get",
    dataType: "json",
    success: function (data) {
      btn.next().html(data['html_chaps']);
      btn.attr("data-loaded", 1);
      let activeChap = document.getElementById('activeChap')
      activeChap.scrollIntoView(false);
    },
    error: function (xhr, errmsg, err) {
        let msg = `${xhr.status} ${xhr.statusText}`
        eventNotification(msg, 'error')
    },
  });
}

function toggleChapNav(e) {
  let btn = $(this);
  btn.next()[0].classList.toggle('visible')
  getChapsAjax(btn);
}
$('#chaps-toggle')[0].addEventListener('click', toggleChapNav);


// Close Toggles
function closeToggles(e) {
  let chapNav = $('#chaps-nav')[0]
  let chapToggle = $('#chaps-toggle')[0]
  if (chapNav.classList.contains('visible')) {
    if (e.target !== chapToggle && !$(e.target).closest(chapNav).length) {
      chapNav.classList.remove('visible')
    }
  }
  if (stylesMenu.classList.contains('visible')) {
    if (e.target !== stylesBtn && !$(e.target).closest(stylesMenu).length) {
      stylesMenu.classList.remove('visible')
    }
  }
}

document.body.addEventListener('click', closeToggles, false)

})();
