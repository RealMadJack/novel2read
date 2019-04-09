/* Project specific Javascript goes here. */

(function () {

// Timeout Cleaner
let wto;
const ajaxDelay = 300
const ajaxDelaySearch = 350

// Swiper Slider config
let slides = window.innerWidth > 1750 ? 'auto' : 'auto'
let slideDepth = window.innerWidth > 2000 ? 280 : 550
let swiperOptions = {
    pagination: '.swiper-pagination',
    effect: 'coverflow',
    // grabCursor: true,
    centeredSlides: true,
    loop: true,
    slidesPerView: slides,
    nextButton: '.swiper-button-next',
    prevButton: '.swiper-button-prev',
    coverflow: {
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


// Form filters
$(".js-filter-form").change(function() {
    $(".js-filter-form").submit();
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


// Ajax animations
function btnAjaxAnimate(btn) {
    btn.setAttribute("style", "width: 100px;")
    btn.html('...')
}


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

$(".js-vote-btn").click(function () {
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
                        btn.parents()[2].remove();
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

$(".js-lib-btn").click(function () {
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



})();

