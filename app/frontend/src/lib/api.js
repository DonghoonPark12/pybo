import qs from "qs"
import { access_token, username, is_login } from "./store.js"
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params) // qs.stringify(params)는 params 데이터를
    }                               // 'application/x-www-form-urlencoded' 형식에 맞게끔 변환하는 역할

    //let _url = 'http://127.0.0.1:8000' + url
    let _url = import.meta.env.VITE_SERVER_URL + url
    if (method === 'get') {
        _url += "?" + new URLSearchParams(params)
    }

    let options = {
        method: method,
        headers: {
            'Content-Type': content_type
        }
    }

    // svelte 컴포넌트가 아닌 fastapi 함수는 스토어 변수를 사용할 때 $access_token 처럼 $ 기호로 참조할 수 없다.
    // 따라서 스토어 변수의 값을 읽으려면 get 함수를 사용해야 하고 값을 저장할때는 access_token.set 처럼 set 함수를 사용해야 한다.
    const _access_token = get(access_token)
    // 스토어 변수인 access_token에 값이 있을 경우에 HTTP 헤더에 Authorization 항목을 추가
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
    }

    if (method !== 'get') {
        options['body'] = body
    }

    fetch(_url, options).then(response => {
        if (response.status === 204) { // No content
            if(success_callback) {
                success_callback()
            }
            return
        }
        response.json()
            .then(json => {
            if (response.status >=200 && response.status < 300) {
                if (success_callback) {
                    success_callback(json)
                }
            }else if(operation !== 'login' && response.status === 401) { // token time out
                access_token.set('')
                username.set('')
                is_login.set(false)
                alert("로그인이 필요합니다.")
                push('/user-login')
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

// 응답 상태코드가 204인 경우에는 응답 결과가 없더라도 success_callback을 실행할 수 있도록 다음과 같이 수정
// 처음에 'headers' 대신 'header' 오타가 있었는데, 이 오타 때문에 Content-Type 헤더가 제대로 설정되지 않아 서버에서
// JSON 형식을 제대로 인식하지 못하고 422 에러가 발생하였었다.

// operation이 'get'인 경우에는 파라미터를 GET 방식에 맞게끔 URLSearchParams를 사용하여 파라미터를 조립하도록 했고
// 'get'이 아닌 경우에만 options['body'] 항목에 전달 받은 파라미터 값을 설정하게 했다.

// body 항목에 값을 설정할 때는 JSON.stringify(params) 처럼 params를 JSON 문자열로 변경해야 한다.
// 성공은 HTTP 프로토콜의 응답코드가 200 ~ 299 까지인 경우이므로 이를 체크하여 성공인 경우 매개변수로 전달받은 success_callback을 실행하게 하였다.

// svelte 파일에서 .env 파일의 항목을 읽기 위해서는 반드시 VITE_로 시작하도록 환경변수명을 등록해야 한다.