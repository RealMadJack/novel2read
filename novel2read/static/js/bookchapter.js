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
const styles = document.body.querySelector('.bookchapter__styles')
const stylesCollapse = document.getElementById('stylesCollapse')
const toggleStyles = document.getElementById('toggleStyles')

function setDomTheme(theme) {
  let body = document.body.classList;
  if (theme == 'dark') {
    body.remove('tm-color-light')
    body.add('tm-color-dark')
  } else if (theme == 'light') {
    body.remove('tm-color-dark');
    body.add('tm-color-light');
  }
}

function manageStyles(e) {
  e.preventDefault();
  const lt = document.getElementById('lightTheme');
  const dt = document.getElementById('darkTheme');
  if (e.target === toggleStyles) {
    stylesCollapse.classList.toggle('visible')
  }
  if (e.target === lt) {
    setDomTheme('light');
  } else if (e.target === dt) {
    setDomTheme('dark');
  }
  return false
}

function closeStyles(e) {
  if (e.target !== toggleStyles) {
    stylesCollapse.classList.remove('visible')
  }
  return false
}

styles.addEventListener('click', manageStyles)
document.body.addEventListener('click', closeStyles)

})();
