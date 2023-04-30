function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

const eXes = Array.from(document.getElementsByClassName("order-del"))
eXes.forEach(X => {
    X.addEventListener("click", () => {
        $.ajax({
            url: `${window.location.origin}/order/del`,
            method: "POST",
            contentType: "application/json",
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            data: {
                "value": parseInt(X.id)
            },
        })
    })
})