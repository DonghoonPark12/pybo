import { writable } from 'svelte/store'

// "새로고침"을 하는 순간 스토어 변수가 초기화된다.
// 스토어 변수의 초기화 현상은 브라우저 새로고침 외에도
// 자바스크립트의 location.href 또는 a 태그를 통한 링크를 호출할 경우에도 발생
// 따라서 이러한 문제를 해결하려면 스토어에 저장한 변수 값이 항상 유지될 수 있게 지속성을 지닌 스토어가 필요

//export const page = writable(0)


// persist_storage 함수는 이름(key)과 초기값(initValue)을 입력받아 writable 스토어를 생성하여 리턴하는 함수이다.
// persist_storage 함수는 localStorage를 사용하여 지속성을 갖도록 했다.
// localStorage에 해당 이름의 값이 이미 존재하는 경우에는 초기값 대신 기존의 값으로 스토어를 생성하여 리턴
// store의 subscribe 함수는 스토어에 저장된 값이 변경될 때 실행되는 콜백 함수
// 따라서 스토어 변수의 값이 변경 될 때 localStorage의 값도 함께 변경될 것
const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)

// 로그인 성공시 취득한 액세스 토큰과 사용자명을 스토어에 저장하고 내비게이션 바에도 로그인 여부를 표시
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)

