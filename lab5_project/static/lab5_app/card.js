const cards = Array.from(document.getElementsByClassName("card"))
cards.forEach(card => {
    card.addEventListener("click", () => {
        card.querySelector(".link-provider").href = `/shop/item/${card.id}`
    })
})