buttons = document.getElementById("valgBtns")

function send_vote(id, candidate) {
    const xhr = new XMLHttpRequest()
    xhr.open("POST", "/api/vote")
    xhr.setRequestHeader("Content-Type", "application/json");
    const body = JSON.stringify({
        id: id,
        candidate: candidate
    })
    xhr.onload = () => {
/*         if (xhr.readyState == 4 && xhr.status == 201) {
            pass
        } else {
            pass
        } */
    }
    xhr.send(body)
}

function selection(elem, exclusive, className="is-info") {
    if (exclusive) {
        buttons.getElementsByClassName(className)[0]?.classList.remove(className)
    }
    elem.classList.add(className)
}

function vote_event(id, className="is-info") {
    candidate = buttons.getElementsByClassName(className)[0]?.id
    send_vote(id, candidate)
}