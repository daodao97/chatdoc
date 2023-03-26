function err(message) {
    ElMessage.error(message)
}

function myFetch(input, init) {
    return new Promise((resolve, reject) => {
        fetch(input, init).then(res => {
            json = resolve(res.json())
            if (json.code != 0) {
                err(json.message)
                reject(new Error(json.message))
            } else {
                resolve(json)
            }
        }).catch(err => {
            reject(err)
        })
    })
}

export async function fetchDcoList() {
    return new Promise((resolve, reject) => {
        myFetch("/api/my_docs").then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function fetchQuery(doc_id, query) {
    return new Promise((resolve, reject) => {
        myFetch("/api/ask/" + doc_id + "?question=" + query).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function fetchMsg(doc_id) {
    return new Promise((resolve, reject) => {
        myFetch("/api/msg/" + doc_id).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function fetchDelDoc(doc_id) {
    return new Promise((resolve, reject) => {
        myFetch("/api/del/" + doc_id, { method: "DELETE" }).then(res => resolve(res)).catch(e => reject(e))
    })
}

export async function fetchAddLink(link) {
    return new Promise((resolve, reject) => {
        myFetch("/api/add_link", {
            method: "POST", 
            body: JSON.stringify({ link: link }), 
            headers: {
                "Content-Type": "application/json",
            }
        }).then(res => resolve(res)).catch(e => reject(e))
    })
}