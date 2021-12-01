if (member !== "") {
    let path = "/chat/unread/";
    $.ajax({
        url: path,
        method: "GET",
        dataType: "json",
        success: (data) => {
            let dot = document.getElementById('new_chat');
            if (data['unread']) {
                dot.style.display = 'inline';
            } else {
                dot.style.display = 'none';

            }
        },
        error: (request, status, error) => {
            console.log(status + " " + error);
        }
    });
    $(() => {
        setInterval(() => {
            $.ajax({
                url: path,
                method: "GET",
                dataType: "json",
                success: (data) => {
                    let dot = document.getElementById('new_chat');
                    if (data['unread']) {
                        dot.style.display = 'inline';
                    } else {
                        dot.style.display = 'none';
                    }
                },
                error: (request, status, error) => {
                    console.log(status + " " + error);
                }
            })
        }, 30000);
    });
}