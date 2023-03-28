export function formatByteSize(byteSize) {
    if (byteSize == 0) {
        return '-'
    }
    const kilobyte = 1024;
    const megabyte = kilobyte * 1024;

    if (byteSize < kilobyte) {
        return byteSize + ' B';
    } else if (byteSize < megabyte) {
        return (byteSize / kilobyte).toFixed(1) + ' KB';
    } else {
        return (byteSize / megabyte).toFixed(1) + ' MB';
    }
}

export function docState(state) {
    switch (state) {
        case 0:
            return ''
        case 1:
            return 'doing'
        case 2:
            return 'done'
    }
}

export function nameWithoutExt(name) {
    return name.slice(0, name.lastIndexOf('.'))
}

export function docType(doc) {
    if (doc['doc_type'] == "application/pdf") {
        return 'pdf'
    }
    if (doc['doc_type'] == "application/epub+zip") {
        return 'epub'
    }
    if (doc['doc_type'] == "text/plain") {
        return 'txt'
    }
    if (doc['doc_type'] == "text/markdown") {
        return 'md'
    }
    if (doc['doc_type'] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        return 'docx'
    }
    if (doc['doc_type'] == "web") {
        return 'web'
    }
}

export function docUrl(doc) {
    let base = location.origin
    if (import.meta.env.DEV) {
        base = `http://${location.hostname}:8000`
    }

    if (doc['doc_type'] == "application/pdf") {
        return "pdfjs/web/viewer.html?file=" + decodeURIComponent(`${base}/static/${doc.doc_id}/${doc.doc_name}`)
    }
    if (doc['doc_type'] == "application/epub+zip") {
        return "epub/index.html?url=" + decodeURIComponent(`${base}/static/${doc.doc_id}/${doc.doc_name}`)
    }
    if (doc['doc_type'] == "text/markdown") {
        return "md/index.html?url=" + decodeURIComponent(`${base}/static/${doc.doc_id}/${doc.doc_name}`)
    }
    if (doc['doc_type'] == "text/plain") {
        return `${base}/static/${doc.doc_id}/${doc.doc_name}`
    }
    if (doc['doc_type'] == "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
        return "docx/index.html?url=" + decodeURIComponent(`${base}/static/${doc.doc_id}/${doc.doc_name}`)
    }
    if (doc['doc_type'] == "web") {
        return doc.doc_name
    }

}

export function showLastMessage(after) {
    setTimeout(() => {
        const element = document.getElementsByClassName('message-item');
        element.length > 0 && element[element.length - 1].scrollIntoView({
            block: 'center', // 值有start,center,end,nearest，当前显示在视图区域中间
            behavior: 'smooth' // 值有auto,instant,smooth，缓动动画（当前是慢速的）
        })
    }, after || 100)
}