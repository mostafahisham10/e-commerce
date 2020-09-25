const updateBtns = document.querySelectorAll(".update-cart");

for (let updateBtn of updateBtns) {
    updateBtn.addEventListener("click", function () {
        const productId = this.dataset.product;
        const action = this.dataset.action;
        updateUserOrder(productId, action);
    })
}

function updateUserOrder(productId, action) {
    const url = "/update-item/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",  
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({
            "productId": productId,
            "action": action
        })
    })

        .then((response) => response.json())

        .then((data) => {
            console.log(`Data: ${data}`);
            // Refresh page
            location.reload();
        })
}
