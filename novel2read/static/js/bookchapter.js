(function () {

// Toggles
let chapToggle = document.getElementById('chaps-toggle');
let chapNav = document.getElementById('chaps-nav');
let activeChap = document.getElementById('activeChap')

function toggleElem(e) {
  e.preventDefault();
  chapNav.classList.toggle('dblock');
  setTimeout(() => {
    chapNav.classList.toggle('active');
  }, 10)
  activeChap.scrollIntoView(false);
}

function closeElem(e) {
  if (chapNav.classList.contains('active')) {
    if (e.target !== chapToggle) {
      chapNav.classList.toggle('dblock');
      setTimeout(() => {
        chapNav.classList.toggle('active');
      }, 10)
    }
  }
  return false
}

chapToggle.addEventListener('click', toggleElem);
document.body.addEventListener('click', closeElem)


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
}

const styles = document.body.querySelector('.chap-styles')
const stylesMenu = document.getElementById('stylesMenu')
const stylesBtn = document.getElementById('stylesBtn')

function manageStyles(e) {
  const tm_color = e.target.getAttribute('data-theme-color');
  const tm_font = e.target.getAttribute('data-theme-font');

  if (e.target === stylesBtn) {
    stylesMenu.classList.toggle('visible')
  }

  if (tm_color) {
    setBodyCls(tm_color)
  }
  if (tm_font) {
    setBodyCls(tm_font)
  }
}

function closeStyles(e) {
  if (stylesMenu.classList.contains('visible')) {
    if (e.target !== stylesBtn && !$(e.target).closest(stylesMenu).length) {
      stylesMenu.classList.remove('visible')
    }
  }
}

styles.addEventListener('click', manageStyles, false)
document.body.addEventListener('click', closeStyles, false)

})();
