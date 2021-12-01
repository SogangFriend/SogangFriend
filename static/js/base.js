if (member !== "") {
    let path = "/chat/unread/";
    $.ajax({
        url: path,
        method: "GET",
        dataType: "json",
        success: (data) => {
            console.log(data);
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
                    console.log(data);
                },
                error: (request, status, error) => {
                    console.log(status + " " + error);
                }
            })
        }, 30000);
    });
}