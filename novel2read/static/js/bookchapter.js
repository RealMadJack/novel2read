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
    behavior: 'smooth'
  });
}



// Theming
const styles = document.body.querySelector('.bookchapter__styles')
const stylesCollapse = document.getElementById('stylesCollapse')
const toggleStyles = document.getElementById('toggleStyles')
const lt = document.getElementById('lightTheme');
const dt = document.getElementById('darkTheme');
let theme = localStorage.getItem('theme', '')

if (theme === 'light') {
  setDomTheme('light');
} else if (theme === 'dark') {
  setDomTheme('dark');
}

function setDomTheme(theme) {
  body = document.body;
  if (theme == 'dark') {
    body.classList.add('dark-theme')
  } else {
    body.classList.remove('dark-theme');
  }
}

function manageStyles(e) {
  e.preventDefault();
  if (e.target === toggleStyles) {
    console.log(e.target)
    stylesCollapse.classList.toggle('visible')
  }
  if (e.target === lt) {
    localStorage.setItem('theme', 'light')
    setDomTheme('light');
  } else if (e.target === dt) {
    localStorage.setItem('theme', 'dark')
    setDomTheme('dark');
  }
  return false
}

styles.addEventListener('click', manageStyles)

})();
