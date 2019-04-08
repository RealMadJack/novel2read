/* Project specific Javascript goes here. */

(function () {

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
            console.log(csrftoken)
        }
    }
});


// Notifications
function eventNotification(msg='', flag='info') {
    let body = document.body;
    let container = document.getElementsByClassName('container')[1]
    let alertBox = document.createElement('div')
    alertBox.className = `alert alert-${flag} alert-animate`
    alertBox.textContent = msg
    container.appendChild(alertBox)
    setTimeout(() => {
        container.removeChild(alertBox)
    }, 3000);
}



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
                $(".js-bvotes").html(data.book_votes)
                $(".js-uvotes").html(data.user_votes)
                eventNotification('Successfuly voted.')
            } else {
                eventNotification(data.info_msg, 'warning');
            }
        },
        error: function (xhr, errmsg, err) {
            let msg = `${xhr.status} ${xhr.statusText}`
            eventNotification(msg, 'danger')
        },
    });
}

$(".js-vote-btn").click(function () {
    let btn = $(this);
    vote_post(btn);
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
                        btn.html('<i class="fas fa-bookmark"></i>')
                    } else {
                        btn.html('<i class="fas fa-check"></i> In Library')
                    }
                    btn.attr("data-lib-in", 1)
                    eventNotification('Book added to Library.')
                } else {
                    if (btn[0].hasAttribute("data-bookmark")) {
                        btn.html('<i class="far fa-bookmark"></i>')
                    } else {
                        btn.html('Add to Library')
                    }
                    btn.attr("data-lib-in", 0)
                    eventNotification('Book removed from Library.')
                }
            } else {
                eventNotification(data.info_msg, 'warning');
            }
        },
        error: function (xhr, errmsg, err) {
            let msg = `${xhr.status} ${xhr.statusText}`
            eventNotification(msg, 'danger')
        },
    });
}

$(".js-lib-btn").click(function () {
    let btn = $(this);
    library_post(btn);
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
            console.log(resp)
            // $('#id_search_field').val('');
            // $('.booksearch__formresult')[0].classList.add('animate')
            $('.booksearch__formresult').html(resp.html_search_form_result)
        },
        error : function (xhr, errmsg, err) {
            let msg = `${xhr.status} ${xhr.statusText}`
            eventNotification(msg, 'danger')
        }
    });
};

$('#search-form').on('submit', function(e){
    e.preventDefault();
    let form = $(this);
    search_post(form);
});


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



})();

