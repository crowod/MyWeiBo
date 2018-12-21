(function ($) {
    var post_id = [];
    var like_post_id = [];

    $(document).ready(function () {
        update_me();
    });

    $(document).ready(function () {
        $.ajax({
            url: 'posts/all',
            type: 'GET',
            data: '',
            success: function (result) {
                posts_update(result)
            }
        })
    });

    $('#publish').on('click', function () {
        var username = document.querySelector('.user-profile-main-screen-name').innerText;
        var content = document.querySelector("#post-input").value;
        var data = new URLSearchParams();
        data.append('username', username);
        data.append('content', content);

        $.ajax({
            url: 'posts/add',
            type: 'POST',
            data: data.toString(),
            success: function (result) {
                document.querySelector("#post-input").value = "";
                $('.message-feed .message-card-container').each(function () {
                    $(this).remove();
                });
                post_id = result['posts_id'];
                posts_update(result);
            }
        })
    });

    function posts_update(result)
// language=HTML
    // language=HTML
    {
        for (var i in result['data']) {
            var date = new Date(result['data'][i]['datetime']);
            date = date.getFullYear() + '/' + (date.getMonth() + 1) + '/' + date.getDate() + " " +
                date.getHours() + ":" + date.getMinutes();
            $('.message-feed').append(
                $(
                    `<div class="message-card-container" id=${result['data'][i]['id']}>
                    <div class="message-card">
                    <div class="message-card-header is-flex">
                    <div class="message-card-header-left">
                    <img class="message-card-topic-img" src=${result['data'][i]['user'][0]['avatar_url']}>
                    </div>
                    <div class="message-card-header-main">
                    <h1 class="topic-name">
                    <a href="/${result['data'][i]['user'][0]['username']}/post">
                    <span>${result['data'][i]['user'][0]['username']}</span>
                    </a>
                    </h1>
                    <p class="topic-extra">
                    <span class="message-time">${date}</span>
                    </p>
                    </div>
                    <div class="message-card-header-right">
                    </div>
                    </div>
                    <div class="message-card-body">
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
                    <div class="message-card-footer">
                    <div class="op-wrap">
                    <div class="op-item ">
                    <a><svg class="symbol symbol-dig like">
                    <use xlink:href="#symbol-dig"></use></svg><p>${result['data'][i]['total_liked']}</p></a>
                    </div>
                    </div>
                    </div>
                    </div>
                    </div>`
                )
            );
        }
        $('.message-card-container').each(function () {
            if (post_id.indexOf(parseInt($(this)[0].id)) !== -1) {
                $(this).find('.message-card-header-right').append(
                    $(
                        `<svg class="symbol dropdown-trigger trash"><use xlink:href="#symbol-trash"></svg></use></svg>`
                    )
                )
            }
            if (like_post_id.indexOf(parseInt($(this)[0].id)) !== -1) {
                $(this).find('.like').parent().parent().addClass('is-active');
            }
        });
    }

    function update_me() {
        $.ajax({
            url: '/users/me',
            type: 'GET',
            data: '',
            success: function (result) {
                document.querySelector('.user-profile-main-screen-name').innerHTML = result['data']['username'];
                document.querySelector('.user-profile-main-item').innerHTML = 'Earned ' + result['data']['likes_earn'] + ' likes';
                document.querySelector('#following > span:nth-child(2)').innerHTML = result['data']['following_num'];
                document.querySelector('#follower > span:nth-child(2)').innerHTML = result['data']['follower_num'];
                document.querySelector('#follower > span:nth-child(2)').innerHTML = result['data']['follower_num'];
                document.querySelector('.user-profile .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
                document.querySelector('.site-header-right .user-avatar-content').style.backgroundImage = `url(${result['data']['avatar_url']})`;
                post_id = result['data']['post_id'];
                like_post_id = result['data']['like_post_id']
                $('#welcome')[0].innerHTML = 'Welcome ' + result['data']['username'] + '!';
            }
        });
    }

    $(document).on('click', '.trash', function () {
        var post_id = $(this).parents('.message-card-container')[0].id;
        var element = $(this).parents('.message-card-container');
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
        var post_id = $(this).parents('.message-card-container')[0].id;
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
})
(jQuery);


