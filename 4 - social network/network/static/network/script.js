document.addEventListener('DOMContentLoaded', function () {

    create_new_post();
    like_post();
    edit_posts();
    pagination_bar();
    follow_btn();
});

function edit_posts() {
    let posts = document.getElementsByClassName("edit_form");
    Array.from(posts).forEach((element) => {

        let textarea = element.getElementsByClassName("edit_textarea_div")[0];
        let post = element.getElementsByClassName("post_card")[0];
        let save_btn = element.getElementsByClassName("textarea_btn")[0];
        let edit_btn = element.getElementsByClassName("edit_post")[0];
        let textarea_content = textarea.getElementsByClassName("edit_textarea")[0];
        textarea.style.display = "none";

        save_btn.addEventListener("click", () => {
            textarea.style.display = "none";
            post.style.display = "block";
            post.getElementsByClassName("post_body")[0].innerText = textarea_content.value;
            update_backend().then(console.log);
        });

        try {
            edit_btn.addEventListener("click", () => {
                textarea.style.display = "block";
                post.style.display = "none";
            });
        } catch (e) {
            //edit_btn does not exist as the post does not belong to the user.
        }

        const request = new Request(
            "api/edit",
            {headers: {'X-CSRFToken': getCookie("csrftoken")}}
        );


        async function update_backend() {
            return (await fetch(request, {
                method: 'POST',
                mode: 'same-origin',  // Do not send CSRF token to another domain.
                body: JSON.stringify({
                    "id": textarea_content.dataset.id,
                    "body": textarea_content.value,
                })
            })).json();
        }


    });
}

function follow_btn(){

    let button = document.getElementById("follow")

    if (button === null)
        return



    button.addEventListener("click",() => {
        if (button.dataset.action === "Follow"){
            button.dataset.action = "Unfollow";
            button.innerText = "Unfollow";
            post("Follow");
        }
        else if (button.dataset.action === "Unfollow"){
            button.dataset.action = "Follow";
            button.innerText = "Follow";
            post("Unfollow");
        }
    } )

    function post(action){

        const request = new Request(
            window.location.origin + "/api/follow",
            {headers: {'X-CSRFToken': getCookie("csrftoken")}}
        );

        async function fetchFollow() {
            return (await fetch(request, {
                method: 'POST',
                mode: 'same-origin',  // Do not send CSRF token to another domain.
                body: JSON.stringify({
                    "action": action,
                    "username": button.dataset.user
                })
            })).json();
        }

        fetchFollow().then((response) => {


                let count = document.getElementById("follower_count");
                let count_value = parseInt(count.innerText)

                if (response["status"] === "OK") {
                    if (action === "Follow")
                        count.innerText = count_value + 1;
                    else if (action === "Unfollow")
                        count.innerText = count_value - 1;
                }
            }
        );
    }
}

function create_new_post() {


    let post_body = document.getElementById("new_post_body");
    let post_button = document.getElementById("new_post_btn");
    let post_body_length = document.getElementById("body_length");

    if (post_body === null || post_button === null ||post_body_length === null)
        return

    post_button.disabled = post_body.value.length === 0;
    post_body_length.innerText = `${post_body.value.toString().length}/4000`;

    post_body.addEventListener("keyup", () => {
        post_button.disabled = post_body.value.length === 0 || post_body.value.length > 4000;
        post_body_length.innerText = `${post_body.value.toString().length}/4000`;

        if (post_body.value.length === 0 || post_body.value.length > 4000)
            post_body_length.style.color = "red";
        else
            post_body_length.style.color = "grey";

    });

}

function pagination_bar() {
    let pag_bar = document.getElementById("pag_bar");

    if (pag_bar === null)
        return

    // When the document loads make the first adjustment
    responsive_pag_bar();

    window.addEventListener("resize", responsive_pag_bar);

    function responsive_pag_bar() {
        if (document.documentElement.clientWidth < 600) {
            pag_bar.className = "pagination justify-content-center";
        } else {
            pag_bar.className = "pagination justify-content-center pagination-lg"
        }
    }

}


function like_post() {
    Array.from(document.getElementsByClassName("like_btn")).forEach(
        (element) => {
            element.addEventListener("click", () => {
                const id = element.dataset.post;
                const csrftoken = getCookie("csrftoken");

                const request = new Request(
                    window.location.origin + "/api/like",
                    {headers: {'X-CSRFToken': csrftoken}}
                );

                async function fetchLike() {
                    return (await fetch(request, {
                        method: 'POST',
                        mode: 'same-origin',  // Do not send CSRF token to another domain.
                        body: JSON.stringify({
                            "id": id,
                        })
                    })).json();
                }

                fetchLike().then((response) => {
                        if (response["status"] === "success") {
                            element.innerHTML = `❤ ${response["like_count"]}`;
                        }
                    }
                );
            });
        }
    );
}

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