function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const handleLikeClick = (buttonId) => {
    // document는 브라우저에 표시된 화면 자체를 의미
    const likeButton = document.getElementById(buttonId)
    //원하는 태그 데이터 추출, 클래스는 .i, id는 #i 이런식으로 호출하면됨.
    //디폴트는 태그 추출임.
    const likeIcon = likeButton.querySelector("i");    
    const csrftoken = getCookie('csrftoken');
    

    // like-button-{{ post.id }}
    const postId = buttonId.split("-").pop()
    // /posts/5/post_like
    const url = "/posts/" + postId + "/post_like"

    //서버로 좋아요 api를 호출
    // 자바스크립트에서 api를 호출할 때는 fetch라는 놈을 사용함
    fetch(url, {
        method: "POST",
        // /posts 앞부분의 127.~~어쩌고 부분을 origin이라고 함. 그래서 same-origin이라는
        // 속성이 있는듯
        mode: "same-origin",
        headers: {
            'X-CSRFToken': csrftoken
            // 'Content-Type': 'application/x-www-form-urlencoded',
          }
    })
    .then(response => response.json())
    .then(data => {
        //결과를 받고 html(좋아요 하트) 모습을 변경
        if(data.result ==="like"){
            //좋아요 셋팅
            likeIcon.classList.replace("fa-heart-o", "fa-heart")
        } else {
            likeIcon.classList.replace("fa-heart", "fa-heart-o")
        }
    }
        );
}