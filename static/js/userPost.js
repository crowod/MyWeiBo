var like_post_id = [];
var useravatar ;
var username;
$(document).ready(function () {
    $.ajax({
        url: '/users/me',
        type: 'GET',
        data: '',
        success: function (result) {
                document.querySelector('.user-profile-main-screen-name').innerHTML = result['data']['username'];
                document.querySelector('.user-profile-main-item').innerHTML = 'Earned ' + result['data']['likes_earn'] + ' likes';
                document.querySelector('#following > span:nth-child(2)').innerHTML = result['data']['following_num'];
                document.querySelector('#follower > span:nth-child(2)').innerHTML = result['data']['follower_num'];
                document.querySelector('.user-profile .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
                document.querySelector('.site-header-right .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
                username = document.querySelector('.user-profile-main-screen-name').innerHTML;
                $('#welcome')[0].innerHTML = 'Welcome ' + result['data']['username'] + '!';
                useravatar = result['data']['avatar_url'];
                like_post_id = result['data']['like_post_id']
                $.ajax({
                    url: '/posts/' + username,
                    type: 'GET',
                    data: '',
                    success: function (result) {
                        posts_update(result)
                    }
                })
            }
    })

});


function posts_update(result) {
    for (var i in result['data']) {
        var date = new Date(result['data'][i]['datetime']);
        date = date.getFullYear() + '/' + date.getMonth() + '/' + date.getDay();
        $('#append').append(
            $(
                `<div class="user-activity-container" id=${result['data'][i]['id']}>
                    <div class="user-activity">
                        <div class="user-activity-header is-flex">
                            <div class="user-activity-header-left">
                                <div class="user-activity-header-left-avatar">
                                    <span>
                                        <div class="user-avatar ">
                                            <div class="user-avatar-content avatar"></div>
                                        </div>
                                    </span>
                                </div>
                            </div>
                            <div class="user-activity-header-main">
                                <h1 class="user-name">
                                    <a href="" id="id_username">${username}</a>
                                </h1>
                                <p class="post-time"><span>${date}</span></p>
                            </div>
                            <div class="user-activity-header-right">
                                <svg class="symbol dropdown-trigger trash">
                                    <use xlink:href="#symbol-trash"></use>
                                </svg>
                            </div>
                        </div>
                        <div class="user-activity-body">
                            <div class="user-activity-content">
                                <div class="user-activity-post">
                                    <div class="readable-content">
                                        <div class="readable-content-collapse">
                                            <span>${result['data'][i]['content']}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="user-activity-footer">
                            <div class="op-wrap">
                                <div class="op-item ">
                                    <a>
                                        <svg class="symbol symbol-dig like">
                                            <use xlink:href="#symbol-dig"></use>
                                        </svg>
                                        <p>${result['data'][i]['total_liked']}</p>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`
            )
        )
    }
    $('.user-activity-container').each(function () {
        if (like_post_id.indexOf(parseInt($(this)[0].id)) !== -1) {
            $(this).find('.like').parent().parent().addClass('is-active');
        }
        $('.avatar').css('background-image', 'url(' + useravatar + ') ');
    });
}


$(document).on('click', '.trash', function () {
    var post_id = $(this).parents('.user-activity-container')[0].id;
    var element = $(this).parents('.user-activity-container');
    var data = new URLSearchParams();
    data.append('post_id', post_id);
    $.ajax({
        url: 'posts/delete',
        type: 'POST',
        data: data.toString(),
        success: function (result) {
            element.remove();
        }
    })
});

$(document).on('click', '.like', function () {
    var post_id = $(this).parents('.user-activity-container')[0].id;
    var element = $(this).parent().parent();
    var data = new URLSearchParams();
    data.append('post_id', post_id);
    $.ajax({
        url: 'like',
        type: 'POST',
        data: data.toString(),
        success: function (result) {
            if (element.hasClass('is-active'))
                element.removeClass('is-active');
            else
                element.addClass('is-active');
            element.find('p').text(result['total_like']);
        }
    })
});