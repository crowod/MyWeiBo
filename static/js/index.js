(function ($) {
    $(document).ready(function () {
        $.ajax({
            url: '/users/me',
            type: 'GET',
            data: '',
            success: function (result) {
                document.querySelector('.user-profile-main-screen-name').innerHTML = result['data']['username'];
                document.querySelector('#following > span:nth-child(2)').innerHTML = result['data']['following_num'];
                document.querySelector('#follower > span:nth-child(2)').innerHTML = result['data']['follower_num'];

            }
        })
    });

    $(document).ready(function () {
        $.ajax({
            url: '/posts/all',
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
            url: '/posts/add',
            type: 'POST',
            data: data.toString(),
            success: function (result) {
                if (result['status'] === 201) {
                    document.querySelector("#post-input").value = "";
                    $('.message-feed .message-card-container').each(function () {
                        $(this).remove();
                    });
                    posts_update(result);
                }
            }
        })
    });

    function posts_update(result) {
        for (var i in result['data']) {
            var date = new Date(result['data'][i]['datetime']);
            date = date.getFullYear() + '/' + date.getMonth() + '/' + date.getDay();
            $('.message-feed').append(
                $(
                    `<div class="message-card-container">
                    <div class="message-card">
                    <div class="message-card-header is-flex">
                    <div class="message-card-header-left">
                    <img class="message-card-topic-img" src="../static/image/avatar.png">
                    </div>
                    <div class="message-card-header-main">
                    <h1 class="topic-name">
                    <span>${result['data'][i]['user'][0]['username']}</span>
                    </h1>
                    <p class="topic-extra">
                    <span class="message-time">${date}</span>
                    </p>
                    </div>
                    <div class="message-card-header-right">
                    <svg class="symbol dropdown-trigger"><use xlink:href="#symbol-trash"></use></svg>
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
                    <a><svg class="symbol symbol-dig"><use xlink:href="#symbol-dig"></use></svg>${result['data'][i]['total_liked']}</a>
                    </div>
                    <div class="op-item ">
                    <a><svg class="symbol symbol-comment"><use xlink:href="#symbol-comment"></use></svg>0</a>
                    </div>
                    </div>
                    </div>
                    </div>
                    </div>`
                )
            )
        }
    }
})
(jQuery);


