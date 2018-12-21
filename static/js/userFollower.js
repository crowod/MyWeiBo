
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
                $('#welcome')[0].innerHTML = 'Welcome ' + result['data']['username'] + '!';
                username = document.querySelector('.user-profile-main-screen-name').innerHTML;
                $.ajax({
                    url: '/followers/' + username,
                    type: 'GET',
                    data: '',
                    success: function (result) {
                        follower_update(result);
                    }
                })

        }
    })

});

function follower_update(result) {
    for (var i in result['data']) {
        if (result['data'][i]['is_following'])
            temp = 'Unfollow';
        else
            temp = 'Follow';
        $('#append').append(
            $(
                `<div class="user-card is-small ">
                    <div class="user-card-header is-flex">
                        <div class="user-card-header-avatar">
                            <div class="user-avatar ">
                              <div class="user-avatar-content"></div>
                            </div>
                        </div>
                        <div class="user-card-info">
                            <a href="/${result['data'][i]['username']}/post">
                                <h1 class="user-card-title">${result['data'][i]['username']}</h1>
                            </a>
                            <p class="user-card-extra">Followers ${result['data'][i]['follower_num']}</p>
                        </div>
                        <div>
                            <div class="user-follow">
                                <button class="btn btn-warning user-follow-warn temp">${temp}</button>
                            </div>
                        </div>
                    </div>
                 </div>`
            )
        )
    }
    $('.user-card.is-small').each(function () {
        $(this).find('.user-avatar-content').css('background-image', 'url(' + result['data'][i]['avatar_url'] + ') ');
    });
}

$(document).on('click', '.temp', function () {
    var data = new URLSearchParams();
    var element = $(this).parent().parent().parent();
    var user = element.find('h1')[0].innerText;
    data.append('following_name', user);
    if(document.querySelector('.user-follow').innerText === "Follow"){
        $.ajax({
            url: '/following/add',
            type: 'POST',
            data: data.toString(),
            success: function (result) {
                $('.user-follow').find('button').text('Unfollow');
            }
        })
    }else if(document.querySelector('.user-follow').innerText === "Unfollow"){
        $.ajax({
            url: '/following/cancel',
            type: 'POST',
            data: data.toString(),
            success: function (result) {
                $('.user-follow').find('button').text('Follow');
            }
        })
    }

});
