const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)


    //let _url = 'http://127.0.0.1:8000' + url
    let _url = import.meta.env.VITE_SERVER_URL + url
    if (method === 'get') {
        _url += "?" + new URLSearchParams(params)
    }

    let options = {
        method: method,
        header: {
            'Content-Type': content_type
        }
    }

    if (method !== 'get') {
        options['body'] = body
    }

    fetch(_url, options).then(response => {
        response.json().then(json => {
            if (response.status >=200 && response.status < 300) {
                if (success_callback) {
                    success_callback(json)
                }
            }
            else {
                if (failure_callback){
                    failure_callback(json)
                }
                else {
                    alert(JSON.stringify(json))
                }
            }
        }).catch(error => { alert(JSON.stringify(error)) })
    })
}

export default fastapi

// peration이 'get'인 경우에는 파라미터를 GET 방식에 맞게끔 URLSearchParams를 사용하여 파라미터를 조립하도록 했고
// 'get'이 아닌 경우에만 options['body'] 항목에 전달 받은 파라미터 값을 설정하게 했다.
// body 항목에 값을 설정할 때는 JSON.stringify(params) 처럼 params를 JSON 문자열로 변경해야 한다.
// 성공은 HTTP 프로토콜의 응답코드가 200 ~ 299 까지인 경우이므로 이를 체크하여 성공인 경우 매개변수로 전달받은 success_callback을 실행하게 하였다.
// svelte 파일에서 .env 파일의 항목을 읽기 위해서는 반드시 VITE_로 시작하도록 환경변수명을 등록해야 한다.