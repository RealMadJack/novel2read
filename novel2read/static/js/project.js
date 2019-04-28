/* Project specific Javascript goes here. */

(function () {

// Global vars
let wto;
const ajaxDelay = 200
const ajaxDelaySearch = 250


// Infinite Scroll
let scrollThreshold = location.pathname === "/" ? false : true;
let scrollHistory = location.pathname === "/" ? false : true;
$('.infinite-container').infiniteScroll({
    path: '.infinite-more-link',
    append: '.infinite-item',
    button: '.infinite-more-link',
    scrollThreshold: scrollThreshold,
    status: '.loading',
    history: scrollHistory,
});


// Select
let selectOptions = {}

$('select').selectize(selectOptions);
// disable search
$('.selectize-input > input').prop('disabled', 'disabled');

// Swiper Slider config
let slides = window.innerWidth > 1750 ? 'auto' : 'auto'
let slideDepth = window.innerWidth > 2020 ? 300 : 500
let swiperOptions = {
    // pagination: {
    //     el: '.swiper-pagination',
    //     dynamicBullets: true,
    // },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    autoplay: {
        delay: 7000,
        disableOnInteraction: true,
    },
    roundLengths: true,
    centeredSlides: true,
    loop: true,
    slidesPerView: slides,
    effect: 'coverflow',
    coverflowEffect: {
        rotate: 0,
        stretch: 0,
        depth: slideDepth,
        modifier: 1,
        slideShadows: false,
    },
    //preventClicks: false,
    //preventClicksPropagation: false,
    slideToClickedSlide: true,
}
let swiper = new Swiper('.swiper-container', swiperOptions);
$('.swiper-container').animate({opacity: 1.0}, 150)



// Global Toggle next
$(".js-toggle-next").on('click', function () {
    let btn = $(this);
    btn.next().toggle();
})


// Tags nav
$(".tags-dropdown").on('click', function() {
    $('.js-tags-nav').slideToggle(300);
});


// Form filters
$(".filters-dropdown").on('click', function() {
    $('.js-filter-form').slideToggle(300);
});

$(".js-filter-form").change(function() {
    $(this).submit();
});

// tag livefilter
$('.js-tag-filter li').each(function(){
    $(this).attr('data-search-term', $(this).text().toLowerCase());
});
$('.js-tag-input').on('keyup', function(){
    var searchTerm = $(this).val().toLowerCase();
    $('.js-tag-filter li').each(function(){
        if ($(this).filter('[data-search-term *= ' + searchTerm + ']').length > 0 || searchTerm.length < 1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
});


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


// CSRF
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let csrf_form = $("[name=csrfmiddlewaretoken]").val()
let csrftoken = csrf_form ? csrf_form : getCookie('csrftoken');

// Setup ajax connections safely
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// Ajax theming
function themeStylesPost(btn) {
    data = {}
    let btn_tm_color = btn.attr("data-theme-color")
    let btn_tm_font = btn.attr("data-theme-font")
    let btn_tm_fz = btn.attr("data-theme-fz")
    let btn_tm_lh = btn.attr("data-theme-lh")
    if (btn_tm_color) {
        data['tm_color'] = btn_tm_color
    }
    if (btn_tm_font) {
        data['tm_font'] = btn_tm_font
    }
    if (btn_tm_fz) {
        data['tm_fz'] = btn_tm_fz
    }
    if (btn_tm_lh) {
        data['tm_lh'] = btn_tm_lh
    }
    $.ajax({
        url: btn.attr("data-theme-url"),
        type: "post",
        dataType: "json",
        data: data,
        success: function (data) {
            // console.log(data)
        },
        error: function (xhr, errmsg, err) {
            let msg = `${xhr.status} ${xhr.statusText}`
            eventNotification(msg, 'error')
        },
    });
}
$(".js-theme").click(function () {
    let btn = $(this);
    wto = setTimeout(function() {
        themeStylesPost(btn);
    }, ajaxDelay);
})


// Ajax Votes
function vote_post(btn) {
    $.ajax({
        url: btn.attr("data-vote-url"),
        type: "post",
        dataType: "json",
        success: function (data) {
            if (data.is_valid) {
                btn.parent().parent().find('.js-bvotes').html(data.book_votes)
                $(".js-uvotes").html(data.user_votes)
                // eventNotification('Successfuly voted.')
            } else {
                eventNotification(data.info_msg, 'warning');
            }
        },
        error: function (xhr, errmsg, err) {
            let msg = `${xhr.status} ${xhr.statusText}`
            eventNotification(msg, 'error')
        },
    });
}

$(document).on('click', '.js-vote-btn', function () {
    let btn = $(this);
    wto = setTimeout(function() {
        vote_post(btn);
    }, ajaxDelay);
})


// Ajax library
function library_post(btn) {
    let data = {
        'lib_in': btn.attr("data-lib-in"),
    }
    $.ajax({
        url: btn.attr("data-lib-url"),
        type: "post",
        dataType: "json",
        data: data,
        success: function (data) {
            if (data.is_valid) {
                if (!data.in_lib) {
                    if (btn[0].hasAttribute("data-bookmark")) {
                        btn.html('<i class="fas fa-bookmark"></i>');
                        eventNotification('Book added to Library.');
                    } else {
                        btn.html('<i class="fas fa-check"></i> In Library');
                    }
                    btn.attr("data-lib-in", 1);
                } else {
                    if (btn[0].hasAttribute("data-bookmark")) {
                        btn.html('<i class="far fa-bookmark"></i>')
                        eventNotification('Book removed from Library.')
                    } else if (btn[0].hasAttribute("data-lib-remonly")) {
                        btn.parents()[3].remove();
                        // eventNotification('Book removed from Library.');
                    } else {
                        btn.html('Add to Library')
                    }
                    btn.attr("data-lib-in", 0)
                }
            } else {
                eventNotification(data.info_msg, 'warning');
            }
        },
        error: function (xhr, errmsg, err) {
            let msg = `${xhr.status} ${xhr.statusText}`
            eventNotification(msg, 'error')
        },
    });
}

$(document).on('click', '.js-lib-btn', function () {
    clearTimeout(wto);
    let btn = $(this);
    wto = setTimeout(function() {

        if (btn[0].hasAttribute("data-lib-remonly")) {
            if (confirm('Are you sure you want to remove this book?')) {
                library_post(btn);
            } else {
                return false;
            }
        }

        library_post(btn);
    }, ajaxDelay);
})


// Ajax Search
function search_post(form) {
    $.ajax({
        url : form.attr('action'),
        type : "post",
        dataType: "json",
        data : {
            'search_field': $('#id_search_field').val()
        },
        success : function(resp) {
            // $('#id_search_field').val('');
            // $('.booksearch__formresult')[0].classList.add('animate')
            $('.booksearch__formresult').html(resp.html_search_form_result)
        },
        error : function (xhr, errmsg, err) {
            let msg = `${xhr.status} ${xhr.statusText}`
            eventNotification(msg, 'error')
        }
    });
};

// enter keypress disable
// $('#search-form').on('keyup keypress', function(e) {
//     let keyCode = e.keyCode || e.which;
//     if (keyCode === 13) {
//         e.preventDefault();
//         return false;
//     }
// });
$('#search-form').on('change paste keyup', function(e){
    e.preventDefault();
    clearTimeout(wto);
    let form = $(this);

    if ($('#id_search_field').val()) {
        wto = setTimeout(function() {
            search_post(form);
        }, ajaxDelaySearch);
    }
    return false;
});



//////////////////////
/// BookChapter.js ///
//////////////////////
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
styles.addEventListener('click', manageStyles, false)


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

